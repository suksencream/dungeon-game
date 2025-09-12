# game/main.py
import pygame, sys, time
from typing import Tuple
from .level_loader import load_level, level_path_for
from .world import World, TILE
from .player import Player
from .enemy import Enemy
from .ui import UI
from .path_api import Pathfinder

SCREEN_W = 1280
SCREEN_H = 720

BG_GRAD_TOP = (255, 230, 240)
BG_GRAD_BOTTOM = (240, 255, 250)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Cookie Run: Dungeon (Heuristic Search)")
        self.clock = pygame.time.Clock()

        # state
        self.level_index = 1
        self.total_levels = 10
        self.unlocked_to = 1

        self.offset = (40, 60)  # world draw offset
        self.running = True
        self.scene = "menu"  # menu, playing, level_complete, game_complete
        self.ui = UI(SCREEN_W, SCREEN_H)

        # ai control
        self.pathfinder = Pathfinder(mode="greedy", heuristic="manhattan")

        # load first level
        self.load_level(self.level_index)

    def load_level(self, i: int):
        lvl = load_level(level_path_for(i))
        self.world = World(lvl)
        self.player = Player(lvl.player_start)
        self.enemies = [Enemy(e.pos, speed=e.speed) for e in lvl.enemies]
        self.scene = "menu"

    def gradient_bg(self):
        # simple vertical gradient
        for y in range(SCREEN_H):
            t = y / SCREEN_H
            r = int(BG_GRAD_TOP[0]*(1-t) + BG_GRAD_BOTTOM[0]*t)
            g = int(BG_GRAD_TOP[1]*(1-t) + BG_GRAD_BOTTOM[1]*t)
            b = int(BG_GRAD_TOP[2]*(1-t) + BG_GRAD_BOTTOM[2]*t)
            pygame.draw.line(self.screen, (r,g,b), (0,y), (SCREEN_W,y))

    def handle_input(self):
        input_dir = (0,0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: input_dir = (-1,0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: input_dir = (1,0)
        if keys[pygame.K_UP] or keys[pygame.K_w]: input_dir = (0,-1)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: input_dir = (0,1)
        return input_dir

    def update(self, dt: float):
        if self.scene != "playing":
            return
        inp = self.handle_input()
        self.player.update(dt, self.world, inp)

        # enemies chase the player using the selected pathfinder
        ppos = self.player.grid_pos()
        for e in self.enemies:
            e.update(dt, self.world, ppos, self.pathfinder)
            if e.grid_pos() == ppos:
                # caught!
                self.scene = "menu"  # back to menu; you can make a 'fail' scene if you want
                break

        # reach exit?
        if ppos == self.world.level.exit_pos:
            if self.level_index < self.total_levels:
                self.unlocked_to = max(self.unlocked_to, self.level_index + 1)
                self.scene = "level_complete"
            else:
                self.scene = "game_complete"

    def draw(self):
        self.gradient_bg()
        # world
        self.world.draw(self.screen, self.offset)
        # entities
        self.player.draw(self.screen, self.world, self.offset)
        for e in self.enemies:
            e.draw(self.screen, self.offset)

        # overlay UI
        if self.scene == "menu":
            self.ui.draw_banner(self.screen, "Press ENTER to Start", (255,140,120))
        elif self.scene == "level_complete":
            self.ui.draw_banner(self.screen, "LEVEL CLEARED! 🎉", (120,200,120))
        elif self.scene == "game_complete":
            self.ui.draw_banner(self.screen, "YOU ESCAPED THE OVEN! 🍪✨", (255,170,60))

        self.ui.draw_panel(self.screen, self.level_index, self.total_levels,
                           self.pathfinder.mode, self.pathfinder.heuristic, self.unlocked_to)

        pygame.display.flip()

    def next_unlocked(self):
        self.level_index = min(self.unlocked_to, self.total_levels)
        self.load_level(self.level_index)

    def restart_level(self):
        self.load_level(self.level_index)

    def run(self):
        while self.running:
            dt = self.clock.tick(60)/1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.scene in ("menu", "level_complete", "game_complete"):
                            if self.scene == "level_complete":
                                # go to next
                                self.level_index += 1
                                self.load_level(self.level_index)
                                self.scene = "playing"
                            elif self.scene == "game_complete":
                                # restart all
                                self.level_index = 1
                                self.unlocked_to = 1
                                self.load_level(self.level_index)
                                self.scene = "playing"
                            else:
                                self.scene = "playing"
                    elif event.key == pygame.K_r:
                        self.restart_level()
                    elif event.key == pygame.K_n:
                        self.next_unlocked()
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
