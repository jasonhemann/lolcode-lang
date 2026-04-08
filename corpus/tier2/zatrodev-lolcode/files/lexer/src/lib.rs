use std::{
    fmt,
    iter::{self},
    mem::replace,
};

use crate::token::{Span, Token, TokenKind};

mod test;
pub mod token;

pub struct Lexer<'a> {
    words: Box<dyn Iterator<Item = &'a str> + 'a>,
    pub current: Option<&'a str>,
    previous: Option<&'a str>,
    peek: Option<&'a str>,
    position: usize,
}

enum Number {
    Integer(i64),
    Float(f64),
}

impl fmt::Display for Number {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Number::Integer(i) => write!(f, "{}", i),
            Number::Float(fl) => write!(f, "{}", fl),
        }
    }
}

impl<'a> Lexer<'a> {
    pub fn new(input: &'a str) -> Self {
        const NEWLINE_MARKER: &str = "\n";
        let iter = input.lines().flat_map(move |line| {
            line.split(|c| c == ' ' || c == '\t')
                .chain(iter::once(NEWLINE_MARKER))
        });

        let mut words = Box::new(iter);

        let current = words.next();
        let peek = words.next();

        let l = Lexer {
            words: words,
            current,
            peek,
            previous: None,
            position: 0,
        };

        return l;
    }

    fn advance(&mut self) {
        self.position += 1;
        self.previous = self.current;
        self.current = self.peek;
        self.peek = self.words.next();
    }

    pub fn prepend_items(&mut self, new_items: Vec<&'a str>) {
        let remaining_iter = replace(&mut self.words, Box::new(iter::empty()));

        let new_iter = new_items.into_iter();
        let combined_iter = new_iter.chain(remaining_iter);

        self.words = Box::new(combined_iter);

        self.current = self.words.next();
        self.peek = self.words.next();
    }

