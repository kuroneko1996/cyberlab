from settings import TILE_SIZE, SLITHER_SPEED


def collide_with_map(sprite, group, axis):
    """
    Check for collisions and align the sprite so that
    it does not overlap with other sprites in the group
    :param sprite: sprite to be aligned
    :param group: other sprites
    :param axis: about which axis to check for collisions
    :return: if there is a collision, return the sprite
     with which this sprite could have collided, false otherwise
    """
    hits = [s for s in group if sprite.get_hit_rect().colliderect(s.get_hit_rect())]

    for hit in hits:
        hit.on_hit()

    if hits:
        hit = hits[0]
        if axis == 'x':
            if sprite.vx > 0:
                sprite.x = (hit.get_hit_rect().left - sprite.get_hit_rect().width) / TILE_SIZE
            elif sprite.vx < 0:
                sprite.x = hit.get_hit_rect().right / TILE_SIZE

            sprite.vx = 0
            sprite.get_hit_rect().x = sprite.x * TILE_SIZE
        elif axis == 'y':
            if sprite.vy > 0:
                sprite.y = (hit.get_hit_rect().top - sprite.get_hit_rect().height) / TILE_SIZE
            elif sprite.vy < 0:
                sprite.y = hit.get_hit_rect().bottom / TILE_SIZE

            sprite.vy = 0
            sprite.get_hit_rect().y = sprite.y * TILE_SIZE

        return hit
    else:
        return False


def slither(group, hit, sprite, axis):
    """Slithers the sprite along the hit in the direction with an opening"""
    if axis == "x":
        if there_is_space(hit, group, "right"):
            sprite.x += SLITHER_SPEED
        elif there_is_space(hit, group, "left"):
            sprite.x -= SLITHER_SPEED
    elif axis == "y":
        if there_is_space(hit, group, "down"):
            sprite.y += SLITHER_SPEED
        elif there_is_space(hit, group, "up"):
            sprite.y -= SLITHER_SPEED
    else:
        assert False


def there_is_space(hit, group, direction):
    """Returns true if there is space in the direction given"""
    if direction == "up":
        point = (hit.get_hit_rect().x, hit.get_hit_rect().y - 1)
    elif direction == "down":
        point = (hit.get_hit_rect().x, hit.get_hit_rect().y + hit.get_hit_rect().height + 1)
    elif direction == "right":
        point = (hit.get_hit_rect().x  + hit.get_hit_rect().width + 1, hit.get_hit_rect().y)
    elif direction == "left":
        point = (hit.get_hit_rect().x - 1, hit.get_hit_rect().y)
    else:
        assert False

    hits = [s for s in group if s.get_hit_rect().collidepoint(point)]

    return not hits


def collide_with_triggers(sprite, triggers):
    hits = [s for s in triggers if sprite.get_rect().inflate(20, 20).colliderect(s.hit_rect)]
    for hit in hits:
        hit.on_hit()
