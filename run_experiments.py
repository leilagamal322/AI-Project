"""
Main experiment orchestration script.
Runs multiple search algorithms on maze environments with various seeds.
Collects metrics, generates visualizations, and creates report.
"""
import argparse
import json
import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Any

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

from env.maze_env import MazeEnv
from algos.search import (
    breadth_first_search,
    depth_first_search,
    uniform_cost_search,
    iterative_deepening_search,
    greedy_best_first_search,
    a_star_search,
    minmax_search
)
from heuristics import get_heuristic_function
from viz.visualize import (
    plot_maze_solution,
    plot_comparison_bar,
    plot_multiple_metrics,
    plot_heatmap
)


# Algorithm registry
ALGORITHM_REGISTRY = {
    'bfs': ('BFS', breadth_first_search, {}),
    'dfs': ('DFS', depth_first_search, {}),
    'ucs': ('UCS', uniform_cost_search, {}),
    'ids': ('IDS', iterative_deepening_search, {}),
    'greedy_manhattan': ('Greedy (Manhattan)', greedy_best_first_search, 
                        {'heuristic_func': get_heuristic_function('manhattan')}),
    'greedy_euclidean': ('Greedy (Euclidean)', greedy_best_first_search,
                        {'heuristic_func': get_heuristic_function('euclidean')}),
    'astar_manhattan': ('A* (Manhattan)', a_star_search,
                       {'heuristic_func': get_heuristic_function('manhattan')}),
    'astar_euclidean': ('A* (Euclidean)', a_star_search,
                       {'heuristic_func': get_heuristic_function('euclidean')}),
}


def run_single_experiment(env: MazeEnv,
                         algorithm_key: str,
                         verbose: bool = False) -> Dict[str, Any]:
    """
    Run a single algorithm on given environment.
    
    Args:
        env: Maze environment
        algorithm_key: Key from ALGORITHM_REGISTRY
        verbose: Print progress
        
    Returns:
        Dictionary with results
    """
    if algorithm_key not in ALGORITHM_REGISTRY:
        raise ValueError(f"Unknown algorithm: {algorithm_key}")
    
    algo_name, algo_func, algo_params = ALGORITHM_REGISTRY[algorithm_key]
    
    if verbose:
        print(f"  Running {algo_name}...", end=' ')
    
    try:
        result = algo_func(env, **algo_params)
        
        if verbose:
            status = "SUCCESS" if result.success else "FAILED"
            print(f"{status} (runtime: {result.runtime:.4f}s)")
        
        # Convert to dict and add metadata
        result_dict = result.to_dict()
        result_dict['algorithm'] = algo_name
        result_dict['algorithm_key'] = algorithm_key
        
        return {
            'result': result,
            'result_dict': result_dict,
            'algo_name': algo_name
        }
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {
            'result': None,
            'result_dict': {
                'algorithm': algo_name,
                'algorithm_key': algorithm_key,
                'success': False,
                'error': str(e)
            },
            'algo_name': algo_name
        }


