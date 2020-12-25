import numpy as np
import math
import itertools


class Tile:
    id: int
    image: np.ndarray
    edges = {str}  # Also flipped versions!


def parse(data: str) -> {int: Tile}:
    tiles = {}

    for part in data.split("\n\n"):
        tile = Tile()
        lines = part.split("\n")

        tile.id = int(lines[0][5:-1])
        tile.image = np.array(list(map(list, lines[1:])), dtype="str")

        tile.edges = set()
        tile.edges.add("".join(tile.image[0, :]))
        tile.edges.add("".join(tile.image[-1, :]))
        tile.edges.add("".join(tile.image[:, 0]))
        tile.edges.add("".join(tile.image[:, -1]))
        tile.edges.add("".join(reversed(tile.image[0, :])))
        tile.edges.add("".join(reversed(tile.image[-1, :])))
        tile.edges.add("".join(reversed(tile.image[:, 0])))
        tile.edges.add("".join(reversed(tile.image[:, -1])))

        tiles[tile.id] = tile

    return tiles


def first():
    with open("input") as f:
        tiles = parse(f.read())

    length = round(math.sqrt(len(tiles)))
    tile_size = 8   # Hard coded but whatever
    image = np.empty((length * tile_size, length * tile_size), dtype=str)
    image_edges = np.empty((length, length, 4), dtype=np.ndarray)  # Third index is the orientation of the edge

    last_unique = []
    corners = []

    for tile in tiles:
        edges = []
        for edge in tiles[tile].edges:
            if "".join(reversed(edge)) not in edges:
                edges.append(edge)

        edges_shared = 0
        for tile2 in tiles:
            if tile2 != tile:
                for edge in edges:
                    if edge in tiles[tile2].edges:
                        edges.remove(edge)
                        edges_shared += 1

        if edges_shared <= 2:
            corners.append(tile)
            last_unique = edges

    print("First part: ", math.prod(corners))

    # Fill in upper left corner of image_ids
    dir0: int = 0
    dir1: int = 0

    corner = tiles[corners[-1]]

    if last_unique[0] == "".join(corner.image[:, 0]) or last_unique[0] == "".join(reversed(corner.image[:, 0])):
        dir0 = 0
    elif last_unique[0] == "".join(corner.image[0, :]) or last_unique[0] == "".join(reversed(corner.image[0, :])):
        dir0 = 1
    elif last_unique[0] == "".join(corner.image[:, -1]) or last_unique[0] == "".join(reversed(corner.image[:, -1])):
        dir0 = 2
    elif last_unique[0] == "".join(corner.image[-1, :]) or last_unique[0] == "".join(reversed(corner.image[-1, :])):
        dir0 = 3
    else:
        print("Fuck 0")

    if last_unique[1] == "".join(corner.image[:, 0]) or last_unique[1] == "".join(reversed(corner.image[:, 0])):
        dir1 = 0
    elif last_unique[1] == "".join(corner.image[0, :]) or last_unique[1] == "".join(reversed(corner.image[0, :])):
        dir1 = 1
    elif last_unique[1] == "".join(corner.image[:, -1]) or last_unique[1] == "".join(reversed(corner.image[:, -1])):
        dir1 = 2
    elif last_unique[1] == "".join(corner.image[-1, :]) or last_unique[1] == "".join(reversed(corner.image[-1, :])):
        dir1 = 3
    else:
        print("Fuck 1")

    corner_dir = {dir0, dir1}

    if corner_dir == {1, 2}:
        corner.image = np.rot90(corner.image)
    elif corner_dir == {2, 3}:
        corner.image = np.rot90(np.rot90(np.image))
    elif corner_dir == {3, 0}:
        corner.image = np.rot90(np.rot90(np.rot90(np.image)))

    image[0:tile_size, 0:tile_size] = corner.image[1:-1, 1:-1]
    image_edges[0, 0, 0] = corner.image[:, -1]
    image_edges[0, 0, 3] = corner.image[-1, :]

    del tiles[corners[-1]]

    print("Image rendering...")
    for (row, col) in itertools.product(range(length), range(length)):
        if col != 0:
            # Find parner from [row, col-1, 0]
            border = image_edges[row, col - 1, 0]

            id = id_by_edge(tiles, "".join(border))
            tile = tiles[id]
            del tiles[id]

            dir = find_dir(border, tile.image)
            rotate(2, dir, tile)

            # Check if we need to flip it
            if np.any(tile.image[:, 0] != border):
                tile.image = np.flip(tile.image, 0)

            image[(row*tile_size):((row+1)*tile_size), (col*tile_size):((col+1)*tile_size)] = tile.image[1:-1, 1:-1]
            image_edges[row, col, 0] = tile.image[:, -1]
            image_edges[row, col, 3] = tile.image[-1, :]

        elif row != 0:
            # Find parner from [row-1, col, 3]
            border = image_edges[row - 1, col, 3]

            id = id_by_edge(tiles, "".join(border))
            tile = tiles[id]
            del tiles[id]

            dir = find_dir(border, tile.image)
            rotate(1, dir, tile)

            # Check if we need to flip it
            if np.any(tile.image[0, :] != border):
                tile.image = np.flip(tile.image, 1)

            image[(row*tile_size):((row+1)*tile_size), (col*tile_size):((col+1)*tile_size)] = tile.image[1:-1, 1:-1]
            image_edges[row, col, 0] = tile.image[:, -1]
            image_edges[row, col, 3] = tile.image[-1, :]

    print("Image rendered... Complete!")

    original_rocks = np.sum(image == '#')
    print("Starting number of rocks: ", original_rocks)

    # Now onto the part of finding the sea monster!
    sea_monster_inds = get_monster()

    # Really want to do this more functionally
    width = max(sea_monster_inds, key=lambda x: x[1])[1] + 1
    height = max(sea_monster_inds, key=lambda x: x[0])[0] + 1

    i = 0
    monsters = []
    while monsters == []:   # I like it this way ;(
        image = np.rot90(image)
        if i == 3:
            image = np.flip(image, axis=0)
        if i == 7:
            image = np.flip(image, axis=1)
        if i == 11:
            image = np.flip(image, axis=0)
        if i == 15:
            print("i == 5, FUCK")
        i += 1
        # Check if the sea monster can start at all of these positions!
        for row, col in itertools.product(range(length*tile_size - height), range(length*tile_size - width)):
            if monster_at(row, col, image, sea_monster_inds):
                monsters.append((row, col))

    print("Monsters: ", monsters)

    for (start_row, start_col) in monsters:
        for (row, col) in sea_monster_inds:
            image[start_row + row, start_col + col] = 'O'

    num_hash = np.sum(image == '#')
    print("The number of rocks is: ", num_hash)


