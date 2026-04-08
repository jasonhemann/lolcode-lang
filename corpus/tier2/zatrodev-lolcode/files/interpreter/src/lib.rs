use std::cell::RefCell;
use std::rc::Rc;

use parser::ast::*;
use parser::lexer::token::TokenKind;

use crate::environment::{Env, Environment, InterpreterEvent};
use crate::object::Object;

pub mod environment;
pub mod object;

type EvalError = String;
type EvalResult = Result<Rc<Object>, EvalError>;

/// The main entry point for the interpreter. It dispatches evaluation based on the Node type.
pub fn eval(node: Node, env: &Env) -> EvalResult {
    match node {
        Node::Program(p) => eval_statements(&p.body, env),
        Node::Statement(s) => eval_statement(&s, env),
        Node::Expression(e) => eval_expression(&e, env),
    }
}

/// Evaluates a vector of statements, handling early returns and breaks.
fn eval_statements(statements: &Vec<Statement>, env: &Env) -> EvalResult {
    let mut result = Rc::new(Object::Noob);
    for stmt in statements {
        result = eval_statement(stmt, env)?;
        // If a return or break signal is received, stop execution of the block and bubble it up.
        match *result {
            Object::ReturnValue(_) | Object::BreakValue => return Ok(result),
            _ => {}
        }
    }
    Ok(result)
}

/// Evaluates a single statement node from the AST.
fn eval_statement(statement: &Statement, env: &Env) -> EvalResult {
    match statement {
        Statement::Expression(expr) | Statement::Expr(expr) => {
            let value = eval_expression(expr, env)?;
            env.borrow_mut().set("IT".to_string(), Rc::clone(&value));
            Ok(value)
        }
        Statement::Declaration(decl) => eval_declaration_statement(decl, env),
        Statement::Assignment(assign) => eval_assignment_statement(assign, env),
        Statement::Print(print_stmt) => eval_print_statement(print_stmt, env),
        Statement::Input(input_stmt) => eval_input_statement(input_stmt, env),
        Statement::If(if_stmt) => eval_if_statement(if_stmt, env),
        Statement::Switch(switch_stmt) => eval_switch_statement(switch_stmt, env),
        Statement::Loop(loop_stmt) => eval_loop_statement(loop_stmt, env),
        Statement::FunctionDeclaration(func_decl) => eval_function_declaration(func_decl, env),
        Statement::Return(ret_stmt) => {
            let value = eval_expression(&ret_stmt.argument, env)?;
            Ok(Rc::new(Object::ReturnValue(value)))
        }
        Statement::Recast(recast_stmt) => eval_recast_statement(recast_stmt, env),
        Statement::Break(_) => Ok(Rc::new(Object::BreakValue)),
    }
}

//<editor-fold desc="Statement Implementations">
fn eval_declaration_statement(decl: &Declaration, env: &Env) -> EvalResult {
    let value = match &decl.expr {
        Some(expr) => eval_expression(expr, env)?,
        None => Rc::new(Object::Noob), // I HAS A VAR
    };
    if let TokenKind::IDENTIFIER { name } = &decl.identifier.kind {
        env.borrow_mut().set(name.clone(), value);
        Ok(Rc::new(Object::Noob))
    } else {
        Err(format!(
            "Expected identifier in declaration, found {:?}",
            decl.identifier.kind
        ))
    }
}

fn eval_assignment_statement(assign: &Assignment, env: &Env) -> EvalResult {
    let value = eval_expression(&assign.expr, env)?;
    if let TokenKind::IDENTIFIER { name } = &assign.identifier.kind {
        // In LOLCODE, assignment can also declare. We use `set` which handles both.
        env.borrow_mut().set(name.clone(), value);
        Ok(Rc::new(Object::Noob))
    } else {
        Err(format!(
            "Expected identifier in assignment, found {:?}",
            assign.identifier.kind
        ))
    }
}

