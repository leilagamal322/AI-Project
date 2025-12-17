# Phase 2: Connect 4 Adversarial Search Implementation

## Quick Start

### Running the Demo

```bash
# Run comparison demo (default - recommended)
python phase2_demo.py

# Interactive demo (watch algorithms play)
python phase2_demo.py --mode interactive

# Custom settings
python phase2_demo.py --depth 5 --tests 5
```

### Running Tests

```bash
# Test basic functionality
python test_phase2.py
```

## Files Overview

### Core Implementation

- **`env/connect4_env.py`**: Connect 4 game environment
  - Game state representation
  - Move generation and validation
  - Win/loss/draw detection
  - Undo functionality for search

- **`algos/adversarial_search.py`**: Search algorithms
  - Minimax implementation
  - Alpha-Beta Pruning implementation
  - Evaluation function (threat-based heuristic)
  - Performance tracking

- **`viz/connect4_viz.py`**: Visualization tools
  - Board state visualization
  - Performance comparison charts
  - Move progression visualization

### Demo & Documentation

- **`phase2_demo.py`**: Main demo script
  - Runs Minimax vs Alpha-Beta comparisons
  - Generates visualizations
  - Interactive gameplay demo

- **`PHASE2_REPORT.md`**: Comprehensive report
  - Game modeling details
  - Algorithm explanations
  - Performance analysis
  - Results and observations

- **`test_phase2.py`**: Unit tests
  - Basic game functionality tests
  - Algorithm correctness tests

## Output

Results are saved to `results/phase2/`:
- `comparison_test{1,2,3}.png`: Individual test comparisons
- `aggregate_comparison.png`: Overall performance comparison
- `position{1,2,3}_initial.png`: Initial board states
- `moves_test{1,2,3}.png`: Move progression sequences

## Key Features

1. **Complete Game Environment**
   - Full Connect 4 rules implementation
   - State representation and transitions
   - Terminal state detection

2. **Adversarial Search Algorithms**
   - Minimax with depth limiting
   - Alpha-Beta Pruning
   - Performance metrics tracking

3. **Evaluation Function**
   - Threat detection (3-in-a-row with open space)
   - Center control bonus
   - Two-in-a-row patterns
   - Terminal state handling

4. **Visualization**
   - Board state visualization
   - Performance comparison charts
   - Move progression tracking

## Usage Examples

### Basic Comparison

```python
from env.connect4_env import Connect4Env
from algos.adversarial_search import minimax_search, alphabeta_search

# Create game
game = Connect4Env()

# Make some initial moves
game.make_move(3)
game.make_move(2)

# Run Minimax
best_move_mm, tracker_mm = minimax_search(game.copy(), max_depth=4)
print(f"Minimax: Column {best_move_mm}, {tracker_mm.nodes_expanded} nodes")

# Run Alpha-Beta
best_move_ab, tracker_ab = alphabeta_search(game.copy(), max_depth=4)
print(f"Alpha-Beta: Column {best_move_ab}, {tracker_ab.nodes_expanded} nodes")
print(f"Pruned: {tracker_ab.nodes_pruned} nodes")
```

### Visualization

```python
from viz.connect4_viz import plot_board, plot_performance_comparison
import matplotlib.pyplot as plt

game = Connect4Env()
game.make_move(3)

# Plot board
fig, ax = plt.subplots(figsize=(8, 7))
plot_board(game, title="Connect 4 Board", ax=ax)
plt.show()

# Compare algorithms
mm_stats = {'nodes_expanded': 15000, 'time_taken': 0.5, ...}
ab_stats = {'nodes_expanded': 3000, 'time_taken': 0.1, ...}
fig = plot_performance_comparison(mm_stats, ab_stats)
plt.show()
```

## Performance Expectations

For depth=4 on typical mid-game positions:
- **Minimax**: ~15,000-25,000 nodes, ~0.5-1.5 seconds
- **Alpha-Beta**: ~2,000-5,000 nodes, ~0.05-0.3 seconds
- **Improvement**: 60-80% node reduction, 3-5x speedup

## Requirements

See `requirements.txt`. Main dependencies:
- numpy >= 1.21.0
- matplotlib >= 3.4.0
- pandas >= 1.3.0 (optional, for data analysis)

## Project Structure

```
.
├── env/
│   ├── connect4_env.py       # Game environment
│   └── __init__.py
├── algos/
│   ├── adversarial_search.py # Minimax & Alpha-Beta
│   └── __init__.py
├── viz/
│   ├── connect4_viz.py       # Visualization
│   └── __init__.py
├── phase2_demo.py            # Main demo script
├── test_phase2.py            # Unit tests
├── PHASE2_REPORT.md          # Full report
└── PHASE2_README.md          # This file
```

## Notes

- Default search depth is 4 (adjustable)
- Evaluation function uses threat detection and center control
- Both algorithms return optimal moves (for given depth)
- Alpha-Beta maintains optimality while being much faster

