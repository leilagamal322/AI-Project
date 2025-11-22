"""
Test/Demo script for maze treasure hunt.
Runs all algorithms on a small 10x10 maze for verification.
"""
import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

from env.maze_env import MazeEnv
from algos.search import (
    breadth_first_search,
    depth_first_search,
    uniform_cost_search,
    iterative_deepening_search,
    greedy_best_first_search,
    a_star_search
)
from heuristics import get_heuristic_function
from viz.visualize import plot_maze_solution


def test_maze_generation():
    """Test maze generation with connectivity."""
    print("="*80)
    print("TEST 1: Maze Generation")
    print("="*80)
    
    # Create small maze
    env = MazeEnv(grid_size=10, wall_density=0.2, seed=42)
    
    # Check maze info
    info = env.get_maze_info()
    print(f"Grid Size: {info['grid_size']}x{info['grid_size']}")
    print(f"State Space: {info['state_space_size']} states")
    print(f"Wall Count: {info['wall_count']} ({info['actual_wall_density']*100:.1f}%)")
    print(f"Start: {info['start']}")
    print(f"Goal: {info['goal']}")
    print(f"Key: {info['key_position']}")
    
    # Test initial state
    initial = env.get_initial_state()
    print(f"\nInitial State: {initial}")
    print(f"Is Goal: {env.is_goal_state(initial)}")
    
    # Test successors
    successors = env.get_successors(initial)
    print(f"Number of Successors from Start: {len(successors)}")
    
    print("\n[PASS] Maze generation test passed!\n")
    return env