fn eval_print_statement(print_stmt: &Print, env: &Env) -> EvalResult {
    let mut parts = Vec::new();

    for expr in &print_stmt.exprs {
        let value = eval_expression(expr, env)?;
        parts.push(format!("{}", value));
    }

    let output_string = parts.join("");
    let final_message = format!("{}\n", output_string);

    // Access the environment and the sender
    if let Some(sender) = &env.borrow().event_sender {
        sender
            .send(InterpreterEvent::Stdout(final_message))
            .expect("Failed to send output to GUI. Did the app close?");
    }

    Ok(Rc::new(Object::Noob))
}

fn eval_input_statement(input: &Input, env: &Env) -> EvalResult {
    // 1. Determine the input source (GUI Channel or Stdin Fallback)
    let buffer = {
        let env_borrow = env.borrow();

        // Check if we have the channels connected (GUI Mode)
        if let (Some(sender), Some(receiver)) =
            (&env_borrow.event_sender, &env_borrow.input_receiver)
        {
            // Tell the GUI we need input
            sender
                .send(InterpreterEvent::RequestInput)
                .map_err(|e| format!("Failed to send input request: {}", e))?;

            // Block the thread and wait for the GUI to reply
            receiver
                .borrow_mut()
                .recv()
                .map_err(|e| format!("Failed to receive input: {}", e))?
        } else {
            // Fallback: Standard Input (CLI/Test Mode)
            let mut buffer = String::new();
            if std::io::stdin().read_line(&mut buffer).is_err() {
                return Err("Failed to read from standard input".into());
            }
            buffer
        }
    };

    // 2. Process the input and update the variable
    let value = Rc::new(Object::Yarn(buffer.trim().to_string()));

    if let TokenKind::IDENTIFIER { name } = &input.identifier.kind {
        env.borrow_mut().set(name.clone(), value);
        Ok(Rc::new(Object::Noob))
    } else {
        Err(format!(
            "GIMMEH target must be an identifier, got {:?}",
            input.identifier.kind
        ))
    }
}

fn eval_recast_statement(recast: &RecastStatement, env: &Env) -> EvalResult {
    if let TokenKind::IDENTIFIER { name } = &recast.identifier.kind {
        let current_val = env
            .borrow()
            .get(name)
            .ok_or_else(|| format!("Variable '{}' not found for recast", name))?;
        let new_val = cast_object(&current_val, &recast.new_type)?;
        env.borrow_mut().set(name.clone(), new_val);
        Ok(Rc::new(Object::Noob))
    } else {
        Err("Recast target must be an identifier".into())
    }
}

fn eval_function_declaration(func_decl: &FunctionDeclaration, env: &Env) -> EvalResult {
    let func = Object::Function {
        name: func_decl.name.clone(),
        params: func_decl.params.clone(),
        body: func_decl.body.clone(),
        env: Rc::clone(env), // Capture the current environment
    };
    env.borrow_mut().set(func_decl.name.clone(), Rc::new(func));
    Ok(Rc::new(Object::Noob))
}

fn eval_if_statement(if_stmt: &If, env: &Env) -> EvalResult {
    let condition = eval_expression(&if_stmt.condition, env)?;

    env.borrow_mut()
        .set("IT".to_string(), Rc::clone(&condition));

    if is_truthy(&condition) {
        return eval_statements(&if_stmt.consequent.body, env);
    }

    for (elif_cond, elif_block) in &if_stmt.elif_branches {
        let condition = eval_expression(elif_cond, env)?;

        env.borrow_mut()
            .set("IT".to_string(), Rc::clone(&condition));

        if is_truthy(&condition) {
            return eval_statements(&elif_block.body, env);
        }
    }

    if let Some(alternate) = &if_stmt.alternate {
        return eval_statements(&alternate.body, env);
    }

    Ok(Rc::new(Object::Noob))
}

