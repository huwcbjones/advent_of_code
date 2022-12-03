use std::env;
use std::process::ExitCode;

#[derive(Clone, Eq, PartialEq)]
enum Hand {
    Rock,
    Paper,
    Scissors,
}

#[derive(Eq, PartialEq)]
enum Player {
    X,
    Y,
    Z,
}

trait ScoreTrait {
    fn score(&self, other: &Hand) -> u64;
}
impl ScoreTrait for Hand {
    fn score(&self, other: &Hand) -> u64 {
        let hand = match self {
            Hand::Rock => 1,
            Hand::Paper => 2,
            Hand::Scissors => 3,
        };
        let mut score: u64 = 0;
        if self == other {
            score = 3;
        } else if match self {
            Hand::Rock => other == &Hand::Scissors,
            Hand::Scissors => other == &Hand::Paper,
            Hand::Paper => other == &Hand::Rock,
        } {
            score = 6;
        }
        hand + score
    }
}

fn main() -> ExitCode {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        println!("Usage: <input>");
        return ExitCode::FAILURE;
    }
    let lines = util::read_lines(&args[1]).unwrap();

    let games: Vec<(Hand, Player)> = lines
        .flatten()
        .map(|l| {
            let (o, y) = l.trim().split_once(' ').unwrap();
            let opponent = match o {
                "A" => Hand::Rock,
                "B" => Hand::Paper,
                "C" => Hand::Scissors,
                _ => panic!("Unknown move: {o:?}"),
            };
            let you: Player = match y {
                "X" => Player::X,
                "Y" => Player::Y,
                "Z" => Player::Z,
                _ => panic!("Unknown move: {y:?}"),
            };
            (opponent, you)
        })
        .collect();

    let part1_score: u64 = games
        .iter()
        .map(|(o, y)| {
            let you = match y {
                Player::X => Hand::Rock,
                Player::Y => Hand::Paper,
                Player::Z => Hand::Scissors,
            };
            you.score(o)
        })
        .sum();
    println!("Part 1: {}", part1_score);

    let part2_score: u64 = games
        .iter()
        .map(|(o, r)| {
            let y = match r {
                Player::X => match o {
                    // lose
                    Hand::Rock => Hand::Scissors,
                    Hand::Paper => Hand::Rock,
                    Hand::Scissors => Hand::Paper,
                },
                Player::Y => o.clone(), // draw
                Player::Z => match o {
                    // win
                    Hand::Rock => Hand::Paper,
                    Hand::Paper => Hand::Scissors,
                    Hand::Scissors => Hand::Rock,
                },
            };
            y.score(o)
        })
        .sum();
    println!("Part 2: {}", part2_score);

    ExitCode::SUCCESS
}
