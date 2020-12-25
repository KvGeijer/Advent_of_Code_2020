
def parse(data: str) -> (int, [int]):
    lines = data.split("\n")
    earliest = int(lines[0])
    departures = []
    for dep in lines[1].strip().split(','):
        if dep != 'x':
            departures.append(int(dep))
    return earliest, departures


def first():
    with open("input") as f:
        earliest, times = parse(f.read())

    best = -1
    dist = 10000

    for time in times:
        if abs(time - earliest % time) < dist:
            dist = abs(time - earliest % time)
            best = time

    print("The best bus is ", best, " with a waiting time of ", dist, ".\nGiving a solution of ", best * dist)


def parse2(data: str) -> [(int, int)]:
    lines = data.split("\n")
    departures = []
    for ind, dep in enumerate(lines[1].strip().split(',')):
        if dep != 'x':
            departures.append((ind, int(dep)))

    return departures


def validate(deps: [(int, int)], start: int) -> bool:
    for offset, time in deps:
        if (start + offset) % time != 0:
            return False
    return True


def second():
    with open("input") as f:
        departments = parse2(f.read())

    deps = sorted(departments, reverse=True, key=lambda x: x[1])
    i = 1

    while True:
        start = deps[0][1] * i - deps[0][0]

        if validate(deps, start):
            print("The earliest possible start: ", start)
            return

        i += 1


# a is larger than b!
def gcd(a:int, b:int) -> int:
    rest = a % b
    if rest == 0:
        return b
    else:
        return gcd(b, rest)


def lcm(a: int, b: int) -> int:
    if a>=b:
        return abs(a*b)//gcd(a, b)
    else:
        return abs(a*b)//gcd(b, a)


def second2():
    with open("input") as f:
        departments = parse2(f.read())

    # Could sort it here, but don't know if that makes it faster...
    current = 0
    common = 1

    for offset, time in departments:

        while (current + offset) % time != 0:
            current += common

        common = lcm(common, time)

    print("The magical time is ", current)


second2()


