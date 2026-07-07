import pygame
from settings import *
from ray_casting import ray_casting
from map import mini_map

class Drawing:
    def __init__(self, sc, sc_map):
        self.sc = sc
        self.sc_map = sc_map
        self.font = pygame.font.SysFont('Arial', 24, bold=True)
        self.textures = {1: pygame.image.load('textures/wall.png').convert(),
                         2: pygame.image.load('textures/wall.jpg').convert(),
                         'S': pygame.image.load('textures/background.png').convert()}

    def background(self, angle):
        # pygame.draw.rect(self.sc, BLUE, (0, 0, WIDTH, HALF_HEIGHT))
        sky_offset = -10 * math.degrees(angle) % WIDTH
        self.sc.blit(self.textures['S'], (sky_offset, 0))
        self.sc.blit(self.textures['S'], (sky_offset  - WIDTH, 0))
        self.sc.blit(self.textures['S'], (sky_offset + WIDTH, 0))
        pygame.draw.rect(self.sc, DARK_GRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def world(self, player_pos, player_angle):
        ray_casting(self.sc, player_pos, player_angle, self.textures)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0 , RED)
        self.sc.blit(render, FPS_POS)

    def mini_map(self, player):
        self.sc_map.fill(LIGHT_BLUE)
        map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE

        pygame.draw.line(self.sc_map, WHITE, (map_x, map_y), (map_x + 15 * math.cos(player.angle), map_y + 15 * math.sin(player.angle)), 2)
        pygame.draw.circle(self.sc_map, RED, (map_x, map_y), 5)

        for x,y in mini_map:
            pygame.draw.rect(self.sc_map, BROWN, (x, y, MAP_TILE, MAP_TILE))
        self.sc.blit(self.sc_map, MAP_POS)