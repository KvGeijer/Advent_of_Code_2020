from itertools import tee

class Rule:
    char: str
    rules: [[int]]

    def __init__(self):
        self.char = 'nothing'
        self.rules = []

    def isalpha(self):
        return self.char != 'nothing'

    def __repr__(self):
        if self.isalpha():
            return self.char
        else:
            return str(self.rules)


def parse(data: str) -> ({int: Rule}, [str]):
    [rules, messages] = data.split('\n\n')

    rules_dict = {}
    for line in rules.split("\n"):
        # splitted = list(filter('|'.__ne__, rule.split('\n')))

        rule = Rule()

        temp_list = []
        splitted = line.split(' ')
        for el in splitted[1:]:
            if el[0] == '"':
                rule.char = el[1]
            elif el != '|':
                temp_list.append(int(el))
            else:
                rule.rules.append(temp_list)
                temp_list = []

        rule.rules.append(temp_list)

        rules_dict[int(splitted[0][0:-1])] = rule

    return rules_dict, messages.split('\n')


def first():
    with open("input4") as f:
        rules_dict, messages = parse(f.read())

    valids: {int: [str]} = dict()

    def find_strs(rule_nbr: int) -> [str]:
        if rule_nbr in valids:
            return valids[rule_nbr]
        else:   # The real deal
            rule_obj = rules_dict[rule_nbr]

            if rule_obj.isalpha():
                valids[rule_nbr] = [rule_obj.char]
                return [rule_obj.char]

            # Possible for all rules
            possible = []

            for rule in rule_obj.rules:
                # Possible for this rule
                poss = [""]
                for num in rule:
                    # like poss but a temp for each num
                    temp = []
                    for option in find_strs(num):
                        for earlier in poss:
                            temp.append(earlier + option)
                    poss = temp
                possible += poss

            valids[rule_nbr] = possible
            return possible

    match0 = find_strs(0)

    sum = 0
    for message in messages:
        sum += 1 if message in match0 else 0

    # print(match0)
    print(sum)


def add_paran(text: str) -> str:
    return "(" + text + ")"


def add_brack(text: str) -> str:
    return "[" + text + "]"


def get_next(iterable):
    try:
        return iterable.__next__()
    except StopIteration:
        return "0"


def next_pair(iter1, iter2):
    one = get_next(iter1)
    two = get_next(iter2)

    if one != "0" and two != "0":
        return one, two
    elif one == "0" and two == "0":
        return "1", "1"
    else:
        return "-1", "-1"


# Takes out whatever is in the paranthesis, and then removes it x times as well as recurses back to eq
def eq_paran(iter_clean, iter_dirty) -> bool:
    paran = []
    while True:
        dirty = get_next(iter_dirty)
        if dirty == ")":
            # Has reached the end of the paranthesis
            break
        elif dirty in [".", "[", "]", "0"]:
            print("Invalid shit inside paranthesis")
            # breakpoint()

        paran.append(dirty)

    string = "".join(paran)

    # Now loop inf time till we run out of space in iter_clean or dont match, call back to eq at all times
    i = 0
    first_compl = False
    while True:
        clean = get_next(iter_clean)

        if clean == "0":
            if first_compl and get_next(iter_dirty) == "0":
                return True
            else:
                return False
        elif clean == "0":
            return False
        elif clean != string[i]:
            return False

        i += 1
        if i >= len(string):
            first_compl = True
            i = 0
            iter_dirty, dirt_copy = tee(iter_dirty)
            iter_clean, clean_copy = tee(iter_clean)
            if eq(clean_copy, dirt_copy):
                return True


def brack_snd_eq(iter_clean, iter_dirty, snd, num_loops) -> bool:
    for loop in range(num_loops):
        for char in snd:
            clean = get_next(iter_clean)

            if clean == "0":
                return False
            elif clean != char:
                return False

    return eq(iter_clean, iter_dirty)


def eq_brack(iter_clean, iter_dirty) -> bool:
    brack = []
    fst: str
    snd: str

    while True:
        dirty = get_next(iter_dirty)
        if dirty == ".":
            fst = "".join(brack)
            brack = []
        elif dirty == "]":
            snd = "".join(brack)
            break
        elif dirty in ["(", ")", "0"]:
            print("Invalid shit inside brackets")
            breakpoint()
        else:
            brack.append(dirty)

    num_loops = 0
    i = 0
    while True:
        clean = get_next(iter_clean)

        if clean == "0":
            return False
        elif clean != fst[i]:
            return False

        i += 1
        if i >= len(fst):
            i = 0
            num_loops += 1

            iter_dirty, dirt_copy = tee(iter_dirty)
            iter_clean, clean_copy = tee(iter_clean)
            if brack_snd_eq(clean_copy, dirt_copy, snd, num_loops):
                return True


