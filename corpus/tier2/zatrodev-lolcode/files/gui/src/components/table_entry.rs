use crate::theme::ThemeColors;
use iced::border::Radius;
use iced::widget::text::Wrapping;
use iced::widget::{Container, Text};
use iced::{Alignment, Color, Font, Shadow, Theme};
use iced::{Background, Border, Length, widget::container};

// creates a simple rectangular container with centered text
pub fn table_entry<'a>(
    content: &'a str,
    theme: &ThemeColors,
    font: Font,
    cell_bg: Color,
    cell_text: Color,
    width: Length,
    height: Length,
) -> Container<'a, ()> {
    let border = theme.table_border;
    Container::new(
        Text::new(content)
            .font(font)
            .align_x(Alignment::Center)
            .align_y(Alignment::Center)
            .wrapping(Wrapping::WordOrGlyph),
    )
    .align_x(Alignment::Center)
    // .align_y(Alignment::Center)
    .style(move |_theme: &Theme| container::Style {
        background: Some(Background::Color(cell_bg)),
        text_color: Some(cell_text),
        border: Border {
            color: border,
            width: 1.0,
            radius: Radius::new(0),
        },
        shadow: Shadow::default(),
    })
    .width(width)
    .height(height)
    .padding(6)
}
