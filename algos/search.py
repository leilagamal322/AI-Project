import heapq
import time
import tracemalloc
from typing import Tuple, List, Optional, Callable, Dict, Any
from collections import deque
import sys


class SearchResult:
    
    def __init__(self, 
                 success: bool,
                 path: Optional[List[Tuple[int, int, bool]]] = None,
                 actions: Optional[List[str]] = None,
                 nodes_expanded: int = 0,
                 nodes_generated: int = 0,
                 path_cost: float = 0,
                 runtime: float = 0,
                 memory_peak: float = 0,
                 visited_states: Optional[set] = None):
        self.success = success
        self.path = path if path else []
        self.actions = actions if actions else []
        self.nodes_expanded = nodes_expanded
        self.nodes_generated = nodes_generated
        self.path_cost = path_cost
        self.runtime = runtime
        self.memory_peak = memory_peak
        self.visited_states = visited_states if visited_states else set()
    
    def to_dict(self) -> dict:
        return {
            'success': self.success,
            'path_length': len(self.path),
            'path_cost': self.path_cost,
            'nodes_expanded': self.nodes_expanded,
            'nodes_generated': self.nodes_generated,
            'runtime': self.runtime,
            'memory_peak': self.memory_peak,
            'visited_count': len(self.visited_states)
        }


def breadth_first_search(env) -> SearchResult:
    tracemalloc.start()
    start_time = time.time()
    
    initial_state = env.get_initial_state()
    queue = deque([(initial_state, [initial_state], [], 0)])
    visited = {initial_state}
    
    nodes_expanded = 0
    nodes_generated = 1
    
    while queue:
        state, path, actions, cost = queue.popleft()
        nodes_expanded += 1
        
        if env.is_goal_state(state):
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            runtime = time.time() - start_time
            
            return SearchResult(
                success=True,
                path=path,
                actions=actions,
                nodes_expanded=nodes_expanded,
                nodes_generated=nodes_generated,
                path_cost=cost,
                runtime=runtime,
                memory_peak=peak / (1024 * 1024),
                visited_states=visited
            )
        
        for next_state, action, step_cost in env.get_successors(state):
            if next_state not in visited:
                visited.add(next_state)
                nodes_generated += 1
                queue.append((
                    next_state,
                    path + [next_state],
                    actions + [action],
                    cost + step_cost
                ))
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    runtime = time.time() - start_time
    
    return SearchResult(
        success=False,
        nodes_expanded=nodes_expanded,
        nodes_generated=nodes_generated,
        runtime=runtime,
        memory_peak=peak / (1024 * 1024),
        visited_states=visited
    )


def depth_first_search(env, max_depth: int = 10000) -> SearchResult:
    tracemalloc.start()
    start_time = time.time()
    
    initial_state = env.get_initial_state()
    stack = [(initial_state, [initial_state], [], 0, 0)]
    visited = {initial_state}
    
    nodes_expanded = 0
    nodes_generated = 1
    
    while stack:
        state, path, actions, cost, depth = stack.pop()
        nodes_expanded += 1
        
        if env.is_goal_state(state):
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            runtime = time.time() - start_time
            
            return SearchResult(
                success=True,
                path=path,
                actions=actions,
                nodes_expanded=nodes_expanded,
                nodes_generated=nodes_generated,
                path_cost=cost,
                runtime=runtime,
                memory_peak=peak / (1024 * 1024),
                visited_states=visited
            )
        
        if depth < max_depth:
            for next_state, action, step_cost in env.get_successors(state):
                if next_state not in visited:
                    visited.add(next_state)
                    nodes_generated += 1
                    stack.append((
                        next_state,
                        path + [next_state],
                        actions + [action],
                        cost + step_cost,
                        depth + 1
                    ))
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    runtime = time.time() - start_time
    
    return SearchResult(
        success=False,
        nodes_expanded=nodes_expanded,
        nodes_generated=nodes_generated,
        runtime=runtime,
        memory_peak=peak / (1024 * 1024),
        visited_states=visited
    )


def uniform_cost_search(env) -> SearchResult:
    tracemalloc.start()
    start_time = time.time()
    
    initial_state = env.get_initial_state()
    counter = 0
    pq = [(0, counter, initial_state, [initial_state], [])]
    visited = set()
    
    nodes_expanded = 0
    nodes_generated = 1
    
    while pq:
        cost, _, state, path, actions = heapq.heappop(pq)
        
        if state in visited:
            continue
            
        visited.add(state)
        nodes_expanded += 1
        
        if env.is_goal_state(state):
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            runtime = time.time() - start_time
            
            return SearchResult(
                success=True,
                path=path,
                actions=actions,
                nodes_expanded=nodes_expanded,
                nodes_generated=nodes_generated,
                path_cost=cost,
                runtime=runtime,
                memory_peak=peak / (1024 * 1024),
                visited_states=visited
            )
        
        for next_state, action, step_cost in env.get_successors(state):
            if next_state not in visited:
                nodes_generated += 1
                counter += 1
                heapq.heappush(pq, (
                    cost + step_cost,
                    counter,
                    next_state,
                    path + [next_state],
                    actions + [action]
                ))
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    runtime = time.time() - start_time
    
    return SearchResult(
        success=False,
        nodes_expanded=nodes_expanded,
        nodes_generated=nodes_generated,
        runtime=runtime,
        memory_peak=peak / (1024 * 1024),
        visited_states=visited
    )


