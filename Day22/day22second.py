from collections import deque


def parse(text: str) -> (deque, deque):
    (my, theirs) = map(lambda x: x.split("\n")[1:], text.split("\n\n"))

    return deque(map(int, my)), deque(map(int, theirs))


def score(deck: deque) -> int:
    rev = reversed(deck)
    result = 0
    for ind, card in enumerate(rev, 1):
        result += ind * card

    return result


def deque_to_tuple(deck: deque) -> tuple:
    return tuple((i for i in deck))


def cpy_slice(deck: deque, slice: int) -> deque:
    cpy = deck.copy()
    return deque([cpy.popleft() for i in range(slice)])


def round(my_deck: deque, their_deck: deque) -> bool:
    my_card = my_deck.popleft()
    their_card = their_deck.popleft()

    # Should we recurse?
    if my_card <= len(my_deck) and their_card <= len(their_deck):
        # This probably won't work... But this is the idea
        winner = game(cpy_slice(my_deck, my_card), cpy_slice(their_deck, their_card))

        # Ugly duplicate of code, but....
        if winner:
            my_deck.append(my_card)
            my_deck.append(their_card)
            return True
        else:
            their_deck.append(their_card)
            their_deck.append(my_card)
            return False

    elif my_card > their_card:
        my_deck.append(my_card)
        my_deck.append(their_card)
        return True
    elif their_card > my_card:
        their_deck.append(their_card)
        their_deck.append(my_card)
        return False
    else:
        print("What to do? It is a tie...")
        exit(-1)


# Did I win a game with the given decks?
def game(my_deck: deque, their_deck: deque) -> bool:
    # Are the deques really hashable?
    earlier = {deque_to_tuple(my_deck)}

    while my_deck and their_deck:
        round(my_deck, their_deck)
        tup = deque_to_tuple(my_deck)
        if tup in earlier:
            # Infinite loop, we win. Life is unfair
            return True
        else:
            earlier.add(tup)

    return bool(my_deck)


def second():
    with open("input") as f:
        my_deck, their_deck = parse(f.read())

    if game(my_deck, their_deck):
        print(score(my_deck))
    else:
        print(score(their_deck))


second()