def parse_second(data: str) -> ([{int}], {int}, [[int]], [int]):
    [req, our, nearby] = data.split("\n\n")

    oksets = []
    okset = set()
    for line in req.split('\n'):
        words = line.split(' ')

        temp_set = set()
        for r in [-1, -3]:
            [start, stop] = map(int, words[r].split('-'))

            okset |= set(range(start, stop+1))
            temp_set |= set(range(start, stop+1))

        oksets.append(temp_set)

    tickets = [[int(x) for x in line.split(',')] for line in nearby.split('\n')[1:]]

    our = list(map(int, our.split("\n")[1].split(",")))

    return oksets, okset, tickets, our


def valid_ticket(ticket: [int], okset: {int}) -> bool:
    return all(map(lambda x: x in okset, ticket))


def second():
    with open('input', 'r') as f:
        oksets, okset, tickets, our = parse_second(f.read())

    tickets = [ticket for ticket in tickets if valid_ticket(ticket, okset)]

    possible = [set(range(len(oksets))) for i in oksets]

    print(possible)

    for ticket in tickets:
        for posset, el in zip(possible, ticket):    #Posset possible fields of that column
            remove = []
            for pos in posset:
                if el not in oksets[pos]:
                    remove.append(pos)

            for pos in remove:
                posset.remove(pos)

    fields = [-1] * len(possible)

    for col, poss in sorted(enumerate(possible), key=lambda x: len(x[1])):
        for field in poss:
            # if field not in fields:
            if fields[field] == -1:
                fields[field] = col
                break

    cols = fields[0:6]
    print(cols)

    prod = 1
    for col in cols:
        prod *= our[col]

    print(prod)












second()