fn eval_switch_statement(switch: &Switch, env: &Env) -> EvalResult {
    let condition = eval_expression(&switch.condition, env)?;

    env.borrow_mut()
        .set("IT".to_string(), Rc::clone(&condition));

    let mut found_match = false;

    for (case_expr, case_block) in &switch.cases {
        if !found_match {
            let case_val = eval_expression(case_expr, env)?;
            if are_objects_equal(&condition, &case_val) {
                found_match = true;
            }
        }

        if found_match {
            let result = eval_statements(&case_block.body, env)?;

            if let Object::BreakValue = *result {
                return Ok(Rc::new(Object::Noob));
            }

            if let Object::ReturnValue(_) = *result {
                return Ok(result);
            }
        }
    }

    if let Some(default_block) = &switch.default {
        let result = eval_statements(&default_block.body, env)?;

        // Even in default, catch GTFO so it doesn't crash the program
        if let Object::BreakValue = *result {
            return Ok(Rc::new(Object::Noob));
        }
        // Propagate returns
        if let Object::ReturnValue(_) = *result {
            return Ok(result);
        }
    }

    Ok(Rc::new(Object::Noob))
}

fn eval_loop_statement(loop_stmt: &LoopStatement, env: &Env) -> EvalResult {
    if let TokenKind::IDENTIFIER { name: var_name } = &loop_stmt.variable.kind {
        loop {
            // 1. Check condition (if it exists)
            if let Some(cond) = &loop_stmt.condition {
                let cond_val = eval_expression(&cond.expr, env)?;
                let should_break = match cond.condition.kind {
                    TokenKind::WILE => !is_truthy(&cond_val),
                    TokenKind::TIL => is_truthy(&cond_val),
                    _ => return Err("Invalid loop condition type".into()),
                };
                if should_break {
                    break;
                }
            }

            // 2. Execute body
            let result = eval_statements(&loop_stmt.body.body, env)?;
            match *result {
                Object::ReturnValue(_) => return Ok(result), // Propagate return
                Object::BreakValue => break,                 // Handle GTFO
                _ => {}
            }

            // 3. Update counter variable
            let counter_obj = env
                .borrow()
                .get(var_name)
                .ok_or_else(|| format!("Loop variable '{}' disappeared", var_name))?;
            if let Object::Numbr(i) = *counter_obj {
                let new_val = match loop_stmt.operation.kind {
                    TokenKind::UPPIN => i + 1,
                    TokenKind::NERFIN => i - 1,
                    _ => return Err("Invalid loop operation".into()),
                };
                env.borrow_mut()
                    .set(var_name.clone(), Rc::new(Object::Numbr(new_val)));
            } else {
                return Err(format!("Loop counter '{}' must be a NUMBR", var_name));
            }
        }
        Ok(Rc::new(Object::Noob))
    } else {
        Err("Loop variable must be an identifier".into())
    }
}

/// Evaluates an expression node from the AST.
fn eval_expression(expression: &Expression, env: &Env) -> EvalResult {
    match expression {
        Expression::LITERAL(lit) => eval_literal(lit),
        Expression::IDENTIFIER(id) => eval_identifier(id, env),
        Expression::PREFIX(prefix_expr) => eval_prefix_expression(prefix_expr, env),
        Expression::FunctionCall(call) => eval_function_call(call, env),
        Expression::Typecast(cast) => {
            let val = eval_expression(&cast.expression, env)?;
            cast_object(&val, &cast.target_type)
        }
    }
}

fn eval_literal(literal: &Literal) -> EvalResult {
    match literal {
        Literal::NUMBR(n) => Ok(Rc::new(Object::Numbr(n.raw))),
        Literal::NUMBAR(n) => Ok(Rc::new(Object::Numbar(n.raw))),
        Literal::YARN(y) => Ok(Rc::new(Object::Yarn(y.raw.clone()))),
        Literal::TROOF(t) => Ok(Rc::new(Object::Troof(t.raw))),
    }
}

