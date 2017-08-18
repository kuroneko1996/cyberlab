def collide_with_map(sprite, group, axis):
    hits = [s for s in group if sprite.hit_rect.colliderect(s.hit_rect)]

    for hit in hits:
        hit.on_hit()

    if hits:
        hit = hits[0]
        if axis == 'x':
            if sprite.vx > 0:
                sprite.x = hit.hit_rect.left - sprite.hit_rect.width
            elif sprite.vx < 0:
                sprite.x = hit.hit_rect.right

            slither(group, hit, sprite, "y")

            sprite.vx = 0
            sprite.hit_rect.x = sprite.x
        elif axis == 'y':
            if sprite.vy > 0:
                sprite.y = hit.hit_rect.top - sprite.hit_rect.height
            elif sprite.vy < 0:
                sprite.y = hit.hit_rect.bottom

            slither(group, hit, sprite, "x")

            sprite.vy = 0
            sprite.hit_rect.y = sprite.y


def slither(group, hit, sprite, axis):
    """Slithers the sprite along the hit in the direction with an opening"""
    if axis == "x":
        if there_is_space(hit, group, "right"):
            sprite.x += 1
        elif there_is_space(hit, group, "left"):
            sprite.x -= 1
    elif axis == "y":
        if there_is_space(hit, group, "down"):
            sprite.y += 1
        elif there_is_space(hit, group, "up"):
            sprite.y -= 1
    else:
        assert False


def there_is_space(hit, group, direction):
    """Returns true if there is space in the direction given"""
    if direction == "up":
        point = (hit.hit_rect.x, hit.hit_rect.y - 1)
    elif direction == "down":
        point = (hit.hit_rect.x, hit.hit_rect.y + hit.hit_rect.height + 1)
    elif direction == "right":
        point = (hit.hit_rect.x  + hit.hit_rect.width + 1, hit.hit_rect.y)
    elif direction == "left":
        point = (hit.hit_rect.x - 1, hit.hit_rect.y)
    else:
        assert False

    hits = [s for s in group if s.hit_rect.collidepoint(point)]

    return not hits


def collide_with_triggers(sprite, triggers):
    hits = [s for s in triggers if sprite.hit_rect.colliderect(s.hit_rect)]
    for hit in hits:
        hit.on_hit()
