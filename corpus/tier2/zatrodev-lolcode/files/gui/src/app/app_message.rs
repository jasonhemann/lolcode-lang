use interpreter::environment::InterpreterEvent;

#[derive(Debug, Clone)]
pub enum Message {
    Edit(crate::editor::EditorMessage),
    ConsoleMsg(crate::console::ConsoleMessage),
    Editor(crate::editor::EditorMessage),
    TopBar(crate::top_bar::TopBarMessage),
    NoOp,
    InterpreterEvent(InterpreterEvent),
    InterpreterFinished,
}
