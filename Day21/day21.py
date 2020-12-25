# import itertools as it
import re


def intersperse(val, sequence):
    first = True
    for item in sequence:
        if not first:
            yield val
        yield item
        first = False


def parse(text: str) -> ({str}, {str}, [({str}, {str})]):
    ingredients = set()
    allergens = set()
    recepies = []
    for line in text.split('\n'):
        first, second = re.sub(',', '', line).split("(")

        ingr = set(first[:-1].split(" "))
        aller = set(second[:-1].split(" ")[1:])

        ingredients |= ingr
        allergens |= aller
        recepies.append((ingr, aller))

    return ingredients, allergens, recepies


def parse_adv() -> ({str}, {str}, [({str}, {str})], {str: [str]}, {str}):
    with open("input") as f:
        ingredients, allergens, recepies = parse(f.read())

    # Create a dict, key= allergens, value= possible ingredients
    matches = dict()
    for (ingrs, allers) in recepies:
        for aller in allers:
            if aller not in matches:
                matches[aller] = set().union(ingrs)
            else:
                matches[aller] &= ingrs

    free_ingr = ingredients
    for not_frees in matches.values():
        free_ingr -= not_frees

    return ingredients, allergens, recepies, matches, free_ingr


def first():
    ingredients, allergens, recepies, matches, free_ingr = parse_adv()

    result = 0
    for (ingrs, _) in recepies:
        for ingr in ingrs:
            if ingr in free_ingr:
                result += 1

    print("Result of first: ", result)


def second():
    ingredients, allergens, recepies, matches, free_ingr = parse_adv()

    pairs = []

    while matches != dict():
        sort_matches = list(matches.items())
        sort_matches.sort(key=lambda x: len(x[1]))
        for (ingr, allergs) in sort_matches:
            if len(allergs) == 1:
                allerg = next(iter(allergs))
                pairs.append((ingr, allerg))

                del matches[ingr]
                for other_ingr, other_allergs in matches.copy().items():
                    if allerg in other_allergs:
                        other_allergs.remove(allerg)
                        if other_allergs == set():
                            del matches[ingr]
            elif len(allergs) == 0:
                print("Length of allergs is zero you dumwat")
                breakpoint()
            else:
                # No conclusions to be drawn. Redo and sort again...
                break

    print("Done?")

    pairs.sort(key=lambda x: x[0])

    with open("output", 'w') as f:
        f.write("".join(intersperse(',', map(lambda x: x[1], pairs))))




second()
