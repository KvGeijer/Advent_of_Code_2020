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


def second():
    with open("input") as f:
        rules_dict, messages = parse(f.read())

    valids: {int: [str]} = dict()

    def find_strs(rule_nbr: int) -> [str]:
        if rule_nbr in valids:
            return valids[rule_nbr]
        else:  # The real deal
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

    # To generate everything needed
    find_strs(0)

    valid_dict = {key: set(lst) for (key, lst) in valids.items()}

    # They all have the same length!!
    length = max(map(len, valids[31]))

    # How many times can it match 31 from the right? How many match 42 from left? Can it work?
    def match0(message: str) -> bool:
        if len(message) % length != 0:
            return False

        match_left: int = 0
        match_right: int = 0

        # How many times match 42 from left?
        for match_left in range(len(message)//length):
            start = length * match_left
            end = start + length
            if message[start:end] not in valid_dict[42]:
                break

        # How many times can it match 31 from the right?
        for match_right in range(len(message)//length):
            start = len(message) - (length * (match_right + 1))
            end = start + length
            if message[start:end] not in valid_dict[31]:
                break

        if match_left + match_right >= len(message)//length and \
                match_left > match_right:
            return True
        else:
            return False

    result = 0
    for i, message in enumerate(messages):
        if match0(message):
            result += 1
            print(i, True, message)
        else:
            print(i, False, message)
    # summ = sum(map(match0, messages))
    # print(summ)
    print()
    print("Result: ", result)

second()