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
    hits = [s for s in group if sprite.hit_rect.colliderect(s.hit_rect)]

    for hit in hits:
        hit.on_hit()

    if hits:
        hit = hits[0]
        if axis == 'x':
            if sprite.vx > 0:
                sprite.x = (hit.hit_rect.left - sprite.hit_rect.width) / TILE_SIZE
            elif sprite.vx < 0:
                sprite.x = hit.hit_rect.right / TILE_SIZE

            sprite.vx = 0
            sprite.hit_rect.x = sprite.x * TILE_SIZE
        elif axis == 'y':
            if sprite.vy > 0:
                sprite.y = (hit.hit_rect.top - sprite.hit_rect.height) / TILE_SIZE
            elif sprite.vy < 0:
                sprite.y = hit.hit_rect.bottom / TILE_SIZE

            sprite.vy = 0
            sprite.hit_rect.y = sprite.y * TILE_SIZE

        return hit
    else:
        return False


def slither(group, hit, sprite, axis, do_slither = True):
    """Slithers the sprite along the hit in the direction with an opening"""
    if axis == "x":
        if there_is_space(hit, group, "right"):
            sprite.move(SLITHER_SPEED, 0, do_slither)
        elif there_is_space(hit, group, "left"):
            sprite.move(-SLITHER_SPEED, 0, do_slither)
    elif axis == "y":
        if there_is_space(hit, group, "down"):
            sprite.move(0, SLITHER_SPEED, do_slither)
        elif there_is_space(hit, group, "up"):
            sprite.move(0, -SLITHER_SPEED, do_slither)
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


def can_walk(sprite, group, dx, dy):
    """
    Produces true if the sprite can be moved by (dx,dy)
    :param sprite: sprite that is being moved
    :param group: clipping group
    :param dx: x shift
    :param dy: y shift
    :return: true if the sprite can be moved, false otherwise
    """

    # Hypothesis: this does not account for the full path from current position to the next position
    return not [s for s in group if sprite.hit_rect.inflate(dx, dy).move(dx, dy).colliderect(s.hit_rect)]