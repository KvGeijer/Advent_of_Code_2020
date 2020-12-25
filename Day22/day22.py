from collections import deque


def parse(text: str) -> (deque, deque):
    (my, theirs) = map(lambda x: x.split("\n")[1:], text.split("\n\n"))

    return deque(map(int, my)), deque(map(int, theirs))


# Assumes they are non.empty
def one_round(my_deck: deque, their_deck: deque):
    my = my_deck.popleft()
    their = their_deck.popleft()

    if my > their:
        my_deck.append(my)
        my_deck.append(their)
    elif their > my:
        their_deck.append(their)
        their_deck.append(my)
    else:
        print("What to do? It is a tie...")
        exit(-1)


def first():
    with open("input") as f:
        my_deck, their_deck = parse(f.read())

    while my_deck and their_deck:   # Checks if they are non-empty
        one_round(my_deck, their_deck)

    score = 0

    if my_deck:
        my_deck.reverse()
        for ind, card in enumerate(my_deck, 1):
            score += ind*card
    elif their_deck:
        their_deck.reverse()
        for ind, card in enumerate(their_deck, 1):
            score += ind * card
    else:
        print("No one lost? Nani!?")
        exit(-1)

    print(score)


first()