use std::iter;
use std::char;
use std::int;

#[deriving(Eq)]
pub enum Token {
    END_TOKEN,
    INT_LITERAL(int),
    OP_PLUS
}

struct Stream {
    content: ~str,
    pos: uint,
    marks: ~[uint]
}

impl Stream {
    fn new(content: ~str) -> Stream {
        Stream {
            content: content, 
            pos: 0,
            marks: ~[]
        }
    }

    fn peek(&mut self) -> char {
        self.content.char_at(self.pos)
    }

    fn next_char(&mut self) -> char {
        let chr = self.peek();
        self.pos += 1;
        chr
    }

    fn has_next(&self) -> bool {
        self.pos < self.content.len()
    }

    fn push_mark(&mut self) {
        self.marks.push(self.pos)
    }

    fn pop_mark(&mut self) {
        self.pos = self.marks.pop().unwrap()
    }

    fn try_consume(&mut self, test: &str) -> bool {
        
        let mut result = true;
        self.push_mark();

        for idx in iter::range(0, test.len()) {
            if !self.has_next() {
                result = false;
                break;
            } 

            if self.next_char() != test.char_at(idx) {
                result = false;
                break;
            }
        }

        self.pop_mark();
        result
    }

    fn skip(&mut self, amount: uint) {
        self.pos += amount;
    }

    fn rest<'lt>(&'lt self) -> &'lt str {
        if !self.has_next() {
            ""
        } else {
            self.content.slice(self.pos, self.content.len())
        }
    }
}



pub fn tokenize(inp: &str) -> ~[Token] {
    
    let mut result = ~[];
    let mut stream = Stream::new(inp.to_owned());

    while stream.has_next() {
        
        // Whitespace
        if stream.peek().is_whitespace() {
            stream.skip(1)
        }

        if stream.peek().is_digit() {
            // Number literals
        
            let literal = INT_LITERAL(from_str(read_num(&mut stream)).unwrap());
            result.push(literal);
        
        } else if stream.peek() == '+' {
            // Plus operator

            result.push(OP_PLUS);
            stream.skip(1)
        }
    }

    result.push(END_TOKEN);
    result
}

fn read_num(stream: &mut Stream) -> ~str {
    
    let mut result = ~"";
    
    while stream.has_next() && stream.peek().is_digit() {
        result.push_char(stream.next_char())
    }

    result
}