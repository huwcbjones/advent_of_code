use std::{env, io};
use std::fs::File;
use std::io::BufRead;
use std::path::Path;
use std::process::ExitCode;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
    where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn main() -> ExitCode {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        println!("Usage: <input>");
        return ExitCode::FAILURE;
    }
    let file = read_lines(&args[1]).unwrap();
    let mut running_total: u64 = 0;
    let mut calories: Vec<u64> = Vec::new();
    for line in file {
        if let Ok(ip) = line {
            let entry = ip.trim();
            if entry == "" {
                calories.push(running_total);
                running_total = 0;
                continue
            }
            let calorie: u64 = entry.parse().unwrap();
            running_total += calorie;
        }
    }
    calories.sort_unstable_by(|a, b| b.partial_cmp(a).unwrap());
    assert!(calories.len() > 3);
    println!("Part 1: {}", calories[0]);
    println!("Part 2: {}", calories[0] + calories[1] + calories[2]);
    return ExitCode::SUCCESS;
}
