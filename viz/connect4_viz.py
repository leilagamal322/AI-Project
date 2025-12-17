import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Rectangle
import numpy as np
from typing import List, Tuple, Dict, Optional
from env.connect4_env import Connect4Env


def plot_board(game: Connect4Env, 
               title: str = "Connect 4 Board",
               highlight_move: Optional[Tuple[int, int]] = None,
               ax: Optional[plt.Axes] = None) -> plt.Axes:
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 7))
    
    board = game.board
    rows, cols = game.ROWS, game.COLS
    
    ax.set_facecolor('#4169E1')
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(-0.5, rows - 0.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    for row in range(rows):
        for col in range(cols):
            circle = Circle((col, rows - 1 - row), 0.4, 
                           facecolor='white', 
                           edgecolor='black', 
                           linewidth=2)
            ax.add_patch(circle)
            
            if board[row, col] == 1:
                token = Circle((col, rows - 1 - row), 0.35,
                              facecolor='#FF4444',
                              edgecolor='#AA0000',
                              linewidth=1.5)
                ax.add_patch(token)
            elif board[row, col] == -1:
                token = Circle((col, rows - 1 - row), 0.35,
                              facecolor='#FFD700',
                              edgecolor='#B8860B',
                              linewidth=1.5)
                ax.add_patch(token)
    
    if highlight_move:
        row, col = highlight_move
        highlight = Circle((col, rows - 1 - row), 0.45,
                          facecolor='none',
                          edgecolor='green',
                          linewidth=3,
                          linestyle='--')
        ax.add_patch(highlight)
    
    for col in range(cols):
        ax.text(col, rows + 0.3, str(col), 
               ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    return ax


def plot_move_progression(games: List[Connect4Env],
                         title: str = "Move Progression",
                         moves_per_row: int = 4) -> plt.Figure:
    n_games = len(games)
    n_cols = min(moves_per_row, n_games)
    n_rows = (n_games + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(4*n_cols, 4*n_rows))
    if n_games == 1:
        axes = [axes]
    elif n_rows == 1:
        axes = axes if isinstance(axes, np.ndarray) else [axes]
    else:
        axes = axes.flatten()
    
    fig.suptitle(title, fontsize=16, fontweight='bold', y=0.98)
    
    for i, game in enumerate(games):
        if i < len(axes):
            plot_board(game, title=f"Move {i}", ax=axes[i])
    
    for i in range(n_games, len(axes)):
        axes[i].axis('off')
    
    plt.tight_layout()
    return fig


def plot_performance_comparison(minimax_stats: Dict,
                               alphabeta_stats: Dict,
                               title: str = "Minimax vs Alpha-Beta Performance") -> plt.Figure:
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(title, fontsize=16, fontweight='bold')
    
    metrics = [
        ('nodes_expanded', 'Nodes Expanded', 'Number of nodes'),
        ('time_taken', 'Time Taken (seconds)', 'Time (seconds)'),
        ('nodes_pruned', 'Nodes Pruned', 'Number of nodes'),
        ('max_depth_reached', 'Max Depth Reached', 'Depth')
    ]
    
    for idx, (metric_key, ylabel, ylabel_short) in enumerate(metrics):
        ax = axes[idx // 2, idx % 2]
        
        mm_value = minimax_stats.get(metric_key, 0)
        ab_value = alphabeta_stats.get(metric_key, 0)
        
        algorithms = ['Minimax', 'Alpha-Beta']
        values = [mm_value, ab_value]
        colors = ['#FF6B6B', '#4ECDC4']
        
        bars = ax.bar(algorithms, values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(ylabel_short, fontsize=13, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{val:,.0f}' if isinstance(val, (int, float)) and val >= 1 else f'{val:.4f}',
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    return fig


def plot_game_tree_simple(explored_nodes: List[Tuple],
                          pruned_nodes: List[Tuple] = None,
                          title: str = "Partial Game Tree") -> plt.Figure:
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.axis('off')
    
    nodes_by_depth = {}
    for node in explored_nodes:
        if len(node) >= 2:
            depth = node[0]
            if depth not in nodes_by_depth:
                nodes_by_depth[depth] = []
            nodes_by_depth[depth].append(node)
    
    max_depth = max(nodes_by_depth.keys()) if nodes_by_depth else 0
    
    y_spacing = 1.0
    for depth in range(max_depth + 1):
        if depth not in nodes_by_depth:
            continue
        
        nodes = nodes_by_depth[depth]
        x_positions = np.linspace(0.1, 0.9, len(nodes))
        
        for i, node in enumerate(nodes):
            x = x_positions[i]
            y = max_depth - depth
            
            is_pruned = False
            if pruned_nodes:
                for pnode in pruned_nodes:
                    if len(pnode) >= 2 and pnode[0] == depth:
                        is_pruned = True
                        break
            
            color = '#FF9999' if is_pruned else '#66B2FF'
            alpha = 0.5 if is_pruned else 0.8
            
            circle = Circle((x, y), 0.05, color=color, alpha=alpha, edgecolor='black')
            ax.add_patch(circle)
            
            label = str(node[1]) if len(node) > 1 else str(i)
            ax.text(x, y, label, ha='center', va='center', fontsize=8, fontweight='bold')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.5, max_depth + 0.5)
    ax.text(0.5, -0.2, 'Depth increases downward', ha='center', fontsize=10, style='italic')
    
    explored_patch = patches.Patch(color='#66B2FF', alpha=0.8, label='Explored')
    pruned_patch = patches.Patch(color='#FF9999', alpha=0.5, label='Pruned (Alpha-Beta)')
    ax.legend(handles=[explored_patch, pruned_patch], loc='upper right', fontsize=10)
    
    plt.tight_layout()
    return fig


def save_game_state_image(game: Connect4Env, 
                         filepath: str,
                         title: str = "Connect 4 Board"):
    fig, ax = plt.subplots(figsize=(8, 7))
    plot_board(game, title=title, ax=ax)
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close(fig)


def create_comparison_table(minimax_stats: Dict,
                           alphabeta_stats: Dict) -> str:
    table = "\n" + "="*70 + "\n"
    table += "PERFORMANCE COMPARISON: Minimax vs Alpha-Beta\n"
    table += "="*70 + "\n\n"
    table += f"{'Metric':<25} {'Minimax':<20} {'Alpha-Beta':<20}\n"
    table += "-"*70 + "\n"
    
    metrics = [
        ('Nodes Expanded', 'nodes_expanded'),
        ('Nodes Pruned', 'nodes_pruned'),
        ('Time Taken (s)', 'time_taken'),
        ('Max Depth Reached', 'max_depth_reached'),
    ]
    
    for label, key in metrics:
        mm_val = minimax_stats.get(key, 0)
        ab_val = alphabeta_stats.get(key, 0)
        
        if isinstance(mm_val, float) and mm_val < 1:
            mm_str = f"{mm_val:.4f}"
            ab_str = f"{ab_val:.4f}"
        else:
            mm_str = f"{int(mm_val):,}"
            ab_str = f"{int(ab_val):,}"
        
        table += f"{label:<25} {mm_str:<20} {ab_str:<20}\n"
    
    table += "="*70 + "\n"
    
    if minimax_stats.get('nodes_expanded', 0) > 0:
        improvement = (1 - alphabeta_stats.get('nodes_expanded', 0) / 
                      minimax_stats.get('nodes_expanded', 1)) * 100
        table += f"\nEfficiency Improvement: {improvement:.2f}% fewer nodes expanded\n"
    
    if minimax_stats.get('time_taken', 0) > 0:
        speedup = minimax_stats.get('time_taken', 1) / max(alphabeta_stats.get('time_taken', 0.001), 0.001)
        table += f"Speedup: {speedup:.2f}x faster\n"
    
    return table
