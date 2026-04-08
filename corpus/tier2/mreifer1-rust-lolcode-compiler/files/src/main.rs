use std::env;
use std::fs;
use std::collections::HashSet;
use std::process::Command;

/// Trait for a simple lolcompiler front-end. 
/// Errors should cause immediate exit inside the implementation.
pub trait Compiler {
    fn compile(&mut self, source: &str);
    fn next_token(&mut self) -> String;
    fn parse(&mut self);
    fn current_token(&self) -> String;
    fn set_current_token(&mut self, tok: String);
}

pub struct LolcodeCompiler {
    pub lexer: MyLexicalAnalyzer,
    pub current_tok: String,
    pub token_stack: Vec<String>,     
    pub html_output: String,
    pub var_stack: Vec<(String, String)>,     
}

impl LolcodeCompiler {
    /// creates a instance of LolcodeCompiler with the needed fields initalized
    pub fn new() -> Self {
        Self {
            lexer: MyLexicalAnalyzer::new(""),
            current_tok: String::new(),
            token_stack: Vec::new(),
            html_output: String::new(),
            var_stack: Vec::new(),
        }
    }
    /// slots in first token 
    fn start(&mut self) {
        let candidate = self.lexer.tokens.pop().unwrap_or_default();
        self.token_stack.push(candidate.clone());
        self.set_current_token(candidate);
    }
    /// converts my stack of syntactically correct tokens into html and resolves statically scoped variables
    fn generate_html(&mut self) -> String {
    let mut html = String::new();
    let mut i: usize = 0;

    // is body open
    let mut opened_body = false;

    // track which block is open
    let mut block_stack: Vec<String> = Vec::new();

    // variable scopes 
    // bottom level is the global scope
    let mut var_scopes: Vec<Vec<(String, String)>> = vec![vec![]];

    
    let ensure_body = |html: &mut String, opened_body: &mut bool| {
        if !*opened_body {
            html.push_str("<body>\n");
            *opened_body = true;
        }
    };

    
    let gather_text = |tokens: &Vec<String>, mut j: usize, end_upper: &str| -> (String, usize) {
        let mut out = String::new();
        while j < tokens.len() && tokens[j].to_uppercase() != end_upper {
            if !out.is_empty() { out.push(' '); }
            out.push_str(&tokens[j]);
            j += 1;
        }
        (out, j)
    };

    // rename token stack
    let tokens = &self.token_stack;

    // standard opening tags
    html.push_str("<!DOCTYPE html>\n<html>\n");
    block_stack.push("html".to_string());

    while i < tokens.len() {
        let tok_upper = tokens[i].to_uppercase();

        match tok_upper.as_str() {
            "#HAI" => {
                // already handled above just move next token
                i += 1;
            }

            "#KTHXBYE" => {
                // end of file
                break;
            }

            // for comments
            "#OBTW" => {
                html.push_str("<!-- ");
                i += 1;
                while i < tokens.len() && tokens[i].to_uppercase() != "#TLDR" {
                    html.push_str(&tokens[i]);
                    html.push(' ');
                    i += 1;
                }
                html.push_str("-->\n");
               // if current token is tldr +1 to index
                if i < tokens.len() && tokens[i].to_uppercase() == "#TLDR" { i += 1; }
            }

            // check which opening tag
            "#MAEK HEAD" => {
                html.push_str("<head>\n");
                block_stack.push("head".to_string());
                i += 1;
            }

            "#MAEK PARAGRAF" => {
                ensure_body(&mut html, &mut opened_body);
                html.push_str("<p>");
                block_stack.push("p".to_string());
                var_scopes.push(vec![]);
                i += 1;
            }

            "#MAEK LIST" => {
                ensure_body(&mut html, &mut opened_body);
                html.push_str("<ul>\n");
                block_stack.push("ul".to_string());
                i += 1;
            }

            // closing for #OIC
            "#OIC" => {
                // pop block name
                if let Some(name) = block_stack.pop() {
                    match name.as_str() {
                        "head" => {
                            html.push_str("</head>\n");
                        }
                        "p" => {
                            html.push_str("</p>\n");
                        }
                        "ul" => {
                            html.push_str("</ul>\n");
                        }
                        "html" => {
                            // html should be at the end (just empty block)
                        }
                        other => {
                            // unkown block (should never get hit)
                            let _ = other;
                        }
                    }
                }
                // IMPORTANT (POP VARIABLE SCOPE (LOCAL SCOPE))
                if var_scopes.len() > 1 {
                    var_scopes.pop();
                }
                i += 1;
            }

            // Different GIMMEH ...
            "#GIMMEH TITLE" => {
                i += 1;
                let (text, j) = gather_text(tokens, i, "#MKAY");
                html.push_str(&format!("<title>{}</title>\n", text.trim()));
                i = j;
                if i < tokens.len() && tokens[i].to_uppercase() == "#MKAY" { i += 1; }
            }

            "#GIMMEH BOLD" => {
                i += 1;
                html.push_str("<b>");
                while i < tokens.len() && tokens[i].to_uppercase() != "#MKAY" {
                    html.push_str(&tokens[i]);
                    html.push(' ');
                    i += 1;
                }
                html.push_str("</b>");
                if i < tokens.len() && tokens[i].to_uppercase() == "#MKAY" { i += 1; }
            }

            "#GIMMEH ITALICS" => {
                i += 1;
                html.push_str("<i>");
                while i < tokens.len() && tokens[i].to_uppercase() != "#MKAY" {
                    html.push_str(&tokens[i]);
                    html.push(' ');
                    i += 1;
                }
                html.push_str("</i>");
                if i < tokens.len() && tokens[i].to_uppercase() == "#MKAY" { i += 1; }
            }

            "#GIMMEH ITEM" => {
                i += 1;
                html.push_str("<li>");
                while i < tokens.len() && tokens[i].to_uppercase() != "#MKAY" {
                    let sub = tokens[i].to_uppercase();
                    if sub == "#GIMMEH BOLD" || sub == "#GIMMEH ITALICS" || sub == "#LEMME SEE" {
                        break;
                    }
                    html.push_str(&tokens[i]);
                    html.push(' ');
                    i += 1;
                }
                html.push_str("</li>\n");
                if i < tokens.len() && tokens[i].to_uppercase() == "#MKAY" { i += 1; }
            }

            "#GIMMEH NEWLINE" => {
                ensure_body(&mut html, &mut opened_body);
                html.push_str("<br/>\n");
                i += 1;
            }

            "#GIMMEH SOUNDZ" => {
                i += 1;
                let (addr, j) = gather_text(tokens, i, "#MKAY");
                let src = addr.trim();
                html.push_str(&format!("<audio controls>\n  <source src=\"{}\">\n</audio>\n", src));
                i = j;
                if i < tokens.len() && tokens[i].to_uppercase() == "#MKAY" { i += 1; }
            }

            "#GIMMEH VIDZ" => {
                i += 1;
                let (addr, j) = gather_text(tokens, i, "#MKAY");
                let src = addr.trim();
                html.push_str(&format!("<iframe src=\"{}\"></iframe>\n", src));
                i = j;
                if i < tokens.len() && tokens[i].to_uppercase() == "#MKAY" { i += 1; }
            }

            // variable decleration
            "#I HAZ" => {
                i += 1;
                if i >= tokens.len() { break; }
                let var_name = tokens[i].clone();
                i += 1;
                if i < tokens.len() && tokens[i].to_uppercase() == "#IT IZ" {
                    i += 1;
                }
                let (val, j) = gather_text(tokens, i, "#MKAY");
                let value = val.trim().to_string();
                // PUSH TO THE CURRENT SCOPE
                if let Some(scope) = var_scopes.last_mut() {
                    scope.push((var_name, value));
                }
                i = j;
                if i < tokens.len() && tokens[i].to_uppercase() == "#MKAY" { i += 1; }
            }

            // Use variable
            t if t == "#LEMME SEE" || t == "#LEMME" => {
                if tokens[i].to_uppercase() == "#LEMME SEE" {
                    i += 1;
                } else {
                    i += 1;
                    if i < tokens.len() && tokens[i].to_uppercase() == "SEE" { i += 1; }
                }
                if i >= tokens.len() { break; }
                let var_name = tokens[i].clone();
                // LOOKUP FROM MOST INNER SCOPE TO OUTER SCOPE (so we get local variables) <- done by .rev
                let mut found: Option<String> = None;
                for scope in var_scopes.iter().rev() {
                    if let Some((_, v)) = scope.iter().rev().find(|(n, _)| n.eq_ignore_ascii_case(&var_name)) {
                        found = Some(v.clone());
                        break;
                    }
                }
                if let Some(val) = found {
                    html.push_str(&val);
                    html.push(' ');
                }
                while i < tokens.len() && tokens[i].to_uppercase() != "#MKAY" {
                    i += 1;
                }
                if i < tokens.len() && tokens[i].to_uppercase() == "#MKAY" { i += 1; }
            }

            // normal text
            other => {
                if !other.starts_with('#') {
                    let top_block = block_stack.last().map(|s| s.as_str()).unwrap_or("");
                    if top_block != "head" {
                        ensure_body(&mut html, &mut opened_body);
                    }

                    html.push_str(&tokens[i]);
                    html.push(' ');
                }
                i += 1;
            }
        } 
    }

    // close any tags that weren't
    while let Some(name) = block_stack.pop() {
        match name.as_str() {
            "head" => { html.push_str("</head>\n"); }
            "p" => { html.push_str("</p>\n"); }
            "ul" => { html.push_str("</ul>\n"); }
            "html" => { /* closed at the end */ }
            _ => {}
        }
    }

    if opened_body {
        html.push_str("</body>\n");
    }

    html.push_str("</html>\n");
    html
}
}

