#!/usr/bin/env python
# coding=utf-8

""" Traduit l'arbre syntaxique en language python """

import AST
from AST import addToClass

__author__  = "Tristan Seuret, David Rihs"
__version__ = "1.0.0"

# Stocke les variables qui ont été déclarées
vars = dict()

# noeud de programme
# retourne la suite d'opcodes de tous les enfants
@addToClass(AST.ProgramNode)
def compile(self):
	resultPython = ""
	for c in self.children:
		resultPython += c.compile()
	return resultPython

# Commentaire
@addToClass(AST.CommentNode)
def compile(self):
	resultPython = ""
	comment = None
	if(len(self.children) == 2) :
		resultPython += self.children[0].compile()
		comment = self.children[1].compile()
	else :
		comment = self.children[0].compile()

	# Commentaire multiligne "OBTW ... TLDR"
	if(comment[0] == "O") :
		resultPython += "#" + comment[4:-4].replace("\n", "\n#")[:-1]
	# Commentaire monoligne "BTW ... "
	else:
		resultPython += "#" + comment[3:] + "\n"
	
	return resultPython

# Variable ou nombre
@addToClass(AST.TokenNode)
def compile(self):
	if(isinstance(self.tok, str) and self.tok not in vars.keys()):
		raise Exception("Var %s wasn't assigned before using it" % self.tok)
	return str(self.tok)

# Chaîne de caractères
@addToClass(AST.StringNode)
def compile(self):
	return self.tok

# Opérations arithmétiques binaires
@addToClass(AST.OpNode)
def compile(self):
	resultPython = ""
	# modulo, min, max
	if(len(self.op) > 1) :
		if(self.op == "MOD OF") :
			resultPython += self.children[0].compile() + " % " + self.children[1].compile()
		elif(self.op == "BIGGR OF") :
			resultPython += "max(" + self.children[0].compile() + "," + self.children[1].compile() + ")"
		elif(self.op == "SMALLR OF") :	
			resultPython += "min(" + self.children[0].compile() + "," + self.children[1].compile() + ")"
	# +, -, *, /
	else:
		resultPython += self.children[0].compile()
		resultPython += " " + self.op + " "
		resultPython += self.children[1].compile()
	
	return resultPython + "\n"

# Opérations incrémentales (unaire)
@addToClass(AST.IncOpNode)
def compile(self):
	return self.children[0].tok + " " + self.op + "= 1\n"

# Opérations de comparaisons (==, !=)
@addToClass(AST.CompNode)
def compile(self):
	resultPython = ""
	resultPython += self.children[0].compile()
	resultPython += " " + self.op + " "
	resultPython += self.children[1].compile()
	
	return resultPython + "\n"

# Opérations booleens
@addToClass(AST.BoolOpNode)
def compile(self):
	resultPython = ""
	# not
	if(len(self.children) == 1) :
		resultPython += "not "
		resultPython += "True" if self.children[0].tok == '0' else "False"
	# and, or
	else:
		resultPython += "True" if self.children[0].tok == '0' else "False"
		resultPython += " " + self.op + " "
		resultPython += "True" if self.children[1].tok == '0' else "False"
	return resultPython + "\n"

# Assignation de variable
@addToClass(AST.AssignNode)
def compile(self):
	resultPython = ""
	resultPython += self.children[0].tok + " = "
	resultPython += self.children[1].compile() + "\n"
	return resultPython

# Declaration de variable
@addToClass(AST.DeclarationNode)
def compile(self):
	resultPython = ""
	try:
		resultPython += self.children[0].compile() + " = "
	except:
		vars[self.children[0].tok] = self.children[1].compile()
		resultPython += self.children[0].compile() + " = "
	resultPython += self.children[1].compile() + "\n"
	return resultPython

# While
@addToClass(AST.WhileNode)
def compile(self):
	resultPython = "while "
	resultPython += self.children[0].compile()[:-1] + " :\n"
	block = self.children[1].compile()
	resultPython += "\t" + block.replace("\n", "\n\t")[:-1]
	return resultPython

# If
@addToClass(AST.IfNode)
def compile(self):
	resultPython = "if "
	resultPython += self.children[0].compile()[:-1] + " :\n"
	blockIf= self.children[1].compile()
	resultPython += "\t" + blockIf.replace("\n", "\n\t")[:-1]
	# Test si "else" existe
	if(len(self.children) == 3):
		blockElse = self.children[2].compile()
		resultPython += "else :\n\t" + blockElse.replace("\n", "\n\t")[:-1]
	return resultPython

# For
@addToClass(AST.ForNode)
def compile(self):
	resultPython = "for " + self.value + " in range(int(" + self.value + "), int("
	resultPython += self.until.compile() + "), "
	resultPython += "1" if self.inc == "+" else "-1"
	resultPython += ") :\n"
	block = self.children[0].compile()
	resultPython += "\t" + block.replace("\n", "\n\t")[:-1]
	return resultPython

# Break
@addToClass(AST.BreakNode)
def compile(self):
	return "break\n"

if __name__ == "__main__":
	from lolcode_parser import parse
	import sys, os

	prog = open(sys.argv[1]).read()
	
	ast = parse(prog)
	compiled = ast.compile()
	name = "result.py"   
	
	outfile = open(name, 'w')
	outfile.write(compiled)
	outfile.close()
	
	print ("Wrote output to", name)