# Checks if el could be match. But match can contain the wierd []().
def eq(iter_clean, iter_dirty) -> bool:

    while True:

        dirty = get_next(iter_dirty)

        if dirty == "[":
            clean1, clean2 = tee(iter_clean)
            dirt1, dirt2 = tee(iter_dirty)
            return eq_brack(clean2, dirt1) or eq(clean1, dirt2)
        elif dirty == "(":
            clean1, clean2 = tee(iter_clean)
            dirt1, dirt2 = tee(iter_dirty)
            return eq_paran(clean1, dirt1) or eq(clean2, dirt2)
        elif dirty == ")":
            dirty = get_next(iter_dirty)

        clean = get_next(iter_clean)

        if clean == dirty == "0":
            return True
        elif (clean == "0" or dirty == "0") and clean != dirty:
            # One ran out of sring
            return False
        elif clean != dirty:
            return False

            # clean == dirty, continue to next


# Just like contains but, also with special rules for ()[].
def cont_spec(el: str, lst: [str]):
    for match in lst:
        if eq(iter(el), iter(match)):
            return True
    return False


def second():
    with open("input4") as f:
        rules_dict, messages = parse(f.read())

    # rule8 = Rule()
    # rule8.rules = [[42], [42, 8]]
    # rule11 = Rule()
    # rule11.rules = [[42, 31], [42, 11, 31]]

    # rules_dict[8] = rule8
    # rules_dict[11] = rule11

    valids: {int: [str]} = dict()

    def find_strs(rule_nbr: int) -> [str]:
        if rule_nbr in valids:
            return valids[rule_nbr]
        else:   # The real deal

            if rule_nbr == 8:
                asd = True

            rule_obj = rules_dict[rule_nbr]

            if rule_obj.isalpha():
                valids[rule_nbr] = [rule_obj.char]
                return [rule_obj.char]

            # Possible for all rules
            possible = []

            for rule in rule_obj.rules:
                # Possible for this rule
                poss = [""]
                for num in rule:
                    # like poss but a temp for each num
                    temp = []
                    for option in find_strs(num):
                        for earlier in poss:
                            if rule_nbr == 11 and earlier != "":
                                # Is this really correct?
                                temp.append(earlier + '.' + option)
                            else:
                                temp.append(earlier + option)

                    poss = temp
                possible += poss

            if rule_nbr == 8:
                possible = list(map(add_paran, possible))
            elif rule_nbr == 11:
                possible = list(map(add_brack, possible))
                # possible = possible

            valids[rule_nbr] = possible
            return possible

    match0 = find_strs(0)
    # match0 = list(map(lambda x: "*" + x))

    sum = 0
    print("Starting sum")
    for ind, message in enumerate(messages):
        if cont_spec(message, match0):
            sum += 1
            print(message)
        print(ind, sum)

    # print(match0)
    print(sum)

# first()
second()

tests = False
if tests:
    print("TRUE TEST CASES")
    print(eq(iter("hej"), iter("hej")))
    print(eq(iter("hejs"), iter("hejs")))
    print(eq(iter("hejhejhej"), iter("hej(hej)")))
    print(eq(iter("hejhej"), iter("hej(hej)")))
    print(eq(iter("hejhejhej"), iter("hej(hej)hej")))
    print(eq(iter("hejhejhejhej"), iter("hej(hej)hej")))
    print(eq(iter("hejhajhajhej"), iter("hej(haj)hej")))
    print(eq(iter("abbba"), iter("a(b)a")))
    print(eq(iter("abba"), iter("a[b.b]a")))
    print(eq(iter("abbbba"), iter("a[b.b]a")))
    print(eq(iter("abbbbbba"), iter("a[b.b]a")))
    print(eq(iter("abbbacccddd"), iter("a(b)a[c.d]")))
    print(eq(iter("abaabacdccdclmmlmm"), iter("(aba)[cdc.lmm]")))
    print(eq(iter("aabb"), iter("a(b)a[c.d]")))

    print("FALSE TEST CASES")
    print(eq(iter("hejs"), iter("hej")))
    print(eq(iter("hej"), iter("hejd")))
    print(eq(iter("haj"), iter("hej")))
    print(eq(iter("hajs"), iter("hej")))
    print(eq(iter("hej"), iter("hej(hej)")))
    print(eq(iter("hejhej"), iter("hej(hej)hej")))
    print(eq(iter("abbbbba"), iter("a[b.b]a")))
    print(eq(iter("abbbbba"), iter("a[b.a]a")))
    print(eq(iter("aabb"), iter("a(b)a[c.d]")))