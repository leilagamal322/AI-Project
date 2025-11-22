# Usage Examples

This document provides practical examples for using the Maze Treasure Hunt search algorithms.

## Quick Start Examples

### Example 1: Basic Test Run

Run all algorithms on a small 10×10 maze for verification:

```bash
py test_demo.py
```

**Output:**
- Console output with metrics for all algorithms
- Visualizations saved to `results/test_demo/`
- Comparison summary showing optimal paths

### Example 2: Simple Experiment (5 Seeds)

Run experiments with default settings:

```bash
py run_experiments.py
```

**Default Configuration:**
- Grid: 50×50
- Wall Density: 20%
- Seeds: 5
- Algorithms: BFS, DFS, UCS, IDS, Greedy (Manhattan), A* (Manhattan), A* (Euclidean)

**Output:**
- `results/results_TIMESTAMP.csv` - Raw data
- `results/summary_TIMESTAMP.csv` - Summary statistics
- `results/viz_*.png` - Individual solution visualizations
- `results/comparison_*.png` - Performance comparison charts

### Example 3: Generate Full Report

Run experiments and generate a comprehensive markdown report:

```bash
py run_experiments.py --generate-report
```

**Output:** 
- All files from Example 2
- `results/report/report_TIMESTAMP.md` - Detailed analysis report

### Example 4: Custom Grid Size

Run on a smaller 20×20 grid for faster experiments:

```bash
py run_experiments.py --grid-size 20 --num-seeds 10
```

### Example 5: Custom Wall Density

Create a more challenging maze with 30% walls:

```bash
py run_experiments.py --wall-density 0.3 --num-seeds 5
```

### Example 6: Specific Algorithms Only

Run only A* variants:

```bash
py run_experiments.py --algorithms astar_manhattan astar_euclidean
```

**Available Algorithm Keys:**
- `bfs` - Breadth-First Search
- `dfs` - Depth-First Search
- `ucs` - Uniform Cost Search
- `ids` - Iterative Deepening Search
- `greedy_manhattan` - Greedy Best-First (Manhattan)
- `greedy_euclidean` - Greedy Best-First (Euclidean)
- `astar_manhattan` - A* (Manhattan)
- `astar_euclidean` - A* (Euclidean)

### Example 7: Adversary Mode (MinMax)

Enable adversarial search with MinMax and Alpha-Beta pruning:

```bash
py run_experiments.py --enable-adversary --minmax-depth 4 --grid-size 20
```

**Note:** MinMax is computationally expensive. Use smaller grids (20×20) and shallow depth.

### Example 8: Quick Test (No Visualizations)

Run experiments without generating visualizations (faster):

```bash
py run_experiments.py --no-viz --num-seeds 3
```

### Example 9: Quiet Mode

Run with minimal console output:

```bash
py run_experiments.py --quiet --num-seeds 5
```

### Example 10: Full Production Run

Comprehensive experiment with report:

```bash
py run_experiments.py --grid-size 50 --wall-density 0.2 --num-seeds 10 --generate-report
```

## Python API Examples

### Example 11: Programmatic Usage

```python
from env.maze_env import MazeEnv
from algos.search import a_star_search, breadth_first_search
from heuristics import get_heuristic_function
from viz.visualize import plot_maze_solution

# Create environment
env = MazeEnv(grid_size=30, wall_density=0.2, seed=42)

# Print maze info
info = env.get_maze_info()
print(f"Grid: {info['grid_size']}x{info['grid_size']}")
print(f"State space: {info['state_space_size']} states")
print(f"Key at: {info['key_position']}")

# Run BFS
bfs_result = breadth_first_search(env)
print(f"\nBFS Results:")
print(f"  Success: {bfs_result.success}")
print(f"  Path cost: {bfs_result.path_cost}")
print(f"  Nodes expanded: {bfs_result.nodes_expanded}")
print(f"  Runtime: {bfs_result.runtime:.4f}s")

# Run A* with Manhattan heuristic
heuristic = get_heuristic_function('manhattan')
astar_result = a_star_search(env, heuristic)
print(f"\nA* Results:")
print(f"  Success: {astar_result.success}")
print(f"  Path cost: {astar_result.path_cost}")
print(f"  Nodes expanded: {astar_result.nodes_expanded}")
print(f"  Runtime: {astar_result.runtime:.4f}s")

# Visualize A* solution
plot_maze_solution(env, astar_result, "A* Solution", 
                  save_path="my_solution.png")
```

