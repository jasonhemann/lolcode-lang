use iced::widget::text_editor::Content;
use iced::widget::{Column, column, row};
use iced::{Length, Subscription, event, keyboard, time};
use interpreter::object::Object;
use std::cell::RefCell;
use std::collections::HashSet;
use std::rc::Rc;
use std::sync::{Arc, Mutex, mpsc};
use std::time::Duration;
use std::{fs, thread};

use lexer::Lexer;
use lexer::token::TokenKind;
use native_dialog::DialogBuilder;
use parser::{Parser, ast::*};

use interpreter::environment::{Environment, InterpreterEvent};
use interpreter::eval;

use crate::app::app_message::Message;
use crate::console::Console;
use crate::editor::{EditorMessage, TextEditorContainer};
use crate::symbol_table::SymbolTable;
use crate::theme::{DARK_MODE, LIGHT_MODE, ThemeColors};
use crate::token_list::TokenList;
use crate::top_bar::{TopBar, TopBarMessage};

#[derive(Clone, Copy)]
pub enum Theme {
    Dark,
    Light,
}

#[derive(Default)]
pub struct MainApp {
    pub editor: TextEditorContainer,
    pub token_list: TokenList,
    pub symbol_table: SymbolTable,
    pub console: Console,
    pub top_bar: TopBar,
    pub current_theme: Theme,
    pub interpreter_sender: Option<mpsc::Sender<String>>,
    interpreter_receiver:
        Option<std::sync::Arc<std::sync::Mutex<mpsc::Receiver<InterpreterEvent>>>>, // FROM interpreter
}

impl Default for Theme {
    fn default() -> Self {
        Theme::Dark
    }
}

impl MainApp {
    pub fn view(&self) -> Column<'_, Message> {
        let theme_colors: &ThemeColors = match self.current_theme {
            Theme::Dark => &DARK_MODE,
            Theme::Light => &LIGHT_MODE,
        };
        let side_panels = column![
            self.token_list.view(theme_colors).map(|_| Message::NoOp),
            self.symbol_table.view(theme_colors).map(|_| Message::NoOp)
        ];

        let main_content = row![
            side_panels.spacing(8).width(Length::FillPortion(2)),
            self.editor.view(theme_colors).map(Message::Edit),
            self.console.view(theme_colors).map(Message::ConsoleMsg),
        ];

