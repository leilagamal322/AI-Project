"""
Quick demonstration script showing basic usage.
Creates a small maze and runs A* algorithm with visualization.
"""
import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

from env.maze_env import MazeEnv
from algos.search import a_star_search
from heuristics import get_heuristic_function
from viz.visualize import plot_maze_solution


def main():
    print("\n" + "="*60)
    print("  MAZE TREASURE HUNT - QUICK DEMO")
    print("="*60)
    
    # Configuration
    grid_size = 20
    wall_density = 0.2
    seed = 42
    
    print(f"\nConfiguration:")
    print(f"  Grid Size: {grid_size}x{grid_size}")
    print(f"  Wall Density: {wall_density*100:.0f}%")
    print(f"  Random Seed: {seed}")
    
    # Create environment
    print("\n[1/3] Creating maze environment...")
    env = MazeEnv(grid_size=grid_size, wall_density=wall_density, seed=seed)
    
    info = env.get_maze_info()
    print(f"  [OK] Maze created successfully")
    print(f"  - Passable cells: {info['passable_cells']}")
    print(f"  - State space: {info['state_space_size']} states")
    print(f"  - Key location: {info['key_position']}")
    
    # Run A* algorithm
    print("\n[2/3] Running A* with Manhattan heuristic...")
    heuristic = get_heuristic_function('manhattan')
    result = a_star_search(env, heuristic)
    
    if result.success:
        print(f"  [OK] Solution found!")
        print(f"  - Path length: {len(result.path)} states")
        print(f"  - Path cost: {result.path_cost}")
        print(f"  - Nodes expanded: {result.nodes_expanded}")
        print(f"  - Nodes generated: {result.nodes_generated}")
        print(f"  - Runtime: {result.runtime:.4f} seconds")
        print(f"  - Memory peak: {result.memory_peak:.2f} MB")
        
        # Show first few steps
        print(f"\n  First 5 steps of solution:")
        for i, state in enumerate(result.path[:5]):
            x, y, has_key = state
            key_status = "[KEY]" if has_key else "[   ]"
            print(f"    {i}. Position ({x:2d}, {y:2d}) {key_status}")
    else:
        print(f"  [FAIL] No solution found")
        return
    
    # Generate visualization
    print("\n[3/3] Generating visualization...")
    output_path = "quick_demo_result.png"
    
    plot_maze_solution(
        env, 
        result, 
        "A* Search Solution",
        save_path=output_path,
        show_visited=True,
        figsize=(10, 10)
    )
    
    print(f"  [OK] Visualization saved to: {output_path}")
    
    print("\n" + "="*60)
    print("  DEMO COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("  • View the visualization: quick_demo_result.png")
    print("  • Run full tests: py test_demo.py")
    print("  • Run experiments: py run_experiments.py")
    print("  • Read documentation: README.md")
    print()


if __name__ == '__main__':
    main()

