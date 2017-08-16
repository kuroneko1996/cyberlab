import pygame as pg


def collide_with_map(sprite, group, axis):
    hits = [s for s in group if sprite.hit_rect.colliderect(s.hit_rect)]

    for hit in hits:
        hit.on_hit()

    if hits:
        if axis == 'x':
            if sprite.vx > 0:
                sprite.x = hits[0].hit_rect.left - sprite.hit_rect.width
            elif sprite.vx < 0:
                sprite.x = hits[0].hit_rect.right
            sprite.vx = 0
            sprite.hit_rect.x = sprite.x
        elif axis == 'y':
            if sprite.vy > 0:
                sprite.y = hits[0].hit_rect.top - sprite.hit_rect.height
            elif sprite.vy < 0:
                sprite.y = hits[0].hit_rect.bottom
            sprite.vy = 0
            sprite.hit_rect.y = sprite.y
