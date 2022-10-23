from src.constants import (
    COLORS,
    SCREEN_DIMENSIONS
)

from src.engine import BoxCamera
from src.background import Background

from src.entities.player import Player
from src.entities.collidable import Collidable
from src.entities.barrier import ColorBarrier
from src.entities.grass import Grass

from src.scenes.scene import Scene

import pygame
import os

class Sandbox(Scene):
    def __init__(self, surfaces, mouse, sprites=...):
        super().__init__(surfaces, mouse, sprites)

        self.player = Player(pygame.Vector2(600, 1125), 4)
        floor = Collidable(pygame.Vector2(0, 1500), pygame.Color(255, 255, 255), pygame.Vector2(5000, 20)) 

        block_c = Collidable(pygame.Vector2(600, 1400), pygame.Color(255, 255, 255), pygame.Vector2(50, 100))  
        block_d = Collidable(pygame.Vector2(850, 1400), pygame.Color(255, 255, 255), pygame.Vector2(50, 100))  

        barrier_a = ColorBarrier(pygame.Vector2(500, 1200), pygame.Vector2(250, 100), COLORS[0], self.player)
        barrier_b = ColorBarrier(pygame.Vector2(950, 1200), pygame.Vector2(250, 50), COLORS[1], self.player)
        barrier_c = ColorBarrier(pygame.Vector2(1300, 1250), pygame.Vector2(75, 250), COLORS[2], self.player)

        self.background = Background()
        self.camera = BoxCamera(self.player)

        self.view = pygame.Surface(SCREEN_DIMENSIONS).get_rect()
        self.entity_view = pygame.Surface(SCREEN_DIMENSIONS).get_rect()

        self.add_sprites(
            self.player, floor, 
            block_c, block_d,
            barrier_a, barrier_b, barrier_c,
        )

        for i in range(100):
            self.add_sprites(
                Grass(pygame.Vector2(1500 + (i * 9), 1510), 4)
            )

    def display(self, screen, dt):
        dt = 2 if dt > 2 else dt
        dt = round(dt, 1)

        cam = self.camera.update(dt)
        self.entity_view.x, self.entity_view.y = cam

        self.background_surface.fill(pygame.Color(0, 0, 0, 0), self.view)
        self.entity_surface.fill(pygame.Color(0, 0, 0, 0), self.entity_view)
        self.ui_surface.fill(pygame.Color(0, 0, 0, 0), self.view)

        self.background.display(self.background_surface, dt)

        display_order = self.sort_sprites(self.sprites)
        for _, v in sorted(display_order.items()):
            for sprite in v: 
                if not sprite.active:
                    continue

                sprite.display(self, dt)
        
        self.mouse.display(self, self.player)

        screen.blit(self.background_surface, (0, 0))
        screen.blit(self.entity_surface, -cam)
        screen.blit(self.ui_surface, (0, 0))

        self.frames += 1
    