#!/usr/bin/env python
# coding=utf-8

""" Construit l'arbre syntaxique """

import ply.yacc as yacc
from lex import tokens

__author__  = "Tristan Seuret, David Rihs"
__version__ = "1.0.0"

import AST

# Ensemble global
def p_programme_statement(p):
    ''' programme : statement'''
    p[0] = AST.ProgramNode(p[1])

def p_programme_recursive(p):
    ''' programme : statement programme '''
    p[0] = AST.ProgramNode([p[1]]+p[2].children)

# Simplification
def p_statement(p):
    ''' statement : assignation
        | declaration
        | expression
        | structure
        | comment'''
    p[0] = p[1]    

# Break statement
def p_statement_break(p):
    '''statement : BREAK
       | BREAK new_line'''
    p[0] = AST.BreakNode()

# Commentaires
def p_commentary(p):
    ''' comment : statement SL_COMMENT new_line
    | statement ML_COMMENT new_line'''
    p[0] = AST.CommentNode([p[1],AST.StringNode(p[2])])

def p_commentary_alone(p):
    '''comment : SL_COMMENT new_line
    | ML_COMMENT new_line'''
    p[0] = AST.CommentNode([AST.StringNode(p[1])])

# Expression simplification
def p_expression(p):
    '''expression : expression_num
    | expression_bool'''
    p[0] = p[1]

# Mathematical operations
def p_expression_op(p):
    '''expression_num : ADD_OP expression_num AN expression_num 
            | MUL_OP expression_num AN expression_num
            | MOD_OP expression_num AN expression_num
            | MAX_OP expression_num AN expression_num
            | MIN_OP expression_num AN expression_num
            | ADD_OP expression_num AN expression_num new_line
            | MUL_OP expression_num AN expression_num new_line
            | MOD_OP expression_num AN expression_num new_line
            | MAX_OP expression_num AN expression_num new_line
            | MIN_OP expression_num AN expression_num new_line'''
    p[0] = AST.OpNode(p[1], [p[2], p[4]])

# Incrementation
def p_increment_op(p):
    '''expression_num : INC_OP expression_num 
       | INC_OP expression_num new_line'''
    p[0] = AST.IncOpNode(p[1], [p[2]])
    	
# Var or number
def p_expression_num_or_var(p):
    '''expression_num : NUMBER
        | IDENTIFIER 
        | NUMBER new_line
        | IDENTIFIER new_line'''
    p[0] = AST.TokenNode(p[1])

# Boolean
def p_expression_bool(p):
    '''expression_bool : BOOL
       | BOOL new_line'''
    p[0] = AST.TokenNode(p[1])

def p_bool_op(p):
    '''expression_bool : BOOL_OP expression_bool AN expression_bool
       | BOOL_OP expression_bool AN expression_bool new_line'''
    p[0] = AST.BoolOpNode(p[1], [p[2], p[4]])

def p_bool_not(p):
    '''expression_bool : NOT expression_bool
       | NOT expression_bool new_line'''
    p[0] = AST.BoolOpNode(p[1], [p[2]])

# Comparison
def p_comp(p):
    '''expression_bool : COMP expression_num AN expression_num
       | COMP expression_num AN expression_num new_line'''
    p[0] = AST.CompNode(p[1], [p[2],p[4]])

# Var declaration	
def p_declaration(p):
    ''' declaration : DECLARATION IDENTIFIER ASSIGNEMENT_DECL expression
        | DECLARATION IDENTIFIER ASSIGNEMENT_DECL expression new_line'''
    p[0] = AST.DeclarationNode([AST.TokenNode(p[2]),p[4]])

# Var assignation
def p_assign(p):
    ''' assignation : IDENTIFIER ASSIGNEMENT_SIMPLE expression
        | IDENTIFIER ASSIGNEMENT_SIMPLE expression new_line'''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

# New line
def p_newLine(p):
    ''' new_line : NL'''
    p[0] = AST.NlNode(p[1])

def p_multipleNewLine(p):
    ''' new_line : NL NL'''
    p[0] = AST.NlNode(p[1])

# Loops 
## While
def p_while(p):
    ''' structure : WHILE expression_bool programme END_LOOP 
        | WHILE expression_bool programme END_LOOP new_line'''
    p[0] = AST.WhileNode([p[2],p[3]])  

## For
def p_for(p):
    ''' structure : FOR IDENTIFIER UNTIL expression_num programme END_LOOP
        | FOR IDENTIFIER UNTIL expression_num programme END_LOOP new_line'''
    p[0] = AST.ForNode(p[1],p[2],p[4], [p[5]])

# If
## If simple
def p_if(p):
    ''' structure : expression_bool IF new_line IF_TRUE new_line programme IF_END
        | expression_bool IF new_line IF_TRUE new_line programme IF_END new_line'''
    p[0] = AST.IfNode([p[1],p[6]])

## If else
def p_ifElse(p):
    ''' structure : expression_bool IF new_line IF_TRUE new_line programme IF_FALSE new_line programme IF_END
        | expression_bool IF new_line IF_TRUE new_line programme IF_FALSE new_line programme IF_END new_line'''
    p[0] = AST.IfNode([p[1],p[6], p[9]])

# Erreur
def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        yacc.yacc().errok()
    else:
        print ("Syntax error: unexpected end of file!")

def parse(program):
    return yacc.parse(program)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys 
    	
    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)
    if result:
        print (result)
            
        import os
        os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
        graph.write_pdf(name) 
        print ("wrote ast to", name)
    else:
        print ("Parsing returned no result!")