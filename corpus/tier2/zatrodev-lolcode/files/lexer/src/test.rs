#[cfg(test)]
mod tests {
    use crate::Lexer;
    use crate::token::{Token, TokenKind};
    use insta::*;

    fn test_token_set(l: &mut Lexer) -> Vec<Token> {
        let mut token_vs: Vec<Token> = vec![];
        loop {
            let t = l.next_token();
            token_vs.push(t.clone());
            if t.kind == TokenKind::EOF {
                break;
            }
        }
        token_vs
    }

    pub fn test_lexer_common(name: &str, input: &str) {
        let mut l = Lexer::new(input);
        let token_vs = test_token_set(&mut l);

        assert_debug_snapshot!(name, token_vs);
    }

    #[test]
    fn test_basic() {
        test_lexer_common("basic", "HAI KTHXBYE");
    }

    #[test]
    fn test_string() {
        test_lexer_common("string", r#""hello world""#);
    }

    #[test]
    fn test_numbers() {
        test_lexer_common("numbers", "123 456.789");
    }

    #[test]
    fn test_operators() {
        test_lexer_common("operators", "SUM OF DIFF OF PRODUKT OF QUOSHUNT OF MOD OF");
    }

    #[test]
    fn test_comments() {
        test_lexer_common(
            "comments",
            r#"
            BTW This is a single-line comment
            OBTW
                This is a multi-line
                comment
            TLDR
        "#,
        );
    }

    #[test]
    fn test_identifier() {
        test_lexer_common("identifier", "variableName42");
    }

    #[test]
    fn test_span_positions() {
        test_lexer_common("spans", "HAI \"test\" 123");
    }
}
