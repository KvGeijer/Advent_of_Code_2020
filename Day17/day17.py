import numpy as np


def parse1(text: str) -> np.ndarray:

    lines = text.split('\n')
    n = len(lines[0]) + 2*6

    grid = np.array([[[False for row in range(1+6*2)] for j in range(n)] for k in range(n)], dtype=bool)

    for row, line in enumerate(lines):
        for col, el in enumerate(line):
            grid[6+row, 6+col, 6] = el == '#'

    return grid


def update(grid: np.ndarray):
    copy = np.copy(grid)

    rows, cols, layers = np.shape(grid)

    for layer in range(layers):
        for col in range(cols):
            for row in range(rows):
                neighbours = 0
                for off_layer in [-1, 0, 1]:
                    for off_col in [-1, 0, 1]:
                        for off_row in [-1, 0, 1]:
                            if 0 <= row + off_row < rows and 0 <= col + off_col < cols and 0 <= layer + off_layer < layers:
                                neighbours += 1 if copy[row + off_row, col + off_col, layer + off_layer] else 0

                if grid[row, col, layer] and neighbours not in [3, 4]:
                    grid[row, col, layer] = False
                elif (not grid[row, col, layer]) and neighbours == 3:
                    grid[row, col, layer] = True


def first():
    with open('input') as f:
        grid = parse1(f.read())

    for k in range(6):
        update(grid)

    print(np.sum(grid))


def parse2(text: str) -> np.ndarray:

    lines = text.split('\n')
    n = len(lines[0]) + 2*6

    grid = np.array([[[[False for row in range(1+6*2)] for j in range(1+6*2)] for k in range(n)] for l in range(n)], dtype=bool)

    for row, line in enumerate(lines):
        for col, el in enumerate(line):
            grid[6+row, 6+col, 6, 6] = el == '#'

    return grid


def update2(grid: np.ndarray):
    copy = np.copy(grid)

    rows, cols, layers, planes = np.shape(grid)

    for plane in range(planes):
        for layer in range(layers):
            for col in range(cols):
                for row in range(rows):
                    neighbours = 0
                    for off_plane in [-1, 0, 1]:
                        for off_layer in [-1, 0, 1]:
                            for off_col in [-1, 0, 1]:
                                for off_row in [-1, 0, 1]:
                                    if 0 <= row + off_row < rows and 0 <= col + off_col < cols \
                                            and 0 <= layer + off_layer < layers and 0 <= plane + off_plane < planes:
                                        neighbours += 1 if copy[row + off_row, col + off_col, \
                                                                layer + off_layer, plane + off_plane] else 0

                    if grid[row, col, layer, plane] and neighbours not in [3, 4]:
                        grid[row, col, layer, plane] = False
                    elif (not grid[row, col, layer, plane]) and neighbours == 3:
                        grid[row, col, layer, plane] = True


def second():
    with open('input') as f:
        grid = parse2(f.read())

    for k in range(6):
        update2(grid)

    print(np.sum(grid))


second()