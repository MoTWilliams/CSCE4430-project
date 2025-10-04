use a_star::Coord;
use a_star::astar_algo::a_star;
use a_star::map::{H, W, MAP, S, F};

fn main() {
    let found_path: Option<Vec<Coord>> = a_star();

    // Print the map
    for y in (0..H).rev() {
        for x in 0..W {
            let pos = Coord {x: x, y: y};
            let cell = 
                if MAP[x][y] == 0 {"██"} 
                else if x == S.x && y == S.y {"SS"}
                else if x == F.x && y == F.y {"FF"}
                else if found_path.as_ref().map_or(
                    false, |path| path.contains(&pos)) {"[]"}
                else {".."};
            print!("{cell}");
        }
        println!();
    }
}
