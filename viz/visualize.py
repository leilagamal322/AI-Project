"""
Visualization functions for maze and search results.
Creates plots showing maze, visited nodes, and solution paths.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import List, Tuple, Optional, Set
import os


def plot_maze_solution(env,
                       result,
                       algorithm_name: str,
                       save_path: Optional[str] = None,
                       show_visited: bool = True,
                       figsize: Tuple[int, int] = (12, 12)):
    """
    Plot maze with solution path and visited nodes.
    
    Args:
        env: Maze environment
        result: SearchResult object
        algorithm_name: Name of algorithm for title
        save_path: Path to save figure (optional)
        show_visited: Whether to show visited nodes
        figsize: Figure size
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Draw grid
    grid_size = env.grid_size
    
    # Draw walls (black)
    for i in range(grid_size):
        for j in range(grid_size):
            if env.grid[i, j] == 1:
                rect = patches.Rectangle((j, i), 1, 1, 
                                         linewidth=0, 
                                         facecolor='black')
                ax.add_patch(rect)
    
    # Draw visited nodes (light blue with transparency)
    if show_visited and result.visited_states:
        for state in result.visited_states:
            x, y, _ = state
            rect = patches.Rectangle((y, x), 1, 1,
                                     linewidth=0,
                                     facecolor='lightblue',
                                     alpha=0.3)
            ax.add_patch(rect)
    
    # Draw path (yellow)
    if result.path:
        for state in result.path:
            x, y, _ = state
            rect = patches.Rectangle((y, x), 1, 1,
                                     linewidth=0,
                                     facecolor='yellow',
                                     alpha=0.6)
            ax.add_patch(rect)
        
        # Draw path line
        path_coords = [(y + 0.5, x + 0.5) for x, y, _ in result.path]
        path_x = [coord[0] for coord in path_coords]
        path_y = [coord[1] for coord in path_coords]
        ax.plot(path_x, path_y, 'r-', linewidth=2, alpha=0.7)
    
    # Draw start (green)
    start_x, start_y = env.start
    ax.add_patch(patches.Rectangle((start_y, start_x), 1, 1,
                                   linewidth=2,
                                   edgecolor='green',
                                   facecolor='lightgreen',
                                   alpha=0.8))
    ax.text(start_y + 0.5, start_x + 0.5, 'S',
           ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Draw goal (red)
    goal_x, goal_y = env.goal
    ax.add_patch(patches.Rectangle((goal_y, goal_x), 1, 1,
                                   linewidth=2,
                                   edgecolor='red',
                                   facecolor='lightcoral',
                                   alpha=0.8))
    ax.text(goal_y + 0.5, goal_x + 0.5, 'G',
           ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Draw key (gold star)
    key_x, key_y = env.key_pos
    ax.plot(key_y + 0.5, key_x + 0.5, '*', 
           markersize=20, color='gold', markeredgecolor='orange', markeredgewidth=2)
    
    # Set axis properties
    ax.set_xlim(0, grid_size)
    ax.set_ylim(0, grid_size)
    ax.set_aspect('equal')
    ax.invert_yaxis()  # Invert y-axis so (0,0) is top-left
    
    # Add grid lines
    ax.set_xticks(range(0, grid_size + 1, max(1, grid_size // 10)))
    ax.set_yticks(range(0, grid_size + 1, max(1, grid_size // 10)))
    ax.grid(True, alpha=0.3, linewidth=0.5)
    
    # Title with metrics
    title = f'{algorithm_name}\n'
    title += f'Success: {result.success} | '
    title += f'Path Length: {len(result.path)} | '
    title += f'Cost: {result.path_cost:.1f}\n'
    title += f'Nodes Expanded: {result.nodes_expanded} | '
    title += f'Runtime: {result.runtime:.4f}s'
    
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_xlabel('Column (Y)')
    ax.set_ylabel('Row (X)')
    
    plt.tight_layout()
    
    if save_path:
        save_dir = os.path.dirname(save_path)
        if save_dir:  # Only create directory if path contains directory
            os.makedirs(save_dir, exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved visualization to {save_path}")
    
    plt.close()


def plot_comparison_bar(data: dict,
                       metric_name: str,
                       ylabel: str,
                       title: str,
                       save_path: Optional[str] = None,
                       figsize: Tuple[int, int] = (10, 6),
                       log_scale: bool = False):
    """
    Create bar chart comparing algorithms on a single metric.
    
    Args:
        data: Dict mapping algorithm name to (mean, std) tuple
        metric_name: Name of metric
        ylabel: Y-axis label
        title: Plot title
        save_path: Path to save figure
        figsize: Figure size
        log_scale: Use logarithmic y-axis
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    algorithms = list(data.keys())
    means = [data[alg][0] for alg in algorithms]
    stds = [data[alg][1] for alg in algorithms]
    
    x_pos = np.arange(len(algorithms))
    
    bars = ax.bar(x_pos, means, yerr=stds, 
                  capsize=5, alpha=0.7, 
                  color='steelblue', edgecolor='black')
    
    # Add value labels on bars
    for i, (bar, mean, std) in enumerate(zip(bars, means, stds)):
        height = bar.get_height()
        if log_scale:
            label_text = f'{mean:.2e}'
        else:
            label_text = f'{mean:.2f}'
        ax.text(bar.get_x() + bar.get_width()/2., height,
               label_text,
               ha='center', va='bottom', fontsize=9)
    
    ax.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(algorithms, rotation=45, ha='right')
    
    if log_scale:
        ax.set_yscale('log')
    
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved comparison plot to {save_path}")
    
    plt.close()


def plot_multiple_metrics(data: dict,
                         metrics: List[str],
                         save_path: Optional[str] = None,
                         figsize: Tuple[int, int] = (16, 10)):
    """
    Create subplot grid comparing multiple metrics across algorithms.
    
    Args:
        data: Dict of {algorithm: {metric: (mean, std)}}
        metrics: List of metric names to plot
        save_path: Path to save figure
        figsize: Figure size
    """
    n_metrics = len(metrics)
    n_cols = 2
    n_rows = (n_metrics + 1) // 2
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axes.flatten() if n_metrics > 1 else [axes]
    
    algorithms = list(data.keys())
    x_pos = np.arange(len(algorithms))
    
    metric_configs = {
        'runtime': ('Runtime (s)', 'Mean Runtime', False),
        'nodes_expanded': ('Nodes Expanded', 'Mean Nodes Expanded', False),
        'nodes_generated': ('Nodes Generated', 'Mean Nodes Generated', False),
        'path_cost': ('Path Cost', 'Mean Path Cost', False),
        'memory_peak': ('Memory (MB)', 'Mean Peak Memory', False),
        'path_length': ('Path Length', 'Mean Path Length', False)
    }
    
    for idx, metric in enumerate(metrics):
        if idx >= len(axes):
            break
            
        ax = axes[idx]
        
        means = [data[alg].get(metric, (0, 0))[0] for alg in algorithms]
        stds = [data[alg].get(metric, (0, 0))[1] for alg in algorithms]
        
        bars = ax.bar(x_pos, means, yerr=stds,
                     capsize=4, alpha=0.7,
                     color='steelblue', edgecolor='black')
        
        # Add value labels
        for bar, mean in zip(bars, means):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{mean:.2f}',
                   ha='center', va='bottom', fontsize=8)
        
        ylabel, title, log_scale = metric_configs.get(
            metric, 
            (metric.replace('_', ' ').title(), f'Mean {metric}', False)
        )
        
        ax.set_ylabel(ylabel, fontsize=10, fontweight='bold')
        ax.set_title(title, fontsize=11, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(algorithms, rotation=45, ha='right', fontsize=9)
        ax.grid(True, alpha=0.3, axis='y')
    
    # Hide unused subplots
    for idx in range(n_metrics, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved multi-metric comparison to {save_path}")
    
    plt.close()


def plot_heatmap(env, 
                 visited_states: Set[Tuple[int, int, bool]],
                 algorithm_name: str,
                 save_path: Optional[str] = None,
                 figsize: Tuple[int, int] = (10, 10)):
    """
    Create heatmap showing visit frequency for each cell.
    
    Args:
        env: Maze environment
        visited_states: Set of visited states
        algorithm_name: Algorithm name for title
        save_path: Path to save figure
        figsize: Figure size
    """
    grid_size = env.grid_size
    visit_count = np.zeros((grid_size, grid_size))
    
    # Count visits to each cell
    for state in visited_states:
        x, y, _ = state
        visit_count[x, y] += 1
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Create heatmap
    im = ax.imshow(visit_count, cmap='YlOrRd', interpolation='nearest')
    
    # Overlay walls in black
    for i in range(grid_size):
        for j in range(grid_size):
            if env.grid[i, j] == 1:
                rect = patches.Rectangle((j-0.5, i-0.5), 1, 1,
                                        linewidth=0,
                                        facecolor='black')
                ax.add_patch(rect)
    
    # Mark special locations
    start_x, start_y = env.start
    goal_x, goal_y = env.goal
    key_x, key_y = env.key_pos
    
    ax.plot(start_y, start_x, 's', markersize=15, 
           color='lime', markeredgecolor='green', markeredgewidth=2)
    ax.plot(goal_y, goal_x, 's', markersize=15,
           color='red', markeredgecolor='darkred', markeredgewidth=2)
    ax.plot(key_y, key_x, '*', markersize=20,
           color='gold', markeredgecolor='orange', markeredgewidth=2)
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Visit Count', rotation=270, labelpad=20, fontweight='bold')
    
    ax.set_title(f'{algorithm_name} - Visit Heatmap\n'
                f'Total Visits: {len(visited_states)}',
                fontsize=12, fontweight='bold')
    ax.set_xlabel('Column (Y)')
    ax.set_ylabel('Row (X)')
    
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved heatmap to {save_path}")
    
    plt.close()


def create_summary_table_image(summary_df,
                               save_path: str,
                               figsize: Tuple[int, int] = (14, 8)):
    """
    Create an image of a summary table.
    
    Args:
        summary_df: Pandas DataFrame with summary statistics
        save_path: Path to save image
        figsize: Figure size
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.axis('tight')
    ax.axis('off')
    
    # Create table
    table_data = []
    table_data.append(list(summary_df.columns))
    for idx, row in summary_df.iterrows():
        table_data.append(list(row))
    
    table = ax.table(cellText=table_data,
                    cellLoc='center',
                    loc='center',
                    colWidths=[0.15] * len(summary_df.columns))
    
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)
    
    # Style header row
    for i in range(len(summary_df.columns)):
        cell = table[(0, i)]
        cell.set_facecolor('#4CAF50')
        cell.set_text_props(weight='bold', color='white')
    
    # Alternate row colors
    for i in range(1, len(table_data)):
        for j in range(len(summary_df.columns)):
            cell = table[(i, j)]
            if i % 2 == 0:
                cell.set_facecolor('#f0f0f0')
            else:
                cell.set_facecolor('#ffffff')
    
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Saved summary table to {save_path}")
    
    plt.close()

