# game/player.py
import os
import pygame
from typing import Tuple
from .world import TILE

COOKIE_FALLBACK = (230, 160, 90)   # fallback color if image missing
OUTLINE = (90, 50, 30)

class Player:
    def __init__(self, start_grid: Tuple[int, int]):
        self.gx, self.gy = start_grid  # grid coordinates (integers)

        # Try to load cookie sprite (game/assets/cookie.png)
        self.sprite = None
        try:
            here = os.path.dirname(__file__)
            img_path = os.path.join(here, "assets", "cookie.png")
            if os.path.exists(img_path):
                img = pygame.image.load(img_path).convert_alpha()
                # scale slightly smaller than a tile to leave padding
                self.sprite = pygame.transform.smoothscale(img, (TILE - 6, TILE - 6))
        except Exception:
            self.sprite = None

    def grid_pos(self) -> Tuple[int, int]:
        return (self.gx, self.gy)

    def try_move(self, dx: int, dy: int, world) -> None:
        """
        Attempt to move exactly one tile in (dx, dy).
        Only moves if target is inside bounds and not a wall.
        """
        nx, ny = self.gx + dx, self.gy + dy
        if not world.is_blocked(nx, ny):
            self.gx, self.gy = nx, ny

    def update(self, dt: float, world, input_dir: Tuple[int, int]) -> None:
        """
        Kept for compatibility with previous loop.
        We now move only on keypress via try_move(), so this is a no-op.
        """
        return

    def draw(self, surf: pygame.Surface, world, offset=(0, 0)) -> None:
        px, py = world.pix_from_grid(self.gx, self.gy, offset)
        if self.sprite:
            rect = self.sprite.get_rect(center=(px, py))
            surf.blit(self.sprite, rect)
        else:
            # fallback cookie-looking circle
            pygame.draw.circle(surf, COOKIE_FALLBACK, (px, py), TILE // 2 - 6)
            pygame.draw.circle(surf, OUTLINE, (px, py), TILE // 2 - 6, 2)