# game/main.py
import pygame, sys, time, os
from .level_loader import load_level, level_path_for
from .world import World
from .player import Player
from .enemy import Enemy
from .ui import UI
from .path_api import Pathfinder

SCREEN_W = 1400
SCREEN_H = 800

BG_GRAD_TOP = (255, 230, 240)
BG_GRAD_BOTTOM = (240, 255, 250)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Cookie Run: Escape the Oven")
        self.clock = pygame.time.Clock()

        # global state
        self.level_index = 1
        self.total_levels = 10
        self.unlocked_to = 1
        self.offset = (40, 60)
        self.running = True
        self.scene = "main_menu"
        self.ui = UI(SCREEN_W, SCREEN_H)

        # menu background
        self.menu_bg = None
        try:
            bg_path = os.path.join("game", "assets", "menu-bg.jpg")
            if os.path.exists(bg_path):
                img = pygame.image.load(bg_path).convert()
                self.menu_bg = pygame.transform.scale(img, (SCREEN_W, SCREEN_H))
        except Exception:
            self.menu_bg = None

        self.play_btn_rect = pygame.Rect(0, 0, 220, 68)
        self.back_btn_rect = None   # sidebar Back-to-Menu rect (set by UI)

        # ai control (placeholder toggles for teammate later)
        self.pathfinder = Pathfinder(mode="greedy", heuristic="manhattan")

        # load first level
        self.load_level(self.level_index)

    # --- level ---
    def load_level(self, i: int):
        lvl = load_level(level_path_for(i))
        self.world = World(lvl)
        self.player = Player(lvl.player_start)
        self.enemies = []
        if getattr(lvl, "enemies", None):
            first = lvl.enemies[0]  # one enemy per level for now
            self.enemies.append(Enemy(first.pos, speed=getattr(first, "speed", 3.0)))

    # --- helpers ---
    def restart_level(self):
        self.load_level(self.level_index)

    def next_unlocked(self):
        self.level_index = min(self.unlocked_to, self.total_levels)
        self.load_level(self.level_index)

    # --- visuals ---
    def gradient_bg(self):
        for y in range(SCREEN_H):
            t = y / SCREEN_H
            r = int(BG_GRAD_TOP[0] * (1 - t) + BG_GRAD_BOTTOM[0] * t)
            g = int(BG_GRAD_TOP[1] * (1 - t) + BG_GRAD_BOTTOM[1] * t)
            b = int(BG_GRAD_TOP[2] * (1 - t) + BG_GRAD_BOTTOM[2] * t)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_W, y))

    # --- update ---
    def update(self, dt: float):
        if self.scene != "playing":
            return
        # enemies are static for now; just check collision and win
        ppos = self.player.grid_pos()
        if any(e.grid_pos() == ppos for e in self.enemies):
            self.scene = "game_over"
            return
        if ppos == self.world.level.exit_pos:
            if self.level_index < self.total_levels:
                self.unlocked_to = max(self.unlocked_to, self.level_index + 1)
                self.scene = "level_complete"
            else:
                self.scene = "game_complete"

    # --- draw ---
    def draw(self):
        if self.scene == "main_menu":
            if self.menu_bg:
                self.screen.blit(self.menu_bg, (0, 0))
                overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 120))  # soften background
                self.screen.blit(overlay, (0, 0))
            else:
                self.gradient_bg()

            self.ui.draw_title(self.screen, "COOKIE RUN: ESCAPE THE OVEN", (255, 170, 120), y=180)
            cx, cy = SCREEN_W // 2, SCREEN_H // 2 + 30
            self.play_btn_rect = self.ui.draw_button(self.screen, "PLAY", (cx, cy))
            self.ui.draw_subtitle(self.screen,
                                "Use WASD/Arrows to move • Don't get caught!",
                                (255, 235, 200), y=cy + 80)

        else:
            # Base world + entities always draw first
            self.gradient_bg()
            self.world.draw(self.screen, self.offset)
            self.player.draw(self.screen, self.world, self.offset)
            for e in self.enemies:
                e.draw(self.screen, self.offset)

            # Right sidebar (always on during gameplay-style scenes)
            self.back_btn_rect = self.ui.draw_panel(
                self.screen,
                self.level_index, self.total_levels,
                self.pathfinder.mode, self.pathfinder.heuristic,
                self.unlocked_to
            )

            # Overlay scenes: darken whole screen, then center the text
            if self.scene in ("level_complete", "game_over", "game_complete"):
                overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 160))  # darker overlay
                self.screen.blit(overlay, (0, 0))

                if self.scene == "level_complete":
                    self.ui.draw_title(self.screen, "LEVEL CLEARED!", (120, 200, 120),
                                    y=SCREEN_H // 2 - 40)
                    self.ui.draw_subtitle(self.screen, "Press ENTER to continue",
                                        (220, 255, 220), y=SCREEN_H // 2 + 10)

                elif self.scene == "game_over":
                    self.ui.draw_title(self.screen, "CAUGHT! GAME OVER", (255, 80, 100),
                                    y=SCREEN_H // 2 - 40)
                    self.ui.draw_subtitle(self.screen, "Press ENTER to retry",
                                        (255, 200, 200), y=SCREEN_H // 2 + 10)

                elif self.scene == "game_complete":
                    self.ui.draw_title(self.screen, "CONGRATULATIONS!", (255, 200, 80),
                                    y=SCREEN_H // 2 - 60)
                    self.ui.draw_subtitle(self.screen, "You escaped all 10 levels!",
                                        (255, 230, 180), y=SCREEN_H // 2)
                    # Big center Back-to-Menu button as well
                    center_btn = self.ui.draw_button(self.screen, "BACK TO MENU",
                                                    (SCREEN_W // 2, SCREEN_H - 110))
                    self.back_btn_rect = center_btn

        pygame.display.flip()

    # --- loop ---
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # mouse
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.scene == "main_menu" and self.play_btn_rect.collidepoint(event.pos):
                        self.scene = "playing"
                    elif self.back_btn_rect and self.back_btn_rect.collidepoint(event.pos):
                        # works from sidebar OR from final congrats screen
                        self.scene = "main_menu"
                        self.level_index = 1
                        self.unlocked_to = 1
                        self.load_level(self.level_index)

                # keyboard
                elif event.type == pygame.KEYDOWN:
                    # one-tile movement in playing scene
                    if self.scene == "playing":
                        move_map = {
                            pygame.K_LEFT:  (-1, 0), pygame.K_a: (-1, 0),
                            pygame.K_RIGHT: ( 1, 0), pygame.K_d: ( 1, 0),
                            pygame.K_UP:    ( 0,-1), pygame.K_w: ( 0,-1),
                            pygame.K_DOWN:  ( 0, 1), pygame.K_s: ( 0, 1),
                        }
                        if event.key in move_map:
                            dx, dy = move_map[event.key]
                            self.player.try_move(dx, dy, self.world)

                            # immediate checks
                            ppos = self.player.grid_pos()
                            if any(e.grid_pos() == ppos for e in self.enemies):
                                self.scene = "game_over"
                            elif ppos == self.world.level.exit_pos:
                                if self.level_index < self.total_levels:
                                    self.unlocked_to = max(self.unlocked_to, self.level_index + 1)
                                    self.scene = "level_complete"
                                else:
                                    self.scene = "game_complete"
                            continue  # don't process other actions on this key press

                    # Enter / Return across scenes
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if self.scene == "main_menu":
                            self.scene = "playing"
                        elif self.scene == "level_complete":
                            self.level_index += 1
                            self.load_level(self.level_index)
                            self.scene = "playing"
                        elif self.scene == "game_complete":
                            # reset and go to menu
                            self.level_index = 1
                            self.unlocked_to = 1
                            self.load_level(self.level_index)
                            self.scene = "main_menu"
                        elif self.scene == "game_over":
                            self.restart_level()
                            self.scene = "playing"

                    elif event.key == pygame.K_r:
                        self.restart_level()
                        if self.scene != "main_menu":
                            self.scene = "playing"

                    elif event.key == pygame.K_n:
                        self.next_unlocked()
                        self.scene = "playing"

                    # algorithm toggles (placeholders for your teammate)
                    elif event.key == pygame.K_g:
                        self.pathfinder.set_mode("greedy", self.pathfinder.heuristic)
                    elif event.key == pygame.K_a:
                        self.pathfinder.set_mode("astar", self.pathfinder.heuristic)
                    elif event.key == pygame.K_1:
                        self.pathfinder.set_mode(self.pathfinder.mode, "manhattan")
                    elif event.key == pygame.K_2:
                        self.pathfinder.set_mode(self.pathfinder.mode, "euclidean")

            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()

def main():
    Game().run()

if __name__ == "__main__":
    main()