def iterative_deepening_search(env, max_depth: int = 1000) -> SearchResult:
    tracemalloc.start()
    start_time = time.time()
    
    total_nodes_expanded = 0
    total_nodes_generated = 0
    all_visited = set()
    
    def depth_limited_search(depth_limit: int):
        nonlocal total_nodes_expanded, total_nodes_generated
        
        initial_state = env.get_initial_state()
        stack = [(initial_state, [initial_state], [], 0, 0)]
        visited_at_depth = {initial_state}
        
        nodes_exp = 0
        nodes_gen = 1
        
        while stack:
            state, path, actions, cost, depth = stack.pop()
            nodes_exp += 1
            all_visited.add(state)
            
            if env.is_goal_state(state):
                return True, path, actions, cost, nodes_exp, nodes_gen
            
            if depth < depth_limit:
                for next_state, action, step_cost in env.get_successors(state):
                    if next_state not in visited_at_depth:
                        visited_at_depth.add(next_state)
                        nodes_gen += 1
                        stack.append((
                            next_state,
                            path + [next_state],
                            actions + [action],
                            cost + step_cost,
                            depth + 1
                        ))
        
        return False, None, None, 0, nodes_exp, nodes_gen
    
    for depth_limit in range(max_depth + 1):
        found, path, actions, cost, nodes_exp, nodes_gen = depth_limited_search(depth_limit)
        total_nodes_expanded += nodes_exp
        total_nodes_generated += nodes_gen
        
        if found:
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            runtime = time.time() - start_time
            
            return SearchResult(
                success=True,
                path=path,
                actions=actions,
                nodes_expanded=total_nodes_expanded,
                nodes_generated=total_nodes_generated,
                path_cost=cost,
                runtime=runtime,
                memory_peak=peak / (1024 * 1024),
                visited_states=all_visited
            )
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    runtime = time.time() - start_time
    
    return SearchResult(
        success=False,
        nodes_expanded=total_nodes_expanded,
        nodes_generated=total_nodes_generated,
        runtime=runtime,
        memory_peak=peak / (1024 * 1024),
        visited_states=all_visited
    )


def greedy_best_first_search(env, heuristic_func: Callable) -> SearchResult:
    tracemalloc.start()
    start_time = time.time()
    
    initial_state = env.get_initial_state()
    goal = env.goal
    key_pos = env.key_pos
    
    counter = 0
    h = heuristic_func(initial_state, goal, key_pos)
    pq = [(h, counter, initial_state, [initial_state], [], 0)]
    visited = set()
    
    nodes_expanded = 0
    nodes_generated = 1
    
    while pq:
        _, _, state, path, actions, cost = heapq.heappop(pq)
        
        if state in visited:
            continue
            
        visited.add(state)
        nodes_expanded += 1
        
        if env.is_goal_state(state):
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            runtime = time.time() - start_time
            
            return SearchResult(
                success=True,
                path=path,
                actions=actions,
                nodes_expanded=nodes_expanded,
                nodes_generated=nodes_generated,
                path_cost=cost,
                runtime=runtime,
                memory_peak=peak / (1024 * 1024),
                visited_states=visited
            )
        
        for next_state, action, step_cost in env.get_successors(state):
            if next_state not in visited:
                nodes_generated += 1
                counter += 1
                h = heuristic_func(next_state, goal, key_pos)
                heapq.heappush(pq, (
                    h,
                    counter,
                    next_state,
                    path + [next_state],
                    actions + [action],
                    cost + step_cost
                ))
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    runtime = time.time() - start_time
    
    return SearchResult(
        success=False,
        nodes_expanded=nodes_expanded,
        nodes_generated=nodes_generated,
        runtime=runtime,
        memory_peak=peak / (1024 * 1024),
        visited_states=visited
    )


