from settings import *

# multipliers to transform coordinates into other octants
MULT = [
  [1,  0,  0, -1, -1,  0,  0,  1],
  [0,  1, -1,  0,  0, -1,  1,  0],
  [0,  1,  1,  0,  0, -1, -1,  0],
  [1,  0,  0,  1, -1,  0,  0, -1],
]

data = {}


def calc_fov(startx, starty, radius, visibility_data):
    global data
    data = {}

    def blocked_func(x, y):
        return is_blocked(x, y, visibility_data)

    light(startx, starty)
    for octant in range(8):
        cast_light(cx=startx, cy=starty, row=1, light_start=1.0, light_end=0.0, radius=radius,
                   xx=MULT[0][octant], xy=MULT[1][octant], yx=MULT[2][octant], yy=MULT[3][octant],
                   light_func=light, blocked_func=blocked_func)

    return data


def cast_light(cx, cy, row, light_start, light_end, radius, xx, xy, yx, yy, light_func, blocked_func):
    new_start = 0.0
    if light_start < light_end:
        return

    radius_sqr = radius * radius

    for j in range(row, radius + 1):
        blocked = False
        dx, dy = -j-1, -j
        while dx <= 0:
            dx += 1
            # translate dx, dy into map coordinates
            mx = cx + dx * xx + dy * xy
            my = cy + dx * yx + dy * yy
            l_slope = (dx-0.5)/(dy+0.5)
            r_slope = (dx+0.5)/(dy-0.5)
            if light_start < r_slope:
                continue
            elif light_end > l_slope:
                break
            else:
                if dx*dx + dy*dy < radius_sqr:
                    light_func(mx, my)

                if blocked:
                    if blocked_func(mx, my):
                        new_start = r_slope
                        continue
                    else:
                        blocked = False
                        light_start = new_start
                else:
                    if blocked_func(mx, my) and j < radius:
                        blocked = True
                        cast_light(cx=cx, cy=cy, row=j+1, light_start=light_start, light_end=l_slope,
                                   radius=radius, xx=xx, xy=xy, yx=yx, yy=yy,
                                   light_func=light_func, blocked_func=blocked_func)
                        new_start = r_slope

        if blocked:
            break


def is_blocked(x, y, visibility_map):
    return not visibility_map[x][y]


def light(mx, my):
    data[fov_index(mx, my)] = True


def fov_index(mx, my):
    return mx * FOV_RADIUS + my
