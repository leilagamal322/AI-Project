# Getting Started with Maze Treasure Hunt

Welcome! This guide will help you get up and running quickly.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- numpy (array operations)
- matplotlib (visualization)
- pandas (data analysis)

### Step 2: Verify Installation

Check that Python can find all modules:

```bash
py -c "import numpy, matplotlib, pandas; print('All dependencies installed!')"
```

## Quick Start (5 minutes)

### Option 1: Quick Demo

Run a simple demonstration on a 20×20 maze:

```bash
py quick_demo.py
```

**What it does:**
- Creates a small maze
- Runs A* algorithm
- Shows performance metrics
- Generates visualization

**Output:**
- Console: Performance statistics
- File: `quick_demo_result.png` (visualization)

### Option 2: Comprehensive Tests

Run all algorithms on a 10×10 maze:

```bash
py test_demo.py
```

**What it does:**
- Tests all 8 search algorithms
- Verifies correctness
- Compares performance
- Generates visualizations

**Output:**
- Console: Detailed test results and comparison
- Directory: `results/test_demo/*.png` (8 visualizations)

## Basic Usage

### Running Experiments

#### 1. Default Configuration

```bash
py run_experiments.py
```

Runs 5 seeds on 50×50 maze with 7 algorithms.

#### 2. With Report Generation

```bash
py run_experiments.py --generate-report
```

Same as above, plus generates a comprehensive markdown report.

#### 3. Custom Configuration

```bash
py run_experiments.py --grid-size 30 --wall-density 0.15 --num-seeds 10
```

Customize grid size, wall density, and number of random seeds.

## Understanding the Output

### Console Output

You'll see progress like this:

```
================================================================================
MAZE TREASURE HUNT EXPERIMENTS
================================================================================
Grid Size: 50x50
Wall Density: 0.2
Number of Seeds: 5
Algorithms: bfs, dfs, ucs, ids, greedy_manhattan, astar_manhattan, astar_euclidean
Output Directory: results
================================================================================

[Seed 1/5] Creating maze (seed=42)...
  Maze created: 1943 passable cells, key at (38, 27)
  Running BFS... SUCCESS (runtime: 0.0234s)
  Running DFS... SUCCESS (runtime: 0.0156s)
  Running UCS... SUCCESS (runtime: 0.0289s)
  ...
```

### Output Files

After running experiments, check the `results/` directory:

```
results/
├── results_TIMESTAMP.csv              # Raw data (all runs)
├── summary_TIMESTAMP.csv              # Summary statistics
├── comparison_runtime_TIMESTAMP.png   # Runtime comparison
├── comparison_nodes_expanded_TIMESTAMP.png
├── comparison_multi_TIMESTAMP.png     # Multi-metric view
├── viz_*.png                          # Individual solutions
└── report/
    └── report_TIMESTAMP.md            # Full report
```

## Common Commands

### Quick Test (Recommended for first run)

```bash
py quick_demo.py
```

### Full Test Suite

```bash
py test_demo.py
```

### Small Experiment (Fast)

```bash
py run_experiments.py --grid-size 20 --num-seeds 3
```

### Standard Experiment

```bash
py run_experiments.py --num-seeds 5
```

### Large Experiment (Slow but thorough)

```bash
py run_experiments.py --num-seeds 20 --generate-report
```

### Test Specific Algorithms

```bash
py run_experiments.py --algorithms astar_manhattan astar_euclidean
```

### Quiet Mode (Less output)

```bash
py run_experiments.py --quiet
```

## Next Steps

### 1. Explore Visualizations

Open any PNG file in `results/` or `results/test_demo/` to see:
- Maze layout with walls
- Start (green), goal (red), key (gold star)
- Visited states (light blue)
- Solution path (yellow with red line)

### 2. Read the Report

If you used `--generate-report`, open:

```
results/report/report_TIMESTAMP.md
```

This contains:
- Problem definition
- Algorithm descriptions
- Performance comparison
- Analysis and conclusions

### 3. Examine Raw Data

Open CSV files with Excel, Python pandas, or any spreadsheet software:

```python
import pandas as pd
df = pd.read_csv('results/results_TIMESTAMP.csv')
print(df.describe())
```

### 4. Try Advanced Examples

See `EXAMPLES.md` for 18 detailed usage examples, including:
- Python API usage
- Custom configurations
- Batch processing
- Advanced visualizations

