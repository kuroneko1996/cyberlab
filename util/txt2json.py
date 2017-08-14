import sys, json


def print_usage():
    print("""USAGE: python txt2json.py <input txt file> <output json file>""")


def main():
    if len(sys.argv) < 3:
        print_usage()
        return

    in_file = sys.argv[1]
    out_file = sys.argv[2]

    data = []
    with open(in_file, 'rt') as f:
        for line in f:
            data.append(line.strip())

    out_map = []

    for row, tiles in enumerate(data):
        for col, tile in enumerate(tiles):
            if tile == '1':
                out_map.append({"x": col, "y": row, "name": "WALL"})
            elif tile == 'P': \
                out_map.append({"x": col, "y": row, "name": "PLAYER"})

    with open(out_file, 'wt') as f:
        f.write(json.dumps(out_map, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()