import pygame as pg


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


def collide_with_map(sprite, group, axis):
    if axis == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vx > 0:
                sprite.x = hits[0].rect.left - sprite.hit_rect.width
            elif sprite.vx < 0:
                sprite.x = hits[0].rect.right
            sprite.vx = 0
            sprite.hit_rect.x = sprite.x
    elif axis == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vy > 0:
                sprite.y = hits[0].rect.top - sprite.hit_rect.height
            elif sprite.vy < 0:
                sprite.y = hits[0].rect.bottom
            sprite.vy = 0
            sprite.hit_rect.y = sprite.y
