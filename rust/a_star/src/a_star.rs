use std::collections::HashMap;

fn euc_distance(s:(u32,u32), d:(u32,u32)) -> f64 {
    ((((s.0-d.0)*(s.0-d.0)) + ((s.1-d.1)*(s.1-d.1))) as f64).sqrt()
}

fn reconstruct_path(
        came_from:HashMap<(u32,u32),(u32,u32)>, mut current:(u32,u32)) 
        -> Vec::<(u32,u32)>{
    let mut total_path = Vec::<(u32,u32)>::new();

    while came_from.contains_key(&current) {
        current = came_from[&current];
        total_path.insert(0, current);
    }

    total_path
}

pub fn a_star() {
    println!("A*");
}