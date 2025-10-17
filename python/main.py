# pylint: disable=missing-docstring

from termcolor import colored as cd

from a_star_algo import a_star
from map_const import W, H, S, G, is_wall
from custom_types import Mode, Coord, Result
from shared import euc_dist  # for path length calc


def print_result(res: Result):
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


def path_length(path):
    return sum(euc_dist(path[i-1], path[i]) for i in range(1, len(path))) if len(path) >= 2 else 0.0


def print_metrics(name: str, res: Result):
    print(
        f"\n{name:<7}| nodes explored = {len(res.cloud)} | "
        f"path steps = {len(res.path)} | path length = {path_length(res.path):.2f}"
    )
    if not res.path:
        print(cd(f"{name} WARNING: No path found.", "red"))


print()


# --- BASIC ---
res_basic = a_star(Mode.BASIC)
print_result(res_basic)
print_metrics("BASIC", res_basic)


# --- SCREENED ---
res_screen = a_star(Mode.SCREENED)
print_result(res_screen)
print_metrics("SCREEN", res_screen)

# --- Comparison ---
if len(res_basic.cloud) > 0 and len(res_screen.cloud) > 0:
    reduction = (len(res_basic.cloud) - len(res_screen.cloud)) / len(res_basic.cloud) * 100
    print(f"\nReduction in explored nodes (SCREEN vs BASIC): {reduction:.2f}%  (paper ≈ 13.18%)")
