package token

import (
	"bufio"
	"fmt"
	"strconv"
	"strings"
)

// Token is key/value pair with a int key and interface{} value
type Token struct {
	Type  int
	Value interface{}
}

func (t Token) String() string {
	return fmt.Sprint(t.Value)
}

// Exported token types
const (
	Err = iota
	TokHAI
	KTHXBYE
	Literal
	Ident
	EOL
	IHASA
	ITZ
	R
	MAEK
	ISNOW
	ANOOB
	ATROOF
	ANUMBR
	ANUMBAR
	AYARN
	IIZ
	BOTHSAEM
	DIFFRINT
	BIGGROF
	SMALLROF
	SUMOF
	DIFFOF
	PRODUKTOF
	QUOSHUNTOF
	MODOF
	NOT
	BOTHOF
	EITHEROF
	WONOF
	ANYOF
	ALLOF
	SMOOSH
	AN
	MKAY
	NumTokens
)

var phraseRoot = initPhrases([]phraseInit{
	{EOL, EOLPhrase},
	{TokHAI, "HAI"},
	{KTHXBYE, "KTHXBYE"},
	{IHASA, "I HAS A"},
	{ITZ, "ITZ"},
	{R, "R"},
	{MAEK, "MAEK"},
	{ISNOW, "IS NOW"},
	{ANOOB, "A NOOB"},
	{ATROOF, "A TROOF"},
	{ATROOF, "A YARN"},
	{ATROOF, "A NUMBR"},
	{ATROOF, "A NUMBAR"},
	{IIZ, "I IZ"},
	{BOTHSAEM, "BOTH SAEM"},
	{DIFFRINT, "DIFFRINT"},
	{BIGGROF, "BIGGR OF"},
	{SMALLROF, "SMALLR OF"},
	{SUMOF, "SUM OF"},
	{DIFFOF, "DIFF OF"},
	{PRODUKTOF, "PRODUKT OF"},
	{QUOSHUNTOF, "QUOSHUNT OF"},
	{MODOF, "MOD OF"},
	{NOT, "NOT"},
	{BOTHOF, "BOTH OF"},
	{EITHEROF, "EITHER OF"},
	{WONOF, "WON OF"},
	{ALLOF, "ALL OF"},
	{ANYOF, "ANY OF"},
	{SMOOSH, "SMOOSH"},
	{AN, "AN"},
	{MKAY, "MKAY"},
})

type phraseNode struct {
	t     int
	nodes map[string]*phraseNode
	msg   string
}

func newPhraseNode() *phraseNode {
	return &phraseNode{Err, make(map[string]*phraseNode), ""}
}

type phraseInit struct {
	t      int
	phrase string
}

func initPhrases(phraseInits []phraseInit) *phraseNode {
	phraseRoot := newPhraseNode()
	for _, init := range phraseInits {
		initPhrase(phraseRoot, init.t, strings.Split(init.phrase, " "), init.phrase)
	}
	return phraseRoot
}

// Recursively build phrase tree
func initPhrase(root *phraseNode, t int, words []string, msg string) {
	if len(words) == 0 {
		root.t = t
		root.msg = msg
		return
	}
	word := words[0]
	node := root.nodes[word]
	if node == nil {
		node = newPhraseNode()
		root.nodes[word] = node
	}
	initPhrase(node, t, words[1:], msg)
}

// How EOL is displayed in errors and such
const EOLPhrase = "End-of-line"

// emitFragments reads from a bufio.Reader and emits string fragments on the given channel,
// omitting all comments and converting line separators "," into "\n" fragments
func emitFragments(reader *bufio.Reader, out chan<- string) {
	defer close(out)
	insideComment := false
txtLine:
	for {
		txt, err := reader.ReadString('\n')
		if err != nil {
			return
		}
		for _, line := range strings.Split(txt, ",") {
			fragments := strings.Fields(line)
			if len(fragments) == 0 {
				continue //ignore empty lines
			}
			start := 0
			if insideComment {
				if fragments[0] != "TLDR" {
					continue
				}
				insideComment = false
				if len(fragments) == 1 {
					continue
				}
				start = 1
			} else {
				if fragments[0] == "OBTW" {
					insideComment = true
					continue
				}
			}
			for i := start; i < len(fragments); i++ {
				if fragments[i] == "BTW" {
					if i > start {
						out <- EOLPhrase
					}
					continue txtLine
				}
				out <- fragments[i]
			}
			out <- EOLPhrase
		}
	}
}

// EmitTokens parses a Lolcode reader and emits a stream of Tokens
func EmitTokens(reader *bufio.Reader, out chan<- Token) {
	frags := make(chan string, 100)
	go emitFragments(reader, frags)
	for word := range frags {
		// Emit as many phrase tokens as possible
		for ok := true; ok; {
			word, ok = parsePhraseToken(word, frags, out)
		}
		switch {
		case word == "": // end of input
			close(out)
			return
		case word == "WIN": // TROOF literal
			out <- Token{Literal, true}
		case word == "FAIL":
			out <- Token{Literal, false}
		case word == "NOOB": // NOOB is a literal; casting to type NOOB is not allowed
			out <- Token{Literal, nil}
		case word[0] == '"': // yarn literal
			out <- yarnLiteralToToken(word)
		case isIdentifier(word):
			out <- Token{Ident, word}
		default:
			if numbr, err := strconv.ParseInt(word, 0, 64); err == nil {
				out <- Token{Literal, numbr}
				continue
			}
			if numbar, err := strconv.ParseFloat(word, 64); err == nil {
				out <- Token{Literal, numbar}
				continue
			}
			out <- Token{Err, "Syntax error: unexpected token " + word}
		}
	}
}

// Reads a phrase starting with the given fragment (word)
// uses single-word look-ahead to parse as long a phrase as possible
func parsePhraseToken(word string, frags <-chan string, out chan<- Token) (string, bool) {
	phraseNode := phraseRoot
	hasRead := false
	for {
		nextNode := phraseNode.nodes[word]
		if nextNode == nil {
			if hasRead {
				token := Token{phraseNode.t, phraseNode.msg}
				if token.Type == Err {
					// If we have an Error, fill in a parser error as the value
					token.Value = getErrMessageForPhrase(phraseNode, word)
				}
				out <- token
				return word, true
			} //else
			return word, false
		}
		hasRead = true
		phraseNode = nextNode
		word = <-frags
	}
}

func isIdentifier(s string) bool {
	if len(s) == 0 || !isLetter(s[0]) {
		return false
	}
	for i := 1; i < len(s); i++ {
		if l := s[i]; !isLetter(l) && !isNumberOrUnderscore(l) {
			return false
		}
	}
	return true
}

func isLetter(l byte) bool {
	return l >= 'a' && l <= 'z' || l >= 'A' && l <= 'Z'
}

func isNumberOrUnderscore(l byte) bool {
	return l >= '0' && l <= '9' || l == '_'
}

// TODO: add string escaping
func yarnLiteralToToken(str string) Token {
	// String literal must end with '"' and have length at least 2
	if l := len(str); l < 2 || str[l-1] != '"' {
		return Token{Err, "Invalid string literal: " + str}
	}
	// chop off the start and end quotes
	return Token{Literal, str[1 : len(str)-1]}
}

func getErrMessageForPhrase(node *phraseNode, word string) string {
	var out strings.Builder
	w := out.WriteString
	w(word)
	w(": expected ")
	sep := ""
	for word := range node.nodes {
		w(sep)
		w(word)
		sep = " or "
	}
	return out.String()
}