fn eval_identifier(id: &IDENTIFIER, env: &Env) -> EvalResult {
    match id.name.as_str() {
        "WIN" => Ok(Rc::new(Object::Troof(true))),
        "FAIL" => Ok(Rc::new(Object::Troof(false))),
        _ => env
            .borrow()
            .get(&id.name)
            .ok_or_else(|| format!("Identifier not found: {}", id.name)),
    }
}

fn eval_function_call(call: &FunctionCall, env: &Env) -> EvalResult {
    let func_obj = env
        .borrow()
        .get(&call.name.name)
        .ok_or_else(|| format!("Function '{}' not found", call.name.name))?;

    if let Object::Function {
        name: _,
        params,
        body,
        env: func_env,
    } = &*func_obj
    {
        if params.len() != call.arguments.len() {
            return Err(format!(
                "Function '{}' expected {} arguments but got {}",
                call.name.name,
                params.len(),
                call.arguments.len()
            ));
        }

        let mut args = Vec::new();
        for arg_expr in &call.arguments {
            args.push(eval_expression(arg_expr, env)?);
        }

        // Create a new environment for the function call, enclosed by the function's definition environment
        let mut extended_env = Environment::new_isolated(func_env);
        for (param, arg) in params.iter().zip(args) {
            extended_env.set(param.name.clone(), arg);
        }

        let evaluated = eval_statements(&body.body, &Rc::new(RefCell::new(extended_env)))?;

        // Unwrap the return value if it exists
        if let Object::ReturnValue(val) = &*evaluated {
            return Ok(Rc::clone(val));
        }

        if let Object::BreakValue = *evaluated {
            return Ok(Rc::new(Object::Noob)); // Functions return NOOB on break
        }

        Ok(evaluated) // Implicit return of the last evaluated statement
    } else {
        Err(format!("'{}' is not a function", call.name.name))
    }
}

