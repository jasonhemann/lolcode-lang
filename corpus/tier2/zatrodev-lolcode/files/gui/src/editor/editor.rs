use crate::editor::highlighter::LolCodeHighlighter;
use crate::theme::ThemeColors;
use iced::border::Radius;
use iced::widget::scrollable::{Rail, Scroller};
use iced::widget::{Scrollable, Text, TextEditor};
use iced::widget::{column, container, row, scrollable, text::Wrapping, text_editor};
use iced::{Background, Border, Color, Element, Length, Padding, Shadow};

use super::EditorMessage;

const OVERFLOW_LENGTH: usize = 52;

#[derive(Default)]
pub struct TextEditorContainer {
    pub content: text_editor::Content,
}

impl TextEditorContainer {
    pub fn update(&mut self, message: EditorMessage) {
        match message {
            EditorMessage::Edit(action) => {
                self.content.perform(action);
            }
            EditorMessage::InsertTab => {
                let tab_char = "    ";
                self.content
                    .perform(text_editor::Action::Edit(text_editor::Edit::Paste(
                        std::sync::Arc::new(tab_char.to_string()),
                    )));
            }
        }
    }

    pub fn view(&self, theme: &ThemeColors) -> Element<'_, EditorMessage> {
        let text_color = theme.text_editor_text;
        let editor_panel_color = theme.text_editor;
        let border_color = theme.border;
        let label_color = theme.label;
        let line_color = theme.label_light;
        let selection_color = theme.text_selection;
        let scroll_track_color = theme.scroll_track;

        // Line numbers
        let mut line_numbers_col = column![].width(40).padding(Padding::ZERO.top(5));

        let binding = self.content.text();
        let content_split: Vec<&str> = binding.split("\n").collect();

        for i in 1..=self.content.line_count() {
            let content_in_line = content_split[i - 1];

            if content_in_line.len() > OVERFLOW_LENGTH {
                let multiply_factor = content_in_line.len() / OVERFLOW_LENGTH;

                line_numbers_col =
                    line_numbers_col.push(Text::new(format!("{:>3}", i)).color(line_color));

                for _ in 0..multiply_factor {
                    line_numbers_col = line_numbers_col.push(Text::new(" "));
                }
            } else {
                line_numbers_col =
                    line_numbers_col.push(Text::new(format!("{:>3}", i)).color(line_color));
            }
        }

        // Inner text editor
        let editor = TextEditor::new(&self.content)
            .wrapping(Wrapping::WordOrGlyph)
            .on_action(EditorMessage::Edit)
            .height(Length::Shrink)
            .highlight_with::<LolCodeHighlighter>((), |style, _theme| {
                iced::advanced::text::highlighter::Format {
                    color: style.color,
                    font: None,
                }
            })
            .style(move |_theme: &iced::Theme, _status| text_editor::Style {
                value: text_color,
                placeholder: text_color,
                selection: selection_color,
                icon: text_color,
                background: Background::Color(Color::TRANSPARENT),
                border: Border::default(),
            });

        let editor_with_lines = row![line_numbers_col, editor];

        let scrollable_container =
            Scrollable::new(editor_with_lines).style(move |_theme: &iced::Theme, _status| {
                scrollable::Style {
                    container: container::Style {
                        background: Some(Background::Color(editor_panel_color)),
                        text_color: Some(text_color),
                        border: Border {
                            color: border_color,
                            width: 0.0,
                            radius: Radius::new(10),
                        },
                        shadow: Shadow::default(),
                    },
                    vertical_rail: Rail {
                        background: Some(Background::Color(editor_panel_color)),
                        border: Border::default(),
                        scroller: Scroller {
                            color: scroll_track_color,
                            border: Border::default(),
                        },
                    },
                    horizontal_rail: Rail {
                        background: Some(Background::Color(editor_panel_color)),
                        border: Border::default(),
                        scroller: Scroller {
                            color: scroll_track_color,
                            border: Border::default(),
                        },
                    },
                    gap: Some(Background::Color(editor_panel_color)),
                }
            });

        let editor_container = container(scrollable_container)
            .padding(Padding::ZERO.top(8).bottom(8))
            .height(Length::Fill)
            .style(move |_| container::Style {
                background: Some(Background::Color(editor_panel_color)),
                text_color: Some(text_color),
                border: Border {
                    color: border_color,
                    width: 0.0,
                    radius: Radius::new(10),
                },
                shadow: Shadow::default(),
            });

        column![Text::new("").color(label_color), editor_container]
            .width(Length::FillPortion(3))
            .height(Length::Fill)
            .into()
    }
}
