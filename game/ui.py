# game/ui.py
import pygame

PANEL_BG = (255, 245, 252)
PANEL_STROKE = (230, 160, 215)
TEXT = (60, 40, 50)
ACCENT = (255, 170, 60)
OK = (60, 200, 140)

class UI:
    def __init__(self, screen_w: int, screen_h: int):
        self.font = pygame.font.Font(None, 24)
        self.big = pygame.font.Font(None, 36)
        self.huge = pygame.font.Font(None, 64)
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.panel_w = 320

    def draw_panel(self, surf, level_i, total_levels, mode, heuristic, unlocked_to):
        """
        Draws the right-side control panel. Also draws a small 'Back to Menu' button at the bottom
        and RETURNS its rect so the game can detect clicks.
        """
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
            ("[G] Greedy  |  [A] A*", self.font, TEXT),
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
            ("ENTER: Confirm / Continue", self.font, TEXT),
        ]
        ty = y + 16
        for txt, fnt, col in lines:
            if txt == "":
                ty += 6
                continue
            surf.blit(fnt.render(txt, True, col), (x + 14, ty))
            ty += fnt.get_height() + 6

        # Small “Back to Menu” button at the bottom of the panel
        btn_w, btn_h = w - 28, 46
        btn_rect = pygame.Rect(x + 14, y + h - btn_h - 14, btn_w, btn_h)
        mouse = pygame.mouse.get_pos()
        hover = btn_rect.collidepoint(mouse)
        base = (255, 160, 90)
        edge = (220, 120, 70)
        glow = (255, 200, 150) if hover else (255, 180, 130)
        pygame.draw.rect(surf, base, btn_rect, border_radius=14)
        pygame.draw.rect(surf, edge, btn_rect, 3, border_radius=14)
        hi = pygame.Rect(btn_rect.x + 8, btn_rect.y + 8, btn_rect.w - 16, btn_rect.h // 3)
        pygame.draw.rect(surf, glow, hi, border_radius=10)
        label = self.big.render("Back to Menu", True, (255, 255, 255))
        surf.blit(label, label.get_rect(center=btn_rect.center))
        return btn_rect

    def draw_banner(self, surf, text, color):
        s = self.big.render(text, True, color)
        surf.blit(s, s.get_rect(center=(self.screen_w // 2, 28)))

    def draw_title(self, surf, text, color, y=160):
        s = self.huge.render(text, True, color)
        surf.blit(s, s.get_rect(center=(self.screen_w // 2, y)))

    def draw_subtitle(self, surf, text, color, y=220):
        s = self.big.render(text, True, color)
        surf.blit(s, s.get_rect(center=(self.screen_w // 2, y)))

    def draw_button(self, surf, label, center_xy, enabled=True):
        """
        Big rounded candy-style button (used on main menu and congratulations screen).
        Returns its rect for click detection.
        """
        text_surf = self.huge.render(label, True, (255, 255, 255))
        pad_x, pad_y = 32, 16
        w = text_surf.get_width() + pad_x * 2
        h = text_surf.get_height() + pad_y * 2
        rect = pygame.Rect(0, 0, w, h)
        rect.center = center_xy

        mouse = pygame.mouse.get_pos()
        hover = rect.collidepoint(mouse)
        base = (255, 160, 90) if enabled else (180, 180, 180)
        edge = (220, 120, 70) if enabled else (150, 150, 150)
        glow = (255, 200, 150) if (hover and enabled) else (255, 180, 130)

        pygame.draw.rect(surf, base, rect, border_radius=22)
        pygame.draw.rect(surf, edge, rect, 4, border_radius=22)
        hi = pygame.Rect(rect.x + 10, rect.y + 10, rect.w - 20, rect.h // 3)
        pygame.draw.rect(surf, glow, hi, border_radius=14)
        surf.blit(text_surf, text_surf.get_rect(center=rect.center))
        return rect