/// It handles all operators like SUM OF, BOTH SAEM, etc.
fn eval_prefix_expression(prefix: &PrefixExpression, env: &Env) -> EvalResult {
    match prefix {
        PrefixExpression::Unary(unary_expr) => {
            let operand = eval_expression(&unary_expr.operand, env)?;
            match unary_expr.op.kind {
                TokenKind::NOT => Ok(Rc::new(Object::Troof(!is_truthy(&operand)))),
                _ => Err(format!("Unknown unary operator: {:?}", unary_expr.op.kind)),
            }
        }
        PrefixExpression::Binary(bin_expr) => {
            let left = eval_expression(&bin_expr.left, env)?;
            let right = eval_expression(&bin_expr.right, env)?;

            // Coerce NUMBR to NUMBAR if mixed for arithmetic
            let (left_f, right_f, is_float) = coerce_to_float(&left, &right);

            match bin_expr.op.kind {
                // Arithmetic
                TokenKind::SUM => {
                    if is_float {
                        Ok(Rc::new(Object::Numbar(left_f + right_f)))
                    } else {
                        Ok(Rc::new(Object::Numbr(left.as_numbr()? + right.as_numbr()?)))
                    }
                }
                TokenKind::DIFF => {
                    if is_float {
                        Ok(Rc::new(Object::Numbar(left_f - right_f)))
                    } else {
                        Ok(Rc::new(Object::Numbr(left.as_numbr()? - right.as_numbr()?)))
                    }
                }
                TokenKind::PRODUKT => {
                    if is_float {
                        Ok(Rc::new(Object::Numbar(left_f * right_f)))
                    } else {
                        Ok(Rc::new(Object::Numbr(left.as_numbr()? * right.as_numbr()?)))
                    }
                }
                TokenKind::QUOSHUNT => {
                    if right_f == 0.0 {
                        return Err("Division by zero".into());
                    }
                    Ok(Rc::new(Object::Numbar(left_f / right_f)))
                }
                TokenKind::MOD => {
                    let num = left.as_numbr()?;
                    let denom = right.as_numbr()?;

                    if denom == 0 {
                        return Err("Modulo by zero".into());
                    }

                    Ok(Rc::new(Object::Numbr(num % denom)))
                }
                // Comparison
                TokenKind::BIGGR => {
                    if is_float {
                        Ok(Rc::new(Object::Numbar(left_f.max(right_f))))
                    } else {
                        Ok(Rc::new(Object::Numbr(
                            left.as_numbr()?.max(right.as_numbr()?),
                        )))
                    }
                }
                TokenKind::SMALLR => {
                    if is_float {
                        Ok(Rc::new(Object::Numbar(left_f.min(right_f))))
                    } else {
                        Ok(Rc::new(Object::Numbr(
                            left.as_numbr()?.min(right.as_numbr()?),
                        )))
                    }
                }
                TokenKind::BothSaem => Ok(Rc::new(Object::Troof(are_objects_equal(&left, &right)))),
                TokenKind::DIFFRINT => {
                    Ok(Rc::new(Object::Troof(!are_objects_equal(&left, &right))))
                }

                // Boolean
                TokenKind::BothOf => Ok(Rc::new(Object::Troof(
                    is_truthy(&left) && is_truthy(&right),
                ))),
                TokenKind::EitherOf => Ok(Rc::new(Object::Troof(
                    is_truthy(&left) || is_truthy(&right),
                ))),
                TokenKind::WonOf => {
                    Ok(Rc::new(Object::Troof(is_truthy(&left) ^ is_truthy(&right))))
                }

                _ => Err(format!("Unknown binary operator: {:?}", bin_expr.op.kind)),
            }
        }
        PrefixExpression::Multi(multi_expr) => {
            let mut args = Vec::new();
            for arg_expr in &multi_expr.args {
                args.push(eval_expression(arg_expr, env)?);
            }

            match multi_expr.op.kind {
                TokenKind::AllOf => {
                    for arg in args {
                        if !is_truthy(&arg) {
                            return Ok(Rc::new(Object::Troof(false)));
                        }
                    }
                    Ok(Rc::new(Object::Troof(true)))
                }
                TokenKind::AnyOf => {
                    for arg in args {
                        if is_truthy(&arg) {
                            return Ok(Rc::new(Object::Troof(true)));
                        }
                    }
                    Ok(Rc::new(Object::Troof(false)))
                }
                TokenKind::SMOOSH => {
                    let mut result = String::new();
                    for arg in args {
                        result.push_str(&object_to_yarn(&arg));
                    }
                    Ok(Rc::new(Object::Yarn(result)))
                }
                _ => Err(format!(
                    "Unknown multi-arg operator: {:?}",
                    multi_expr.op.kind
                )),
            }
        }
    }
}

/// A "truthy" value is anything that is not FAIL or NOOB.
fn is_truthy(obj: &Object) -> bool {
    match obj {
        Object::Troof(false) => false,
        Object::Noob => false,
        Object::Numbr(0) => false,
        Object::Numbar(n) if *n == 0.0 => false,
        Object::Yarn(s) if s.is_empty() => false,
        _ => true,
    }
}

/// Checks for logical equality between two LOLCODE objects.
fn are_objects_equal(left: &Object, right: &Object) -> bool {
    match (left, right) {
        (Object::Noob, Object::Noob) => true,
        (Object::Numbr(l), Object::Numbr(r)) => l == r,
        (Object::Numbar(l), Object::Numbar(r)) => l == r,
        // Coerce and compare mixed numbers
        (Object::Numbr(l), Object::Numbar(r)) => (*l as f64) == *r,
        (Object::Numbar(l), Object::Numbr(r)) => *l == (*r as f64),
        (Object::Yarn(l), Object::Yarn(r)) => l == r,
        (Object::Troof(l), Object::Troof(r)) => l == r,
        _ => false, // Different types are not equal
    }
}

