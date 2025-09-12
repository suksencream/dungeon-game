# game/player.py
import pygame
from typing import Tuple

TILE = 48
COOKIE_BROWN = (186, 124, 80)
GLOW = (255, 225, 120)

class Player:
    def __init__(self, start_grid_pos: Tuple[int,int], speed: float=6.0):
        self.gx, self.gy = start_grid_pos
        self.px, self.py = 0, 0  # pixel
        self.speed = speed
        self._sync_pixel(start_grid_pos)

    def _sync_pixel(self, gp):
        self.px, self.py = gp[0]*TILE + TILE//2, gp[1]*TILE + TILE//2

    def grid_pos(self):
        return (self.gx, self.gy)

    def update(self, dt, world, input_dir):
        # input_dir is (-1/0/1, -1/0/1) from main
        if input_dir == (0,0):
            return
        nx, ny = self.gx + input_dir[0], self.gy + input_dir[1]
        if not world.is_blocked(nx, ny):
            self.gx, self.gy = nx, ny
            self._sync_pixel((self.gx, self.gy))

    def draw(self, surf, world, offset=(0,0)):
        x = self.gx*TILE + TILE//2 + offset[0]
        y = self.gy*TILE + TILE//2 + offset[1]
        pygame.draw.circle(surf, GLOW, (x, y), TILE//2 - 6)
        pygame.draw.circle(surf, COOKIE_BROWN, (x, y-2), TILE//2 - 8)
        # cute face
        pygame.draw.circle(surf, (40, 20, 10), (x-7, y-4), 3)
        pygame.draw.circle(surf, (40, 20, 10), (x+7, y-4), 3)
        pygame.draw.arc(surf, (40, 20, 10), (x-8, y+2, 16, 10), 3.6, 6.0, 2)
