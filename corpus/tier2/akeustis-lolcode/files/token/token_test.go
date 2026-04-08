package token

import (
	"bufio"
	"strings"
	"testing"
)

const lolCode = `HAI 1.2
tok0,tok1 BTW comments here, including some commas
tok2

	BTW full line comment
tok3 BTW, OBTW doesnt work here
tok4	 OBTW   illegal comment
tok5, OBTW legal comment,, TLDR tok6,,,
tok7, OBTW legal comment TLDR
BTW that TLDR doesn't work lulz, TLDR BTW
KTHXBYE
`

func TestEmitFragments(t *testing.T) {
	expected := []string{"HAI", "1.2", EOLPhrase,
		"tok0", EOLPhrase, "tok1", EOLPhrase,
		"tok2", EOLPhrase,
		"tok3", EOLPhrase,
		"tok4", "OBTW", "illegal", "comment", EOLPhrase,
		"tok5", EOLPhrase,
		"tok6", EOLPhrase,
		"tok7", EOLPhrase,
		"KTHXBYE", EOLPhrase}
	reader := bufio.NewReader(strings.NewReader(lolCode))
	fragments := make(chan string, 100)
	go emitFragments(reader, fragments)
	i := 0
	for fragment := range fragments {
		if fragment != expected[i] {
			t.Fatalf("Expected: %s Got: %s", expected[i], fragment)
		}
		i++
	}
	if i != len(expected) {
		t.Fatalf("Expected %d tokens, got %d", len(expected), i)
	}
}

const lolCode2 = `HAI 1.2
I HAS A FISH ITZ 5
BTW full line comment
OBTW,TLDR 
FISH R "foo"
WIN,FAIL,NOOB
KTHXBYE

`

func TestEmitTokens(t *testing.T) {
	L := func(i interface{}) Token {
		return Token{Literal, i}
	}
	I := func(s string) Token {
		return Token{Ident, s}
	}
	EOL := Token{EOL, EOLPhrase}
	expected := []Token{
		Token{TokHAI, "HAI"}, L(float64(1.2)), EOL,
		Token{IHASA, "I HAS A"}, I("FISH"), Token{ITZ, "ITZ"}, L(int64(5)), EOL,
		I("FISH"), Token{R, "R"}, L("foo"), EOL,
		L(true), EOL, L(false), EOL, L(nil), EOL,
		Token{KTHXBYE, "KTHXBYE"}, EOL,
	}
	reader := bufio.NewReader(strings.NewReader(lolCode2))
	tokens := make(chan Token, 100)
	go EmitTokens(reader, tokens)
	i := 0
	for token := range tokens {
		if token != expected[i] {
			t.Fatalf("Expected: %v Got: %v", expected[i], token)
		}
		i++
	}
	if i != len(expected) {
		t.Fatalf("Expected %d tokens, got %d", len(expected), i)
	}
}

func TestIsIdentifier(t *testing.T) {
	identifiers := []string{
		"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_",
		"MY_VAR1",
		"f__1_0",
		"k",
	}
	for _, id := range identifiers {
		if !isIdentifier(id) {
			t.Fatalf("expected %s to be an identifier", id)
		}
	}
	nonIdentifiers := []string{
		"_v", "4ever", "$v", "k-1", "p[]",
	}
	for _, id := range nonIdentifiers {
		if isIdentifier(id) {
			t.Fatalf("expected %s to not be an identifier", id)
		}
	}
}
