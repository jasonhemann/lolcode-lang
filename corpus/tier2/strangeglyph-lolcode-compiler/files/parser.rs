use self::lexer::Token;

mod lexer;



fn main() {
    let mut tokens = lexer::tokenize("1 + 2");
    println!("Tokens: {:?}", tokens)
    println!("{:?}", ASTNode::parse(&mut tokens.iter().map(|&e| e), 0))
}



enum ASTNode {
    INT(int),
    ADD(~ASTNode, ~ASTNode)
}

trait Parseable {
    fn lbp(&self) -> uint;
    fn unary<'a, I: Iterator<Token>>(&self, tokens: &mut I) -> ASTNode;
    fn binary<'a, I: Iterator<Token>>(&self, left: ASTNode, tokens: &mut I) -> ASTNode;
}


impl Parseable for Token {
    fn lbp(&self) -> uint {
        match *self {
            lexer::END_TOKEN    => 0,
            lexer::OP_PLUS      => 10,
            _                   => fail!("{:?} has no left binding power", self)
        }
    }

    fn unary<'a, I: Iterator<Token>>(&self, tokens: &mut I) -> ASTNode {
        match *self {
            lexer::INT_LITERAL(val) => INT(val),
            _                       => fail!("{:?} has no unary meaning", self)
        }
    }

    fn binary<'a, I: Iterator<Token>>(&self, left: ASTNode, tokens: &mut I) -> ASTNode {
        match *self {
            lexer::OP_PLUS  => ADD(~left, ~ASTNode::parse(tokens, self.lbp()).expect("Expected a righthandside for +")),
            _               => fail!("{:?} has no binary meaning", self)
        }
    }
}


impl ASTNode { 
    fn parse<'a, I: Iterator<Token>>(tokens: &mut I, rbp: uint) -> Option<ASTNode> {

        println!("Parsing subexpr with rbp: {:u}", rbp);

        let mut current = match tokens.next() {
            Some(token) => token, 
            None => return None
        };

        println!("Current: {:?}", current)


        let mut left = current.unary(tokens);

        println!("Left: {:?}", left);
      

        let mut next = match tokens.next() {
            Some(token) => token,
            None => return None
        };

        println!("Next: {:?}", next);



        while rbp < next.lbp() {
            current = next;
            
            left = current.binary(left, tokens);
            
            next = match tokens.next() {
                Some(token) => token,
                None => break
            }; 


            println!("Current: {:?}, Next: {:?}, Left: {:?}", current, next, left);
        } 

        Some(left) 
    } 
}