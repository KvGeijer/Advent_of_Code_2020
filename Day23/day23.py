input = '158937462'


class Node(object):

    def __init__(self, nbr):
        self.value = nbr
        self.next = None


def set_up():
    nbrs = map(int, list(input))

    start = Node(next(nbrs))
    behind = start

    nodes = [start]

    for nbr in nbrs:
        current = Node(nbr)
        behind.next = current
        behind = current
        nodes.append(current)

    behind.next = start
    return start


def pickup(start: Node) -> Node:
    ret = start.next
    current = ret
    for i in range(3-1):
        current = current.next

    start.next = current.next
    current.next = None

    return ret


def round(current: Node) -> Node:

    # Pick up three
    picked = pickup(current)

    destination = current
    goal = current.value-1
    while destination.value != goal:
        destination = destination.next
        if destination == current:
            goal -= 1
            if goal < 1:
                goal = 9

    dest_next = destination.next
    destination.next = picked

    for i in range(3-1):
        picked = picked.next

    picked.next = dest_next

    return current.next


def result(current: Node) -> str:
    while current.value != 1:
        current = current.next

    current = current.next

    res = []
    while current.value != 1:
        res.append(str(current.value))
        current = current.next

    return "".join(res)


def result2(current: Node) -> int:
    while current.value != 1:
        current = current.next

    current = current.next
    return current.value * current.next.value


def first():
    current = set_up()

    for turn in range(100):
        current = round(current)

    print(result(current))


def set_up2() -> (Node, {int: Node}):
    nbrs = map(int, list(input))

    start = Node(next(nbrs))
    behind = start

    nodes = {start.value: start}

    for nbr in nbrs:
        current = Node(nbr)
        behind.next = current
        behind = current
        nodes[current.value] = current

    for i in range(9+1, 1000000 + 1):
        current = Node(i)
        behind.next = current
        behind = current
        nodes[current.value] = current

    behind.next = start
    return start, nodes


def round2(current: Node, nodes: {int: Node}) -> Node:

    # Pick up three
    picked = pickup(current)
    picked_val = set()
    temp = picked
    while temp is not None:
        picked_val.add(temp.value)
        temp = temp.next

    goal = current.value-1

    while goal in picked_val or goal == 0:
        goal -= 1
        if goal < 1:
            goal = 1000000

    destination = nodes[goal]

    dest_next = destination.next
    destination.next = picked

    for i in range(3-1):
        picked = picked.next

    picked.next = dest_next

    return current.next


def second():
    current, nodes = set_up2()

    for turn in range(10000000):
        if turn % 10000 == 0:
            print("Turn: ", turn, " completed!")
        current = round2(current, nodes)

    print(result2(current))


second()