    pub fn next_token(&mut self) -> Token {
        loop {
            let mut skipped_content = false;

            if self.skip_whitespace() {
                skipped_content = true;
            }

            if self.skip_comments() {
                skipped_content = true;
            }

            if !skipped_content {
                break;
            }
        }

        let start_position = self.position;

        let t = match self.current {
            Some(str) => {
                match str {
                    // Start-end
                    "HAI" => self.simple_token(TokenKind::HAI, 3),
                    "KTHXBYE" => self.simple_token(TokenKind::KTHXBYE, 7),

                    // Variable-declaring block
                    "WAZZUP" => self.simple_token(TokenKind::WAZZUP, 6),
                    "BUHBYE" => self.simple_token(TokenKind::BUHBYE, 6),

                    // Declaring variables
                    "ITZ" => self.simple_token(TokenKind::ITZ, 3),
                    // "I IZ" is for function calling
                    "I" => self.match_multi_word(
                        "I",
                        &[("HAS A", TokenKind::IHasA, 2), ("IZ", TokenKind::IIz, 1)],
                    ),

                    // Types
                    "NUMBR" => self.simple_token(TokenKind::TYPENUMBR, 5),
                    "NUMBAR" => self.simple_token(TokenKind::TYPENUMBAR, 6),
                    "YARN" => self.simple_token(TokenKind::TYPEYARN, 4),
                    "TROOF" => self.simple_token(TokenKind::TYPETROOF, 5),
                    "NOOB" => self.simple_token(TokenKind::NOOB, 4),
                    "WIN" => self.simple_token(TokenKind::TROOF(true), 3),
                    "FAIL" => self.simple_token(TokenKind::TROOF(false), 4),
                    "IT" => self.simple_token(TokenKind::IT, 2),

                    // IO
                    "VISIBLE" => self.simple_token(TokenKind::VISIBLE, 7),
                    "GIMMEH" => self.simple_token(TokenKind::GIMMEH, 6),
                    "+" => self.simple_token(TokenKind::PLUS, 1),

                    // Mathematical operations
                    "SUM" => self.match_full_keyword("SUM OF", TokenKind::SUM, 1),
                    "DIFF" => self.match_full_keyword("DIFF OF", TokenKind::DIFF, 1),
                    "PRODUKT" => self.match_full_keyword("PRODUKT OF", TokenKind::PRODUKT, 1),
                    "QUOSHUNT" => self.match_full_keyword("QUOSHUNT OF", TokenKind::QUOSHUNT, 1),
                    "MOD" => self.match_full_keyword("MOD OF", TokenKind::MOD, 1),
                    "BIGGR" => self.match_full_keyword("BIGGR OF", TokenKind::BIGGR, 1),
                    "SMALLR" => self.match_full_keyword("SMALLR OF", TokenKind::SMALLR, 1),

                    // Concatenation
                    "SMOOSH" => self.simple_token(TokenKind::SMOOSH, 6),

                    // Boolean operations
                    "NOT" => self.simple_token(TokenKind::NOT, 3),
                    "EITHER" => self.match_full_keyword("EITHER OF", TokenKind::EitherOf, 1),
                    "WON" => self.match_full_keyword("WON OF", TokenKind::WonOf, 1),
                    "ALL" => self.match_full_keyword("ALL OF", TokenKind::AllOf, 1),
                    "ANY" => self.match_full_keyword("ANY OF", TokenKind::AnyOf, 1),
                    "BOTH" => self.match_multi_word(
                        "BOTH",
                        &[
                            // Comparison operation
                            ("SAEM", TokenKind::BothSaem, 1),
                            ("OF", TokenKind::BothOf, 1),
                        ],
                    ),

                    // Comparison operation
                    "DIFFRINT" => self.simple_token(TokenKind::DIFFRINT, 8),

                    // Typecasting
                    "IS" => self.match_full_keyword("IS NOW A", TokenKind::IsNowA, 2),
                    "MAEK" => self.simple_token(TokenKind::MAEK, 4),

                    // Re-assignments
                    "R" => self.simple_token(TokenKind::R, 1),

                    // If-then
                    "O" => self.match_full_keyword("O RLY?", TokenKind::ORly, 1),
                    "YA" => self.match_full_keyword("YA RLY", TokenKind::YaRly, 1),
                    "MEBBE" => self.simple_token(TokenKind::Mebbe, 5),
                    "NO" => self.match_full_keyword("NO WAI", TokenKind::NoWai, 1),

                    // Switch
                    "WTF?" => self.simple_token(TokenKind::WTF, 4),
                    "OMG" => self.simple_token(TokenKind::OMG, 3),
                    "OMGWTF" => self.simple_token(TokenKind::OMGWTF, 6),

                    // End of block
                    "OIC" => self.simple_token(TokenKind::OIC, 3),

                    // Loops
                    "IM" => self.match_multi_word(
                        "IM",
                        &[
                            ("IN YR", TokenKind::ImInYr, 2),
                            ("OUTTA YR", TokenKind::ImOuttaYr, 2),
                        ],
                    ),
                    "YR" => self.simple_token(TokenKind::Yr, 2),
                    "TIL" => self.simple_token(TokenKind::TIL, 3),
                    "WILE" => self.simple_token(TokenKind::WILE, 4),
                    "UPPIN" => self.simple_token(TokenKind::UPPIN, 5),
                    "NERFIN" => self.simple_token(TokenKind::NERFIN, 6),

                    // Functions
                    "HOW" => self.match_full_keyword("HOW IZ I", TokenKind::HowIzI, 2),
                    "FOUND" => self.match_full_keyword("FOUND YR", TokenKind::FoundYr, 1),
                    "GTFO" => self.simple_token(TokenKind::GTFO, 4),
                    "IF" => self.match_full_keyword("IF U SAY SO", TokenKind::IfUSaySo, 3),

                    // Delimiters
                    "A" => self.simple_token(TokenKind::A, 1),
                    "AN" => self.simple_token(TokenKind::AN, 2),
                    "MKAY" => self.simple_token(TokenKind::MKAY, 4),
                    // Literals
                    s if s.starts_with('"') => TokenKind::YARN(self.read_literal()),

                    // Identifiers
                    s => {
                        let ch = s
                            .chars()
                            .next()
                            .map(|s| s.to_ascii_lowercase())
                            .unwrap_or_default();

                        if is_letter(ch) {
                            let identifier =
                                String::from(self.current.expect("Should not be empty"));
                            self.position += identifier.len();

                            TokenKind::IDENTIFIER { name: identifier }
                        } else if is_digit(ch) {
                            let number = self.read_number();
                            match number {
                                Some(Number::Integer(i)) => TokenKind::NUMBR(i),
                                Some(Number::Float(f)) => TokenKind::NUMBAR(f),
                                None => TokenKind::ILLEGAL,
                            }
                        } else {
                            TokenKind::ILLEGAL
                        }
                    }
                }
            }
            None => TokenKind::EOF,
        };

        self.advance();

        Token {
            span: Span {
                start: start_position,
                end: self.position - 1,
            },
            kind: t,
        }
    }

    fn match_multi_word(&mut self, base: &str, options: &[(&str, TokenKind, usize)]) -> TokenKind {
        let current_position = self.position;

        for (pattern, kind, skip_count) in options {
            let full_phrase = format!("{} {}", base, pattern);
            let mut phrase_iter = full_phrase.split(' ');
            let mut matched = true;

            // Skip the base word we've already matched
            phrase_iter.next();

            // Check subsequent words
            for expected in phrase_iter {
                if self.peek.unwrap_or_default().trim_end_matches("\n") != expected {
                    matched = false;
                    break;
                }
                self.advance();
            }

            if matched {
                self.position += full_phrase.len() - skip_count;
                return kind.clone();
            }

            self.position = current_position;
        }

        TokenKind::ILLEGAL
    }