## Troubleshooting

### Problem: "Python not found"

**Windows:**
```bash
py quick_demo.py    # Use 'py' launcher
```

**Linux/Mac:**
```bash
python3 quick_demo.py
```

### Problem: "Module not found"

**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Problem: "Maze generation timeout"

**Solution:** Reduce wall density
```bash
py run_experiments.py --wall-density 0.15
```

### Problem: "Out of memory"

**Solution:** Use smaller grid
```bash
py run_experiments.py --grid-size 30
```

### Problem: "Too slow"

**Solutions:**
```bash
# Fewer seeds
py run_experiments.py --num-seeds 3

# Smaller grid
py run_experiments.py --grid-size 20

# Faster algorithms only
py run_experiments.py --algorithms astar_manhattan greedy_manhattan

# No visualizations
py run_experiments.py --no-viz
```

## Learning Path

### Level 1: Beginner (Start here!)

1. Run quick demo
   ```bash
   py quick_demo.py
   ```

2. Run test suite
   ```bash
   py test_demo.py
   ```

3. Look at generated visualizations

4. Read `README.md` introduction

### Level 2: Intermediate

1. Run experiments with different configurations
   ```bash
   py run_experiments.py --grid-size 30 --num-seeds 5
   ```

2. Generate and read report
   ```bash
   py run_experiments.py --generate-report
   ```

3. Explore `EXAMPLES.md` for usage patterns

4. Examine the CSV data files

### Level 3: Advanced

1. Use Python API directly (see Example 11 in `EXAMPLES.md`)

2. Modify algorithms in `algos/search.py`

3. Create custom heuristics in `heuristics.py`

4. Add new experiments in `run_experiments.py`

5. Read the code and understand implementation details

## Key Files Reference

| File | Purpose | When to Use |
|------|---------|-------------|
| `quick_demo.py` | Simple demo | First run, quick test |
| `test_demo.py` | Comprehensive tests | Verify installation |
| `run_experiments.py` | Main experiments | Actual research/analysis |
| `README.md` | Full documentation | Complete reference |
| `EXAMPLES.md` | Usage examples | Learn specific tasks |
| `PROJECT_SUMMARY.md` | Project overview | Understand structure |

## Tips

1. **Start small**: Use 10×10 or 20×20 grids for testing
2. **Use seeds**: Same seed = same maze (reproducibility)
3. **Save reports**: Use `--generate-report` for comprehensive analysis
4. **Compare algorithms**: Look at comparison plots in results/
5. **Check optimality**: Report shows which algorithms found optimal solutions

## Expected Performance

On a typical laptop:

| Grid Size | Algorithms | Seeds | Time |
|-----------|-----------|-------|------|
| 10×10 | All (8) | 1 | ~1 second |
| 20×20 | All (8) | 5 | ~10 seconds |
| 50×50 | All (7)* | 5 | ~30-60 seconds |

*Excluding MinMax (too slow for large grids)

## What to Expect

### Typical Results (50×50 maze)

- **Optimal Path Cost**: ~40-60 moves
- **Fastest Algorithm**: Greedy Best-First or A*
- **Most Node-Efficient**: A* with Manhattan heuristic
- **Most Reliable**: BFS, UCS, A*

### Visualizations

You'll see:
- Black cells = walls
- White cells = passable
- Light blue = visited by algorithm
- Yellow = solution path
- Green square = start
- Red square = goal
- Gold star = key

## Getting Help

1. **README.md**: Comprehensive documentation
2. **EXAMPLES.md**: 18 practical examples
3. **Code comments**: All functions documented
4. **Test output**: Shows expected behavior

## Quick Reference Card

```bash
# Quick test
py quick_demo.py

# Full test
py test_demo.py

# Basic experiment
py run_experiments.py

# With report
py run_experiments.py --generate-report

# Custom size
py run_experiments.py --grid-size 30

# Specific algorithms
py run_experiments.py --algorithms astar_manhattan astar_euclidean

# Help
py run_experiments.py --help
```

---

**Ready to start?** Run:

```bash
py quick_demo.py
```

Then explore the generated visualization and try the test suite!

For more details, see:
- **Complete documentation**: `README.md`
- **Usage examples**: `EXAMPLES.md`
- **Project overview**: `PROJECT_SUMMARY.md`