def run_experiments(grid_size: int = 50,
                   wall_density: float = 0.2,
                   algorithms: List[str] = None,
                   num_seeds: int = 5,
                   base_seed: int = 42,
                   enable_adversary: bool = False,
                   minmax_depth: int = 4,
                   output_dir: str = 'results',
                   visualize: bool = True,
                   verbose: bool = True):
    """
    Run full experiment suite.
    
    Args:
        grid_size: Maze grid size
        wall_density: Wall density (0-1)
        algorithms: List of algorithm keys to run
        num_seeds: Number of different random seeds
        base_seed: Starting seed value
        enable_adversary: Enable MinMax adversary mode
        minmax_depth: Depth limit for MinMax
        output_dir: Output directory for results
        visualize: Generate visualizations
        verbose: Print progress
        
    Returns:
        DataFrame with all results
    """
    if algorithms is None:
        algorithms = ['bfs', 'dfs', 'ucs', 'ids', 
                     'greedy_manhattan', 'astar_manhattan', 'astar_euclidean']
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Add MinMax if adversary enabled
    if enable_adversary and 'minmax' not in algorithms:
        ALGORITHM_REGISTRY['minmax'] = (
            'MinMax (Alpha-Beta)', 
            minmax_search,
            {
                'heuristic_func': get_heuristic_function('manhattan'),
                'max_depth': minmax_depth,
                'use_alpha_beta': True
            }
        )
        algorithms.append('minmax')
    
    all_results = []
    
    if verbose:
        print("=" * 80)
        print(f"MAZE TREASURE HUNT EXPERIMENTS")
        print("=" * 80)
        print(f"Grid Size: {grid_size}x{grid_size}")
        print(f"Wall Density: {wall_density}")
        print(f"Number of Seeds: {num_seeds}")
        print(f"Algorithms: {', '.join(algorithms)}")
        print(f"Output Directory: {output_dir}")
        print("=" * 80)
    
    # Run experiments for each seed
    for seed_idx in range(num_seeds):
        seed = base_seed + seed_idx
        
        if verbose:
            print(f"\n[Seed {seed_idx + 1}/{num_seeds}] Creating maze (seed={seed})...")
        
        # Create environment
        env = MazeEnv(grid_size=grid_size, 
                     wall_density=wall_density,
                     seed=seed)
        
        maze_info = env.get_maze_info()
        
        if verbose:
            print(f"  Maze created: {maze_info['passable_cells']} passable cells, "
                  f"key at {maze_info['key_position']}")
        
        # Run each algorithm
        for algo_key in algorithms:
            exp_result = run_single_experiment(env, algo_key, verbose)
            
            if exp_result['result'] is not None:
                result = exp_result['result']
                result_dict = exp_result['result_dict']
                algo_name = exp_result['algo_name']
                
                # Add seed and maze info
                result_dict['seed'] = seed
                result_dict['grid_size'] = grid_size
                result_dict['wall_density'] = wall_density
                
                all_results.append(result_dict)
                
                # Generate visualization
                if visualize and result.success:
                    viz_path = os.path.join(
                        output_dir,
                        f'viz_{algo_key}_seed{seed}_{timestamp}.png'
                    )
                    try:
                        plot_maze_solution(
                            env, result, algo_name,
                            save_path=viz_path,
                            show_visited=True
                        )
                    except Exception as e:
                        if verbose:
                            print(f"    Warning: Visualization failed: {e}")
    
    # Convert to DataFrame
    df = pd.DataFrame(all_results)
    
    # Save raw results
    csv_path = os.path.join(output_dir, f'results_{timestamp}.csv')
    df.to_csv(csv_path, index=False)
    if verbose:
        print(f"\n{'='*80}")
        print(f"Raw results saved to: {csv_path}")
    
    # Compute summary statistics
    summary = compute_summary_statistics(df, verbose)
    
    # Save summary
    summary_path = os.path.join(output_dir, f'summary_{timestamp}.csv')
    summary.to_csv(summary_path)
    if verbose:
        print(f"Summary statistics saved to: {summary_path}")
    
    # Generate comparison plots
    if visualize:
        generate_comparison_plots(df, output_dir, timestamp, verbose)
    
    return df, summary


