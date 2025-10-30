"""
This module implements the A* algorithm itself, as well as the standard and 
screened node expansion
"""
import heapq
from map_const import H, W, S, G, in_bounds, is_wall
from custom_types import Mode, Coord, FrontierObj, Result
from shared import EPS, euc_dist, h, reconstruct_path, build_rim


def valid_neighbors(c: Coord):
    """ 
    Checks the current cell's neighbors in the order N, E, S, W, NE, SE, SW, NW 
    and returns a list of neighbor cells that are all in-bounds and not 
    obstacles.
    """
    mask = (
        Coord(c.x, c.y + 1), Coord(c.x + 1, c.y),
        Coord(c.x, c.y - 1), Coord(c.x - 1, c.y),
        Coord(c.x + 1, c.y + 1), Coord(c.x + 1, c.y - 1),
        Coord(c.x - 1, c.y - 1), Coord(c.x - 1, c.y + 1)
    )
    return [n for n in mask if in_bounds(n) and not is_wall(n)]


def screened_neighbors(c: Coord):
    """
    Implements a relaxed screening rule inspired by 'Path Planning of Mobile 
    Robot Based on A* Algorithm'. It checks neighbors in the order N, E, S, W, 
    NE, SE, SW, NW and keeps neighbors that improve the heuristic evaluation,
    but still allows detours if no such nodes exist.
    """
    mask = (
        Coord(c.x, c.y + 1), Coord(c.x + 1, c.y), 
        Coord(c.x, c.y - 1), Coord(c.x - 1, c.y),
        Coord(c.x + 1, c.y + 1), Coord(c.x + 1, c.y - 1),
        Coord(c.x - 1, c.y - 1), Coord(c.x - 1, c.y + 1)
    )

    # Prefer nodes that are closer to goal than the current node. Allow slight
    # tolerance in case no valid neighbors move toward the goal.
    hc = euc_dist(c, G)
    RELAX = .53         # allow slight tolerance

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
    """
    This function implements a standard A* path-finding algorithm using 
    euclidean distance to the goal as the heuristic and 8-direction movement. 
    The parameter `mode` can be either BASIC, which expands the search to all 
    valid neighbor nodes, or SCREENED, which discards neighbors that aren't 
    closer to the goal than the current node, within a small tollerance. 

    The resulting path and search cloud are returned as a Result object with 
    members path, rim, and cloud, used by the main function to visualize the
    results.
    """

    # g[][] and f[][] are both arrays the size of map, initialized to infinity.

    # g[n] is the cost of the cheapest known path from start to n, with g[start]
    # initialized to 0.
    g = [[float('inf') for _ in range(W)] for _ in range(H)]
    g[S.y][S.x] = 0

    # f[n] is the estimated total cost of the cheapest known path from start to
    # goal through n, calculated as f[n] = g[n] + h(n), where heuristic h(n) is
    # the euclidean distance from n to goal. f[start] is initialized to h(start)

    # MODIFIED FOR ALGO COMPARISON--f[n] is just the cost of the current path,
    # calculated differently for each algorithm
    f = [[float('inf') for _ in range(W)] for _ in range(H)]
    f[S.y][S.x] = h(S)

    # Discovered nodes sorted in ascending order by f-score. Use of a min-heap
    # here allows search in O(log n) time
    open_set = [FrontierObj(f[S.y][S.x], g[S.y][S.x], S)]
    heapq.heapify(open_set)

    # came_from[n] is the node immediately preceding n on the cheapest known
    # path from start to n
    came_from = {}

    # Finalized nodes. No cheaper paths exist through closed[n] to goal
    closed = set()

    # All nodes seen or visited
    seen = {S}

    # A* algorithm to find the cheapest path from start to goal
    while open_set:
        current = heapq.heappop(open_set)
        c = current.pos

        # Skip closed nodes
        if c in closed:
            continue

        closed.add(c)

        # Goal reached
        if c == G:
            result = Result(mode)
            result.path = reconstruct_path(came_from, c)
            result.cloud = seen
            result.rim = build_rim(open_set, closed)
            return result

        # Choose expansion method
        neighbors = screened_neighbors(c) if mode == Mode.SCREENED \
            else valid_neighbors(c)

        # Expand the current node
        for n in neighbors:
            cost = euc_dist(c, n)
            candidate_g = g[c.y][c.x] + cost

            # Relaxation
            if candidate_g + EPS < g[n.y][n.x]:
                came_from[n] = c
                g[n.y][n.x] = candidate_g
                # This line modified for comparison
                f[n.y][n.x] = candidate_g if mode == Mode.UNIFORM \
                    else h(n) if mode == Mode.GREEDY else candidate_g + h(n)
                heapq.heappush(
                    open_set, FrontierObj(f[n.y][n.x], g[n.y][n.x], n)
                )
                seen.add(n)

    # If goal was never reached
    result = Result(mode)
    result.cloud = seen
    return result
