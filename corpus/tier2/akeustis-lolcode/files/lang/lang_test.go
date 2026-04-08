package lang

import (
	"bufio"
	"lol/token"
	"strings"
	"testing"
)

func ns() *namespace {
	return &namespace{vars: make(map[string]interface{})}
}

func tokenChan(code string) <-chan token.Token {
	reader := bufio.NewReader(strings.NewReader(code))
	tokens := make(chan token.Token, 100)
	go token.EmitTokens(reader, tokens)
	return tokens
}

func TestBasicExpressions(t *testing.T) {
	type testCase struct {
		code        string
		expectedVal interface{}
	}
	i := func(x int64) interface{} { return x }
	f := func(x float64) interface{} { return x }
	ns := ns()
	ns.vars["FOO"] = i(-10)
	ns.vars["BAR"] = "5"
	ns.vars["NEWB"] = nil
	testCases := []testCase{
		{"1", i(1)},
		{"2.", f(2)},
		{"FAIL", false},
		{"NOOB", nil},
		{"SUM OF 2 AN 4", i(6)},
		{"PRODUKT OF DIFF OF 14 AN 4 AN 3", i(30)},
		{"QUOSHUNT OF 14 AN 3", i(4)},
		{"PRODUKT OF SUM OF 2 AN \"2.0\" AN \"4\"", f(16)},
		{"FOO", i(-10)},
		{"BAR", "5"},
		{"PRODUKT OF FOO AN BAR", i(-50)},
		{`BOTH SAEM 1 AN "1"`, false},
		{"BOTH SAEM FOO AN -10", true},
		{"DIFFRINT FAIL AN NOOB", true},
		{"NOT BOTH OF WIN AN FAIL", true},
		{"WON OF WON OF EITHER OF 1 0 1 1", true},
		{"ALL OF FOO AN BAR 1 AN 0.2", true},
		{"ALL OF FOO AN BAR 1 AN 0.2", true},
		{"ALL OF NEWB AN BAR 1 AN 0.2", false},
		{"ANY OF 0", false},
		{"ALL OF 0.0", false},
		{`ALL OF ""`, false},
		{"ALL OF WIN WIN AN ANY OF FAIL FAIL WIN MKAY AN WIN MKAY", true},
		{"MAEK FOO A NUMBAR", f(-10)},
		{"MAEK 11.2 A NUMBR", i(11)},
		{"MAEK FOO A YARN", "-10"},
		{"MAEK FOO A TROOF", true},
		{"MAEK FOO A NOOB", nil},
		{"MAEK NEWB A NUMBR", i(0)},
		{"MAEK NEWB A NUMBAR", f(0)},
		{"MAEK NEWB A YARN", ""},
		{"MAEK NEWB A TROOF", false},
		{"BIGGR OF 10.0 AN 20", f(20)},
		{`BIGGR OF FOO AN BAR`, i(5)},
		{`SMALLR OF "12" AN 0.0`, f(0)},
		{`SMOOSH 1 2 BAR AN "LOL"`, "125LOL"},
		{`SUM OF SMOOSH 4 AN 5 AN 6 MKAY AN 123`, i(579)},
	}
	for _, tc := range testCases {
		_, ex, ok := D.Parse(Expr, tokenChan(tc.code+"\n"))
		if !ok {
			t.Fatalf("Parse failed")
		}
		res := ex.(expr)(ns)
		if res != tc.expectedVal {
			t.Fatalf("Expression returned %v %T, expected %v %T", res, res, tc.expectedVal, tc.expectedVal)
		}
	}
}

func TestBasicStatments(t *testing.T) {
	type testCase struct {
		code        string
		variable    string
		expectedVal interface{}
	}

	testCases := []testCase{
		{"6", "IT", int64(6)},
		{"BAR", "IT", "5"},
		{"I HAS A FISH", "FISH", nil},
		{"I HAS A FISH ITZ WIN", "FISH", true},
		{"FOO R \"hello\"", "FOO", "hello"},
		{"BAR IS NOW A NUMBAR", "BAR", float64(5)},
	}
	for _, tc := range testCases {
		ns := ns()
		ns.vars["FOO"] = int64(-10)
		ns.vars["BAR"] = "5"
		_, ex, ok := D.Parse(Statement, tokenChan(tc.code+"\n"))
		if !ok {
			t.Fatalf("Parse failed")
		}
		ex.(statement)(ns)
		res, ok := ns.vars[tc.variable]
		if !ok {
			t.Fatalf("Variable %s not present in namespace", tc.variable)
		}
		if res != tc.expectedVal {
			t.Fatalf("Variable %s contained %v %T, expected %v %T", tc.variable, res, res, tc.expectedVal, tc.expectedVal)
		}
	}
}
