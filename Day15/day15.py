def parse1(data: str) -> (int, {int: int}):
    instr = data.split(',')
    return int(instr[-1]), {int(number): ind for ind, number in enumerate(instr[:-1])}


def solve():
    with open('input') as f:
        next, table = parse1(f.read())

    for i in range(len(table), 30000000 - 1):
        if next in table:
            diff = i - table[next]
            table[next] = i
            next = diff
        else:
            table[next] = i
            next = 0

    print("The number to be announced is ", next)


solve()