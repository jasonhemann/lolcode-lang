use crate::components::table_entry;
use crate::theme::{MAIN_FONT, TITLE_FONT, ThemeColors};
use iced::border::Radius;
use iced::widget::scrollable::{self, Rail, Scroller};
use iced::widget::{Container, Scrollable, Text, column, container, row};
use iced::{Alignment, Background, Border, Element, Length, Padding, Shadow};

#[derive(Debug, Clone)]
pub struct SymbolTableEntry {
    pub identifier: String,
    pub value: String,
}

#[derive(Default)]
pub struct SymbolTable {
    pub entries: Vec<SymbolTableEntry>,
}

impl SymbolTable {
    fn add_entry(&mut self, identifier: &str, value: &str) {
        self.entries.push(SymbolTableEntry {
            identifier: identifier.to_string(),
            value: value.to_string(),
        });
    }

    pub fn update_entry(&mut self, identifier: &str, value: &str) {
        if let Some(entry) = self.entries.iter_mut().find(|e| e.identifier == identifier) {
            entry.value = value.to_string();
        } else {
            self.add_entry(identifier, value);
        }
    }

    pub fn clear(&mut self) {
        self.entries.clear();
    }

    pub fn view<'a>(&'a self, theme: &'a ThemeColors) -> Element<'a, ()> {
        let text_color = theme.text_editor_text;
        let side_panel_color = theme.side_panel;
        let border_color = theme.border;
        let label_color = theme.label;
        let scroll_track_color = theme.scroll_track;

        let header = row![
            table_entry(
                "Identifier",
                theme,
                MAIN_FONT,
                theme.table_header,
                theme.table_header_text,
                Length::Fill,
                Length::Shrink
            ),
            table_entry(
                "Value",
                theme,
                MAIN_FONT,
                theme.table_header,
                theme.table_header_text,
                Length::Fill,
                Length::Shrink
            ),
        ]
        .align_y(Alignment::Center)
        .padding(Padding {
            top: 0.0,
            right: 10.0,
            bottom: 0.0,
            left: 0.0,
        });

        let rows = Self::build_rows(&self.entries, theme, header);

        let content = Scrollable::new(rows)
            .width(Length::Fill)
            .height(Length::Fill)
            .style(move |_theme: &iced::Theme, _status| scrollable::Style {
                container: container::Style {
                    background: Some(Background::Color(side_panel_color)),
                    text_color: Some(text_color),
                    border: Border {
                        color: border_color,
                        width: 0.0,
                        radius: Radius::new(10),
                    },
                    shadow: Shadow::default(),
                },
                vertical_rail: Rail {
                    background: Some(Background::Color(side_panel_color)),
                    border: Border::default(),
                    scroller: Scroller {
                        color: scroll_track_color,
                        border: Border::default(),
                    },
                },
                horizontal_rail: Rail {
                    background: Some(Background::Color(side_panel_color)),
                    border: Border::default(),
                    scroller: Scroller {
                        color: scroll_track_color,
                        border: Border::default(),
                    },
                },
                gap: Some(Background::Color(side_panel_color)),
            });

        let panel = Container::new(content)
            .style(move |_theme: &iced::Theme| container::Style {
                background: Some(Background::Color(side_panel_color)),
                text_color: Some(text_color),
                border: Border {
                    color: border_color,
                    width: 1.5,
                    radius: Radius::new(10),
                },
                shadow: Shadow::default(),
            })
            .width(Length::Fill)
            .height(Length::Fill);
        let label = Text::new("Symbol Table")
            .color(label_color)
            .font(TITLE_FONT);

        column!(label, panel).into()
    }

    fn build_rows<'a>(
        entries: &'a [SymbolTableEntry],
        theme: &'a ThemeColors,
        header: iced::widget::Row<'a, ()>,
    ) -> iced::widget::Column<'a, ()> {
        entries
            .iter()
            .enumerate()
            .fold(column![header], |col, (i, entry)| {
                let (bg, text) = if i % 2 == 0 {
                    (theme.table_row, theme.table_row_text)
                } else {
                    (theme.table_row_alt, theme.table_row_alt_text)
                };

                col.push(
                    row![
                        table_entry(
                            &entry.identifier,
                            theme,
                            MAIN_FONT,
                            bg,
                            text,
                            Length::FillPortion(1),
                            Length::Shrink
                        ),
                        table_entry(
                            &entry.value,
                            theme,
                            MAIN_FONT,
                            bg,
                            text,
                            Length::FillPortion(1),
                            Length::Shrink
                        )
                    ]
                    .align_y(Alignment::Center)
                    .padding(Padding {
                        top: 0.0,
                        right: 10.0,
                        bottom: 0.0,
                        left: 0.0,
                    }),
                )
            })
    }
}
