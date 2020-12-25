
def diff(xs):
        diffs = []
        for i in range(1,len(xs)):
                diffs.append(xs[i] - xs[i-1])
        return diffs


def ones_and_threes(diffs) -> (int, int):
        (ones, threes) = (0, 0)
        for x in diffs:
                if x == 1:
                        ones += 1
                elif x == 3:
                        threes += 1
        return ones, threes

# The first problem
with open("input", 'r') as file:
        inp = [0] + sorted(map(int, file.readlines()))
        diffs = diff(inp)
        ones, threes = ones_and_threes(diffs)
        print(ones * (threes + 1))

# The second part
with open("input", 'r') as file:
        inp = [0] + sorted(map(int, file.readlines()))
        optList = [0] * (len(inp)-1) + [1]

        for i in reversed(range(len(inp)-1)):
                val = inp[i]
                comb = 0
                j = i + 1
                while j < len(inp) and inp[j] - inp[i] <= 3:
                        comb += optList[j]
                        j += 1
                optList[i] = comb

        print(optList)