    fn match_full_keyword(
        &mut self,
        full_keyword: &str,
        kind: TokenKind,
        skip_count: usize,
    ) -> TokenKind {
        let mut phrase_iter = full_keyword.split(' ');
        let current_str = phrase_iter.next().unwrap();

        for _ in 0..skip_count {
            let expected_next_str = phrase_iter.next().unwrap();
            if self.peek.unwrap_or_default().trim_end_matches("\n") == expected_next_str {
                self.advance();
            } else {
                self.position += current_str.len();
                return TokenKind::ILLEGAL;
            }
        }

        self.position += full_keyword.len() - skip_count;
        kind
    }

    fn simple_token(&mut self, kind: TokenKind, len: usize) -> TokenKind {
        self.position += len;
        kind
    }

    fn skip_comments(&mut self) -> bool {
        if self.current == Some("OBTW") {
            let is_valid_placement = match self.previous {
                None => true, // Start of file
                Some("") => true,
                Some("\n") => true, // Start of line
                _ => false,         // Middle of line (Invalid!)
            };

            if !is_valid_placement {
                return false;
            }

            self.position += 4;

            loop {
                self.advance();

                let current_word = match self.current {
                    Some(s) => s,
                    None => {
                        break;
                    }
                };

                if current_word == "TLDR" {
                    self.position += current_word.len() - 1;
                    self.advance();
                    break;
                }

                if self.previous.unwrap_or_default() == "\n" {
                    let current_word_length = current_word.len() as i64;

                    let new_position = self.position as i64 + current_word_length - 1;
                    self.position = new_position as usize;

                    continue;
                }

                if current_word == "\n" {
                    continue;
                }

                self.position += current_word.len();
            }

            return true;
        } else if self.current == Some("BTW") {
            self.position += 3;

            loop {
                if self.peek == None {
                    self.advance();
                    break;
                }

                let peek_str = self.peek.unwrap();

                if peek_str.contains('\n') {
                    let mut iter_with_comment = peek_str.split('\n');
                    iter_with_comment.next();

                    let remaining_words: Vec<&str> = iter_with_comment.collect();
                    self.prepend_items(remaining_words);

                    self.advance();
                    break;
                }

                self.advance();
                self.position += self.current.unwrap_or_default().len();
            }

            return true;
        }

        false
    }

    fn skip_whitespace(&mut self) -> bool {
        let mut skipped = false;
        while let Some(s) = self.current {
            if s == "" {
                self.advance();
                skipped = true;
            } else if s
                .chars()
                .next()
                .map_or(false, |c| c.is_whitespace() && s.len() == 1)
            {
                self.advance();
                self.position -= 1;
                skipped = true;
            } else {
                break;
            }
        }

        skipped
    }

    fn read_number(&mut self) -> Option<Number> {
        let current_str = self
            .current
            .expect("Should not be empty")
            .trim_end_matches("\n");

        self.position += current_str.len();
        let number = if current_str.contains('.') {
            match current_str.parse::<f64>() {
                Ok(num) => Some(Number::Float(num)),
                Err(_) => None,
            }
        } else {
            match current_str.parse::<i64>() {
                Ok(num) => Some(Number::Integer(num)),
                Err(_) => None,
            }
        };

        return number;
    }

    fn read_literal(&mut self) -> String {
        let mut literal = String::new();
        let mut begin_quote_found = false;

        self.position += 1;

        loop {
            let s = if !begin_quote_found {
                begin_quote_found = true;
                self.current.unwrap_or("\u{0}").trim_start_matches('"')
            } else {
                self.current.unwrap_or("\u{0}")
            };

            let s_iter = s.chars();
            let mut prev_ch = '\0';

            for ch in s_iter {
                if ch == '\\' && prev_ch != '\\' {
                    self.position += 1;
                    prev_ch = ch;
                    continue;
                }

                if (ch == '"' && prev_ch != '\\') || ch == '\u{0}' {
                    self.position += 1;
                    return literal;
                }

                literal.push(ch);
                self.position += 1;
                prev_ch = ch;
            }

            self.advance();
            literal.push(' ');
        }
    }
}

fn is_letter(c: char) -> bool {
    c.is_ascii_alphabetic() || c == '_'
}

fn is_digit(c: char) -> bool {
    c >= '0' && c <= '9'
}
