import sys, json


def print_usage():
    print("""USAGE: python tiled2json.py <input json tiled file> <output json file>""")


def move_to_visible_area(out_map):
    """Moves the sprites in the map so that they begin at (0, 0)"""
    min_x = min(map(lambda node: node["x"], out_map))
    min_y = min(map(lambda node: node["y"], out_map))

    for node in out_map:
        node["x"] = node["x"] - min_x
        node["y"] = node["y"] - min_y


def main():
    if len(sys.argv) < 3:
        print_usage()
        return

    in_file = sys.argv[1]
    out_file = sys.argv[2]

    with open(in_file, 'rt') as f:
        data = json.loads(f.read())

    out_map = []

    width = data["width"]
    count = 0
    for tile in data["layers"][0]["data"]:
        col = count % width
        row = count // width
        count += 1

        if tile == 1:
            out_map.append({"x": col, "y": row, "name": "WALL"})
        elif tile == 2:
            out_map.append({"x": col, "y": row, "name": "APPLE"})

        elif tile == 3:
            out_map.append({"x": col, "y": row, "name": "DOOR", "dir": "up"})
        elif tile == 4:
            out_map.append({"x": col, "y": row, "name": "DOOR", "dir": "right"})
        elif tile == 5:
            out_map.append({"x": col, "y": row, "name": "DOOR", "dir": "down"})
        elif tile == 6:
            out_map.append({"x": col, "y": row, "name": "DOOR", "dir": "left"})

        elif 9 <= tile <= 16 or 19 <= tile <= 24:
            out_map.append({"x": col, "y": row, "name": "PLAYER"})

    move_to_visible_area(out_map)

    with open(out_file, 'wt') as f:
        f.write(json.dumps(out_map, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()