impl SyntaxAnalyzer for LolcodeCompiler {
    /// driver "parser"
    fn parse_lolcode(&mut self){
        if self.current_token() != "#HAI" {
            eprintln!("Syntax error: program must start with #HAI, found '{}'", self.current_token());
            std::process::exit(1);
        }
        self.next_token();

        if self.current_token().as_str() == "#OBTW" {
            self.parse_comment();
        }

        if self.current_token().as_str() == "#MAEK HEAD" {
            self.parse_head();
        }

        self.parse_body();

        if self.current_token() != "#KTHXBYE" {
            eprintln!("Syntax error: program must end with #KTHXBYE, found '{}'", self.current_token());
            std::process::exit(1);
        }
        self.next_token();
        
    }
    /// parse head assuming #MAEK HEAD is current token
    fn parse_head(&mut self){
        // move past #MAEK HEAD
        self.next_token();

        self.parse_title();

        // expect #OIC
        if self.current_token() != "#OIC" {
            eprintln!("Syntax error: expected '#OIC' after head section, found '{}'", self.current_token());
            std::process::exit(1);
        }
        self.next_token();
    }
    /// title parser 
    fn parse_title(&mut self){
        if self.current_token() != "#GIMMEH TITLE" {
            eprintln!("Syntax error: title must start with #GIMMEH TITLE, found '{}'", self.current_token());
            std::process::exit(1);
        }
        // move past #GIMMEH TITLE
        self.next_token();

        // check text
        self.parse_text();

        if self.current_token() != "#MKAY" {
            eprintln!("Syntax error: title must end with #MKAY, found '{}'", self.current_token());
            std::process::exit(1);
        }
        // move past ending tag
        self.next_token();
    }
    /// parse #OBTW assuming its current token
    fn parse_comment(&mut self){
        // move past #OBTW
        self.next_token();

        self.parse_text();

        if self.current_token() != "#TLDR" {
            eprintln!("Syntax error: comment must end with #TLDR, found '{}'", self.current_token());
            std::process::exit(1);
        }
        self.next_token();

        if self.current_token() == "#OBTW" {
            self.parse_comment();
        }
    }
    /// parse body (main content)
    fn parse_body(&mut self){

        while !self.current_token().is_empty() && self.current_token() != "#KTHXBYE" {
            match self.current_token().as_str() {
                "#I HAZ" => self.parse_variable_define(),
                "#MAEK PARAGRAF" => self.parse_paragraph(),
                "#OBTW" => self.parse_comment(),
                "#GIMMEH ITALICS" => self.parse_italics(),
                "#GIMMEH LIST"  => self.parse_list(),
                "#GIMMEH NEWLINE" => self.parse_newline(),
                "#GIMMEH SOUNDZ" => self.parse_audio(),
                "#GIMMEH VIDZ" => self.parse_video(),
                "#GIMMEH BOLD" => self.parse_bold(),
                "#LEMME SEE" => self.parse_variable_use(),
                token if !token.starts_with('#') => self.parse_text(),
                _ => {
                    eprintln!("Unexpected token {}", self.current_token());
                    std::process::exit(1);
                }
                
            }
        }
    }
    /// Paragraph parser, then passes to inner paragraph
    fn parse_paragraph(&mut self) {
    // move past #MAEK PARAGRAF
    self.next_token();

    // allowed variable definition
    if self.current_token() == "#I HAZ" {
        self.parse_variable_define();
    }

    self.parse_inner_paragraph(); // will return with #OIC as current token ideally. 

    // closing #oic
    if self.current_token() != "#OIC" {
        eprintln!("Syntax error: expected '#OIC' to close paragraph, found '{}'", self.current_token());
        std::process::exit(1);
    }
    self.next_token();
}
    /// just calls the inner_text parser (calls parse_inner_text for the actual meat of the paragraph)
    fn parse_inner_paragraph(&mut self){
        self.parse_inner_text();
    }
    /// inner part of paragraph parser (parses the main part of the paragraph)
    fn parse_inner_text(&mut self) {
        // Keep parsing until you hit #OIC or run out of tokens
        while !self.current_token().is_empty() && self.current_token() != "#OIC" {
            match self.current_token().as_str() {
                "#LEMME SEE" => self.parse_variable_use(),
                "#GIMMEH BOLD" => self.parse_bold(),
                "#GIMMEH ITALICS" => self.parse_italics(),
                "#MAEK LIST" => self.parse_list(),
                "#GIMMEH SOUNDZ" => self.parse_audio(),
                "#GIMMEH VIDZ" => self.parse_video(),
                "#GIMMEH NEWLINE" => self.parse_newline(),
                token if !token.starts_with('#') => self.parse_text(), 
                _ => {
                    eprintln!("Syntax error in paragraph: unexpected token '{}'", self.current_token());
                    std::process::exit(1);
                }
            }
        }
    }
    /// parser for decarling variables 
    fn parse_variable_define(&mut self){
        // move past "#I HAZ"
        self.next_token();

        // grab var name
        let var_name = self.current_token();
        self.next_token();

        if self.current_token() != "#IT IZ" {
            eprintln!("Syntax error: expected '#IT IZ' after variable name, found '{}'", self.current_token());
            std::process::exit(1);
        }
        // move past #IT IZ
        self.next_token();

        // grab value 
        let var_value = self.current_token();

        self.var_stack.push((var_name.clone(), var_value.clone()));

        // move past the value 
        self.next_token();

        if self.current_token() != "#MKAY" {
            eprintln!("Syntax error: expected '#MKAY' after variable declaration, found '{}'", self.current_token());
            std::process::exit(1);
        }
        self.next_token();
    }
    /// variable use parser (checks if the variable exists in the var stack and if so returns it)
    fn parse_variable_use(&mut self) {

        self.next_token(); // go past #LEMME SEE
        let var_name = self.current_token();

        // check if the variable exists in our stack variable stack. 
        if let Some((_, _)) = self.var_stack.iter().rev().find(|(name, _)| name == &var_name) {
        } else {
            eprintln!("Static Semantic error: variable '{}' not defined in scope", var_name);
            std::process::exit(1);
        }

        self.next_token();
        if self.current_token() != "#MKAY" {
            eprintln!("Syntax error: expected '#MKAY' after variable use, found '{}'", self.current_token());
            std::process::exit(1);
        }
        self.next_token();
    }
    /// bold parser
    fn parse_bold(&mut self){

        // move past #GIMMEH BOLD
        self.next_token();

        // check text
        self.parse_text();

        if self.current_token() != "#MKAY" {
            eprintln!("Syntax error: bold must end with #MKAY, found '{}'", self.current_token());
            std::process::exit(1);
        }
        self.next_token();
    }
    /// Simple italics parser
    fn parse_italics(&mut self){
        // move past #GIMMEH ITALICS
        self.next_token();

        // check text
        self.parse_text();

        if self.current_token() != "#MKAY" {
            eprintln!("Syntax error: italics must end with #MKAY, found '{}'", self.current_token());
            std::process::exit(1);
        }
        self.next_token();
    }
    /// list parser will call parse list items
    fn parse_list(&mut self){
        // move past #MAEK LIST
        self.next_token();

        while !self.current_token().is_empty() && self.current_token() != "#OIC" {
            match self.current_token().as_str() {
                "#GIMMEH ITEM" => self.parse_list_items(),
                _ => {
                    eprintln!("Syntax error in list: unexpected token '{}'", self.current_token());
                    std::process::exit(1);
                }
            }
        }
        if self.current_token() != "#OIC" {
            eprintln!("Syntax error: list must end with #OIC, found '{}'", self.current_token());
            std::process::exit(1);
        }
        self.next_token();
    }
    /// calls inner list items since it is our main part of the list
    fn parse_list_items(&mut self){
        // move past #GIMMEH ITEM
        self.next_token();

        self.parse_inner_list();

        if self.current_token() != "#MKAY" {
            eprintln!("Syntax error: list items must end with #MKAY, found '{}'", self.current_token());
            std::process::exit(1);
        }
        self.next_token();
    }
    /// parses the actual elements in the list
    fn parse_inner_list(&mut self){

        while !self.current_token().is_empty() && self.current_token() != "#MKAY" {
            match self.current_token().as_str() {
                "#LEMME SEE" => self.parse_variable_use(),
                "#GIMMEH BOLD" => self.parse_bold(),
                "#GIMMEH ITALICS" => self.parse_italics(),
                token if !token.starts_with('#') => self.parse_text(), 
                _ => {
                    eprintln!("Syntax error in paragraph: unexpected token '{}'", self.current_token());
                    std::process::exit(1);
                }
            }
        }
    }
    /// audio parser
    fn parse_audio(&mut self){
         // move past #GIMMEH SOUNDZ
        self.next_token();

        // check text
        self.parse_text();

        if self.current_token() != "#MKAY" {
            eprintln!("Syntax error: audio must end with #MKAY, found '{}'", self.current_token());
            std::process::exit(1);
        }
        self.next_token();
    }
    /// video parser
    fn parse_video(&mut self){
        // move past #GIMMEH VIDZ
        self.next_token();

        // check text
        self.parse_text();

        if self.current_token() != "#MKAY" {
            eprintln!("Syntax error: title must end with #MKAY, found '{}'", self.current_token());
            std::process::exit(1);
        }
        self.next_token();
    }
    /// New line parser is very simple because new line is just a single tag
    fn parse_newline(&mut self){
        // nothing to check here 
        // the parent functions that call this already check if it is #GIMMEH NEWLINE
        // there is no required closing tag so this is it.... 
        // just call next token
        self.next_token();
    }
    /// consumes token by token until their is a # (no more text)
    fn parse_text(&mut self) {
    while !self.current_token().is_empty() && !self.current_token().starts_with('#') {
        self.next_token();
    }
}
}