def compute_summary_statistics(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Compute summary statistics from results DataFrame.
    
    Args:
        df: Results DataFrame
        verbose: Print summary
        
    Returns:
        Summary DataFrame
    """
    # Group by algorithm
    metrics = ['runtime', 'nodes_expanded', 'nodes_generated', 
              'path_cost', 'path_length', 'memory_peak']
    
    summary_data = []
    
    for algo in df['algorithm'].unique():
        algo_df = df[df['algorithm'] == algo]
        
        row = {'algorithm': algo}
        
        # Success rate
        row['success_rate'] = algo_df['success'].mean()
        
        # Metrics (only for successful runs)
        success_df = algo_df[algo_df['success'] == True]
        
        if len(success_df) > 0:
            for metric in metrics:
                if metric in success_df.columns:
                    row[f'{metric}_mean'] = success_df[metric].mean()
                    row[f'{metric}_std'] = success_df[metric].std()
        
        summary_data.append(row)
    
    summary_df = pd.DataFrame(summary_data)
    
    if verbose:
        print("\n" + "="*80)
        print("SUMMARY STATISTICS")
        print("="*80)
        print(summary_df.to_string(index=False))
        print("="*80)
    
    return summary_df


def generate_comparison_plots(df: pd.DataFrame,
                              output_dir: str,
                              timestamp: str,
                              verbose: bool = True):
    """
    Generate comparison plots across algorithms.
    
    Args:
        df: Results DataFrame
        output_dir: Output directory
        timestamp: Timestamp string
        verbose: Print progress
    """
    if verbose:
        print("\nGenerating comparison plots...")
    
    # Filter successful runs
    success_df = df[df['success'] == True]
    
    if len(success_df) == 0:
        print("  Warning: No successful runs to plot")
        return
    
    # Prepare data for plotting
    algorithms = success_df['algorithm'].unique()
    
    metrics_data = {}
    for metric in ['runtime', 'nodes_expanded', 'nodes_generated', 'path_cost', 'memory_peak']:
        metric_dict = {}
        for algo in algorithms:
            algo_data = success_df[success_df['algorithm'] == algo][metric]
            if len(algo_data) > 0:
                metric_dict[algo] = (algo_data.mean(), algo_data.std())
        metrics_data[metric] = metric_dict
    
    # Create individual bar charts
    plot_configs = [
        ('runtime', 'Runtime (seconds)', 'Algorithm Runtime Comparison', False),
        ('nodes_expanded', 'Nodes Expanded', 'Nodes Expanded Comparison', False),
        ('nodes_generated', 'Nodes Generated', 'Nodes Generated Comparison', False),
        ('path_cost', 'Path Cost', 'Solution Cost Comparison', False),
        ('memory_peak', 'Memory (MB)', 'Peak Memory Usage Comparison', False)
    ]
    
    for metric, ylabel, title, log_scale in plot_configs:
        if metric in metrics_data and metrics_data[metric]:
            save_path = os.path.join(output_dir, f'comparison_{metric}_{timestamp}.png')
            try:
                plot_comparison_bar(
                    metrics_data[metric],
                    metric,
                    ylabel,
                    title,
                    save_path=save_path,
                    log_scale=log_scale
                )
            except Exception as e:
                if verbose:
                    print(f"  Warning: Failed to create {metric} plot: {e}")
    
    # Create multi-metric comparison
    try:
        multi_data = {}
        for algo in algorithms:
            multi_data[algo] = {}
            algo_df = success_df[success_df['algorithm'] == algo]
            for metric in ['runtime', 'nodes_expanded', 'path_cost', 'memory_peak']:
                if len(algo_df) > 0:
                    multi_data[algo][metric] = (
                        algo_df[metric].mean(),
                        algo_df[metric].std()
                    )
        
        multi_path = os.path.join(output_dir, f'comparison_multi_{timestamp}.png')
        plot_multiple_metrics(
            multi_data,
            ['runtime', 'nodes_expanded', 'path_cost', 'memory_peak'],
            save_path=multi_path
        )
    except Exception as e:
        if verbose:
            print(f"  Warning: Failed to create multi-metric plot: {e}")
    
    if verbose:
        print("  Comparison plots generated")


def generate_report(df: pd.DataFrame,
                   summary: pd.DataFrame,
                   grid_size: int,
                   wall_density: float,
                   num_seeds: int,
                   output_dir: str,
                   timestamp: str):
    """
    Generate markdown report with results.
    
    Args:
        df: Results DataFrame
        summary: Summary statistics DataFrame
        grid_size: Grid size
        wall_density: Wall density
        num_seeds: Number of seeds
        output_dir: Output directory
        timestamp: Timestamp string
    """
    report_dir = os.path.join(output_dir, 'report')
    os.makedirs(report_dir, exist_ok=True)
    
    report_path = os.path.join(report_dir, f'report_{timestamp}.md')
    
    with open(report_path, 'w') as f:
        f.write("# Maze Treasure Hunt - Search Algorithm Analysis\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## 1. Problem Definition\n\n")
        f.write("### Environment Specification\n\n")
        f.write(f"- **Grid Size:** {grid_size} × {grid_size}\n")
        f.write(f"- **Wall Density:** {wall_density * 100:.1f}%\n")
        f.write(f"- **Start Position:** (0, 0)\n")
        f.write(f"- **Goal Position:** ({grid_size-1}, {grid_size-1})\n")
        f.write("- **Key Requirement:** Player must collect key before reaching goal\n")
        f.write("- **Movement:** 4-directional (Up, Down, Left, Right)\n")
        f.write("- **Cost per Move:** 1 (uniform)\n\n")
        
        f.write("### State Space\n\n")
        f.write("State representation: `(x, y, has_key)` where:\n")
        f.write("- `x, y`: Current position in grid\n")
        f.write("- `has_key`: Boolean flag indicating if key has been collected\n\n")
        f.write(f"**State Space Size:** {grid_size} × {grid_size} × 2 = "
               f"{grid_size * grid_size * 2} states\n\n")
        
        f.write("### Algorithms Tested\n\n")
        f.write("1. **BFS (Breadth-First Search):** Complete and optimal for unit costs\n")
        f.write("2. **DFS (Depth-First Search):** Complete with depth limit, not optimal\n")
        f.write("3. **UCS (Uniform Cost Search):** Complete and optimal\n")
        f.write("4. **IDS (Iterative Deepening Search):** Complete and optimal with repeated work\n")
        f.write("5. **Greedy Best-First (Manhattan):** Fast but not optimal\n")
        f.write("6. **A* (Manhattan):** Complete and optimal with admissible heuristic\n")
        f.write("7. **A* (Euclidean):** Complete and optimal with admissible heuristic\n\n")
        
        f.write("### Heuristics\n\n")
        f.write("Both heuristics are **admissible** (never overestimate):\n\n")
        f.write("**Manhattan Distance:** For state `(x, y, has_key)`:\n")
        f.write("```\n")
        f.write("if has_key:\n")
        f.write("    h = |x - goal_x| + |y - goal_y|\n")
        f.write("else:\n")
        f.write("    h = |x - key_x| + |y - key_y| + |key_x - goal_x| + |key_y - goal_y|\n")
        f.write("```\n\n")
        
        f.write("**Euclidean Distance:** Similar but using Euclidean distance.\n\n")
        
        f.write("## 2. Experimental Setup\n\n")
        f.write(f"- **Number of Random Seeds:** {num_seeds}\n")
        f.write(f"- **Grid Configuration:** {grid_size}×{grid_size} with {wall_density*100:.0f}% wall density\n")
        f.write("- **Connectivity:** All mazes guaranteed to have paths start→key→goal\n\n")
        
        f.write("## 3. Results\n\n")
        f.write("### Summary Statistics\n\n")
        f.write("Mean and standard deviation across all seeds:\n\n")
        
        # Format summary table
        f.write("| Algorithm | Success Rate | Avg Runtime (s) | Avg Nodes Expanded | Avg Path Cost | Avg Memory (MB) |\n")
        f.write("|-----------|--------------|-----------------|-------------------|---------------|------------------|\n")
        
        for _, row in summary.iterrows():
            algo = row['algorithm']
            success_rate = row.get('success_rate', 0) * 100
            runtime = row.get('runtime_mean', 0)
            nodes = row.get('nodes_expanded_mean', 0)
            cost = row.get('path_cost_mean', 0)
            memory = row.get('memory_peak_mean', 0)
            
            f.write(f"| {algo} | {success_rate:.0f}% | {runtime:.4f} | "
                   f"{nodes:.0f} | {cost:.1f} | {memory:.2f} |\n")
        
        f.write("\n### Visualizations\n\n")
        f.write("Comparison plots showing algorithm performance:\n\n")
        
        # Link to generated plots
        f.write(f"![Runtime Comparison](../comparison_runtime_{timestamp}.png)\n\n")
        f.write(f"![Nodes Expanded](../comparison_nodes_expanded_{timestamp}.png)\n\n")
        f.write(f"![Multi-Metric Comparison](../comparison_multi_{timestamp}.png)\n\n")
        
        f.write("## 4. Analysis\n\n")
        f.write("### Optimality\n\n")
        
        # Check which algorithms found optimal solutions
        success_df = df[df['success'] == True]
        if len(success_df) > 0:
            optimal_cost = success_df['path_cost'].min()
            f.write(f"**Optimal Path Cost:** {optimal_cost:.1f}\n\n")
            
            f.write("Algorithms that found optimal solutions:\n")
            for algo in success_df['algorithm'].unique():
                algo_cost = success_df[success_df['algorithm'] == algo]['path_cost'].mean()
                if abs(algo_cost - optimal_cost) < 0.1:
                    f.write(f"- {algo} ✓\n")
        
        f.write("\n### Completeness\n\n")
        for algo in summary['algorithm']:
            success_rate = summary[summary['algorithm'] == algo]['success_rate'].values[0]
            status = "✓ Complete" if success_rate >= 0.99 else "✗ Incomplete"
            f.write(f"- **{algo}:** {status} ({success_rate*100:.0f}% success)\n")
        
        f.write("\n### Performance Summary\n\n")
        
        # Find best algorithm for each metric
        if len(success_df) > 0:
            fastest = success_df.groupby('algorithm')['runtime'].mean().idxmin()
            least_nodes = success_df.groupby('algorithm')['nodes_expanded'].mean().idxmin()
            least_memory = success_df.groupby('algorithm')['memory_peak'].mean().idxmin()
            
            f.write(f"- **Fastest Runtime:** {fastest}\n")
            f.write(f"- **Fewest Nodes Expanded:** {least_nodes}\n")
            f.write(f"- **Lowest Memory Usage:** {least_memory}\n")
        
        f.write("\n## 5. Conclusions\n\n")
        f.write("### Key Findings\n\n")
        f.write("1. **A* with Manhattan heuristic** provides the best balance of optimality, "
               "completeness, and efficiency for this problem.\n\n")
        f.write("2. **Greedy Best-First** is fastest but may not find optimal solutions.\n\n")
        f.write("3. **BFS and UCS** guarantee optimality but explore many more nodes.\n\n")
        f.write("4. **Manhattan heuristic** is more effective than Euclidean for grid-based "
               "movement (4-directional).\n\n")
        
        f.write("### Recommendations\n\n")
        f.write("- For **optimal solutions with good performance:** Use A* with Manhattan heuristic\n")
        f.write("- For **quick approximate solutions:** Use Greedy Best-First\n")
        f.write("- For **guaranteed optimality without heuristics:** Use BFS or UCS\n\n")
        
        f.write("---\n\n")
        f.write(f"*Report generated from {num_seeds} experimental runs*\n")
    
    print(f"\nReport generated: {report_path}")
    return report_path


def main():
    parser = argparse.ArgumentParser(
        description='Run maze treasure hunt experiments with search algorithms'
    )
    
    parser.add_argument('--grid-size', type=int, default=50,
                       help='Grid size (default: 50)')
    parser.add_argument('--wall-density', type=float, default=0.2,
                       help='Wall density 0-1 (default: 0.2)')
    parser.add_argument('--algorithms', nargs='+', 
                       default=['bfs', 'dfs', 'ucs', 'ids', 
                               'greedy_manhattan', 'astar_manhattan', 'astar_euclidean'],
                       help='List of algorithms to run')
    parser.add_argument('--num-seeds', type=int, default=5,
                       help='Number of random seeds (default: 5)')
    parser.add_argument('--base-seed', type=int, default=42,
                       help='Base random seed (default: 42)')
    parser.add_argument('--enable-adversary', action='store_true',
                       help='Enable MinMax adversary mode')
    parser.add_argument('--minmax-depth', type=int, default=4,
                       help='MinMax search depth (default: 4)')
    parser.add_argument('--output-dir', type=str, default='results',
                       help='Output directory (default: results)')
    parser.add_argument('--no-viz', action='store_true',
                       help='Disable visualizations')
    parser.add_argument('--quiet', action='store_true',
                       help='Suppress output')
    parser.add_argument('--generate-report', action='store_true',
                       help='Generate markdown report')
    
    args = parser.parse_args()
    
    # Run experiments
    df, summary = run_experiments(
        grid_size=args.grid_size,
        wall_density=args.wall_density,
        algorithms=args.algorithms,
        num_seeds=args.num_seeds,
        base_seed=args.base_seed,
        enable_adversary=args.enable_adversary,
        minmax_depth=args.minmax_depth,
        output_dir=args.output_dir,
        visualize=not args.no_viz,
        verbose=not args.quiet
    )
    
    # Generate report
    if args.generate_report:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        generate_report(
            df, summary,
            args.grid_size,
            args.wall_density,
            args.num_seeds,
            args.output_dir,
            timestamp
        )
    
    print("\nExperiments complete!")


if __name__ == '__main__':
    main()

