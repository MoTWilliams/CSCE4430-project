use a_star::Coord;
use a_star::AStarResult;
use a_star::astar_algo::a_star;
use a_star::screened_astar_algo::screened_a_star;
use a_star::map::{H, W, MAP, S, F};

use colored_text::Colorize;

fn print_result(result: Option<AStarResult>) {
    for y in (0..H).rev() {
        for x in 0..W {
            let pos = Coord {x: x, y: y};
            let cell = 
                if MAP[x][y] == 0 {"██".white()} 
                else if x == S.x && y == S.y {"██".green()} // This line
                else if x == F.x && y == F.y {"██".red()}
                else if result.as_ref().map_or(
                        false, |res| res.path.contains(&pos)) {
                    "██".bright_blue()
                }
                else if result.as_ref().map_or(
                        false, |res| res.rim.contains(&pos)) {
                    "██".bright_yellow()
                }
                else if result.as_ref().map_or(
                        false, |res| res.cloud.contains(&pos)) {
                    "██".rgb(175,175,175)
                }
                else {"██".bright_green()};
            print!("{cell}");
        }
        println!();
    }
}

fn main() {
    // Print basic A* result
    print_result(a_star());
    println!();
    print_result(screened_a_star());   
}
