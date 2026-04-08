use interpreter::environment::Environment;
use interpreter::eval;
use parser::lexer::Lexer;
use parser::Parser;
use std::cell::RefCell;
use std::rc::Rc;
use std::{env, fs, process};

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <filename>", args[0]);
        process::exit(1);
    }

    let filename = &args[1];
    let source_code = match fs::read_to_string(filename) {
        Ok(code) => code,
        Err(e) => {
            eprintln!("Error reading file '{}': {}", filename, e);
            process::exit(1);
        }
    };

    let env = Rc::new(RefCell::new(Environment::default()));
    let lexer = Lexer::new(&source_code);

    let mut parser = Parser::new(lexer);

    match parser.parse_program() {
        Ok(program) => {
            println!("[Parsed Program]");
            println!("{:#?}", program);
            if let Err(e) = eval(parser::ast::Node::Program(program), &env) {
                eprintln!("[Runtime Error] {}", e);
            }
        }
        Err(errors) => {
            eprintln!("[Parse Errors]");
            for e in errors {
                eprintln!("  - {}", e);
            }
        }
    }
}
