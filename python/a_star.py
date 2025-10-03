"""Module for the basic A* algorithm"""
from math import sqrt
import heapq

def valid_neighbors(curr_cell, world):
    """Get the list of neighboring cells that are not wall"""
    x = curr_cell[0]
    y = curr_cell[1]

    valid = []

    mask = ((x-1,y+1),( x ,y+1),(x+1,y+1),
            (x-1, y ),          (x+1, y ),
            (x-1,y-1),( x ,y-1),(x+1,y-1))

    for check in mask:
        if check[0] >= 0 and check[0] < len(world) \
                and check[1] >= 0 and check[1] < len(world[0]) \
                and world[check[0]][check[1]] != 0:
            valid.append((check[0],check[1]))

    return valid


def reconstruct_path(came_from, current):
    """Build the path"""
    path = [current]
    while current in came_from.keys():
        current = came_from[current]
        path.insert(0, current)
    return path

def reconstruct_frontier(frontier):
    """Build the dark outer rim of the searched cloud"""
    rim = set()

    for item in frontier:
        if not item[3] in rim:
            rim.add(item[3])
    
    return rim

def distance(x0, y0, x1, y1):
    """Euclidean distance between two nodes"""
    return sqrt((x0 - x1)*(x0 - x1) + (y0 - y1)*(y0 - y1))

def a_star(x0, y0, x1, y1, world):
    """A* algorithm"""
    # Cost of the cheapest path to node n
    g_scores = [
        [float('inf') for _ in range(len(world[0]))] for _ in range(len(world))
    ]
    g_scores[x0][y0] = 0      # Cost from start to start is 0

    # Guess at cost of path from start to finish, through current
    # f(n) = g(n) + h(n)
    f_scores = [
        [float('inf') for _ in range(len(world[0]))] for _ in range(len(world))
    ]
    h = distance(x0,y0,x1,y1)
    f_scores[x0][y0] = h

    # Discovered nodes, sorted by f-score, then h(n), then g-score
    seq = 0                 # Record order points are added to the frontier
    frontier = [(f_scores[x0][y0], seq, g_scores[x0][y0], (x0,y0))]
    heapq.heapify(frontier)

    came_from = {}          # Path to current node
    closed = set()          # Finalized nodes (no cheaper paths exist)

    # Calculate the path
    while len(frontier) > 0:
        curr_from_frontier = heapq.heappop(frontier)
        current = curr_from_frontier[3]

        # Skip closed nodes
        if (current[0],current[1]) in closed:
            continue

        # Skip stale frontier entries, allow a tiny epsilon for rounding
        g_popped = curr_from_frontier[2]
        if g_popped > g_scores[current[0]][current[1]] + 1e-12:
            continue
        else:
            closed.add((current[0],current[1]))

        # Finished then the goal is reached
        if current == (x1,y1):
            return { "path": reconstruct_path(came_from, current),
                     "cloud": closed,
                     "rim": reconstruct_frontier(frontier)
                    }

        for neighbor in valid_neighbors(current, world):
            d = distance(current[0],current[1],neighbor[0],neighbor[1])
            temp_g = g_scores[current[0]][current[1]] + d
            if temp_g < g_scores[neighbor[0]][neighbor[1]]:
                # Record the new cheapest neighbor
                came_from[(neighbor[0],neighbor[1])] = (current[0],current[1])
                g_neighbor = temp_g
                g_scores[neighbor[0]][neighbor[1]] = g_neighbor
                h_neighbor = distance(neighbor[0],neighbor[1],x1,y1)
                f_neighbor = g_neighbor + h_neighbor
                f_scores[neighbor[0]][neighbor[1]] = f_neighbor
                seq += 1
                heapq.heappush(
                    frontier, (f_neighbor, seq, g_neighbor,
                               (neighbor[0],neighbor[1]))
                )

    # Failed to find a path
    return None
