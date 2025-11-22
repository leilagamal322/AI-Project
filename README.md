# Maze Treasure Hunt - Search Algorithms Comparison

A comprehensive implementation of multiple search algorithms (BFS, DFS, UCS, IDS, Greedy Best-First, A*, MinMax with Alpha-Beta) applied to a maze navigation problem with a key-collection requirement.

## 🎯 Problem Description

### Environment
- **Grid**: 50×50 (configurable)
- **Obstacles**: Randomly placed walls (20% density by default)
- **Objective**: Navigate from start (0,0) to goal (49,49) while collecting a key
- **Constraint**: Player must collect the key before reaching the goal
- **Movement**: 4-directional (Up, Down, Left, Right)
- **Cost**: Uniform cost of 1 per move

### State Space
- **State Representation**: `(x, y, has_key)`
  - `x, y`: Current position in grid
  - `has_key`: Boolean flag indicating key possession
- **State Space Size**: 50 × 50 × 2 = 5,000 states

## 📁 Project Structure

```
.
├── env/
│   └── maze_env.py          # Maze environment with random generation
├── algos/
│   └── search.py            # All search algorithm implementations
├── viz/
│   └── visualize.py         # Visualization functions (matplotlib)
├── heuristics.py            # Heuristic functions (Manhattan, Euclidean)
├── run_experiments.py       # Main experiment orchestration script
├── test_demo.py             # Test script for 10×10 verification
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Quick Start

### Installation

1. Clone or download the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running Tests

First, verify the implementation with a small 10×10 maze:

```bash
python test_demo.py
```

This will:
- Test maze generation and connectivity
- Test all search algorithms
- Generate visualizations in `results/test_demo/`
- Display comparison of algorithm performance

### Running Full Experiments

Run experiments on 50×50 mazes with multiple random seeds:

```bash
# Basic run (5 seeds, default algorithms)
python run_experiments.py

# Custom configuration
python run_experiments.py --grid-size 50 --wall-density 0.2 --num-seeds 10

# Generate comprehensive report
python run_experiments.py --generate-report

# With specific algorithms
python run_experiments.py --algorithms bfs astar_manhattan astar_euclidean --num-seeds 3

# Enable MinMax adversary mode (experimental)
python run_experiments.py --enable-adversary --minmax-depth 4
```

### Command-Line Arguments

```
--grid-size SIZE          Grid dimensions (default: 50)
--wall-density DENSITY    Wall probability 0-1 (default: 0.2)
--algorithms ALGOS        Space-separated algorithm list
--num-seeds N            Number of random seeds (default: 5)
--base-seed SEED         Starting seed value (default: 42)
--enable-adversary       Enable MinMax adversary mode
--minmax-depth DEPTH     MinMax search depth (default: 4)
--output-dir DIR         Output directory (default: results)
--no-viz                 Disable visualizations
--quiet                  Suppress output
--generate-report        Generate markdown report
```

## 🔍 Implemented Algorithms

### Uninformed Search
1. **BFS (Breadth-First Search)**
   - Complete: ✓
   - Optimal: ✓ (for uniform costs)
   - Strategy: Explores states level by level

2. **DFS (Depth-First Search)**
   - Complete: ✓ (with depth limit)
   - Optimal: ✗
   - Strategy: Explores deepest paths first

3. **UCS (Uniform Cost Search)**
   - Complete: ✓
   - Optimal: ✓
   - Strategy: Expands lowest-cost nodes first

4. **IDS (Iterative Deepening Search)**
   - Complete: ✓
   - Optimal: ✓ (for uniform costs)
   - Strategy: Combines DFS memory efficiency with BFS completeness

### Informed Search

5. **Greedy Best-First Search**
   - Complete: ✗
   - Optimal: ✗
   - Heuristics: Manhattan or Euclidean distance
   - Strategy: Expands nodes with best heuristic value

6. **A\* Search**
   - Complete: ✓
   - Optimal: ✓ (with admissible heuristic)
   - Heuristics: Manhattan or Euclidean distance
   - Strategy: Uses f(n) = g(n) + h(n)

### Adversarial Search

7. **MinMax with Alpha-Beta Pruning**
   - Strategy: Turn-based game tree search
   - Player: Minimize path to goal
   - Adversary: Place obstacles to maximize cost
   - Pruning: Alpha-Beta for efficiency

## 📊 Heuristics

Both heuristics are **admissible** (never overestimate true cost):

### Manhattan Distance
```python
if has_key:
    h = |x - goal_x| + |y - goal_y|
else:
    h = |x - key_x| + |y - key_y| + |key_x - goal_x| + |key_y - goal_y|
