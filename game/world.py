# game/world.py
import pygame
from typing import List, Tuple

GridPos = Tuple[int, int]

# Candy palette (more colorful!)
BOARD_FRAME_OUTER = (60, 30, 90)      # deep purple border
BOARD_FRAME_INNER = (245, 210, 240)   # soft pink frame
BOARD_SHADOW      = (200, 150, 200)   # violet shadow
ICE_1             = (255, 240, 245)   # candy white (like frosting)
ICE_2             = (255, 182, 193)   # light pink (strawberry)
LICORICE          = (180, 50, 100)    # candy red walls
LICORICE_SHINE    = (230, 120, 170)   # shiny pink highlight on walls
EXIT_BG           = (230, 200, 255)   # lavender exit tile
EXIT_BORDER       = (160, 90, 200)    # bold purple outline
EXIT_TEXT         = (255, 255, 255)   # white text on exit

TILE = 48  # tile size (px)

class World:
    """
    tiles[y][x] == 1 -> wall, 0 -> floor
    """
    def __init__(self, level):
        self.level = level
        self.w = level.width
        self.h = level.height
        self.tiles = level.tiles

        # precompute a board rect (centered with a small border)
        self.board_pad = 16

    def is_blocked(self, x: int, y: int) -> bool:
        if x < 0 or y < 0 or x >= self.w or y >= self.h:
            return True
        return self.tiles[y][x] == 1

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

    # ---------- drawing ----------
    def _board_rect(self, offset):
        ox, oy = offset
        wpx = self.w * TILE
        hpx = self.h * TILE
        return pygame.Rect(ox - self.board_pad, oy - self.board_pad,
                           wpx + self.board_pad*2, hpx + self.board_pad*2)

    def _draw_frame(self, surf, offset):
        R = self._board_rect(offset)

        # outer shadow
        shadow = R.inflate(10, 10)
        pygame.draw.rect(surf, BOARD_SHADOW, shadow, border_radius=18)

        # outer frame
        pygame.draw.rect(surf, BOARD_FRAME_OUTER, R, border_radius=18)
        # inner cutout
        inner = R.inflate(-8, -8)
        pygame.draw.rect(surf, BOARD_FRAME_INNER, inner, border_radius=14, width=6)

    def _draw_grid(self, surf, offset):
        ox, oy = offset
        for y in range(self.h):
            for x in range(self.w):
                r = pygame.Rect(ox + x*TILE, oy + y*TILE, TILE, TILE)

                # checker pastel “ice” floor
                if self.tiles[y][x] == 0:
                    col = ICE_1 if ((x + y) % 2 == 0) else ICE_2
                    pygame.draw.rect(surf, col, r)
                else:
                    # solid licorice wall with a subtle highlight stripe
                    bar = r.inflate(-8, -8)   # make it look like a bar inside the cell
                    pygame.draw.rect(surf, LICORICE, bar, border_radius=6)
                    # highlight
                    shine = pygame.Rect(bar.x+3, bar.y+3, bar.w-6, 4)
                    pygame.draw.rect(surf, LICORICE_SHINE, shine, border_radius=2)

                # fine grid line
                pygame.draw.rect(surf, (210, 220, 230), r, 1)

    def _draw_exit_badge(self, surf, offset):
        ox, oy = offset
        ex, ey = self.level.exit_pos
        r = pygame.Rect(ox + ex*TILE, oy + ey*TILE, TILE, TILE)

        # a rounded candy badge that overhangs slightly on the right
        badge = r.inflate(14, -8).move(10, 0)
        pygame.draw.rect(surf, EXIT_BG, badge, border_radius=14)
        pygame.draw.rect(surf, EXIT_BORDER, badge, 3, border_radius=14)

        # EXIT text
        font = pygame.font.Font(None, 24)
        s = font.render("EXIT", True, EXIT_TEXT)
        surf.blit(s, s.get_rect(center=badge.center))

    def draw(self, surf: pygame.Surface, offset: Tuple[int,int]=(0,0)):
        # board frame
        self._draw_frame(surf, offset)
        # grid + walls
        self._draw_grid(surf, offset)
        # exit
        self._draw_exit_badge(surf, offset)