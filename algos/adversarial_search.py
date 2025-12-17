import time
from typing import Tuple, List, Optional, Callable, Dict
from copy import deepcopy
import numpy as np
from env.connect4_env import Connect4Env


class PerformanceTracker:
    
    def __init__(self):
        self.nodes_expanded = 0
        self.nodes_pruned = 0
        self.max_depth_reached = 0
        self.start_time = None
        self.end_time = None
        self.move_sequence = []
        
    def reset(self):
        self.nodes_expanded = 0
        self.nodes_pruned = 0
        self.max_depth_reached = 0
        self.start_time = None
        self.end_time = None
        self.move_sequence = []
    
    def start_timer(self):
        self.start_time = time.time()
    
    def stop_timer(self):
        self.end_time = time.time()
    
    def get_elapsed_time(self) -> float:
        if self.start_time is None or self.end_time is None:
            return 0.0
        return self.end_time - self.start_time
    
    def get_stats(self) -> Dict:
        return {
            'nodes_expanded': self.nodes_expanded,
            'nodes_pruned': self.nodes_pruned,
            'max_depth_reached': self.max_depth_reached,
            'time_taken': self.get_elapsed_time(),
            'move_sequence': self.move_sequence.copy()
        }


def evaluate_board(game: Connect4Env, player: int, depth: int = 0) -> float:
    winner = game.check_winner()
    if winner is not None:
        if winner == player:
            return 10000.0 + depth
        elif winner == -player:
            return -10000.0 - depth
        else:
            return 0.0
    
    score = 0.0
    opponent = -player
    
    score += evaluate_threats(game, player) * 100
    score -= evaluate_threats(game, opponent) * 100
    
    center_cols = [2, 3, 4]
    for col in center_cols:
        for row in range(game.ROWS):
            if game.board[row, col] == player:
                score += (3 - abs(col - 3)) * 2
    
    score += evaluate_two_in_row(game, player) * 5
    score -= evaluate_two_in_row(game, opponent) * 5
    
    return score


def evaluate_threats(game: Connect4Env, player: int) -> int:
    threats = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for row in range(game.ROWS):
        for col in range(game.COLS):
            for dr, dc in directions:
                count = 0
                empty_pos = None
                
                for i in range(4):
                    nr, nc = row + dr * i, col + dc * i
                    if not (0 <= nr < game.ROWS and 0 <= nc < game.COLS):
                        break
                    
                    if game.board[nr, nc] == player:
                        count += 1
                    elif game.board[nr, nc] == 0:
                        empty_pos = (nr, nc)
                    else:
                        break
                
                if count == 3 and empty_pos is not None:
                    er, ec = empty_pos
                    if er == game.ROWS - 1 or game.board[er + 1, ec] != 0:
                        threats += 1
                        break
    
    return threats


def evaluate_two_in_row(game: Connect4Env, player: int) -> int:
    pairs = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for row in range(game.ROWS):
        for col in range(game.COLS):
            for dr, dc in directions:
                count = 0
                for i in range(2):
                    nr, nc = row + dr * i, col + dc * i
                    if (0 <= nr < game.ROWS and 0 <= nc < game.COLS and 
                        game.board[nr, nc] == player):
                        count += 1
                    else:
                        break
                
                if count == 2:
                    pairs += 1
                    break
    
    return pairs


def minimax(game: Connect4Env, 
            depth: int, 
            max_depth: int,
            player: int,
            eval_fn: Callable[[Connect4Env, int, int], float],
            tracker: PerformanceTracker) -> Tuple[float, Optional[int]]:
    tracker.nodes_expanded += 1
    tracker.max_depth_reached = max(tracker.max_depth_reached, depth)
    
    if game.is_terminal() or depth >= max_depth:
        utility = game.get_utility(player)
        if utility is not None:
            return (utility, None)
        else:
            return (eval_fn(game, player, depth), None)
    
    valid_actions = game.get_valid_actions()
    
    if len(valid_actions) == 0:
        return (eval_fn(game, player, depth), None)
    
    best_value = float('-inf')
    best_move = None
    
    for col in valid_actions:
        game.make_move(col)
        
        value, _ = minimax(game, depth + 1, max_depth, player, eval_fn, tracker)
        value = -value
        
        game.undo_move()
        
        if value > best_value:
            best_value = value
            best_move = col
    
    return (best_value, best_move)


def alphabeta(game: Connect4Env,
              depth: int,
              max_depth: int,
              player: int,
              alpha: float,
              beta: float,
              eval_fn: Callable[[Connect4Env, int, int], float],
              tracker: PerformanceTracker) -> Tuple[float, Optional[int]]:
    tracker.nodes_expanded += 1
    tracker.max_depth_reached = max(tracker.max_depth_reached, depth)
    
    if game.is_terminal() or depth >= max_depth:
        utility = game.get_utility(player)
        if utility is not None:
            return (utility, None)
        else:
            return (eval_fn(game, player, depth), None)
    
    valid_actions = game.get_valid_actions()
    
    if len(valid_actions) == 0:
        return (eval_fn(game, player, depth), None)
    
    best_value = float('-inf')
    best_move = None
    
    for col in valid_actions:
        game.make_move(col)
        
        value, _ = alphabeta(game, depth + 1, max_depth, player, -beta, -alpha, eval_fn, tracker)
        value = -value
        
        game.undo_move()
        
        if value > best_value:
            best_value = value
            best_move = col
        
        alpha = max(alpha, value)
        
        if alpha >= beta:
            tracker.nodes_pruned += 1
            break
    
    return (best_value, best_move)


def minimax_search(game: Connect4Env,
                   max_depth: int = 4,
                   eval_fn: Optional[Callable] = None) -> Tuple[int, PerformanceTracker]:
    if eval_fn is None:
        eval_fn = evaluate_board
    
    tracker = PerformanceTracker()
    tracker.start_timer()
    
    player = game.current_player
    value, move = minimax(game, 0, max_depth, player, eval_fn, tracker)
    
    tracker.stop_timer()
    
    return (move, tracker)


def alphabeta_search(game: Connect4Env,
                     max_depth: int = 4,
                     eval_fn: Optional[Callable] = None) -> Tuple[int, PerformanceTracker]:
    if eval_fn is None:
        eval_fn = evaluate_board
    
    tracker = PerformanceTracker()
    tracker.start_timer()
    
    player = game.current_player
    value, move = alphabeta(game, 0, max_depth, player, float('-inf'), float('inf'), eval_fn, tracker)
    
    tracker.stop_timer()
    
    return (move, tracker)
