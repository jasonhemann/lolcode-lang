use std::io::stdin;

use lexer::Lexer;
use lexer::token::TokenKind;

pub fn main() {
    println!("Welcome to LOLCODE Lexer!");
    loop {
        let mut input = String::new();
        stdin().read_line(&mut input).expect("Invalid input");

        let mut lexer = Lexer::new(&input);
        loop {
            let token = lexer.next_token();
            if token.kind == TokenKind::EOF {
                break;
            }
        }
    }
}
