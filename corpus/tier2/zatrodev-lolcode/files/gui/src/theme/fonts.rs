use iced::Font;

pub const TITLE_FONT: Font = Font {
    family: iced::font::Family::Name("Rubik"),
    weight: iced::font::Weight::Semibold,
    stretch: iced::font::Stretch::Normal,
    style: iced::font::Style::Normal,
};

pub const MAIN_FONT: Font = Font::with_name("Fira Mono");
