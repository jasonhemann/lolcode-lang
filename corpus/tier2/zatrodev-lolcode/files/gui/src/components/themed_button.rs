use crate::theme::ThemeColors;
use iced::border::Radius;
use iced::widget::row;
use iced::{Alignment, Color, Font, Shadow};
use iced::{
    Background, Border, Length, widget::Button, widget::Text, widget::button, widget::container,
};
use iced_font_awesome::fa_icon_solid;

pub fn themed_button<'a, Message: 'a>(
    label: &'a str,
    icon: &'a str,
    theme: &ThemeColors,
    font: Font,
    border_radius: f32,
    width: Length,
    height: Length,
    on_press: Message,
) -> Button<'a, Message>
where
    Message: Clone,
{
    let button_bg = theme.button;
    let button_text = theme.button_text;
    let has_label = !label.is_empty();
    let hover_button = theme.button_hover;
    let pressed_button = theme.button_pressed;
    let disabled_button = theme.button_disabled;

    let mut content_row = row![fa_icon_solid(icon).size(14.0).color(button_text)];

    if has_label {
        content_row = content_row.push(Text::new(label).color(button_text).font(font).size(14));
    }

    let content = if has_label {
        container(content_row.spacing(6).align_y(Alignment::Center))
            .width(Length::Shrink)
            .height(Length::Shrink)
            .align_x(Alignment::Center)
            .align_y(Alignment::Center)
    } else {
        container(content_row)
            .width(Length::Shrink)
            .height(Length::Shrink)
            .align_x(Alignment::Center)
            .align_y(Alignment::Center)
    };

    button(content)
        .on_press(on_press)
        .padding(10)
        .width(width)
        .height(height)
        .style(move |_theme: &iced::Theme, status| {
            use iced::widget::button::Status;

            match status {
                Status::Active => button::Style {
                    background: Some(Background::Color(button_bg)),
                    text_color: button_text,
                    border: Border {
                        color: Color::BLACK,
                        width: 0.0,
                        radius: Radius::new(border_radius),
                    },
                    shadow: Shadow::default(),
                },
                Status::Hovered => button::Style {
                    background: Some(Background::Color(hover_button)),
                    text_color: button_text,
                    border: Border {
                        color: Color::BLACK,
                        width: 0.0,
                        radius: Radius::new(border_radius),
                    },
                    shadow: Shadow::default(),
                },
                Status::Pressed => button::Style {
                    background: Some(Background::Color(pressed_button)),
                    text_color: button_text,
                    border: Border {
                        color: Color::BLACK,
                        width: 0.0,
                        radius: Radius::new(border_radius),
                    },
                    shadow: Shadow::default(),
                },
                Status::Disabled => button::Style {
                    background: Some(Background::Color(disabled_button)),
                    text_color: button_text,
                    border: Border {
                        color: Color::BLACK,
                        width: 0.0,
                        radius: Radius::new(border_radius),
                    },
                    shadow: Shadow::default(),
                },
            }
        })
}
