# I use numpy for the grid since I don't want linked lists...

import numpy as np

MAP = {'L': 0, '#': 1, '.': 2}


def parse(data: str) -> np.ndarray:
    return np.array([[MAP[c] for c in line] for line in data.split('\n')], dtype=int)


def next_state(grid: np.ndarray) -> bool:
    neighs = np.empty(np.shape(grid), dtype=int)
    max_row = len(grid[:, 0]) - 1
    max_col = len(grid[0, :]) - 1

    for row, col in [(i, j) for j in range(max_col+1) for i in range(max_row+1)]:
        neighs[row, col] = 0
        if grid[row, col] != 2:
            for r, c in [(i, j) for j in [-1, 0, 1] for i in [-1, 0, 1]]:
                while 0 <= r + row <= max_row and 0 <= c + col <= max_col and grid[r + row, c + col] == 2:
                    if r > 0:
                        r += 1
                    elif r < 0:
                        r -= 1
                    if c > 0:
                        c += 1
                    elif c < 0:
                        c -= 1

                if 0 <= r + row <= max_row and 0 <= c + col <= max_col:
                    neighs[row, col] += grid[r + row, c + col]

    modified = False

    for row, col in [(i, j) for j in range(max_col+1) for i in range(max_row+1)]:
        if grid[row, col] == 0 and neighs[row, col] == 0:
            grid[row, col] = 1
            modified = True
        elif grid[row, col] == 1 and neighs[row, col] > 5:
            grid[row, col] = 0
            modified = True

    return modified


def count_seats(grid: np.ndarray) -> int:
    sum = 0
    for el in np.nditer(grid):
        if el == 1:
            sum += 1

    return sum


def main():
    with open('input') as f:
        grid = parse(f.read())

    i = 0

    while next_state(grid) and i < 1000:
        i += 1

    print(i)
    print(count_seats(grid))


main()
