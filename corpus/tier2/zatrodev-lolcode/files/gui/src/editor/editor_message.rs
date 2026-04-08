use iced::widget::text_editor;

#[derive(Debug, Clone)]
pub enum EditorMessage {
    Edit(text_editor::Action),
    InsertTab,
}

