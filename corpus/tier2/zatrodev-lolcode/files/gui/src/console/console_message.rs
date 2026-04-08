use iced::widget::text_editor;

#[derive(Debug, Clone)]
pub enum ConsoleMessage {
    ConsoleMsg(text_editor::Action),
    Submit,
}
