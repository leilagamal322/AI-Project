import math
from typing import Tuple


def manhattan_distance(state: Tuple[int, int, bool], 
                      goal: Tuple[int, int],
                      key_pos: Tuple[int, int]) -> float:
    x, y, has_key = state
    
    if has_key:
        return abs(x - goal[0]) + abs(y - goal[1])
    else:
        dist_to_key = abs(x - key_pos[0]) + abs(y - key_pos[1])
        dist_key_to_goal = abs(key_pos[0] - goal[0]) + abs(key_pos[1] - goal[1])
        return dist_to_key + dist_key_to_goal


def euclidean_distance(state: Tuple[int, int, bool],
                       goal: Tuple[int, int],
                       key_pos: Tuple[int, int]) -> float:
    x, y, has_key = state
    
    if has_key:
        return math.sqrt((x - goal[0])**2 + (y - goal[1])**2)
    else:
        dist_to_key = math.sqrt((x - key_pos[0])**2 + (y - key_pos[1])**2)
        dist_key_to_goal = math.sqrt((key_pos[0] - goal[0])**2 + (key_pos[1] - goal[1])**2)
        return dist_to_key + dist_key_to_goal


def zero_heuristic(state: Tuple[int, int, bool],
                   goal: Tuple[int, int],
                   key_pos: Tuple[int, int]) -> float:
    return 0.0


def get_heuristic_function(name: str):
    heuristics = {
        'manhattan': manhattan_distance,
        'euclidean': euclidean_distance,
        'zero': zero_heuristic
    }
    
    if name.lower() not in heuristics:
        raise ValueError(f"Unknown heuristic: {name}. Choose from {list(heuristics.keys())}")
    
    return heuristics[name.lower()]

