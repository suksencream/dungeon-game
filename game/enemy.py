# game/enemy.py
import os
import pygame
from typing import Tuple, List

TILE = 48
RED = (255, 80, 100)
SHADOW = (50, 0, 20)

class Enemy:
    """
    Static enemy for now (no movement). We just draw it and let Game check collision.
    Uses assets/oven.png if available; falls back to a red circle.
    """
    def __init__(self, start_grid: Tuple[int, int], speed: float = 3.0):
        self.gx, self.gy = start_grid
        self.speed = speed

        # try to load oven image
        self.image = None
        try:
            here = os.path.dirname(__file__)
            p = os.path.join(here, "assets", "oven.png")
            if os.path.exists(p):
                img = pygame.image.load(p).convert_alpha()
                # a little padding so it fits nicely inside the tile
                self.image = pygame.transform.smoothscale(img, (TILE - 8, TILE - 8))
        except Exception:
            self.image = None

    def grid_pos(self) -> Tuple[int, int]:
        return (self.gx, self.gy)

    def update(self, dt: float, world, *args, **kwargs):
        """
        Intentionally does nothing for now — enemy is static.
        Your teammate can add pathfinding later and move (gx, gy) here.
        """
        return

    def draw(self, surf, offset=(0, 0)):
        x = self.gx * TILE + TILE // 2 + offset[0]
        y = self.gy * TILE + TILE // 2 + offset[1]

        if self.image:
            rect = self.image.get_rect(center=(x, y))
            surf.blit(self.image, rect)
        else:
            # fallback: simple red cookie-cutter style
            pygame.draw.circle(surf, SHADOW, (x + 2, y + 2), TILE // 2 - 8)
            pygame.draw.circle(surf, RED, (x, y), TILE // 2 - 10)
            pygame.draw.rect(surf, (0, 0, 0), (x - 6, y - 4, 12, 3), 0)