# game/path_api.py
from typing import List, Tuple, Optional

GridPos = Tuple[int, int]

class Pathfinder:
    """
    Interface that the enemy uses to chase the player.
    Your teammate replaces 'find_path' with Greedy / A* (select via mode string).
    """
    def __init__(self, mode: str = "greedy", heuristic: str = "manhattan"):
        self.mode = mode
        self.heuristic = heuristic

    def set_mode(self, mode: str, heuristic: str):
        self.mode = mode
        self.heuristic = heuristic

    def find_path(self, start: GridPos, goal: GridPos, grid_is_blocked) -> Optional[List[GridPos]]:
        """
        Return a list of grid cells from start to goal (inclusive).
        'grid_is_blocked(x,y) -> bool' indicates walls.
        NOTE: this fallback is intentionally simple so your scene runs now.
        """
        if start == goal:
            return [start]

        # naive step-by-step "greedy" toward goal (placeholder)
        path = [start]
        cx, cy = start
        gx, gy = goal

        safety = 500
        while safety > 0 and (cx, cy) != (gx, gy):
            safety -= 1
            step_x = 0 if cx == gx else (1 if gx > cx else -1)
            step_y = 0 if cy == gy else (1 if gy > cy else -1)

            # try horizontal first
            nx, ny = cx + step_x, cy
            if step_x != 0 and not grid_is_blocked(nx, ny):
                cx, cy = nx, ny
                path.append((cx, cy))
                continue

            # then try vertical
            nx, ny = cx, cy + step_y
            if step_y != 0 and not grid_is_blocked(nx, ny):
                cx, cy = nx, ny
                path.append((cx, cy))
                continue

            # try orthogonal detours
            tried = False
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx, ny = cx + dx, cy + dy
                if not grid_is_blocked(nx, ny):
                    cx, cy = nx, ny
                    path.append((cx, cy))
                    tried = True
                    break
            if not tried:
                return None  # stuck

        return path if (cx, cy) == (gx, gy) else None