```

### Euclidean Distance
Similar to Manhattan but using Euclidean distance formula.

**Note**: Manhattan is more suitable for 4-directional grid movement.

## 📈 Performance Metrics

For each algorithm run, the following metrics are collected:

- **Success**: Whether goal was reached with key
- **Runtime**: Wall-clock execution time (seconds)
- **Nodes Expanded**: Number of states explored
- **Nodes Generated**: Total states generated
- **Path Length**: Number of steps in solution
- **Path Cost**: Total cost of solution path
- **Memory Peak**: Peak memory usage (MB)

## 📊 Output Files

### Results Directory Structure
```
results/
├── results_TIMESTAMP.csv              # Raw experimental data
├── summary_TIMESTAMP.csv              # Summary statistics
├── comparison_runtime_TIMESTAMP.png   # Runtime comparison chart
├── comparison_nodes_expanded_TIMESTAMP.png
├── comparison_multi_TIMESTAMP.png     # Multi-metric comparison
├── viz_ALGORITHM_seedN_TIMESTAMP.png  # Individual solution visualizations
└── report/
    └── report_TIMESTAMP.md           # Comprehensive report
```

### Visualizations

Each visualization includes:
- Grid with walls (black)
- Start position (green)
- Goal position (red)
- Key position (gold star)
- Visited states (light blue overlay)
- Solution path (yellow with red line)

## 🧪 Example Usage

### Python API

```python
from env.maze_env import MazeEnv
from algos.search import a_star_search
from heuristics import get_heuristic_function

# Create environment
env = MazeEnv(grid_size=20, wall_density=0.2, seed=42)

# Run A* with Manhattan heuristic
heuristic = get_heuristic_function('manhattan')
result = a_star_search(env, heuristic)

# Check results
if result.success:
    print(f"Solution found! Cost: {result.path_cost}")
    print(f"Path length: {len(result.path)}")
    print(f"Nodes expanded: {result.nodes_expanded}")
```

## 🔬 Experimental Design

### Default Configuration
- **Grid Size**: 50×50
- **Wall Density**: 20%
- **Random Seeds**: 5 different mazes
- **Connectivity**: Guaranteed paths start→key→goal

### Maze Generation
- Uses deterministic random seed for reproducibility
- Validates connectivity using BFS
- Regenerates if no valid path exists
- Maximum 100 attempts before reducing wall density

## 📝 Report Generation

The `--generate-report` flag creates a comprehensive markdown report including:

1. **Problem Definition**
   - Environment specifications
   - State space analysis
   - Algorithm descriptions

2. **Experimental Setup**
   - Configuration parameters
   - Maze characteristics

3. **Results**
   - Summary statistics table
   - Success rates
   - Performance metrics

4. **Analysis**
   - Optimality comparison
   - Completeness verification
   - Performance rankings

5. **Conclusions**
   - Key findings
   - Algorithm recommendations

## 🎨 Visualization Features

- **Solution Paths**: Yellow overlay with red path line
- **Visited States**: Light blue semi-transparent overlay
- **Special Locations**: Start (green), Goal (red), Key (gold star)
- **Heatmaps**: Visit frequency visualization
- **Comparison Charts**: Bar charts with error bars

## ⚡ Performance Considerations

### For 50×50 Grids:
- **BFS/UCS**: May expand 1000-3000 nodes
- **A\***: Typically 100-500 nodes (most efficient)
- **DFS**: Variable, depends on path structure
- **IDS**: High node count due to repeated searches
- **Greedy**: Very fast but may not find optimal solution

### MinMax with Adversary:
- Computationally expensive (exponential in depth)
- Default depth=4 is reasonable for demonstration
- Limit adversary actions for tractability
- May require reduced grid size (20×20) for interactive play

## 🛠️ Troubleshooting

### No Valid Maze Generated
- Reduce wall density (--wall-density 0.1)
- Use larger grid size
- Try different random seed

### Out of Memory
- Reduce grid size
- Reduce number of seeds
- Disable visualizations (--no-viz)
- Use more efficient algorithms (A*, Greedy)

### Slow Performance
- Reduce grid size for testing
- Use fewer seeds
- Avoid IDS on large grids
- Disable adversary mode

## 📚 Dependencies

- **Python**: 3.7+
- **NumPy**: Array operations and random generation
- **Matplotlib**: Visualization and plotting
- **Pandas**: Data analysis and CSV export

See `requirements.txt` for specific versions.

## 🎓 Educational Value

This project demonstrates:
- **Search algorithm implementation** from scratch
- **Performance comparison** across algorithm families
- **Heuristic design** for informed search
- **State space modeling** with constraints
- **Experimental methodology** with reproducible results
- **Data visualization** and reporting

## 📄 License

This project is provided for educational purposes.

## 🤝 Contributing

Suggestions for improvements:
- Additional search algorithms (Bidirectional, RBFS, etc.)
- Advanced heuristics (pattern databases)
- Interactive visualization (animated GIFs, step-through)
- Parallel algorithm execution
- More sophisticated adversary strategies

## 📞 Support

For issues or questions:
1. Check the test script: `python test_demo.py`
2. Review generated reports in `results/report/`
3. Examine visualizations for debugging

---

**Version**: 1.0  
**Last Updated**: November 2025

