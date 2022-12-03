use std::collections::HashSet;
use std::env;
use std::process::ExitCode;

fn priority(c: &char) -> u32 {
    let offset = match c.is_uppercase() {
        true => 64 - 26,
        false => 96,
    };
    (*c as u32) - offset
}

fn main() -> ExitCode {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        println!("Usage: <input>");
        return ExitCode::FAILURE;
    }
    let lines = util::read_lines(&args[1]).unwrap();
    let backpacks: Vec<Vec<char>> = lines
        .flatten()
        .map(|l| l.trim().chars().collect())
        .collect();

    let part1_score: u32 = backpacks
        .iter()
        .map(|b| {
            let (left, right) = b.split_at(b.len() / 2);
            let compartment1: HashSet<_> = HashSet::from_iter(left);
            let compartment2: HashSet<_> = HashSet::from_iter(right);
            compartment1
                .intersection(&compartment2)
                .map(|c| priority(c))
                .sum::<u32>()
        })
        .sum();
    println!("Part 1: {part1_score}");

    let part2_score: u32 = backpacks
        .chunks(3)
        .map(|rs| {
            rs.iter()
                .map(|b| HashSet::from_iter(b.iter()))
                .reduce(|s: HashSet<&char>, x| HashSet::from_iter(s.intersection(&x).copied()))
                .unwrap()
                .into_iter()
                .map(priority)
                .sum::<u32>()
        })
        .sum();
    println!("Part 2: {part2_score}");
    ExitCode::SUCCESS
}
