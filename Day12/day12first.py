from math import cos, sin, radians


class Waypoint:

    x: float
    y: float

    def __init__(self):
        self.x = 10
        self.y = 1

    def rotate(self, angle):
        x = self.x * cos(radians(angle)) - self.y * sin(radians(angle))
        self.y = self.y * cos(radians(angle)) + self.x * sin(radians(angle))
        self.x = x

    def direction(self, x, y):
        self.x += x
        self.y += y


class Ship:

    x: float
    y: float
    theta: float

    def __init__(self):
        self.x = self.y = self.theta = 0

    def forward(self, length):
        self.x += length * cos(radians(self.theta))
        self.y += length * sin(radians(self.theta))

    def turn(self, angle):
        self.theta += angle

    def direction(self, x, y):
        self.x += x
        self.y += y

    def to_waypoint(self, waypoint, times):
        self.x += times * waypoint.x
        self.y += times * waypoint.y


def parse(data: str):
    return [(line[0], int(line[1:])) for line in data.split('\n')]


def first():
    ship = Ship()
    with open('input') as f:
        instructions = parse(f.read())

    for instr, num in instructions:
        if instr == 'N':
            ship.direction(0, num)
        elif instr == 'W':
            ship.direction(-num, 0)
        elif instr == 'S':
            ship.direction(0, -num)
        elif instr == 'E':
            ship.direction(num, 0)
        elif instr == 'R':
            ship.turn(-num)
        elif instr == 'L':
            ship.turn(num)
        elif instr == 'F':
            ship.forward(num)
        else:
            print("Invalid instruction", instr, num)

    print("Manhattan distance: ", ship.x, ship.y, abs(ship.x) + abs(ship.y))


def second():
    ship = Ship()
    waypoint = Waypoint()
    with open('input') as f:
        instructions = parse(f.read())

    for instr, num in instructions:
        if instr == 'N':
            waypoint.direction(0, num)
        elif instr == 'W':
            waypoint.direction(-num, 0)
        elif instr == 'S':
            waypoint.direction(0, -num)
        elif instr == 'E':
            waypoint.direction(num, 0)
        elif instr == 'R':
            waypoint.rotate(-num)
        elif instr == 'L':
            waypoint.rotate(num)
        elif instr == 'F':
            ship.to_waypoint(waypoint, num)
        else:
            print("Invalid instruction", instr, num)

    print("Manhattan distance: ", abs(ship.x) + abs(ship.y))

second()