/// Converts any object to its YARN representation for SMOOSH or casting.
fn object_to_yarn(obj: &Object) -> String {
    match obj {
        Object::Numbr(n) => n.to_string(),
        Object::Numbar(n) => n.to_string(),
        Object::Yarn(s) => s.clone(),
        Object::Troof(b) => {
            if *b {
                "WIN".to_string()
            } else {
                "FAIL".to_string()
            }
        }
        Object::Noob => "NOOB".to_string(),
        Object::Function { name, .. } => format!("<fn:{}>", name),
        _ => "".to_string(), // Should not happen with user values
    }
}

/// Handles explicit type casting logic.
fn cast_object(obj: &Object, target_type: &LolType) -> EvalResult {
    let result = match target_type {
        LolType::NUMBR => Object::Numbr(match obj {
            Object::Numbr(n) => *n,
            Object::Numbar(n) => *n as i64,
            Object::Yarn(s) => s.parse().unwrap_or(0),
            Object::Troof(b) => {
                if *b {
                    1
                } else {
                    0
                }
            }
            _ => 0,
        }),
        LolType::NUMBAR => Object::Numbar(match obj {
            Object::Numbr(n) => *n as f64,
            Object::Numbar(n) => *n,
            Object::Yarn(s) => s.parse().unwrap_or(0.0),
            Object::Troof(b) => {
                if *b {
                    1.0
                } else {
                    0.0
                }
            }
            _ => 0.0,
        }),
        LolType::YARN => Object::Yarn(object_to_yarn(obj)),
        LolType::TROOF => Object::Troof(is_truthy(obj)),
    };
    Ok(Rc::new(result))
}

/// Helper to coerce mixed NUMBR/NUMBAR types for arithmetic.
/// Returns (left_as_float, right_as_float, should_use_float_math)
fn coerce_to_float(left: &Object, right: &Object) -> (f64, f64, bool) {
    // Helper closure to get the float value and determine if it forces float context
    let get_val = |obj: &Object| -> (f64, bool) {
        match obj {
            Object::Numbar(n) => (*n, true), // Explicit Numbar forces float
            Object::Numbr(n) => (*n as f64, false),
            Object::Yarn(s) => {
                // If it parses as int, it's a number, but doesn't force float math
                if let Ok(i) = s.parse::<i64>() {
                    (i as f64, false)
                }
                // If it fails int parse but passes float parse (e.g. "3.5"), force float
                else if let Ok(f) = s.parse::<f64>() {
                    (f, true)
                } else {
                    (0.0, false) // Invalid strings are 0.0 here, but will error in as_numbr
                }
            }
            Object::Troof(b) => (if *b { 1.0 } else { 0.0 }, false),
            Object::Noob => (0.0, false),
            _ => (0.0, false),
        }
    };

    let (left_f, left_forces_float) = get_val(left);
    let (right_f, right_forces_float) = get_val(right);

    // If either operand is strictly a float type (Numbar or "3.14" string), use float math
    (left_f, right_f, left_forces_float || right_forces_float)
}

// Add a helper trait to easily extract NUMBR value with implicit casting.
trait AsNumbr {
    fn as_numbr(&self) -> Result<i64, String>;
}

impl AsNumbr for Object {
    fn as_numbr(&self) -> Result<i64, String> {
        match self {
            Object::Numbr(n) => Ok(*n),
            Object::Numbar(n) => Ok(*n as i64), // Truncate float
            Object::Yarn(s) => {
                if s.trim().is_empty() {
                    return Ok(0);
                }

                s.trim()
                    .parse::<i64>()
                    .map_err(|_| format!("YARN '{}' could not be implicitly cast to NUMBR", s))
            }
            Object::Troof(b) => Ok(if *b { 1 } else { 0 }), // WIN -> 1, FAIL -> 0
            Object::Noob => Ok(0),
            _ => Err(format!("Cannot implicitly cast type to NUMBR: {:?}", self)),
        }
    }
}
