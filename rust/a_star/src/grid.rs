use crate::Coord;
use crate::map::{in_bounds, is_wall};

pub fn euc_distance(s:Coord, d:Coord) -> f64 {
    let dx = s.x as f64 - d.x as f64;
    let dy = s.y as f64 - d.y as f64;
    dx.hypot(dy)    // same as √((x0-x1)^2 + (y0-y1)^2)
}

pub fn valid_neighbors(n: Coord) -> Vec<Coord> {
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
