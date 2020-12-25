from itertools import product


class Coord:
    def __init__(self, x, se):
        self.x = x
        self.se = se

    def __hash__(self):
        return self.x + self.se

    def __add__(self, other):
        if type(other) != Coord:
            print("Can only add coords, not coord and ", type(other))
            exit(-1)

        return Coord(self.x + other.x, self.se + other.se)

    def __repr__(self):
        return "".join(['(', str(self.x), ' , ', str(self.se), ')'])

    def __eq__(self, other):
        if type(other) != Coord:
            print("Can only add coords, not coord and ", type(other))
            exit(-1)

        return self.x == other.x and self.se == other.se


def parseLine(text: str) -> [Coord]:

    total = Coord(0, 0)

    i = 0
    while i < len(text):
        curr = text[i]

        if curr == 'e':
            coord = Coord(1, 0)
        elif curr == 'w':
            coord = Coord(-1, 0)
        else:
            curr = text[i:i+2]
            i += 1

            if curr == "sw":
                coord = Coord(0, -1)
            elif curr == "se":
                coord = Coord(1, -1)
            elif curr == "nw":
                coord = Coord(-1, 1)
            elif curr == "ne":
                coord = Coord(0, 1)
            else:
                print("invalid coordinate!")
                exit(-1)

        i += 1
        total += coord

    return total


def parse(text: str) -> [Coord]:
    lst = []
    for line in text.split("\n"):
        lst.append(parseLine(line))

    return lst


def first():
    with open("input") as f:
        coords = parse(f.read())

    blacks = set()

    for coord in coords:
        if coord in blacks:
            blacks.remove(coord)
        else:
            blacks.add(coord)

    print(len(blacks))


def second():
    with open("input") as f:
        coords = parse(f.read())

    blacks = set()

    for coord in coords:
        if coord in blacks:
            blacks.remove(coord)
        else:
            blacks.add(coord)

    # For each day create a dict keeping track of neighbours
    offsets = [Coord(1, 0), Coord(-1, 0), Coord(0, 1), Coord(0, -1), Coord(1, -1), Coord(-1, 1)]
    for day in range(100):
        neighs: {Coord: int} = {coord: 0 for coord in blacks}

        for coord, offset in product(blacks, offsets):
            curr = coord + offset

            if curr not in neighs:
                neighs[curr] = 0

            neighs[curr] += 1

        for coord, neigs in neighs.items():
            if coord in blacks and (neigs > 2 or neigs == 0):
                blacks.remove(coord)
            elif coord not in blacks and neigs == 2:
                blacks.add(coord)

        print("Day: ", day, ", nbr black: ", len(blacks))

    print("Final number of black plates: ", len(blacks))




second()