### Example 12: Custom Maze Configuration

```python
from env.maze_env import MazeEnv

# Create maze with custom start and goal
env = MazeEnv(
    grid_size=25,
    wall_density=0.15,
    seed=123,
    start=(0, 0),
    goal=(24, 24)
)

# Get initial state
state = env.get_initial_state()
print(f"Initial state: {state}")  # (0, 0, False)

# Check if goal
print(f"Is goal: {env.is_goal_state(state)}")  # False

# Get possible actions
successors = env.get_successors(state)
print(f"Available moves: {len(successors)}")

for next_state, action, cost in successors:
    print(f"  {action}: move to {next_state[:2]}, cost={cost}")
```

### Example 13: Compare Multiple Heuristics

```python
from env.maze_env import MazeEnv
from algos.search import a_star_search
from heuristics import manhattan_distance, euclidean_distance

env = MazeEnv(grid_size=40, wall_density=0.2, seed=42)

# Try both heuristics
results = {}

for heuristic_name, heuristic_func in [
    ('Manhattan', manhattan_distance),
    ('Euclidean', euclidean_distance)
]:
    result = a_star_search(env, heuristic_func)
    results[heuristic_name] = result
    
    print(f"\nA* with {heuristic_name}:")
    print(f"  Path cost: {result.path_cost}")
    print(f"  Nodes expanded: {result.nodes_expanded}")
    print(f"  Runtime: {result.runtime:.4f}s")

# Find best
best = min(results.items(), key=lambda x: x[1].nodes_expanded)
print(f"\nMost efficient: {best[0]}")
```

### Example 14: Batch Processing Multiple Seeds

```python
from env.maze_env import MazeEnv
from algos.search import a_star_search
from heuristics import get_heuristic_function
import pandas as pd

heuristic = get_heuristic_function('manhattan')
results_list = []

# Run on 10 different mazes
for seed in range(10):
    env = MazeEnv(grid_size=30, wall_density=0.2, seed=seed)
    result = a_star_search(env, heuristic)
    
    results_list.append({
        'seed': seed,
        'success': result.success,
        'path_cost': result.path_cost,
        'nodes_expanded': result.nodes_expanded,
        'runtime': result.runtime
    })

# Create DataFrame and compute statistics
df = pd.DataFrame(results_list)
print("\nSummary Statistics:")
print(df.describe())

# Save to CSV
df.to_csv('batch_results.csv', index=False)
print("\nResults saved to batch_results.csv")
```

### Example 15: Custom Visualization

```python
from env.maze_env import MazeEnv
from algos.search import greedy_best_first_search
from heuristics import get_heuristic_function
from viz.visualize import plot_maze_solution, plot_heatmap

env = MazeEnv(grid_size=25, wall_density=0.2, seed=99)
heuristic = get_heuristic_function('manhattan')
result = greedy_best_first_search(env, heuristic)

# Plot solution with visited states
plot_maze_solution(
    env, result, 
    "Greedy Best-First Search",
    save_path="greedy_solution.png",
    show_visited=True,
    figsize=(12, 12)
)

# Plot heatmap of visits
plot_heatmap(
    env,
    result.visited_states,
    "Greedy Best-First Search",
    save_path="greedy_heatmap.png"
)
```

## Advanced Examples

### Example 16: MinMax with Custom Configuration

