use crate::environment::Env;
use parser::ast::{BlockStatement, IDENTIFIER};
use std::fmt;
use std::rc::Rc;

#[derive(Debug, Clone)]
pub enum Object {
    Numbr(i64),
    Numbar(f64),
    Yarn(String),
    Troof(bool),
    Noob,
    Function {
        name: String,
        params: Vec<IDENTIFIER>,
        body: BlockStatement,
        env: Env,
    },
    // Special object for handling early returns from functions
    ReturnValue(Rc<Object>),
    // Special object for handling GTFO (break)
    BreakValue,
}

impl fmt::Display for Object {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Object::Numbr(val) => write!(f, "{}", val),
            Object::Numbar(val) => write!(f, "{}", val),
            Object::Yarn(val) => write!(f, "{}", val),
            Object::Troof(val) => write!(f, "{}", if *val { "WIN" } else { "FAIL" }),
            Object::Noob => write!(f, "NOOB"),
            Object::Function { name, .. } => write!(f, "<fn:{}>", name),
            Object::ReturnValue(val) => write!(f, "{}", val),
            Object::BreakValue => write!(f, "<break>"),
        }
    }
}
