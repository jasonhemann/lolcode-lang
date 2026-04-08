use super::TopBarMessage;
use crate::app::app::Theme;
use crate::components::themed_button;
use crate::theme::{MAIN_FONT, TITLE_FONT, ThemeColors};
use iced::border::Radius;
use iced::widget::container;
use iced::widget::{Text, row};
use iced::{Background, Border, Element, Length, Shadow};

#[derive(Default)]
pub struct TopBar {
    pub file_path: String,
}

impl TopBar {
    pub fn update(&mut self, message: TopBarMessage) -> Option<TopBarMessage> {
        match message {
            TopBarMessage::ToggleTheme => {
                println!("Toggle theme clicked");
                Some(TopBarMessage::ToggleTheme)
            }
            TopBarMessage::OpenFile => {
                println!("Open file clicked");
                Some(TopBarMessage::OpenFile)
            }
            TopBarMessage::RunCode => {
                println!("Run clicked");
                Some(TopBarMessage::RunCode)
            }
        }
    }

    pub fn view(&self, theme: &ThemeColors, current_theme: Theme) -> Element<'_, TopBarMessage> {
        let file_background = theme.file_background;
        let border_color = theme.border;
        let file_text_color = theme.file_text;

        let file_input = container(Text::new(&self.file_path))
            .padding(5)
            .width(Length::FillPortion(8))
            .height(Length::Fill)
            .style(move |_theme: &iced::Theme| container::Style {
                text_color: Some(file_text_color),
                background: Some(Background::Color(file_background)),
                border: Border {
                    color: border_color,
                    width: 1.5,
                    radius: Radius::new(10),
                },
                shadow: Shadow::default(),
            });
        let open_button = themed_button(
            "Open",
            "folder-open",
            theme,
            TITLE_FONT,
            10.0,
            Length::FillPortion(1),
            Length::Fill,
            TopBarMessage::OpenFile,
        );
        let run_button = themed_button(
            "Run",
            "play",
            theme,
            TITLE_FONT,
            10.0,
            Length::FillPortion(1),
            Length::Fill,
            TopBarMessage::RunCode,
        );
        let toggle_icon = match current_theme {
            Theme::Dark => "sun",
            Theme::Light => "moon",
        };
        let toggle_button = themed_button(
            "",
            toggle_icon,
            theme,
            MAIN_FONT,
            10.0,
            Length::Shrink,
            Length::Fill,
            TopBarMessage::ToggleTheme,
        );

        let bar = row![open_button, file_input, run_button, toggle_button];
        bar.spacing(16).height(Length::Fixed(36.0)).into()
    }
}