```python
from env.maze_env import MazeEnv
from algos.search import minmax_search
from heuristics import get_heuristic_function

# Create smaller environment for MinMax
env = MazeEnv(grid_size=15, wall_density=0.15, seed=42)

# Run MinMax with Alpha-Beta pruning
result = minmax_search(
    env,
    heuristic_func=get_heuristic_function('manhattan'),
    max_depth=6,  # Search depth
    adversary_radius=3,  # Wall placement radius
    adversary_frequency=2,  # Adversary acts every 2 moves
    use_alpha_beta=True  # Enable pruning
)

print(f"MinMax Results:")
print(f"  Success: {result.success}")
print(f"  Path length: {len(result.path)}")
print(f"  Nodes expanded: {result.nodes_expanded}")
print(f"  Runtime: {result.runtime:.4f}s")
```

### Example 17: Testing Maze Connectivity

```python
from env.maze_env import MazeEnv

# Generate maze and check connectivity
for density in [0.1, 0.2, 0.3, 0.4]:
    env = MazeEnv(grid_size=30, wall_density=density, seed=42)
    
    # Check if paths exist
    start_to_key = env._is_connected(env.start, env.key_pos)
    key_to_goal = env._is_connected(env.key_pos, env.goal)
    
    print(f"Density {density*100:.0f}%:")
    print(f"  Start->Key: {start_to_key}")
    print(f"  Key->Goal: {key_to_goal}")
    print(f"  Valid maze: {start_to_key and key_to_goal}")
```

### Example 18: Performance Profiling

```python
import time
from env.maze_env import MazeEnv
from algos.search import *
from heuristics import get_heuristic_function

env = MazeEnv(grid_size=40, wall_density=0.2, seed=42)
heuristic = get_heuristic_function('manhattan')

algorithms = [
    ('BFS', breadth_first_search, {}),
    ('DFS', depth_first_search, {}),
    ('UCS', uniform_cost_search, {}),
    ('A*', a_star_search, {'heuristic_func': heuristic}),
    ('Greedy', greedy_best_first_search, {'heuristic_func': heuristic})
]

print(f"{'Algorithm':<15} {'Time (s)':<12} {'Nodes':<10} {'Optimal':<10}")
print("-" * 50)

for name, algo_func, params in algorithms:
    result = algo_func(env, **params)
    optimal = result.path_cost == 18 if result.success else False
    
    print(f"{name:<15} {result.runtime:<12.4f} {result.nodes_expanded:<10} {optimal}")
```

## Tips and Best Practices

### For Small Experiments (Testing)
```bash
py run_experiments.py --grid-size 10 --num-seeds 3 --algorithms bfs astar_manhattan
```

### For Medium Experiments (Development)
```bash
py run_experiments.py --grid-size 30 --num-seeds 5
```

### For Full Experiments (Publication)
```bash
py run_experiments.py --grid-size 50 --num-seeds 20 --generate-report
```

### For Performance Analysis
```bash
py run_experiments.py --algorithms astar_manhattan astar_euclidean greedy_manhattan --num-seeds 10
```

### For Adversarial Testing
```bash
py run_experiments.py --enable-adversary --grid-size 20 --minmax-depth 5 --num-seeds 3
```

## Common Issues and Solutions

### Issue: Python not found
**Solution:** Use `py` instead of `python` on Windows

### Issue: Maze generation timeout
**Solution:** Reduce wall density: `--wall-density 0.15`

### Issue: Out of memory
**Solution:** Reduce grid size: `--grid-size 30`

### Issue: Slow performance
**Solution:** Use fewer seeds and efficient algorithms:
```bash
py run_experiments.py --algorithms astar_manhattan greedy_manhattan --num-seeds 3
```

## Output Directory Structure

After running experiments, you'll have:

```
results/
├── results_20231122_143022.csv          # Raw data
├── summary_20231122_143022.csv          # Statistics
├── comparison_runtime_20231122_143022.png
├── comparison_nodes_expanded_20231122_143022.png
├── comparison_multi_20231122_143022.png
├── viz_bfs_seed42_20231122_143022.png
├── viz_astar_manhattan_seed42_20231122_143022.png
└── report/
    └── report_20231122_143022.md        # Full report
```

---

For more information, see the main [README.md](README.md).