impl Compiler for LolcodeCompiler {
    /// Starts the compilation process and initalizes a Lexical Analyzer
    fn compile(&mut self, source: &str) {
        self.lexer = MyLexicalAnalyzer::new(source);
        self.lexer.tokenize();
        self.start();
    }
    /// next token (pop and clone it to stack)
    fn next_token(&mut self) -> String {
        if let Some(candidate) = self.lexer.tokens.pop() {
        self.set_current_token(candidate.clone());

        // building ast 
        self.token_stack.push(candidate.clone());

        candidate
        } else {
            self.current_tok.clear();
            String::new()
        }
    }
    /// starts the parsing
    fn parse(&mut self) {
        self.parse_lolcode();
        if !self.lexer.tokens.is_empty() || !self.current_tok.is_empty() {
            eprintln!("Syntax error: Additional tokens found after the sentence.");
            std::process::exit(1);
        }
    }
    /// Returns the current token
    fn current_token(&self) -> String { self.current_tok.clone() }
    /// sets the current token
    fn set_current_token(&mut self, tok: String) { self.current_tok = tok; }
}

/// Trait for a simple lexical analyzer.
/// Implements a character-by-character analysis
/// from a state machine design.
pub trait LexicalAnalyzer {
    fn get_char(&mut self) -> char;
    fn add_char(&mut self, c: char);
    fn lookup(&self, s: &str) -> bool;
}

