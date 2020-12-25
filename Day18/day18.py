

def evaluate(expr: str, ind: int) -> (int, int):
    first = 0
    second = 0

    current = expr[ind]

    if current.isnumeric():
        while current.isnumeric():
            first *= 10
            first += int(current)

            ind += 1
            current = expr[ind]

    elif current == '(':
        ind, first = evaluate(expr, ind+1)
        current = expr[ind]

    while current != ")":
        ind += 1
        current = expr[ind]

        operator = current

        ind += 2
        current = expr[ind]

        if current == '(':
            ind, second = evaluate(expr, ind+1)
            current = expr[ind]
        else:
            second = 0
            while current.isnumeric():
                second *= 10
                second += int(current)

                ind += 1
                current = expr[ind]

        if operator == '+':
            first += second
        elif operator == '*':
            first *= second
        else:
            print("invalid operator!", operator, ind)
            breakpoint()
            exit(-1)

    ind += 1
    return ind, first


def evaluate_publ(expr: str) -> int:
    return evaluate(expr + ")", 0)[1]


def first():
    with open("input") as f:
        lines = f.read().split("\n")

    total = sum(map(evaluate_publ, lines))

    print(total)


def add_one_paran(expr: str) -> str:
    lst = list(expr)
    ind = 0

    for ind, el in enumerate(expr):

        if el == '*':
            found = False
            params = 0
            for ind_in, el_in in enumerate(lst[ind+1:]):

                if el_in == '(':
                    params += 1
                elif found:
                    if el_in == ')':
                        params -= 1
                    if params == 0:
                        if el_in.isnumeric() or el_in == ')':
                            lst.insert(ind + ind_in + 3, ")")
                            return "".join(lst)

                elif el_in == ')':
                    params -= 1
                    if params < 0:
                        break
                elif params == 0 and el_in == '*':
                    break
                elif params == 0 and el_in == '+':
                    lst.insert(ind + 2, "(")
                    found = True

    return expr



# Add paranthesis in all places to make sol for A suffice for B
def add_paran(expr: str) -> str:
    last = expr
    next = add_one_paran(expr)

    while len(last) != len(next):
        last = next
        next = add_one_paran(last)

    return last


def second():
    with open("input") as f:
        lines = f.read().split("\n")

    print(sum(map(evaluate_publ, map(add_paran, lines))))


second()

