use std::env;
use std::fs;
use std::{thread, time};

struct BrainfuckMemory {
    data: Vec::<u8>,
    pointer: usize,
}

/// Returns memory content if it's in range, 0 otherwise
impl std::ops::Index<usize> for BrainfuckMemory {
    type Output = u8;

    fn index(&self, index: usize) -> &u8 {
        if self.data.len() <= index {
            // Out of range, return default cell value
            &0
        }
        else {
            // Return requested value
            &self.data[index]
        }
    }
}

/// If the requested memory location is out of range, grow the memory
impl std::ops::IndexMut<usize> for BrainfuckMemory {
    fn index_mut(&mut self, index: usize) -> &mut u8 {
        while self.data.len() <= index {
            // Out of range, we need to grow the vector
            self.data.push(0)
        }
        &mut self.data[index]
    }
}

/// Shifts the memory pointer by an offset
fn shift(memory: &mut BrainfuckMemory, offset: isize) {
    memory.pointer = memory.pointer.wrapping_add(offset as usize);
    while memory.data.len() <= memory.pointer {
        memory.data.push(0)
    }
}

/// Adds a value to the cell the memory pointer is pointing at
fn add(memory: &mut BrainfuckMemory, value: i8) {
    let idx = memory.pointer;
    memory[idx] = memory[idx].wrapping_add(value as u8);
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let code = fs::read_to_string(&args[1]).expect("Couldn't open input file");
    let program: Vec<char> = code.chars().collect();

    /// Instruction pointer
    let mut ip = 0;

    let mut memory = BrainfuckMemory{ data:Vec::<u8>::with_capacity(50), pointer: 0 };

    let mut cycle_count = 0;

    while ip < program.len() {
        println!("{}", program[ip]);
        match program[ip] {
            '+' => { add(&mut memory, 1) },
            '-' => { add(&mut memory, -1) },
            '>' => { shift(&mut memory, 1) }
            '<' => { shift(&mut memory, -1) }
            '[' => {
                if memory[memory.pointer] == 0 {
                    // Jump to matching bracket
                    let mut depth = 0;
                    while ip < program.len() {
                        match program[ip] {
                            '[' => { depth += 1 },
                            ']' => { depth -= 1 },
                             _  => {},
                        }
                        if depth == 0 {
                            break
                        }
                        ip += 1;
                    }}
                }
            ']' => {
                if memory[memory.pointer] != 0 {
                    // Jump to matching bracket
                    let mut depth = 0;
                    while ip > 0 {
                        match program[ip] {
                            '[' => { depth -= 1 },
                            ']' => { depth += 1 },
                             _  => {},
                        }
                        if depth == 0 {
                            break
                        }
                        ip -= 1;
                    }}
                }
            _ => { ip += 1; continue }
        }

        //TODO: Make sleeping a CLI option
        let sleep_duration = time::Duration::from_millis(10);
        thread::sleep(sleep_duration);

        // step instruction pointer forward
        ip += 1;
        cycle_count += 1;

        // Dump memory
        for i in 0..memory.data.len() {
            print!("{:3} ", memory.data[i])
        }
        // Visualize memory pointer location
        println!("\n{0:>1$}", ind="^", width=memory.pointer * 4 + 3);

        // Dump program code and highlight next instruction
        println!("{} {} {}", &code[..ip], program[ip], &code[ip + 1..]);
    }
    println!("Total cycles: {}, Program length: {}", cycle_count, program.len())
}

