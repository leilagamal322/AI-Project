import os
import sys
from pathlib import Path
import numpy as np
from env.connect4_env import Connect4Env, get_game_complexity_estimate
from algos.adversarial_search import (
    minimax_search, alphabeta_search, PerformanceTracker
)
from viz.connect4_viz import (
    plot_board, plot_move_progression, plot_performance_comparison,
    save_game_state_image, create_comparison_table
)
import matplotlib.pyplot as plt


def run_algorithm_comparison(max_depth: int = 4, test_positions: int = 3):
    print("="*70)
    print("PHASE 2: Connect 4 - Minimax vs Alpha-Beta Comparison")
    print("="*70)
    
    output_dir = Path("results/phase2")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    complexity = get_game_complexity_estimate()
    print("\nGame Complexity Estimate:")
    print(f"  Branching Factor: ~{complexity['branching_factor']}")
    print(f"  Average Depth: ~{complexity['average_depth']} moves")
    print(f"  Maximum Depth: {complexity['maximum_depth']} moves")
    print(f"  State Space: {complexity['state_space_size']}")
    
    all_minimax_stats = []
    all_alphabeta_stats = []
    
    for test_num in range(test_positions):
        print(f"\n{'='*70}")
        print(f"Test Position {test_num + 1}/{test_positions}")
        print(f"{'='*70}")
        
        game = Connect4Env()
        
        moves_played = 0
        max_moves = np.random.randint(4, 12)
        
        while moves_played < max_moves and not game.is_terminal():
            valid_cols = game.get_valid_actions()
            if not valid_cols:
                break
            
            col = np.random.choice(valid_cols)
            game.make_move(col)
            moves_played += 1
        
        print(f"\nInitial position (after {moves_played} moves):")
        print(game.get_board_string())
        print(f"Current player: {'Player 1 (X)' if game.current_player == 1 else 'Player 2 (O)'}")
        
        print("\n" + "-"*70)
        print("Running MINIMAX algorithm...")
        print("-"*70)
        game_mm = game.copy()
        best_move_mm, tracker_mm = minimax_search(game_mm, max_depth=max_depth)
        minimax_stats = tracker_mm.get_stats()
        all_minimax_stats.append(minimax_stats)
        
        print(f"Best move: Column {best_move_mm}")
        print(f"Nodes expanded: {minimax_stats['nodes_expanded']:,}")
        print(f"Max depth reached: {minimax_stats['max_depth_reached']}")
        print(f"Time taken: {minimax_stats['time_taken']:.4f} seconds")
        
        print("\n" + "-"*70)
        print("Running ALPHA-BETA PRUNING algorithm...")
        print("-"*70)
        game_ab = game.copy()
        best_move_ab, tracker_ab = alphabeta_search(game_ab, max_depth=max_depth)
        alphabeta_stats = tracker_ab.get_stats()
        all_alphabeta_stats.append(alphabeta_stats)
        
        print(f"Best move: Column {best_move_ab}")
        print(f"Nodes expanded: {alphabeta_stats['nodes_expanded']:,}")
        print(f"Nodes pruned: {alphabeta_stats['nodes_pruned']:,}")
        print(f"Max depth reached: {alphabeta_stats['max_depth_reached']}")
        print(f"Time taken: {alphabeta_stats['time_taken']:.4f} seconds")
        
        print("\n" + "-"*70)
        print("COMPARISON:")
        print("-"*70)
        improvement = (1 - alphabeta_stats['nodes_expanded'] / 
                      minimax_stats['nodes_expanded']) * 100
        speedup = minimax_stats['time_taken'] / max(alphabeta_stats['time_taken'], 0.0001)
        
        print(f"Nodes reduction: {improvement:.2f}%")
        print(f"Speedup: {speedup:.2f}x")
        print(f"Move agreement: {'✓ Same move' if best_move_mm == best_move_ab else '✗ Different moves'}")
        
        fig = plot_performance_comparison(minimax_stats, alphabeta_stats,
                                         title=f"Test Position {test_num + 1} - Minimax vs Alpha-Beta")
        fig.savefig(output_dir / f"comparison_test{test_num + 1}.png", dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        save_game_state_image(game, output_dir / f"position{test_num + 1}_initial.png",
                            title=f"Test Position {test_num + 1} - Initial State")
        
        if best_move_mm is not None:
            game_copy = game.copy()
            move_sequence = []
            move_sequence.append(game_copy.copy())
            
            game_copy.make_move(best_move_mm)
            move_sequence.append(game_copy.copy())
            
            fig = plot_move_progression(move_sequence, 
                                      title=f"Test {test_num + 1} - Minimax Move Progression")
            fig.savefig(output_dir / f"moves_test{test_num + 1}.png", dpi=150, bbox_inches='tight')
            plt.close(fig)
    
    print("\n" + "="*70)
    print("AGGREGATE STATISTICS (across all test positions)")
    print("="*70)
    
    avg_minimax = {
        'nodes_expanded': np.mean([s['nodes_expanded'] for s in all_minimax_stats]),
        'time_taken': np.mean([s['time_taken'] for s in all_minimax_stats]),
        'max_depth_reached': max([s['max_depth_reached'] for s in all_minimax_stats]),
        'nodes_pruned': 0
    }
    
    avg_alphabeta = {
        'nodes_expanded': np.mean([s['nodes_expanded'] for s in all_alphabeta_stats]),
        'time_taken': np.mean([s['time_taken'] for s in all_alphabeta_stats]),
        'max_depth_reached': max([s['max_depth_reached'] for s in all_alphabeta_stats]),
        'nodes_pruned': np.mean([s['nodes_pruned'] for s in all_alphabeta_stats])
    }
    
    print(create_comparison_table(avg_minimax, avg_alphabeta))
    
    fig = plot_performance_comparison(avg_minimax, avg_alphabeta,
                                     title="Aggregate Performance: Minimax vs Alpha-Beta")
    fig.savefig(output_dir / "aggregate_comparison.png", dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    print(f"\nResults saved to: {output_dir}")
    print("\nDone!")


def interactive_demo():
    print("="*70)
    print("INTERACTIVE DEMO: Watch Minimax and Alpha-Beta play")
    print("="*70)
    
    game = Connect4Env()
    move_count = 0
    max_moves = 8
    
    print("\nStarting game:")
    print(game.get_board_string())
    
    while move_count < max_moves and not game.is_terminal():
        print(f"\n{'='*70}")
        print(f"Move {move_count + 1}")
        print(f"{'='*70}")
        
        if game.current_player == 1:
            print("Player 1 (X) - Using MINIMAX (depth=4)...")
            best_move, tracker = minimax_search(game, max_depth=4)
            print(f"Minimax chose: Column {best_move}")
            print(f"  Nodes expanded: {tracker.get_stats()['nodes_expanded']:,}")
            print(f"  Time: {tracker.get_stats()['time_taken']:.4f}s")
        else:
            print("Player 2 (O) - Using ALPHA-BETA (depth=4)...")
            best_move, tracker = alphabeta_search(game, max_depth=4)
            print(f"Alpha-Beta chose: Column {best_move}")
            print(f"  Nodes expanded: {tracker.get_stats()['nodes_expanded']:,}")
            print(f"  Nodes pruned: {tracker.get_stats()['nodes_pruned']:,}")
            print(f"  Time: {tracker.get_stats()['time_taken']:.4f}s")
        
        if best_move is None:
            print("No valid moves!")
            break
        
        game.make_move(best_move)
        print(f"\nBoard after move:")
        print(game.get_board_string())
        
        winner = game.check_winner()
        if winner == 1:
            print("\n🎉 Player 1 (X) wins!")
            break
        elif winner == -1:
            print("\n🎉 Player 2 (O) wins!")
            break
        elif winner == 0:
            print("\n🤝 Game is a draw!")
            break
        
        move_count += 1
    
    if move_count >= max_moves:
        print(f"\nStopped after {max_moves} moves (game may continue)")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Phase 2: Connect 4 Adversarial Search Demo")
    parser.add_argument("--mode", choices=["comparison", "interactive"], 
                       default="comparison",
                       help="Demo mode: comparison or interactive")
    parser.add_argument("--depth", type=int, default=4,
                       help="Maximum search depth (default: 4)")
    parser.add_argument("--tests", type=int, default=3,
                       help="Number of test positions for comparison (default: 3)")
    
    args = parser.parse_args()
    
    if args.mode == "comparison":
        run_algorithm_comparison(max_depth=args.depth, test_positions=args.tests)
    else:
        interactive_demo()
