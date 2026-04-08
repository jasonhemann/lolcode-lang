mod app;
mod components;
mod console;
mod editor;
mod symbol_table;
mod theme;
mod token_list;
mod top_bar;

use std::path::PathBuf;

use app::MainApp;
use iced::{
    Color, Font, Result, advanced::graphics::core::window, application, daemon::Appearance,
};

use crate::app::app::Theme;

pub fn main() -> Result {
    let icon_path = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("assets/images/icon.png");
    let icon = iced::window::icon::from_file(icon_path).expect("Failed to load window icon");
    let window = window::Settings {
        icon: Some(icon),
        ..Default::default()
    };
    application("LolCode Interpreter", MainApp::update, MainApp::view)
        .font(include_bytes!("../assets/fonts/Rubik-SemiBold.ttf").as_slice())
        .font(include_bytes!("../assets/fonts/FiraMono-Regular.ttf").as_slice())
        .default_font(Font::with_name("Fira Mono"))
        .window(window)
        .exit_on_close_request(true)
        .centered()
        .style(|state, _theme| {
            let is_dark = matches!(state.current_theme, Theme::Dark);

            if is_dark {
                Appearance {
                    background_color: Color::from_rgb(0.10, 0.12, 0.16),
                    text_color: Color::WHITE,
                }
            } else {
                Appearance {
                    background_color: Color::from_rgb(0.94, 0.97, 1.0),
                    text_color: Color::BLACK,
                }
            }
        })
        .subscription(MainApp::subscription)
        .run()
}
