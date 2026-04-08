use crate::object::Object;
use std::cell::RefCell;
use std::collections::HashMap;
use std::rc::Rc;
use std::sync::mpsc::{Receiver, Sender};

pub type Env = Rc<RefCell<Environment>>;

#[derive(Debug, Clone)]
pub enum InterpreterEvent {
    RequestInput,
    Stdout(String),
    VariableUpdate { name: String, value: String },
}

#[derive(Debug, Clone)]
pub struct Environment {
    store: HashMap<String, Rc<Object>>,
    outer: Option<Env>,
    pub event_sender: Option<Sender<InterpreterEvent>>,
    pub input_receiver: Option<Rc<RefCell<Receiver<String>>>>,
}

impl Environment {
    pub fn new(event_sender: Sender<InterpreterEvent>, input_receiver: Receiver<String>) -> Self {
        let mut new_env = Environment::default();

        new_env.event_sender = Some(event_sender);
        new_env.input_receiver = Some(Rc::new(RefCell::new(input_receiver)));

        new_env
    }

    pub fn new_isolated(outer: &Env) -> Self {
        let mut env = Environment::default();

        let parent = outer.borrow();

        env.event_sender = parent.event_sender.clone();
        env.input_receiver = parent.input_receiver.clone();

        env
    }

    pub fn get(&self, name: &str) -> Option<Rc<Object>> {
        match self.store.get(name) {
            Some(obj) => Some(Rc::clone(obj)),
            None => self.outer.as_ref().and_then(|o| o.borrow().get(name)),
        }
    }

    pub fn set(&mut self, name: String, value: Rc<Object>) {
        self.store.insert(name.clone(), value.clone());

        if let Some(sender) = &self.event_sender {
            let _ = sender.send(InterpreterEvent::VariableUpdate {
                name,
                value: value.to_string(),
            });
        }
    }
}

impl Default for Environment {
    fn default() -> Self {
        let mut store = HashMap::new();

        store.insert("IT".to_string(), Rc::new(Object::Noob));

        Self {
            store,
            outer: None,
            event_sender: None,
            input_receiver: None,
        }
    }
}
