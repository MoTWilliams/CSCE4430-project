# pylint: disable=missing-docstring
import heapq
from map_const import H, W, S, G, in_bounds, is_wall
from custom_types import Mode, Coord, FrontierObj, Result
from shared import EPS, euc_dist, h, reconstruct_path, build_rim


def valid_neighbors(c: Coord):
    mask = (
        Coord(c.x, c.y + 1), Coord(c.x + 1, c.y), Coord(c.x, c.y - 1), Coord(c.x - 1, c.y),
        Coord(c.x + 1, c.y + 1), Coord(c.x + 1, c.y - 1),
        Coord(c.x - 1, c.y - 1), Coord(c.x - 1, c.y + 1)
    )
    return [n for n in mask if in_bounds(n) and not is_wall(n)]


def screened_neighbors(c: Coord):
    """
    Implements a relaxed screening rule inspired by
    'Path Planning of Mobile Robot Based on A* Algorithm'.
    It keeps neighbors that improve the heuristic evaluation,
    but still allows detours if no such nodes exist.
    """
    mask = (
        Coord(c.x, c.y + 1), Coord(c.x + 1, c.y), Coord(c.x, c.y - 1), Coord(c.x - 1, c.y),
        Coord(c.x + 1, c.y + 1), Coord(c.x + 1, c.y - 1),
        Coord(c.x - 1, c.y - 1), Coord(c.x - 1, c.y + 1)
    )

    hc = euc_dist(c, G)
    RELAX = .53


   # allow slight tolerance

    valid, preferred = [], []
    for n in mask:
        if in_bounds(n) and not is_wall(n):
            valid.append(n)
            hn = euc_dist(n, G)
            # accept if better heuristic OR nearly the same
            if hn <= hc + RELAX:
                preferred.append(n)

    # fallback if nothing qualified
    return preferred if preferred else valid


def a_star(mode: Mode):
    # Initialize grids as g[y][x]
    g = [[float('inf') for _ in range(W)] for _ in range(H)]
    f = [[float('inf') for _ in range(W)] for _ in range(H)]
    g[S.y][S.x] = 0
    f[S.y][S.x] = h(S)

    open_set = [FrontierObj(f[S.y][S.x], g[S.y][S.x], S)]
    heapq.heapify(open_set)
    came_from = {}
    closed = set()
    seen = {S}

    while open_set:
        current = heapq.heappop(open_set)
        c = current.pos

        if c in closed:
            continue

        closed.add(c)

        # Goal reached
        if c == G:
            result = Result()
            result.path = reconstruct_path(came_from, c)
            result.cloud = seen
            result.rim = build_rim(open_set, closed)
            return result

        # Choose expansion method
        if mode == Mode.BASIC:
            neighbors = valid_neighbors(c)
        else:
            neighbors = screened_neighbors(c)

        for n in neighbors:
            cost = euc_dist(c, n)
            candidate_g = g[c.y][c.x] + cost

            # Relaxation
            if candidate_g + EPS < g[n.y][n.x]:
                came_from[n] = c
                g[n.y][n.x] = candidate_g
                f[n.y][n.x] = candidate_g + h(n)
                heapq.heappush(open_set, FrontierObj(f[n.y][n.x], g[n.y][n.x], n))
                seen.add(n)

    # If goal was never reached
    result = Result()
    result.cloud = seen
    return result