pub struct MyLexicalAnalyzer {
    input: Vec<char>,
    position: usize,
    current_build: String,  
    pub tokens: Vec<String>,
    pub reserved_tokens: HashSet<String>,
}

impl MyLexicalAnalyzer {
    /// Creates a instance of MyLexicalAnalyzer with the required tags 
    pub fn new(source: &str) -> Self {
        let raw_tokens = vec![
            // single-word tags
            "#HAI", "#KTHXBYE", "#OBTW", "#TLDR", "#OIC", "#MKAY",

            // multi-word tags (must be recognized as a unit)
            "#MAEK HEAD", "#MAEK PARAGRAF", "#MAEK LIST",
            "#GIMMEH TITLE", "#GIMMEH BOLD", "#GIMMEH ITALICS",
            "#GIMMEH ITEM", "#GIMMEH NEWLINE",
            "#GIMMEH SOUNDZ", "#GIMMEH VIDZ",

            // variable constructs
            "#I HAZ", "#IT IZ", "#LEMME SEE",
        ];

        let reserved_tokens = raw_tokens
            .into_iter()
            .map(|t| t.to_ascii_uppercase())
            .collect();

        Self {
            input: source.chars().collect(),
            position: 0,
            current_build: String::new(),
            tokens: Vec::new(),
            reserved_tokens,
        }
    }

