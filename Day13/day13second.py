def parse2(data: str) -> [(int, int)]:
    lines = data.split("\n")
    departures = []
    for ind, dep in enumerate(lines[1].strip().split(',')):
        if dep != 'x':
            departures.append((ind, int(dep)))

    return departures


# a must be larger than b!
def gcd(a:int, b:int) -> int:
    rest = a % b
    if rest == 0:
        return b
    else:
        return gcd(b, rest)


def lcm(a: int, b: int) -> int:
    if a >= b:
        return abs(a*b)//gcd(a, b)
    else:
        return abs(a*b)//gcd(b, a)


def second2():
    with open("../Day14/input3") as f:
        departments = parse2(f.read())

    current = 0
    common = 1

    for offset, time in departments:

        while (current + offset) % time != 0:
            current += common

        common = lcm(common, time)

    print("The magical time is ", current)


second2()
