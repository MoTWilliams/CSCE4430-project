use crate::map::{H, W, S, F, in_bounds, is_wall};
use crate::G_EPS;
use crate::Coord;
use crate::State;
use crate::AStarResult;
use crate::shared::{euc_distance, h, reconstruct_path, open_set_coords};

use ordered_float::NotNan;
use std::collections::{HashMap, HashSet, BinaryHeap};

fn valid_neighbors(n: Coord) -> Vec<Coord> {
    let mut valid: Vec<Coord> = Vec::new();

    // Check N, E, S, W, NE, SE, SW, NE
    let mask: [(usize,usize); 8] = [
        (n.x,n.y+1),(n.x+1,n.y),(n.x,n.y-1),(n.x-1,n.y),
        (n.x+1,n.y+1),(n.x+1,n.y-1),(n.x-1,n.y-1),(n.x-1,n.y+1)
    ];

    // Build the valid (not wall) neighbor list
    for check in mask {
        let current = Coord {x: check.0, y: check.1};

        if in_bounds(current) && !is_wall(current) {
            valid.push(current);
        }
    }

    // Return the list
    valid
}

pub fn a_star() -> Option<AStarResult> {
    // Initialize the frontier with the start node
    let mut open_set: BinaryHeap<State> = BinaryHeap::new();
    let mut seen: HashSet<Coord> = HashSet::new();  // For visualization
    let mut seq = 0_usize;
    open_set.push(
        State { 
            f: NotNan::new(h(S)).unwrap(),
            seq: seq,
            g: NotNan::new(0_f64).unwrap(),
            pos: S
        }
    );
    seen.insert(S);
    seq += 1;
    
    // came_from[n] is the coordinates of the node immediately preceding n. This
    // is initialized as an empty HashMap (key-value pairs)
    let mut came_from: HashMap<Coord,Coord> = HashMap::new();

    // Finalized nodes. No cheaper path exists from start to finished through
    // closed[n]
    let mut closed: HashSet<Coord> = HashSet::new();
    
    // Cost of the cheapest path to node n. This is an array the size of the map
    // with the start node's g initialized to 0 and the rest to infinity
    let start_index = S.x * H + S.y;
    let mut g_scores = [f64::INFINITY; H*W];
    g_scores[start_index] = f64::from(open_set.peek().unwrap().g);

    // f_scores[n] = g_scores[n] + h(n), where the heuristic h(n) is the
    // euclidean distance from n to the finish point. This is another array
    // initialized to infinity with the start node initialized to h(start)
    let mut f_scores = [f64::INFINITY; H*W];
    f_scores[start_index] = f64::from(open_set.peek().unwrap().f);

    // A* algorithm
    while open_set.len() != 0 {
        let current = open_set.pop().unwrap();
        let n = current.pos;
        let cur_idx: usize = n.x * H + n.y;

        // Skip closed nodes
        if closed.contains(&n) {continue;}

        // Discard stale frontier entries, allow a tiny epsilon for rounding
        if f64::from(current.g) > g_scores[cur_idx] + G_EPS {
            continue;
        } else {
            closed.insert(n);
        }

        // Finished when the goal is reached
        if current.pos == F {
            return Some(AStarResult {
                path: reconstruct_path(came_from, current.pos), 
                cloud: seen, 
                rim: open_set_coords(open_set, closed)
            });
        }

        // Expand node
        for neighbor in valid_neighbors(n) {
            let nei_idx: usize = neighbor.x * H + neighbor.y;
            let d = euc_distance(n, neighbor);
            let maybe_g = g_scores[cur_idx] + d;

            if maybe_g < g_scores[nei_idx] {
                // Record the new cheapest neighbor
                came_from.insert(neighbor, n);
                g_scores[nei_idx] = maybe_g;
                f_scores[nei_idx] = maybe_g + h(neighbor);

                // Add the neighbor to the frontier
                open_set.push(
                    State {
                        f: NotNan::new(f_scores[nei_idx]).unwrap(),
                        seq: seq,
                        g: NotNan::new(g_scores[nei_idx]).unwrap(),
                        pos: neighbor
                    }
                );
                seen.insert(neighbor);
                seq += 1;
            }
        }
    }

    // Return nothing if no path found
    None
}
