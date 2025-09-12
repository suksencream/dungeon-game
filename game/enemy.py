# game/enemy.py
import pygame
from typing import Tuple, List, Optional
from .path_api import Pathfinder

TILE = 48
RED = (255, 80, 100)
SHADOW = (50, 0, 20)

class Enemy:
    def __init__(self, start_grid: Tuple[int,int], speed: float=3.0):
        self.gx, self.gy = start_grid
        self.speed = speed
        self.path: List[Tuple[int,int]] = []
        self.path_index = 0
        self.repath_timer = 0.0

    def grid_pos(self):
        return (self.gx, self.gy)

    def update(self, dt: float, world, player_pos, pathfinder: Pathfinder):
        # replan every 0.6s (feel free to tweak)
        self.repath_timer -= dt
        if self.repath_timer <= 0:
            self.repath_timer = 0.6
            path = pathfinder.find_path(self.grid_pos(), player_pos, world.is_blocked)
            if path and len(path) > 1:
                self.path = path
                self.path_index = 1

        # follow planned path
        if self.path_index < len(self.path):
            nx, ny = self.path[self.path_index]
            # one-tile step
            if not world.is_blocked(nx, ny):
                self.gx, self.gy = nx, ny
                self.path_index += 1

    def draw(self, surf, offset=(0,0)):
        x = self.gx*TILE + TILE//2 + offset[0]
        y = self.gy*TILE + TILE//2 + offset[1]
        pygame.draw.circle(surf, SHADOW, (x+2, y+2), TILE//2 - 8)
        pygame.draw.circle(surf, RED, (x, y), TILE//2 - 10)
        pygame.draw.rect(surf, (0,0,0), (x-6, y-4, 12, 3), 0)
