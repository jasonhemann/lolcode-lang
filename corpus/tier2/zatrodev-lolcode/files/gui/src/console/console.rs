use crate::theme::{TITLE_FONT, ThemeColors};
use iced::border::Radius;
use iced::widget::scrollable::{Rail, Scroller};
use iced::widget::text::Wrapping;
use iced::widget::text_editor::{Action, Edit, Motion};
use iced::widget::{Scrollable, Text, TextEditor, column, container, scrollable, text_editor};
use iced::{Background, Border, Element, Length, Shadow};
use std::sync::Arc;

use super::ConsoleMessage;

#[derive(Default)]
pub struct Console {
    pub content: text_editor::Content,
    pub is_input_enabled: bool,
}

impl Console {
    pub fn update(&mut self, message: ConsoleMessage) -> Option<String> {
        match message {
            ConsoleMessage::ConsoleMsg(action) => {
                // Only allow editing if input is enabled.
                if !self.is_input_enabled && action.is_edit() {
                    return None;
                }

                self.content.perform(action);
                None
            }

            ConsoleMessage::Submit => {
                let full_text = self.content.text();

                if let Some(last_line) = full_text.lines().last() {
                    let user_input = last_line.to_string();

                    // Handle "clear"
                    if user_input.trim().to_lowercase() == "clear" {
                        self.clear();
                        return None;
                    }

                    self.append_text("\n");

                    return Some(user_input);
                }
                None
            }
        }
    }

    pub fn set_text(&mut self, text: &str) {
        self.content = text_editor::Content::with_text(text);
    }

    pub fn append_text(&mut self, text: &str) {
        // Move cursor to the end of the document
        self.content.perform(Action::Move(Motion::DocumentEnd));

        // Paste the new text at that position
        self.content
            .perform(Action::Edit(Edit::Paste(Arc::new(text.to_string()))));
    }

    pub fn clear(&mut self) {
        self.content = text_editor::Content::with_text("");
    }

    pub fn view(&self, theme: &ThemeColors) -> Element<'_, ConsoleMessage> {
        let text_color = theme.console_text;
        let console_panel_color = theme.console;

        let border_color = if self.is_input_enabled {
            theme.side_panel
        } else {
            theme.border
        };

        let selection_color = theme.text_selection;
        let scroll_track_color = theme.scroll_track;
        let label_color = theme.label;

        // Inner console_content
        let console_content = TextEditor::new(&self.content)
            .wrapping(Wrapping::WordOrGlyph)
            .on_action(|action| {
                // Intercept "Enter" key
                match action {
                    Action::Edit(Edit::Enter) => ConsoleMessage::Submit,
                    _ => ConsoleMessage::ConsoleMsg(action),
                }
            })
            .style(move |_theme: &iced::Theme, _status| text_editor::Style {
                background: Background::Color(console_panel_color),
                value: text_color,
                border: Border {
                    color: border_color,
                    width: 0.0,
                    radius: Radius::new(10),
                },
                placeholder: text_color,
                selection: selection_color,
                icon: text_color,
            });

        // Scrollable with custom track
        let scrollable_console = Scrollable::new(console_content)
            .width(Length::Fill)
            .height(Length::Fill)
            .style(move |_theme: &iced::Theme, _status| scrollable::Style {
                container: container::Style {
                    background: Some(Background::Color(console_panel_color)),
                    text_color: Some(text_color),
                    border: Border {
                        color: border_color,
                        width: 0.0,
                        radius: Radius::new(10),
                    },
                    shadow: Shadow::default(),
                },
                vertical_rail: Rail {
                    background: Some(Background::Color(console_panel_color)),
                    border: Border::default(),
                    scroller: Scroller {
                        color: scroll_track_color,
                        border: Border::default(),
                    },
                },
                horizontal_rail: Rail {
                    background: Some(Background::Color(console_panel_color)),
                    border: Border::default(),
                    scroller: Scroller {
                        color: scroll_track_color,
                        border: Border::default(),
                    },
                },
                gap: Some(Background::Color(console_panel_color)),
            });

        // Outer border container
        let bordered_console = container(scrollable_console)
            .width(Length::Fill)
            .height(Length::Fill)
            .style(move |_theme: &iced::Theme| container::Style {
                background: Some(Background::Color(console_panel_color)),
                text_color: Some(text_color),
                border: Border {
                    color: border_color,
                    width: if self.is_input_enabled { 2.0 } else { 1.5 },
                    radius: Radius::new(10),
                },
                shadow: Shadow::default(),
            });

        // Label + console
        let console_area = column![
            Text::new("Console").color(label_color).font(TITLE_FONT),
            bordered_console,
        ];

        console_area
            .width(Length::FillPortion(2))
            .height(Length::Fill)
            .into()
    }
}
