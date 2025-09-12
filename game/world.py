# game/world.py
import pygame
from typing import List, Tuple, Callable

GridPos = Tuple[int, int]

CANDY_BG = (248, 236, 252)
COOKIE_BROWN = (186, 124, 80)
ICING_WHITE = (255, 250, 246)
JELLY_PINK = (255, 152, 212)
WALL_PURPLE = (180, 120, 220)
FLOOR_MINT = (210, 255, 240)

TILE = 48  # tile size (px)

class World:
    def __init__(self, level):
        self.level = level
        self.w = level.width
        self.h = level.height
        self.tiles = level.tiles

    def is_blocked(self, x: int, y: int) -> bool:
        if x < 0 or y < 0 or x >= self.w or y >= self.h:
            return True
        return self.tiles[y][x] == 1

    def draw(self, surf: pygame.Surface, offset: Tuple[int,int]=(0,0)):
        ox, oy = offset
        # background
        surf.fill(CANDY_BG)

        # checker icing floor
        for y in range(self.h):
            for x in range(self.w):
                r = pygame.Rect(ox + x*TILE, oy + y*TILE, TILE, TILE)
                if self.tiles[y][x] == 1:
                    pygame.draw.rect(surf, WALL_PURPLE, r, border_radius=10)
                    pygame.draw.rect(surf, (255,255,255), r, 3, border_radius=10)
                else:
                    color = FLOOR_MINT if (x+y)%2==0 else ICING_WHITE
                    pygame.draw.rect(surf, color, r)
                    pygame.draw.rect(surf, (230,230,230), r, 1)

        # exit cookie gate
        ex, ey = self.level.exit_pos
        rr = pygame.Rect(ox + ex*TILE + 8, oy + ey*TILE + 8, TILE-16, TILE-16)
        pygame.draw.rect(surf, COOKIE_BROWN, rr, border_radius=8)
        pygame.draw.rect(surf, (120,70,40), rr, 2, border_radius=8)

    def pix_from_grid(self, gx: int, gy: int, offset=(0,0)) -> Tuple[int,int]:
        ox, oy = offset
        return ox + gx*TILE + TILE//2, oy + gy*TILE + TILE//2

    def neighbors_4(self, x: int, y: int) -> List[GridPos]:
        out = []
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if not self.is_blocked(nx, ny):
                out.append((nx, ny))
        return out