    /// tokenize characters from input char array
    pub fn tokenize(&mut self) {
        while self.position < self.input.len() {
            // remove white space until token
            self.skip_whitespace();
            if self.position >= self.input.len() {
                break;
            }

            // read next word
            let word = self.read_word();
            if word.is_empty() {
                continue;
            }

            // if its a prefix check next word to make a 2 worded tag
            if ["#MAEK", "#GIMMEH", "#I", "#IT", "#LEMME"]
                .iter()
                .any(|p| word.to_ascii_uppercase() == *p)
            {
                // peek next word if it a prefix 
                if let Some(next_word) = self.peek_word() {
                    let combined = format!("{} {}", word, next_word);
                    if self.lookup(&combined) {
                        // skip the space and consume the next word 
                        self.skip_whitespace();
                        let _consumed = self.read_word(); // word consumed
                        self.tokens.push(combined.to_ascii_uppercase());
                        continue; // push the 2 worded token and go next iteration
                    } else {
                        // Invalid double worded token
                        eprintln!("Lexical error: invalid token '{}'", combined);
                        std::process::exit(1);
                    }
                }
            }

            // push single word 
            if self.lookup(&word) {
                if self.reserved_tokens.contains(&word.to_ascii_uppercase()) {
                    self.tokens.push(word.to_ascii_uppercase()); // uppercase for tokens
                } else {
                    self.tokens.push(word.clone()); // keep text as-is
                }
            } else {
                eprintln!("Lexical error: invalid token '{}'", word);
                std::process::exit(1);
            }
        }

        // reverse so its FIFO
        self.tokens.reverse();
    }

