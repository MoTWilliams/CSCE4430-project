use crate::map::F;   // Finish coords
use crate::Coord;
use crate::State;
use std::collections::{HashMap, HashSet, BinaryHeap};

pub fn euc_distance(s:Coord, d:Coord) -> f64 {
    let dx = s.x as f64 - d.x as f64;
    let dy = s.y as f64 - d.y as f64;
    dx.hypot(dy)    // same as √((x0-x1)^2 + (y0-y1)^2)
}

pub fn h(n: Coord) -> f64 {
    euc_distance(n, F)
}

pub fn reconstruct_path(
        came_from:HashMap<Coord,Coord>, mut current:Coord) 
        -> Vec<Coord> {
    let mut total_path: Vec<Coord> = Vec::new();
    total_path.insert(0, current);

    while came_from.contains_key(&current) {
        current = came_from[&current];
        total_path.insert(0, current); // Prepend
    }

    total_path
}

pub fn open_set_coords(open_set: BinaryHeap<State>, closed: HashSet<Coord>) -> HashSet<Coord> {
    let mut coords: HashSet<Coord> = HashSet::new();

    for state in open_set {
        if !closed.contains(&state.pos) {
            coords.insert(state.pos);
        }
    }

    coords
}