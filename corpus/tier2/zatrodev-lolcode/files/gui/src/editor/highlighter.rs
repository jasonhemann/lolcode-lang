use std::ops::Range;

use iced::Color;
use iced::widget::text::{Highlighter, Style};
use lexer::Lexer;
use lexer::token::{Classification, TokenKind};

#[derive(Debug, Clone, Copy, Default)]
pub struct LolCodeHighlighter;

impl LolCodeHighlighter {
    fn get_color_for(classification: Classification) -> Color {
        let color_from_hex =
            |r: f32, g: f32, b: f32| Color::from_rgb(r / 255.0, g / 255.0, b / 255.0);

        match classification {
            // Comments: terminal_black
            Classification::Comment => color_from_hex(86.0, 95.0, 137.0),

            // Main Keywords & Structure: purple
            Classification::CodeDelimiter
            | Classification::FunctionDeclaration
            | Classification::FunctionEnd
            | Classification::FunctionReturn
            | Classification::LoopDelimiter
            | Classification::ConditionalStart
            | Classification::SwitchStart
            | Classification::BlockEnd
            | Classification::BreakStatement => color_from_hex(187.0, 154.0, 247.0),

            // Variable Operations: cyan
            Classification::VariableDeclaration
            | Classification::VariableAssignment
            | Classification::VariableReassignment
            | Classification::InputKeyword
            | Classification::OutputKeyword => color_from_hex(125.0, 207.0, 255.0),

            // Identifiers: white
            Classification::Identifier
            | Classification::ImplicitVariable
            | Classification::LoopLabel => color_from_hex(169.0, 177.0, 214.0),

            // Literals: green
            Classification::Literal => color_from_hex(158.0, 206.0, 106.0),

            // Types: orange
            Classification::IntegerType
            | Classification::FloatType
            | Classification::StringType
            | Classification::BooleanType
            | Classification::TypeCasting
            | Classification::TypeConversion => color_from_hex(255.0, 158.0, 100.0),

            // Logic/Flow: yellow
            Classification::ConditionalThen
            | Classification::ConditionalElse
            | Classification::ConditionalElseIf
            | Classification::LoopWhile
            | Classification::LoopUntil
            | Classification::SwitchCase
            | Classification::SwitchDefault => color_from_hex(224.0, 175.0, 104.0),

            // Operators: red
            Classification::ArithmeticOperator
            | Classification::ComparisonOperator
            | Classification::LogicalOperator
            | Classification::StringConcatenation
            | Classification::ArgumentDelimiter
            | Classification::ArgumentTerminator => color_from_hex(247.0, 118.0, 142.0),

            // Default/Others: fg
            _ => color_from_hex(192.0, 202.0, 245.0),
        }
    }
}

impl Highlighter for LolCodeHighlighter {
    type Settings = ();

    type Highlight = Style;

    type Iterator<'a> = Box<dyn Iterator<Item = (Range<usize>, Self::Highlight)> + 'a>;

    fn new(_settings: &Self::Settings) -> Self {
        Self // Return the struct
    }

    fn update(&mut self, _new_settings: &Self::Settings) {
        // No-op since Settings is ()
    }

    fn change_line(&mut self, _line: usize) {
        // No-op
    }

    fn highlight_line(&mut self, line: &str) -> Box<dyn Iterator<Item = (Range<usize>, Style)>> {
        let mut lexer = Lexer::new(line);
        let mut spans = Vec::new();
        let mut last_index = 0;

        loop {
            let token = lexer.next_token();
            if token.kind == TokenKind::EOF {
                break;
            }

            if token.span.start > last_index {
                spans.push((last_index..token.span.start, Style { color: None }));
            }

            let color = Self::get_color_for(token.kind.classification());
            spans.push((
                token.span.start..token.span.end,
                Style { color: Some(color) },
            ));

            last_index = token.span.end;
        }

        if last_index < line.len() {
            spans.push((last_index..line.len(), Style { color: None }));
        }

        Box::new(spans.into_iter())
    }

    fn current_line(&self) -> usize {
        0
    }
}