def a_star_search(env, heuristic_func: Callable) -> SearchResult:
    tracemalloc.start()
    start_time = time.time()
    
    initial_state = env.get_initial_state()
    goal = env.goal
    key_pos = env.key_pos
    
    counter = 0
    h = heuristic_func(initial_state, goal, key_pos)
    pq = [(h, counter, initial_state, [initial_state], [], 0)]
    visited = set()
    
    nodes_expanded = 0
    nodes_generated = 1
    
    while pq:
        f_cost, _, state, path, actions, g_cost = heapq.heappop(pq)
        
        if state in visited:
            continue
            
        visited.add(state)
        nodes_expanded += 1
        
        if env.is_goal_state(state):
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            runtime = time.time() - start_time
            
            return SearchResult(
                success=True,
                path=path,
                actions=actions,
                nodes_expanded=nodes_expanded,
                nodes_generated=nodes_generated,
                path_cost=g_cost,
                runtime=runtime,
                memory_peak=peak / (1024 * 1024),
                visited_states=visited
            )
        
        for next_state, action, step_cost in env.get_successors(state):
            if next_state not in visited:
                nodes_generated += 1
                counter += 1
                new_g_cost = g_cost + step_cost
                h = heuristic_func(next_state, goal, key_pos)
                f = new_g_cost + h
                heapq.heappush(pq, (
                    f,
                    counter,
                    next_state,
                    path + [next_state],
                    actions + [action],
                    new_g_cost
                ))
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    runtime = time.time() - start_time
    
    return SearchResult(
        success=False,
        nodes_expanded=nodes_expanded,
        nodes_generated=nodes_generated,
        runtime=runtime,
        memory_peak=peak / (1024 * 1024),
        visited_states=visited
    )


def minmax_search(env, 
                  heuristic_func: Callable,
                  max_depth: int = 4,
                  adversary_radius: int = 3,
                  adversary_frequency: int = 2,
                  use_alpha_beta: bool = True) -> SearchResult:
    tracemalloc.start()
    start_time = time.time()
    
    initial_state = env.get_initial_state()
    goal = env.goal
    key_pos = env.key_pos
    
    nodes_expanded = 0
    nodes_generated = 1
    visited_states = set()
    move_count = [0]
    
    def evaluate_state(state, depth):
        if env.is_goal_state(state):
            return -1000 + depth
        else:
            return -heuristic_func(state, goal, key_pos)
    
    def max_value(state, depth, alpha, beta, env_copy):
        nonlocal nodes_expanded, nodes_generated
        nodes_expanded += 1
        visited_states.add(state)
        
        if depth >= max_depth or env_copy.is_goal_state(state):
            return evaluate_state(state, depth), None
        
        value = -float('inf')
        best_action = None
        
        successors = env_copy.get_successors(state)
        for next_state, action, _ in successors:
            nodes_generated += 1
            move_count[0] += 1
            
            if move_count[0] % adversary_frequency == 0:
                min_val, _ = min_value(next_state, depth + 1, alpha, beta, env_copy)
            else:
                min_val, _ = max_value(next_state, depth + 1, alpha, beta, env_copy)
            
            if min_val > value:
                value = min_val
                best_action = action
            
            if use_alpha_beta:
                alpha = max(alpha, value)
                if value >= beta:
                    break
        
        return value, best_action
    
    def min_value(state, depth, alpha, beta, env_copy):
        nonlocal nodes_expanded, nodes_generated
        nodes_expanded += 1
        
        if depth >= max_depth or env_copy.is_goal_state(state):
            return evaluate_state(state, depth), None
        
        value = float('inf')
        best_wall_pos = None
        
        adversary_actions = env_copy.get_adversary_actions(state, adversary_radius)
        adversary_actions.append(None)
        
        for wall_pos in adversary_actions[:10]:
            nodes_generated += 1
            
            wall_placed = False
            if wall_pos is not None:
                wall_placed = env_copy.add_temporary_wall(wall_pos)
            
            max_val, _ = max_value(state, depth + 1, alpha, beta, env_copy)
            
            if wall_placed and wall_pos is not None:
                env_copy.remove_temporary_wall(wall_pos)
            
            if max_val < value:
                value = max_val
                best_wall_pos = wall_pos
            
            if use_alpha_beta:
                beta = min(beta, value)
                if value <= alpha:
                    break
        
        return value, best_wall_pos
    
    env_copy = env.copy()
    
    path = [initial_state]
    actions = []
    current_state = initial_state
    cost = 0
    max_steps = 500
    
    for step in range(max_steps):
        if env_copy.is_goal_state(current_state):
            break
        
        _, best_action = max_value(
            current_state, 
            0, 
            -float('inf'), 
            float('inf'), 
            env_copy
        )
        
        if best_action is None:
            break
        
        successors = env_copy.get_successors(current_state)
        next_state = None
        for succ_state, succ_action, step_cost in successors:
            if succ_action == best_action:
                next_state = succ_state
                cost += step_cost
                break
        
        if next_state is None:
            break
        
        path.append(next_state)
        actions.append(best_action)
        current_state = next_state
    
    success = env_copy.is_goal_state(current_state)
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    runtime = time.time() - start_time
    
    return SearchResult(
        success=success,
        path=path,
        actions=actions,
        nodes_expanded=nodes_expanded,
        nodes_generated=nodes_generated,
        path_cost=cost,
        runtime=runtime,
        memory_peak=peak / (1024 * 1024),
        visited_states=visited_states
    )