    /// skip whitespace
    fn skip_whitespace(&mut self) {
        while self.position < self.input.len() && self.input[self.position].is_whitespace() {
            self.position += 1;
        }
    }

    /// assumes position is at a char from skipwhitespace call and starts reading char by char building token
    fn read_word(&mut self) -> String {
        let mut word = String::new();
        while self.position < self.input.len() {
            let c = self.input[self.position];
            if c.is_whitespace() {
                break;
            }
            word.push(c);
            self.position += 1;
        }
        word
    }

    /// like a stack it just peeks at next word
    fn peek_word(&self) -> Option<String> {
        let mut i = self.position;
        // remove white space
        while i < self.input.len() && self.input[i].is_whitespace() {
            i += 1;
        }
        if i >= self.input.len() {
            return None;
        }
        // get next word
        let mut next = String::new();
        while i < self.input.len() && !self.input[i].is_whitespace() {
            next.push(self.input[i]);
            i += 1;
        }
        if next.is_empty() { None } else { Some(next) }
    }
}

impl LexicalAnalyzer for MyLexicalAnalyzer {
    /// get current char and move the position (index)
    fn get_char(&mut self) -> char {
        if self.position < self.input.len() {
            let c = self.input[self.position];
            self.position += 1;
            c
        } else {
            '\0'
        }
    }
    ///  add char to current token
    fn add_char(&mut self, c: char) {
        self.current_build.push(c);
    }