        let app = column![
            self.top_bar
                .view(theme_colors, self.current_theme)
                .map(Message::TopBar),
            main_content.spacing(16).height(Length::Fill)
        ];
        app.padding(16).spacing(20).into()
    }

    pub fn update(&mut self, message: Message) {
        match message {
            Message::Edit(msg) => self.editor.update(msg),
            Message::TopBar(msg) => {
                if let Some(msg) = self.top_bar.update(msg) {
                    match msg {
                        TopBarMessage::ToggleTheme => {
                            self.current_theme = match self.current_theme {
                                Theme::Dark => Theme::Light,
                                Theme::Light => Theme::Dark,
                            };
                        }
                        TopBarMessage::OpenFile => {
                            if let Some(path) = DialogBuilder::file()
                                .set_title("Select a file")
                                .add_filter("LOLCODE", &["lol"])
                                .open_single_file()
                                .show()
                                .unwrap()
                            {
                                println!("Picked file: {}", path.display());
                                if let Ok(contents) = fs::read_to_string(&path) {
                                    self.editor.content = Content::with_text(&contents);
                                    self.top_bar.file_path = path.to_string_lossy().to_string();
                                } else {
                                    println!("Failed to read file");
                                }
                            } else {
                                println!("No file selected");
                            }
                        }

                        TopBarMessage::RunCode => {
                            self.console.clear();
                            self.token_list.clear();
                            self.symbol_table.clear();

                            let code = self.editor.content.text();

                            let mut display_lexer = Lexer::new(&code);
                            loop {
                                let token = display_lexer.next_token();
                                let lexeme =
                                    code.get(token.span.start..token.span.end).unwrap_or("ERR");
                                if token.kind == TokenKind::EOF {
                                    break;
                                }

                                self.token_list
                                    .add_entry(lexeme, &token.kind.classification().to_string());
                            }

                            let lexer = Lexer::new(&code);
                            let mut parser = Parser::new(lexer);

                            match parser.parse_program() {
                                Ok(program) => {
                                    let mut identifiers = HashSet::new();
                                    Self::collect_identifiers_from_program(
                                        &program,
                                        &mut identifiers,
                                    );
                                    let mut symbols_to_display: Vec<_> =
                                        identifiers.into_iter().collect();
                                    symbols_to_display.sort();

                                    for name in symbols_to_display {
                                        self.symbol_table
                                            .update_entry(&name, &Object::Noob.to_string());
                                    }

                                    let (event_tx, event_rx) = mpsc::channel();
                                    let (input_tx, input_rx) = mpsc::channel();

                                    self.interpreter_sender = Some(input_tx);
                                    self.interpreter_receiver =
                                        Some(Arc::new(Mutex::new(event_rx)));

                                    thread::spawn(move || {
                                        let env = Rc::new(RefCell::new(Environment::new(
                                            event_tx.clone(),
                                            input_rx,
                                        )));

                                        let result = eval(Node::Program(program), &env);

                                        match result {
                                            Ok(val) => {
                                                // If result is not NOOB, print it
                                                let output = val.to_string();
                                                if output != "NOOB" {
                                                    let _ = event_tx
                                                        .send(InterpreterEvent::Stdout(output));
                                                }
                                            }
                                            Err(e) => {
                                                let _ = event_tx.send(InterpreterEvent::Stdout(
                                                    format!("\nRuntime Error:\n{}", e),
                                                ));
                                            }
                                        }
                                    });
                                }
                                Err(errors) => {
                                    let error_string: String =
                                        errors.iter().map(|e| format!("{}\n", e)).collect();
                                    self.console
                                        .set_text(&format!("Parse Error(s):\n{}", error_string));
                                }
                            }
                        }
                    }
                }
            }

            Message::InterpreterEvent(event) => match event {
                InterpreterEvent::Stdout(text) => {
                    self.console.append_text(&text);
                }
                InterpreterEvent::RequestInput => {
                    self.console.is_input_enabled = true;
                }
                InterpreterEvent::VariableUpdate { name, value } => {
                    self.symbol_table.update_entry(&name, &value);
                }
            },

            Message::InterpreterFinished => {
                println!("Interpreter thread finished.");
                self.interpreter_sender = None;
                self.interpreter_receiver = None;
                self.console.is_input_enabled = false;
            }

            Message::ConsoleMsg(msg) => {
                let submission = self.console.update(msg);

                if let Some(user_input) = submission {
                    if let Some(tx) = &self.interpreter_sender {
                        let _ = tx.send(user_input);

                        self.console.is_input_enabled = false;
                    } else {
                        println!("Input captured (offline): {}", user_input);
                        self.console.is_input_enabled = false;
                    }
                }
            }

            Message::Editor(EditorMessage::InsertTab) => {
                if !self.console.is_input_enabled {
                    self.editor.update(EditorMessage::InsertTab);
                }
            }

            _ => {}
        }
    }

    fn collect_identifiers_from_program(program: &Program, identifiers: &mut HashSet<String>) {
        identifiers.insert("IT".to_string());
        for stmt in &program.body {
            Self::collect_identifiers_from_statement(stmt, identifiers);
        }
    }

    fn collect_identifiers_from_statement(
        statement: &Statement,
        identifiers: &mut HashSet<String>,
    ) {
        match statement {
            Statement::Declaration(d) => {
                if let TokenKind::IDENTIFIER { name } = &d.identifier.kind {
                    identifiers.insert(name.clone());
                }
            }
            Statement::Assignment(a) => {
                if let TokenKind::IDENTIFIER { name } = &a.identifier.kind {
                    identifiers.insert(name.clone());
                }
            }
            Statement::Input(i) => {
                if let TokenKind::IDENTIFIER { name } = &i.identifier.kind {
                    identifiers.insert(name.clone());
                }
            }
            Statement::Loop(l) => {
                if let TokenKind::IDENTIFIER { name } = &l.variable.kind {
                    identifiers.insert(name.clone());
                }
                for stmt in &l.body.body {
                    Self::collect_identifiers_from_statement(stmt, identifiers);
                }
            }
            Statement::FunctionDeclaration(f) => {
                identifiers.insert(f.name.clone());
            }
            Statement::If(i) => {
                for stmt in &i.consequent.body {
                    Self::collect_identifiers_from_statement(stmt, identifiers);
                }
                for (_, block) in &i.elif_branches {
                    for stmt in &block.body {
                        Self::collect_identifiers_from_statement(stmt, identifiers);
                    }
                }
                if let Some(alt) = &i.alternate {
                    for stmt in &alt.body {
                        Self::collect_identifiers_from_statement(stmt, identifiers);
                    }
                }
            }
            Statement::Switch(s) => {
                for (_, block) in &s.cases {
                    for stmt in &block.body {
                        Self::collect_identifiers_from_statement(stmt, identifiers);
                    }
                }
                if let Some(def) = &s.default {
                    for stmt in &def.body {
                        Self::collect_identifiers_from_statement(stmt, identifiers);
                    }
                }
            }
            _ => {}
        }
    }

    pub fn subscription(&self) -> Subscription<Message> {
        let keyboard_listener = event::listen_with(|event, _status, _window| {
            if let event::Event::Keyboard(keyboard::Event::KeyPressed {
                key: keyboard::Key::Named(keyboard::key::Named::Tab),
                ..
            }) = event
            {
                // Map this directly to your MainApp Message
                return Some(Message::Editor(EditorMessage::InsertTab));
            }
            None
        });

        let interpreter_listener = if let Some(rx_arc) = &self.interpreter_receiver {
            // Poll the receiver every 5ms (feels instant)
            // This is much easier than writing a custom async stream
            let rx = rx_arc.clone();
            time::every(Duration::from_millis(5)).map(move |_| {
                // Try to drain all pending messages
                if let Ok(rx_lock) = rx.lock() {
                    if let Ok(event) = rx_lock.try_recv() {
                        return Message::InterpreterEvent(event);
                    }
                    // Check if channel is closed (thread finished)
                    if let Err(mpsc::TryRecvError::Disconnected) = rx_lock.try_recv() {
                        return Message::InterpreterFinished;
                    }
                }
                Message::NoOp // No-op if nothing happened
            })
        } else {
            Subscription::none()
        };

        Subscription::batch(vec![keyboard_listener, interpreter_listener])
    }
}
