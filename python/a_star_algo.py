# pylint: disable=missing-docstring
import heapq

from map_const import H, W, S, G, in_bounds, is_wall
from custom_types import Coord, FrontierObj, Result
from shared import EPS, euc_dist, h, reconstruct_path, build_rim

def valid_neighbors(c: Coord):
    # N, E, S, W, NE, SE, SW, NE
    mask = (Coord(c.x,c.y+1), Coord(c.x+1,c.y), Coord(c.x,c.y-1),
            Coord(c.x-1,c.y), Coord(c.x+1,c.y+1), Coord(c.x+1,c.y-1),
            Coord(c.x-1,c.y-1), Coord(c.x-1,c.y+1))

    not_walls = []

    for check in mask:
        if in_bounds(check) and not is_wall(check):
            not_walls.append(check)

    return not_walls

def a_star():
    # g[n] is the cheapest path from start to node n. This is an array the size
    # of the map with g[start] initialized to 0 and the rest to infinity.
    g = [[float('inf') for _ in range(H)] for _ in range(W)]
    g[S.x][S.y] = 0

    # f[n] = g[n] + h(n), where heuristic h(n) is the euclidean distance from n
    # to the goal. This is also an array the size of the map initialized to
    # infinity with f[start] = h(start)
    f = [[float('inf') for _ in range(H)] for _ in range(W)]
    f[S.x][S.y] = h(S)

    # Discovered nodes, sorted by f-score, then order added, then g-score
    seq = 0
    open_set = [FrontierObj(f[S.x][S.y], seq, g[S.x][S.y], S)]
    heapq.heapify(open_set)

    # Pairs of coordinates and their cheapest predecessors
    came_from = {}

    # Finalized nodes. No cheaper paths exist through closed[n] to goal
    closed = set()

    # All nodes touched or seen
    seen = set()
    seen.add(S)

    # A* algorithm. Find the cheapest path
    while len(open_set) > 0:
        current = heapq.heappop(open_set)
        c = current.pos

        # Skip closed nodes
        if c in closed:
            continue

        # Discard stale frontier entries, allow a tiny epsilon for rounding
        if current.g > g[c.x][c.y] + EPS :
            continue
        else:
            closed.add(c)

        # Finished when the goal is reached
        if c == G:
            result = Result()
            result.path = reconstruct_path(came_from, c)
            result.cloud = seen
            result.rim = build_rim(open_set, closed)
            return result

        # Expand node
        for n in valid_neighbors(c):
            # g[current] + d(current)
            candidate_g = g[c.x][c.y] + euc_dist(c,n)

            if candidate_g < g[n.x][n.y]:
                # Record the new cheapest neighbor
                came_from[n] = c
                g[n.x][n.y] = candidate_g
                f[n.x][n.y] = candidate_g + h(n)

                # Add the neighbor to the open set
                seq += 1
                heapq.heappush(
                    open_set, FrontierObj(f[n.x][n.y], seq, g[n.x][n.y], n))
                seen.add(n)

    # Return nothing if no path found
    return Result()
