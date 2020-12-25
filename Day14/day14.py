

def first():
    with open("input") as f:
        instructions = f.read().split("\n")

    mem = {}

    # The mask is represented as some set bits and some free ones
    sett = 0
    free = 0

    for line in instructions:
        if line[1] == 'e':     # New number into memory
            [left, right] = line.split(" = ")

            key = int(left[4:-1])
            value = int(right)

            value = (value & free) + sett

            mem[key] = value

        elif line[1] == 'a':    # New mask
            sett = 0
            free = 0
            for el in line[-36:]:
                sett = sett << 1
                free = free << 1
                if el == 'X':
                    free += 1
                elif el == '1':
                    sett += 1

    summ = 0
    for value in mem.values():
        summ += value

    print("The sum in memory is ", summ)


def second():
    with open("input") as f:
        instructions = f.read().split("\n")

    mem = {}

    # The mask is represented as some free bits, some set to ones and some floating, along with the floating branches
    ones: int = 0
    free: int = 0
    floating: int = 0
    branches: [int] = [0]

    for line in instructions:
        if line[1] == 'e':     # New number into memory
            [left, right] = line.split(" = ")

            address = int(left[4:-1])
            value = int(right)

            address = (address & free) + ones

            for branch in branches:
                mem[branch+address] = value

        elif line[1] == 'a':    # New mask
            floating = 0
            free = 0
            ones = 0

            branches = [0]

            for ind, el in enumerate(line[-36:]):

                if el == 'X':
                    floating += 1 << (36 - ind - 1)
                    new_branches = []
                    for branch in branches:
                        new_branches.append((1 << (36 - ind - 1)) + branch)
                    branches = branches + new_branches
                elif el == '1':
                    ones += 1 << (36 - ind - 1)
                else:
                    free += 1 << (36 - ind - 1)

    summ = 0
    for value in mem.values():
        summ += value

    print("The sum in memory is ", summ)


second()