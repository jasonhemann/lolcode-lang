#!/usr/bin/env python
# coding=utf-8

""" Analyse un fichier écrit en LOLCODE et identifie ses lèxèmes """

import ply.lex as lex

__author__  = "Tristan Seuret, David Rihs"
__version__ = "1.0.0"

tokens = (
	'SL_COMMENT','ML_COMMENT',
	'NUMBER',
	'ADD_OP', 'MUL_OP',	'MOD_OP', 'MAX_OP', 'MIN_OP', 'INC_OP',
	'DECLARATION', 'ASSIGNEMENT_DECL', 'ASSIGNEMENT_SIMPLE',
	'BOOL', 'BOOL_OP', 'NOT',
	'COMP',
	'IF', 'IF_TRUE', 'IF_FALSE', 'IF_END',
	'WHILE', 'FOR', 'UNTIL', 'BREAK', 'END_LOOP',
	'NL',
	'AN',
	'IDENTIFIER'
)

# Permet de directement traité les mots simples
oneWordReserved = {
	'NOT'  : 'NOT',
	'AN'   : 'AN',
	'ITZ'  : 'ASSIGNEMENT_DECL',
	'OIC'  : 'IF_END',
	'GTFO' : 'BREAK',
	'R'    : 'ASSIGNEMENT_SIMPLE',
	'TIL'  : 'UNTIL'
}

literals = '();={}'

# Comments
def t_SL_COMMENT(t):
	r'BTW[ ].*'
	return t

def t_ML_COMMENT(t):
	r'OBTW[ ]([\S\s]*?)TLDR'
	return t

# Types
def t_NUMBER(t):
	r'\d+(\.\d+)?'
	try:
		t.value = float(t.value)    
	except ValueError:
		print ("Line %d: Problem while parsing %s!" % (t.lineno,t.value))
		t.value = 0
	return t

# Mathematics operator
def t_ADD_OP(t):
	r'(SUM|DIFF)[ ]OF'
	t.value = '+' if t.value == 'SUM OF' else '-'
	return t
	
def t_MUL_OP(t):
	r'(PRODUKT|QUOSHUNT)[ ]OF'
	t.value = '*' if t.value == 'PRODUKT OF' else '/'
	return t

def t_MOD_OP(t):
	r'MOD[ ]OF'
	return t

def t_MAX_OP(t):
	r'BIGGR[ ]OF'
	return t

def t_MIN_OP(t):
	r'SMALLR[ ]OF'
	return t

def t_INC_OP(t):
	r'UPPIN|NERFIN'
	t.value = '+' if t.value == 'UPPIN' else '-'
	return t

# Declaration
def t_DECLARATION(t):
	r'I[ ]HAS[ ]A'
	return t

# Boolean
def t_BOOL(t):
	r'WIN|FAIL'
	t.value = '1' if t.value == "WIN" else '0'
	return t

def t_BOOL_OP(t):
	r'(BOTH|EITHER)[ ]OF'
	t.value = 'and' if t.value == 'BOTH OF' else 'or'
	return t

# If
def t_IF(t):
	r'O[ ]RLY[?]'
	return t

def t_IF_TRUE(t):
	r'YA[ ]RLY'
	return t

def t_IF_FALSE(t):
	r'NO[ ]WAI'
	return t

# Loops
def t_WHILE(t):
	r'IM[ ]IN[ ]YR[ ]LOOP[ ]WILE'
	return t

def t_FOR(t):
	r'IM[ ]IN[ ]YR[ ]LOOP[ ](UPPIN|NERFIN)[ ]YR'
	t.value = '+' if t.value == 'IM IN YR LOOP UPPIN YR' else '-'
	return t

def t_END_LOOP(t):
	r'IM[ ]OUTTA[ ]YR[ ]LOOP'
	return t

# Comparison
def t_COMP(t):
	r'BOTH[ ]SAEM|DIFFRINT'
	t.value = '==' if t.value == 'BOTH SAEM' else '!='
	return t

# Identifier
def t_IDENTIFIER(t):
	r'[A-z_]\w*'
	if t.value in oneWordReserved.keys() :
		t.type = oneWordReserved[t.value]
	return t

# New line
def t_NL(t):
	r'\n+'
	t.lexer.lineno += len(t.value)
	t.value = len(t.value)
	return t

# Error
def t_error(t):
	print ("Illegal character '%s'" % repr(t.value[0]))
	t.lexer.skip(1)

t_ignore  = ' \t'

lex.lex()

if __name__ == "__main__":
	import sys
	prog = open(sys.argv[1]).read()

	lex.input(prog)

	while 1:
		tok = lex.token()
		if not tok: break
		print ("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
