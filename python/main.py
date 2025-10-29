# pylint: disable=missing-docstring

from termcolor import colored as cd

from a_star_algo import a_star
from map_const import W, H, S, G, is_wall
from custom_types import Mode, Coord, Result
from shared import euc_dist  # for path length calc

def path_length(path):
    return sum(euc_dist(path[i-1], path[i]) for i in range(1, len(path))) \
        if len(path) >= 2 else 0.0

def print_2results(r1: Result, r2: Result):
    gap = 8
    title1 = r1.mode.value["label"].center(2*W," ")
    title2 = r2.mode.value["label"].center(2*W," ")
    print(title1 + " "*2*gap + title2)
    for y in reversed(range(H)):
        for x in range(W + gap + W + 1):
            # Blank space between displays
            if x > W and x <= W + gap:
                print("  ",end="")
            # Left
            if x < W:
                c = Coord(x, y)
                if is_wall(c):
                    print("██", end="")
                elif c == S:
                    print(cd("██", "green"), end="")
                elif c == G:
                    print(cd("██", "red"), end="")
                elif c in r1.path:
                    print(cd("██", "blue"), end="")
                elif c in r1.rim:
                    print(cd("██", "light_yellow"), end="")
                elif c in r1.cloud:
                    print(cd("██", "light_blue"), end="")
                else:
                    print(cd("██", "light_green"), end="")
            # Right
            if x > W + gap:
                c = Coord(x-gap-1-W,y)
                if is_wall(c):
                    print("██", end="")
                elif c == S:
                    print(cd("██", "green"), end="")
                elif c == G:
                    print(cd("██", "red"), end="")
                elif c in r2.path:
                    print(cd("██", "blue"), end="")
                elif c in r2.rim:
                    print(cd("██", "light_yellow"), end="")
                elif c in r2.cloud:
                    print(cd("██", "light_blue"), end="")
                else:
                    print(cd("██", "light_green"), end="")
        print()
    print()

def tabulate(result_list: list[Result]):
    rule = "+"+"-"*19+"+"+"-"*31+"+"+"-"*14+"+"+"-"*14+"+"+"-"*14+"+"
    rule = rule.center(16+4*W," ")

    labels = "|" + "Algorithm".center(19," ") + "|"
    labels += "cost function f(n)".center(31," ") + "|"
    labels += "Nodes Explored".center(14," ") + "|"
    labels += "Path Steps".center(14," ") + "|"
    labels += "Path Length".center(14," ") + "|"
    labels = labels.center(16+4*W," ")

    print(rule + "\n" + labels + "\n" + rule)

    for r in result_list:
        res = "|" + r.mode.value["label"].ljust(19," ") + "|"
        res += r.mode.value["cost function"].center(31," ") + "|"

        if not r.path:
            res += "Path not found".center(44," ") + "|"
        else:
            res += f"{len(r.cloud)}".rjust(14," ") + "|"
            res += f"{len(r.path)}".rjust(14," ") + "|"
            res += f"{path_length(r.path):.2f}".rjust(14," ") + "|"

        res = res.center(16+4*W," ")

        print(res + "\n" + rule)
    print()

def print_1result(res: Result):
    print(res.mode.value["label"].center(W," "))
    for y in reversed(range(H)):
        for x in range(W):
            c = Coord(x, y)
            if is_wall(c):
                print(cd("██", "white"), end="")
            elif c == S:
                print(cd("██", "green"), end="")
            elif c == G:
                print(cd("██", "red"), end="")
            elif c in res.path:
                print(cd("██", "light_blue"), end="")
            elif c in res.rim:
                print(cd("██", "light_yellow"), end="")
            elif c in res.cloud:
                print(cd("██", "dark_grey"), end="")
            else:
                print(cd("██", "light_green"), end="")
        print()



print("\nLegend: ██ = obstacle, ",end="")
print(cd("██", "green") + " = start, " + cd("██", "red") + " = goal, ",end="")
print(cd("██", "blue") + " = path, ",end="")
print(cd("██", "light_yellow") + " = seen, ",end="")
print(cd("██", "light_blue") + " = visited, ",end="")
print(cd("██", "light_green") + " = untouched\n")

results = []
for mode in Mode:
    results.append(a_star(mode))

for i in range(0, len(results), 2):
    if i+1 < len(results):
        print_2results(results[i],results[i+1])
    else:
        print_1result(results[i])

tabulate(results)

# # --- Comparison ---
# if len(results[0].cloud) > 0 and len(results[1].cloud) > 0:
#     reduction = (len(results[0].cloud) - len(results[1].cloud)) / \
#         len(results[0].cloud) * 100
#     print(f"Reduction in explored nodes (Screened vs Basic): {reduction:.2f}% "
#           f" (paper ≈ 13.18%)\n")