    /// return true only if valid token
    fn lookup(&self, s: &str) -> bool {
        let upper = s.to_ascii_uppercase();

        // check if our reserved tokens has the current token
        if self.reserved_tokens.contains(&upper) {
            return true;
        }

        // If the token is a prefix token (spaced token) we must validate with its combined token (2nd word)
        let prefixes = ["#MAEK", "#GIMMEH", "#I", "#IT", "#LEMME"];
        if prefixes.iter().any(|&p| upper == p) {
            // if the current token + next token is a reserved token it is valid
            if let Some(next) = self.peek_word() {
                let combined = format!("{} {}", s, next); // combine the two
                if self.reserved_tokens.contains(&combined.to_ascii_uppercase()) { // validate it exists in our hashset
                    return true;
                }
            }
            // if the combined token is not valid return false
            return false;
        }

        // allow plain text
        let allowed_punct = ",.\":?!%/'";
        let all_good = s.chars().all(|c| {
            c.is_alphanumeric() || c.is_whitespace() || allowed_punct.contains(c)
        });
        if all_good {
            return true;
        }

        // not valid word
        false
    }
}

/// OPTION 1 - Trait for a recursive descent Syntax Analyzer 
/// over Vec<String>. Each function parses a nonterminal in 
/// the grammar. On error: exit immediately.
pub trait SyntaxAnalyzer {
    fn parse_lolcode(&mut self);
    fn parse_head(&mut self);
    fn parse_title(&mut self);
    fn parse_comment(&mut self);
    fn parse_body(&mut self);
    fn parse_paragraph(&mut self);
    fn parse_inner_paragraph(&mut self);
    fn parse_inner_text(&mut self);
    fn parse_variable_define(&mut self);
    fn parse_variable_use(&mut self);
    fn parse_bold(&mut self);
    fn parse_italics(&mut self);
    fn parse_list(&mut self);
    fn parse_list_items(&mut self);
    fn parse_inner_list(&mut self);
    fn parse_audio(&mut self);
    fn parse_video(&mut self);
    fn parse_newline(&mut self);
    fn parse_text(&mut self);
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <input_file.lol>", args[0]);
        std::process::exit(1);
    }

    let filename = &args[1];

    // Only allow .lol files
    if !filename.ends_with(".lol") {
        eprintln!("Error: input file must have a '.lol' extension.");
        std::process::exit(1);
    }

    // Read file contents
    let input = fs::read_to_string(filename).unwrap_or_else(|err| {
        eprintln!("Error reading file '{}': {}", filename, err);
        std::process::exit(1);
    });

    // compile and parse
    let mut compiler = LolcodeCompiler::new();
    compiler.compile(&input);
    compiler.parse();

    // Generate HTML output
    let html_output = compiler.generate_html();

    // write html file using same name as input file
    let output_file = std::path::Path::new(filename).with_extension("html");

    if let Err(err) = fs::write(&output_file, &html_output) {
        eprintln!("Error writing HTML output: {}", err);
        std::process::exit(1);
    }

    // getting abs path for opening (gpt is smart)
    let abs_path = fs::canonicalize(&output_file).unwrap();
    let abs_str = abs_path.to_str().unwrap();

    // open in default browser (gpt is smart)
    if cfg!(target_os = "windows") { 
        let _ = Command::new("cmd")
            .args(["/C", "start", "", abs_str])
            .spawn();
    } else if cfg!(target_os = "macos") {
        let _ = Command::new("open")
            .arg(abs_str)
            .spawn();
    } else {
        let _ = Command::new("xdg-open")
            .arg(abs_str)
            .spawn();
    }
}
