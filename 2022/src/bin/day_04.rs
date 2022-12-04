use std::collections::HashSet;
use std::env;
use std::process::ExitCode;

fn main() -> ExitCode {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        println!("Usage: <input>");
        return ExitCode::FAILURE;
    }
    let lines = util::read_lines(&args[1]).unwrap();

    let pairs: Vec<(HashSet<u64>, HashSet<u64>)> = lines
        .flatten()
        .map(|l| {
            let line = l.trim();
            let (l, r) = line.split_once(',').unwrap();
            let (ll, lu) = l.split_once('-').unwrap();
            let (rl, ru) = r.split_once('-').unwrap();
            let (ll, lu): (u64, u64) = (ll.parse().unwrap(), lu.parse().unwrap());
            let (rl, ru): (u64, u64) = (rl.parse().unwrap(), ru.parse().unwrap());
            (
                HashSet::from_iter(ll..lu + 1),
                HashSet::from_iter(rl..ru + 1),
            )
        })
        .collect();

    let part1 = pairs
        .iter()
        .filter(|(l, r)| l.is_subset(r) || r.is_subset(l))
        .count();
    println!("Part 1: {part1}");

    let part2 = pairs.iter().filter(|(l, r)| !l.is_disjoint(r)).count();
    println!("Part 2: {part2}");
    ExitCode::SUCCESS
}