def monster_at(row: int, col: int, image: np.ndarray, monster_inds: [(int, int)]) -> bool:
    for (off_row, off_col) in monster_inds:
        if image[row + off_row, col + off_col] != '#':
            return False
    return True


def get_monster() -> [(int, int)]:
    with open("sea_monster") as f:
        lines = f.read().split('\n')

    length = len(lines[0])
    monster: (int, int) = []
    for row, col in itertools.product(range(3), range(length)):
        if lines[row][col] == '#':
            monster.append((row, col))

    return monster


def rotate(to: int, now: int, tile):
    for rot in range(to-now + 4):
        tile.image = np.rot90(tile.image)


def find_dir(border, image) -> int:
    border = "".join(border)
    if border == "".join(image[:, 0]) or border == "".join(reversed(image[:, 0])):
        return 2
    elif border == "".join(image[0, :]) or border == "".join(reversed(image[0, :])):
        return 1
    elif border == "".join(image[:, -1]) or border == "".join(reversed(image[:, -1])):
        return 0
    elif border == "".join(image[-1, :]) or border == "".join(reversed(image[-1, :])):
        return 3
    else:
        print("Fuck, no direction found")
        return -1


def id_by_edge(tiles: {int: Tile}, edge: str) -> int:
    for id, tile in tiles.items():
        if edge in tile.edges:
            return id

    print("Fuck, no edge found")
    return -1


first()
