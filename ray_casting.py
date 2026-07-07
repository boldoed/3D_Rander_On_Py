import pygame
from settings import *
from map import world_map, WORLD_HEIGHT, WORLD_WIDTH

# def ray_casting(sc, player_pos, player_angle):
#     cur_angle = player_angle - HALF_FOV
#     xo, yo = player_pos
#     for ray in range(NUM_RAYS):
#         sin_a = math.sin(cur_angle)
#         cos_a = math.cos(cur_angle)
#         for depth in range(1, MAX_DEPTH):
#             x = xo + depth * cos_a
#             y = yo + depth * sin_a
#             # pygame.draw.line(sc, DARK_GRAY, player_pos, (x,y), 2)
#             if (x // TILE * TILE, y // TILE * TILE) in world_map:
#                 depth *= math.cos(player_angle - cur_angle)
#                 proj_height = PROJ_COEFF / depth
#                 c = 255 / (1 + depth * depth * 10 ** -5)
#                 color = (c, c // 3, c // 4)
#                 pygame.draw.rect(sc, color, (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))
#                 break
#         cur_angle += DELTA_ANGLE

def mapping(a, b):
    return (a // TILE) * TILE, (b // TILE) * TILE

def ray_casting(sc, player_pos, player_angle, textures):
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    texture_v, texture_h = 1, 1
    cur_angle = player_angle - HALF_FOV
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)

        #verticals
        x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, WORLD_WIDTH, TILE):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * TILE

        #horizontals
        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, WORLD_HEIGHT, TILE):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * TILE
            
        #projection
        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        offset = int(offset) % TILE
        depth *= math.cos(player_angle - cur_angle)
        depth = max(depth, 100 ** -5)
        proj_height = min(int(PROJ_COEFF / depth), PENTA_HEIGHT)
        # c = 255 / (1 + depth * depth * 10 ** -5 * 2)
        # color = (c, c // 3, c // 4)
        # pygame.draw.rect(sc, color, (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))
        wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
        wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
        sc.blit(wall_column, (ray * SCALE, HALF_HEIGHT - proj_height // 2))

        cur_angle += DELTA_ANGLE