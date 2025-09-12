# game/ui.py
import pygame

PANEL_BG = (255, 245, 252)
PANEL_STROKE = (230, 160, 215)
TEXT = (60, 40, 50)
ACCENT = (255, 170, 60)
OK = (60, 200, 140)
WARN = (255, 80, 100)

class UI:
    def __init__(self, screen_w: int, screen_h: int):
        self.font = pygame.font.Font(None, 24)
        self.big = pygame.font.Font(None, 36)
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.panel_w = 320

    def draw_panel(self, surf, level_i: int, total_levels: int, mode: str, heuristic: str, unlocked_to: int):
        x = self.screen_w - self.panel_w + 10
        y = 10
        w = self.panel_w - 20
        h = self.screen_h - 20
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(surf, PANEL_BG, rect, border_radius=16)
        pygame.draw.rect(surf, PANEL_STROKE, rect, 3, border_radius=16)

        lines = [
            ("COOKIE RUN: DUNGEON", self.big, ACCENT),
            (f"Level: {level_i}/{total_levels}", self.font, TEXT),
            (f"Unlocked: 1..{unlocked_to}", self.font, OK),
            ("", self.font, TEXT),
            ("Mode (toggle):", self.font, TEXT),
            (f"[G] Greedy  |  [A] A*", self.font, TEXT),
            (f"Current: {mode.upper()}", self.font, ACCENT),
            ("", self.font, TEXT),
            ("Heuristic:", self.font, TEXT),
            ("[1] Manhattan  [2] Euclidean", self.font, TEXT),
            (f"Current: {heuristic}", self.font, ACCENT),
            ("", self.font, TEXT),
            ("Controls:", self.font, TEXT),
            ("Arrows/WASD: Move", self.font, TEXT),
            ("N: Next unlocked level", self.font, TEXT),
            ("R: Restart level", self.font, TEXT),
            ("ENTER: Start / Continue", self.font, TEXT)
        ]
        ty = y + 16
        for txt, fnt, col in lines:
            if txt == "":
                ty += 6
                continue
            surf.blit(fnt.render(txt, True, col), (x+14, ty))
            ty += fnt.get_height() + 6

    def draw_banner(self, surf, text: str, color):
        s = self.big.render(text, True, color)
        surf.blit(s, s.get_rect(center=(self.screen_w//2, 28)))
