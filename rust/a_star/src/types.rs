use ordered_float::NotNan;
use std::{cmp::Ordering, collections::{HashSet}};

// Neatly contain (x,y) coordinates
#[derive(Copy, Clone, Debug, Eq, PartialEq, Hash)]
pub struct Coord {pub x: usize, pub y: usize}

impl Coord {
    pub fn new(x: usize, y: usize) -> Self {
        Self {x: x, y: y}
    }
}

// This is the object that gets pushed into the priority queue
#[derive(Copy, Clone, Eq, PartialEq)]
pub struct State {
    pub f: NotNan<f64>,
    pub seq: usize,
    pub g: NotNan<f64>,
    pub pos: Coord,
}

// BinaryHeap is a max-heap by default, so we must re-define (implement) State's
// Ord and PartialOrd traits to make it a min-heap, as well specifying to use
// order pushed (seq) as tie-breaker. This is similar to operator overloading
// in C++.


impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        other.f.cmp(&self.f).then_with(|| self.seq.cmp(&other.seq))
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

// Tiny epsilon for comparing g-scores
pub const G_EPS: f64 = 1e-12;

// Package the path and cloud for visualization
pub struct AStarResult {
    pub path: Vec<Coord>,
    pub cloud: HashSet<Coord>,
    pub rim: HashSet<Coord>
}