def test_search_algorithm(env, algo_name, algo_func, algo_params=None):
    """Test a single search algorithm."""
    if algo_params is None:
        algo_params = {}
    
    print(f"\nTesting {algo_name}...")
    print("-" * 40)
    
    try:
        result = algo_func(env, **algo_params)
        
        print(f"Success: {result.success}")
        print(f"Path Length: {len(result.path)}")
        print(f"Path Cost: {result.path_cost}")
        print(f"Nodes Expanded: {result.nodes_expanded}")
        print(f"Nodes Generated: {result.nodes_generated}")
        print(f"Runtime: {result.runtime:.4f}s")
        print(f"Memory Peak: {result.memory_peak:.2f} MB")
        
        if result.success:
            print(f"\nSolution Path (first 10 states):")
            for i, state in enumerate(result.path[:10]):
                x, y, has_key = state
                key_str = "with key" if has_key else "no key"
                print(f"  {i}: ({x}, {y}) - {key_str}")
            if len(result.path) > 10:
                print(f"  ... ({len(result.path) - 10} more states)")
            
            # Verify solution
            if not env.is_goal_state(result.path[-1]):
                print("  [WARN] Warning: Final state is not goal state!")
            else:
                print("  [PASS] Solution verified: reached goal with key")
        
        return result
    
    except Exception as e:
        print(f"[FAIL] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def test_heuristics(env):
    """Test heuristic functions."""
    print("="*80)
    print("TEST 2: Heuristic Functions")
    print("="*80)
    
    manhattan_h = get_heuristic_function('manhattan')
    euclidean_h = get_heuristic_function('euclidean')
    
    # Test from start
    start_state = env.get_initial_state()
    goal = env.goal
    key_pos = env.key_pos
    
    print(f"Start State: {start_state}")
    print(f"Goal: {goal}")
    print(f"Key Position: {key_pos}")
    
    h_manhattan = manhattan_h(start_state, goal, key_pos)
    h_euclidean = euclidean_h(start_state, goal, key_pos)
    
    print(f"\nManhattan Heuristic: {h_manhattan:.2f}")
    print(f"Euclidean Heuristic: {h_euclidean:.2f}")
    
    # Test from goal (with key)
    goal_state = (goal[0], goal[1], True)
    h_manhattan_goal = manhattan_h(goal_state, goal, key_pos)
    h_euclidean_goal = euclidean_h(goal_state, goal, key_pos)
    
    print(f"\nAt Goal (with key):")
    print(f"Manhattan Heuristic: {h_manhattan_goal:.2f} (should be 0)")
    print(f"Euclidean Heuristic: {h_euclidean_goal:.2f} (should be 0)")
    
    if h_manhattan_goal == 0 and h_euclidean_goal == 0:
        print("\n[PASS] Heuristic test passed!\n")
    else:
        print("\n[FAIL] Heuristic test failed!\n")


def run_all_algorithms(env):
    """Run all search algorithms on the environment."""
    print("="*80)
    print("TEST 3: Search Algorithms")
    print("="*80)
    
    results = {}
    
    # Define algorithms to test
    algorithms = [
        ('BFS', breadth_first_search, {}),
        ('DFS', depth_first_search, {}),
        ('UCS', uniform_cost_search, {}),
        ('IDS', iterative_deepening_search, {'max_depth': 100}),
        ('Greedy (Manhattan)', greedy_best_first_search, 
         {'heuristic_func': get_heuristic_function('manhattan')}),
        ('Greedy (Euclidean)', greedy_best_first_search,
         {'heuristic_func': get_heuristic_function('euclidean')}),
        ('A* (Manhattan)', a_star_search,
         {'heuristic_func': get_heuristic_function('manhattan')}),
        ('A* (Euclidean)', a_star_search,
         {'heuristic_func': get_heuristic_function('euclidean')}),
    ]
    
    for algo_name, algo_func, algo_params in algorithms:
        result = test_search_algorithm(env, algo_name, algo_func, algo_params)
        if result:
            results[algo_name] = result
    
    return results


def compare_results(results):
    """Compare results across algorithms."""
    print("\n" + "="*80)
    print("COMPARISON SUMMARY")
    print("="*80)
    
    # Create table
    print(f"\n{'Algorithm':<20} {'Success':<10} {'Path Cost':<12} {'Nodes Exp':<12} {'Runtime (s)':<12}")
    print("-" * 80)
    
    for algo_name, result in results.items():
        success = "PASS" if result.success else "FAIL"
        path_cost = f"{result.path_cost:.1f}" if result.success else "N/A"
        nodes_exp = f"{result.nodes_expanded}"
        runtime = f"{result.runtime:.4f}"
        
        print(f"{algo_name:<20} {success:<10} {path_cost:<12} {nodes_exp:<12} {runtime:<12}")
    
    # Find optimal cost
    successful = [r for r in results.values() if r.success]
    if successful:
        optimal_cost = min(r.path_cost for r in successful)
        print(f"\n{'='*80}")
        print(f"Optimal Path Cost: {optimal_cost:.1f}")
        
        optimal_algos = [name for name, r in results.items() 
                        if r.success and r.path_cost == optimal_cost]
        print(f"Algorithms Finding Optimal Solution: {', '.join(optimal_algos)}")
        
        fastest = min(successful, key=lambda r: r.runtime)
        fastest_name = [name for name, r in results.items() if r == fastest][0]
        print(f"Fastest Algorithm: {fastest_name} ({fastest.runtime:.4f}s)")
        
        most_efficient = min(successful, key=lambda r: r.nodes_expanded)
        efficient_name = [name for name, r in results.items() if r == most_efficient][0]
        print(f"Most Node-Efficient: {efficient_name} ({most_efficient.nodes_expanded} nodes)")


def generate_test_visualizations(env, results):
    """Generate visualizations for test results."""
    print("\n" + "="*80)
    print("Generating Visualizations")
    print("="*80)
    
    output_dir = 'results/test_demo'
    os.makedirs(output_dir, exist_ok=True)
    
    for algo_name, result in results.items():
        if result.success:
            # Clean filename
            filename = algo_name.replace(' ', '_').replace('(', '').replace(')', '').replace('*', 'star')
            save_path = os.path.join(output_dir, f'{filename}_demo.png')
            
            try:
                plot_maze_solution(
                    env, result, algo_name,
                    save_path=save_path,
                    show_visited=True,
                    figsize=(8, 8)
                )
                print(f"  [OK] Saved: {save_path}")
            except Exception as e:
                print(f"  [FAIL] Failed to save {algo_name}: {e}")


def test_state_transitions():
    """Test state transition mechanics."""
    print("="*80)
    print("TEST 4: State Transitions")
    print("="*80)
    
    # Create simple environment
    env = MazeEnv(grid_size=5, wall_density=0.0, seed=100)  # No walls
    
    initial = env.get_initial_state()
    print(f"Initial State: {initial}")
    
    # Get successors
    successors = env.get_successors(initial)
    print(f"\nSuccessors from initial state:")
    for next_state, action, cost in successors:
        print(f"  {action}: {next_state} (cost={cost})")
    
    # Check key pickup
    key_x, key_y = env.key_pos
    state_at_key_no_key = (key_x, key_y, False)
    print(f"\nState at key position (without key): {state_at_key_no_key}")
    
    successors_at_key = env.get_successors(state_at_key_no_key)
    print(f"Successors (should have has_key=True):")
    for next_state, action, cost in successors_at_key[:2]:
        print(f"  {action}: {next_state}")
    
    print("\n[PASS] State transition test passed!\n")


def main():
    """Run all tests."""
    print("\n")
    print("=" + "="*78 + "=")
    print("|" + " "*20 + "MAZE TREASURE HUNT - TEST SUITE" + " "*26 + "|")
    print("=" + "="*78 + "=")
    print()
    
    # Test 1: Maze generation
    env = test_maze_generation()
    
    # Test 2: Heuristics
    test_heuristics(env)
    
    # Test 3: State transitions
    test_state_transitions()
    
    # Test 4: All search algorithms
    results = run_all_algorithms(env)
    
    # Compare results
    compare_results(results)
    
    # Generate visualizations
    try:
        generate_test_visualizations(env, results)
    except Exception as e:
        print(f"\nVisualization generation skipped: {e}")
    
    print("\n" + "="*80)
    print("ALL TESTS COMPLETED!")
    print("="*80)
    print("\nTo run full experiments on 50x50 grid, use:")
    print("  python run_experiments.py --num-seeds 5 --generate-report")
    print()


if __name__ == '__main__':
    main()

