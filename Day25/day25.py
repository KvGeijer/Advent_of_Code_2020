input = [5099500, 7648211]
input2 = [5764801, 17807724]


def handshake(loop_nbr: int, sub_nbr: int) -> int:
    value = 1
    for i in range(loop_nbr):
        value *= sub_nbr
        value %= 20201227

    return value


def find_loop(key: int) -> int:
    loop_nbr = 1
    value = 1
    sub_nbr = 7

    while True:
        value *= sub_nbr
        value %= 20201227

        if value == key:
            return loop_nbr

        loop_nbr += 1


# I was very tired when I did this, was sort of a bit tired on christmas day... Also did 24 on the 25th
def first():
    card_loop = find_loop(input[0])

    print("The resulting encryption something is ", handshake(card_loop, input[1]))


first()

# print(handshake(8, 7))
# print(handshake(11, 7))