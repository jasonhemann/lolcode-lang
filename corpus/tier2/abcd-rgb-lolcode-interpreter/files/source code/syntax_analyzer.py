import patterns as p
import lexer as l


lexemes = l.lexer("project-testcases/test.lol")
# print(lexemes)

class ParseNode:
    def __init__(self, data, parent=None):
        self.parent = parent
        self.data = data
        self.children = []

    def __str__(self):
        tree = self.data + '\n'
        for child in self.children:
            tree += child.__str__()
        return tree

def print_tree(node, indent=0, prefix=''):
    if node is not None:
        print(' ' * indent + prefix + node.data)
        for child in node.children:
            print_tree(child, indent + 4, "|-- ")


# print(lexemes)
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.parse_tree = None
        
        self.advance()
        
    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok
    
    def check_advance(self):
        if self.tok_idx + 1 < len(self.tokens):
            return self.tokens[self.tok_idx + 1]
        else:
            return None
    
    def parse(self):
        res = self.program()
        return res

    def isFunction(self, node):
        # Traverse parent i times or when the parent is None
        while node.parent is not None:
            node = node.parent
            if node.data == "<function>":
                return True
        return False
    
    
    def program(self):
        # If the token is HAI then we can continue
        self.parse_tree = ParseNode("<program>")
        
        while self.current_tok.keyword == "HOW IZ I":
            self.function(self.parse_tree)

        if self.current_tok.keyword == "HAI":
            self.parse_tree.children.append(ParseNode(self.current_tok.keyword, parent=self.parse_tree))
            self.advance()
            
        while self.current_tok.keyword == "HOW IZ I":
            self.function(self.parse_tree)

        if self.current_tok.keyword == "WAZZUP":
            self.wazzup(self.parse_tree)

        if self.current_tok.keyword != "WAZZUP":
            self.statements(self.parse_tree)
    
        if self.current_tok.keyword == "KTHXBYE":
            self.parse_tree.children.append(ParseNode(self.current_tok.keyword, parent=self.parse_tree))
            return self.parse_tree
        
        raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
        
    def wazzup(self, node):
        wazzup_node = ParseNode("<wazzup>", parent=node)
        
        if self.current_tok.keyword == "WAZZUP":
            node.children.append(wazzup_node)
            wazzup_node.children.append(ParseNode(self.current_tok.keyword, parent=wazzup_node))
            self.advance()
        
        if self.current_tok.keyword == "I HAS A":
            self.declarations(wazzup_node)
            
        if self.current_tok.keyword == "BUHBYE":
            wazzup_node.children.append(ParseNode(self.current_tok.keyword, parent=wazzup_node))
            self.advance()
            return

        raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")


    def declarations(self, node):
        declarations_node = ParseNode("<declarations>", parent=node)
        
        if self.current_tok.keyword  == "I HAS A":
            node.children.append(declarations_node)
            self.declaration(declarations_node)
        
        return


    def declaration(self, node):
        declaration_node = ParseNode("<declaration>", parent=node)

        if self.current_tok.keyword == "I HAS A":
            node.children.append(declaration_node)
            declaration_node.children.append(ParseNode(self.current_tok.keyword, parent=declaration_node))
            self.advance()
            
            if self.current_tok.token_type == "Identifier":
                declaration_node.children.append(ParseNode(self.current_tok.keyword, parent=declaration_node))
                self.advance()
                
                if self.current_tok.keyword == "ITZ":
                    declaration_node.children.append(ParseNode(self.current_tok.keyword, parent=declaration_node))
                    self.advance()
                    self.value(declaration_node)

                
                if self.current_tok.keyword == "I HAS A":
                    self.declaration(node)
                
            else:
                raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
    
    def statements(self, node):
        statements_node = ParseNode("<statements>", parent=node)
        
        if self.current_tok.keyword != "KTHXBYE":
            if self.current_tok.keyword in ["OMG", "OMGWTF", "OIC", "IF U SAY SO", "IM OUTTA YR"]:
                return
            node.children.append(statements_node)
            self.statement(statements_node)
        else:
            return
    
    def lookAhead(self, i):
        if self.tok_idx + i < len(self.tokens):
            return self.tokens[self.tok_idx + i]
        else:
            return None
    
    def backtracking(self, node, i):
        # Traverse parent i times or when the parent is None
        while i > 0 and node.parent is not None:
            node = node.parent
            i -= 1 
        return node.data
    
    def statement(self, node):

            while self.current_tok.keyword != "KTHXBYE":
                statement_node = ParseNode("<statement>", parent=node)
                if self.current_tok.token_type == "Identifier" and self.lookAhead(1) is not None and self.lookAhead(1).keyword == "R":
                    node.children.append(statement_node)
                    self.assignment(statement_node)
                elif self.current_tok.keyword == "GIMMEH":
                    node.children.append(statement_node)
                    self.input(statement_node)
                elif self.current_tok.keyword == "VISIBLE":
                    node.children.append(statement_node)
                    self.output(statement_node)
                elif self.current_tok.keyword == "WTF?":
                    node.children.append(statement_node)
                    self.switch(statement_node)        
                elif self.current_tok.keyword == "IM IN YR":
                    node.children.append(statement_node)
                    self.loop(statement_node)
                elif self.current_tok.keyword == "HOW IZ I":
                    node.children.append(statement_node)
                    self.function(statement_node)
                elif self.current_tok.keyword == "I IZ":
                    node.children.append(statement_node)
                    self.function_call(statement_node)
                elif self.current_tok.keyword == "FOUND YR" and self.isFunction(node):
                    node.children.append(statement_node)
                    statement_node.children.append(ParseNode(self.current_tok.keyword, parent=statement_node))
                    self.advance()
                    self.value(statement_node)
                elif self.backtracking(node, 1) == "<function>":
                    if self.current_tok.keyword == "IF U SAY SO":
                        return
                    elif self.current_tok.keyword == "GTFO":
                        node.children.append(statement_node)
                        statement_node.children.append(ParseNode(self.current_tok.keyword, parent=statement_node))
                        self.advance()
                    elif self.current_tok.keyword == "FOUND YR":
                        node.children.append(statement_node)
                        statement_node.children.append(ParseNode(self.current_tok.keyword, parent=statement_node))
                        self.advance()
                        self.value(statement_node)
                    else:
                        node.children.append(statement_node)
                        expression_node = self.expression(statement_node)
                        
                        # Check if current token if for if-then
                        if self.current_tok.keyword == "O RLY?":
                            self.if_then(expression_node, statement_node)
                        else:
                            statement_node.children.append(expression_node)
                elif self.backtracking(node, 1) == "<loop>":
                    if self.current_tok.keyword == "IM OUTTA YR":
                        return
                    elif self.current_tok.keyword == "GTFO":
                        node.children.append(statement_node)
                        statement_node.children.append(ParseNode(self.current_tok.keyword, parent=statement_node))
                        self.advance()
                    else:
                        raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
                elif self.backtracking(node, 3) == "<switch>":
                    if self.current_tok.keyword == "OMGWTF":
                        return
                    elif self.current_tok.keyword == "OMG":
                        return
                    elif self.current_tok.keyword == "OIC":
                        return
                    elif self.current_tok.keyword == "GTFO":
                        node.children.append(statement_node)
                        statement_node.children.append(ParseNode(self.current_tok.keyword, parent=statement_node))
                        self.advance()
                    else:
                        node.children.append(statement_node)
                        expression_node = self.expression(statement_node)
                        
                        # Check if current token if for if-then
                        if self.current_tok.keyword == "O RLY?":
                            self.if_then(expression_node, statement_node)
                        else:
                            statement_node.children.append(expression_node)

                elif self.backtracking(node, 2) == "<if-then>":
                    if self.current_tok.keyword == "OIC":
                        return
                    elif self.current_tok.keyword == "MEBBE":
                        return
                    elif self.current_tok.keyword == "NO WAI":
                        return
                    else:
                        node.children.append(statement_node)
                        expression_node = self.expression(statement_node)
                        
                        # Check if current token if for if-then
                        if self.current_tok.keyword == "O RLY?":
                            self.if_then(expression_node, statement_node)
                        else:
                            statement_node.children.append(expression_node)
                else:
                    node.children.append(statement_node)
                    expression_node = self.expression(statement_node)
                    
                    # Check if current token if for if-then
                    if self.current_tok.keyword == "O RLY?":
                        self.if_then(expression_node, statement_node)
                    else:
                        statement_node.children.append(expression_node)
                # else:
                #     raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
            return
        
    def expression(self, node):
        expression_node = ParseNode("<expression>", parent=node)
        arithmeticExpressions = ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]
        booleanExpressions = ["BOTH OF", "EITHER OF", "WON OF", "NOT", "ALL OF", "ANY OF"]
        comparisonExpressions = ["BOTH SAEM", "DIFFRINT"]
        # <arithmetic>
        if self.current_tok.keyword in arithmeticExpressions:
            self.arithmetic(expression_node)
        # <concatenation>
        elif self.current_tok.keyword == "SMOOSH":
            self.concatenation(expression_node)
        # <boolean>
        elif self.current_tok.keyword in booleanExpressions:
            self.boolean(expression_node)
        # <comparison>
        elif self.current_tok.keyword in comparisonExpressions:
            self.comparison(expression_node)
        # Typecasting
        elif self.current_tok.keyword == "MAEK":
            self.typecasting(expression_node)
        # Recasting
        elif self.current_tok.token_type == "Identifier" and self.lookAhead(1) is not None and self.lookAhead(1).keyword == "IS NOW A":
            self.recasting(expression_node)
        # function call
        elif self.current_tok.keyword == "I IZ":
            self.function_call(expression_node)
        # NOTE: newly added to accept identifier as an expression
        # identifier
        elif self.current_tok.token_type == "Identifier":
            self.value(expression_node)
        else:
            raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
        
        if node.data == "<statement>":
            return expression_node
        node.children.append(expression_node)
      
        
            
            
    def if_then(self, expression_node, parent_node):
        if_then_node = ParseNode("<if-then>", parent=parent_node)
        parent_node.children.append(if_then_node)
        if_then_node.children.append(expression_node)
        
        if self.current_tok.keyword == "O RLY?":
            if_then_node.children.append(ParseNode(self.current_tok.keyword, parent=if_then_node))
            self.advance()
            if self.current_tok.keyword == "YA RLY":
                self.if_clause(if_then_node)
                if self.current_tok.keyword == "OIC":
                    if_then_node.children.append(ParseNode(self.current_tok.keyword, parent=if_then_node))
                    self.advance()
                    return
                else:
                    raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
    
    def if_clause(self, node):
        if_clause_node = ParseNode("<if-clause>", parent=node)
        if self.current_tok.keyword == "YA RLY":
            node.children.append(if_clause_node)
            if_clause_node.children.append(ParseNode(self.current_tok.keyword, parent=if_clause_node))
            self.advance()
            self.statements(if_clause_node)
            while self.current_tok.keyword == "MEBBE":
                self.else_if_clause(node)
            if self.current_tok.keyword == "NO WAI":
                self.else_clause(node)
        else:
            raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
        
    # TODO: add support for MEBBE
    def else_if_clause(self, node):
        else_if_clause_node = ParseNode("<else-if-clause>", parent=node)
        if self.current_tok.keyword == "MEBBE":
            node.children.append(else_if_clause_node)
            else_if_clause_node.children.append(ParseNode(self.current_tok.keyword, parent=else_if_clause_node))
            self.advance()
            self.expression(else_if_clause_node)
            self.statements(else_if_clause_node)
        else:
            raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
    
    def else_clause(self, node):
        else_clause_node = ParseNode("<else-clause>", parent=node)
        if self.current_tok.keyword == "NO WAI":
            node.children.append(else_clause_node)
            else_clause_node.children.append(ParseNode(self.current_tok.keyword, parent=else_clause_node))
            self.advance()
            self.statements(else_clause_node)
        else:
            raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
        
    def comparison(self, node):
        comparison_node = ParseNode("<comparison>", parent=node)
        if self.current_tok.keyword in ["BOTH SAEM", "DIFFRINT"]:
            node.children.append(comparison_node)
            comparison_node.children.append(ParseNode(self.current_tok.keyword, parent=comparison_node))
            self.advance()
            self.value(comparison_node)
            if self.current_tok.keyword == "AN":
                comparison_node.children.append(ParseNode(self.current_tok.keyword, parent=comparison_node))
                self.advance()
                relationalOperations = ["BIGGR OF", "SMALLR OF"]
                if self.current_tok.keyword in relationalOperations:
                    comparison_node.children.append(ParseNode(self.current_tok.keyword, parent=comparison_node))
                    self.advance()
                    self.value(comparison_node)
                    if self.current_tok.keyword == "AN":
                        comparison_node.children.append(ParseNode(self.current_tok.keyword, parent=comparison_node))
                        self.advance()
                        self.value(comparison_node)
                else: 
                    self.value(comparison_node)
        else:
            raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")

    def boolean(self, node):
        boolean_node = ParseNode("<boolean>", parent=node)
        binaryBoolean = ["BOTH OF", "EITHER OF", "WON OF"]
        unaryBoolean = ["NOT"]
        infiniteBoolean = ["ALL OF", "ANY OF"]
        if self.current_tok.keyword in  binaryBoolean:
            node.children.append(boolean_node)
            boolean_node.children.append(ParseNode(self.current_tok.keyword, parent=boolean_node))
            self.advance()
            self.value(boolean_node)
            if self.current_tok.keyword == "AN":
                boolean_node.children.append(ParseNode(self.current_tok.keyword, parent=boolean_node))
                self.advance()
                self.value(boolean_node)
        elif self.current_tok.keyword in unaryBoolean:
            node.children.append(boolean_node)
            boolean_node.children.append(ParseNode(self.current_tok.keyword, parent=boolean_node))
            self.advance()
            self.value(boolean_node)
        elif self.current_tok.keyword in infiniteBoolean:
            node.children.append(boolean_node)
            boolean_node.children.append(ParseNode(self.current_tok.keyword, parent=boolean_node))
            self.advance()
            self.value(boolean_node)
            while self.current_tok.keyword == "AN":
                boolean_node.children.append(ParseNode(self.current_tok.keyword, parent=boolean_node))
                self.advance()
                self.value(boolean_node)
            if self.current_tok.keyword == "MKAY":
                boolean_node.children.append(ParseNode(self.current_tok.keyword, parent=boolean_node))
                self.advance()
        else:
            raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")

    def typecasting(self, node):
        typecasting_node = ParseNode("<typecasting>", parent=node)

        if self.current_tok.keyword == "MAEK":
            node.children.append(typecasting_node)
            typecasting_node.children.append(ParseNode(self.current_tok.keyword, parent=typecasting_node))
            self.advance()
            self.value(typecasting_node)

            # Optional A
            if self.current_tok.keyword == "A":
                typecasting_node.children.append(ParseNode(self.current_tok.keyword, parent=typecasting_node))
                self.advance()
            
            if self.current_tok.token_type == "TYPE Literal":
                typecasting_node.children.append(ParseNode(self.current_tok.keyword, parent=typecasting_node))
                self.advance()
            else:
                raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")

    # Just like assignment using R         
    def recasting(self, node):
        recasting_node = ParseNode("<recasting>", parent=node)
        
        if self.current_tok.token_type == "Identifier":
            node.children.append(recasting_node)
            # recasting_node.children.append(ParseNode(self.current_tok.keyword, parent=recasting_node))
            # self.advance()
            self.value(recasting_node)
            if self.current_tok.keyword == "IS NOW A":
                recasting_node.children.append(ParseNode(self.current_tok.keyword, parent=recasting_node))
                self.advance()
                if self.current_tok.token_type == "TYPE Literal":
                    recasting_node.children.append(ParseNode(self.current_tok.keyword, parent=recasting_node))
                    self.advance()
                else:
                    raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
            else: 
                raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
        

    def concatenation(self, node):
        concatenation_node = ParseNode("<concatenation>", parent=node)
        if self.current_tok.keyword == "SMOOSH":
            node.children.append(concatenation_node)
            concatenation_node.children.append(ParseNode(self.current_tok.keyword, parent=concatenation_node))
            self.advance()
            self.value(concatenation_node)
            while self.current_tok.keyword == "AN":
                concatenation_node.children.append(ParseNode(self.current_tok.keyword, parent=concatenation_node))
                self.advance()
                self.value(concatenation_node)
        else:
            raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
    
    def arithmetic(self, expression_node: ParseNode):
        arithmeticNode = ParseNode("<arithmetic>", parent=expression_node)
        
        # <arithmetic> -> <value> <arithmetic_operator> <value> for any arithmetic operator
        expression_node.children.append(arithmeticNode)
        arithmeticNode.children.append(ParseNode(self.current_tok.keyword, parent=arithmeticNode))
        self.advance()
        self.value(arithmeticNode)
        if self.current_tok.keyword == "AN":
            arithmeticNode.children.append(ParseNode(self.current_tok.keyword, parent=arithmeticNode))
            self.advance()
            self.value(arithmeticNode)
        else:
            raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")

    def function(self, node):
        function_node = ParseNode("<function>", parent=node)
        if self.current_tok.keyword == "HOW IZ I":
            node.children.append(function_node)
            function_node.children.append(ParseNode(self.current_tok.keyword, parent=function_node))
            self.advance()
            if self.current_tok.token_type == "Identifier":
                function_node.children.append(ParseNode(self.current_tok.keyword, parent=function_node))
                self.advance()
                if self.current_tok.keyword == "YR":
                    function_node.children.append(ParseNode(self.current_tok.keyword, parent=function_node))
                    self.advance()
                    self.parameter(function_node)
                    while self.current_tok.keyword == "AN":
                        self.more_parameters(function_node)
                else:
                    raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
                self.statements(function_node)

                if self.current_tok.keyword == "IF U SAY SO":
                    function_node.children.append(ParseNode(self.current_tok.keyword, parent=function_node))
                    self.advance()
            else:
                raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
        else:
            raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")

    def parameter(self, node):
        parameter_node = ParseNode("<parameter>", parent=node)
        if self.current_tok.token_type == "Identifier":
            node.children.append(parameter_node)
            parameter_node.children.append(ParseNode(self.current_tok.keyword, parent=parameter_node))
            self.advance()
        else:
            raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")

    def more_parameters(self, node):
        more_parameters_node = ParseNode("<more_parameters>", parent=node)
        if self.current_tok.keyword == "AN":
            node.children.append(more_parameters_node)
            more_parameters_node.children.append(ParseNode(self.current_tok.keyword, parent=more_parameters_node))
            self.advance()
            if self.current_tok.keyword == "YR":
                more_parameters_node.children.append(ParseNode(self.current_tok.keyword, parent=more_parameters_node))
                self.advance()
                self.parameter(more_parameters_node)
            else:
                raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
        else:
            raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")

    def function_call(self, node):
        function_call_node = ParseNode("<function_call>", parent=node)
        if self.current_tok.keyword == "I IZ":
            node.children.append(function_call_node)
            function_call_node.children.append(ParseNode(self.current_tok.keyword, parent=function_call_node))
            self.advance()
            if self.current_tok.token_type == "Identifier":
                function_call_node.children.append(ParseNode(self.current_tok.keyword, parent=function_call_node))
                self.advance()
                if self.current_tok.keyword == "YR":
                    function_call_node.children.append(ParseNode(self.current_tok.keyword, parent=function_call_node))
                    self.advance()
                    self.argument(function_call_node)
                    while self.current_tok.keyword == "AN":
                        self.more_arguments(function_call_node)
                if self.current_tok.keyword == "MKAY":
                    function_call_node.children.append(ParseNode(self.current_tok.keyword, parent=function_call_node))
                    self.advance()
                else:
                    raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")  
            else:
                raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
        else:
            raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
        
    def argument(self, node):
        argument_node = ParseNode("<argument>", parent=node)
        node.children.append(argument_node)
        self.value(argument_node)
    
    def more_arguments(self, node):
        more_arguments_node = ParseNode("<more_arguments>", parent=node)
        if self.current_tok.keyword == "AN":
            node.children.append(more_arguments_node)
            more_arguments_node.children.append(ParseNode(self.current_tok.keyword, parent=more_arguments_node))
            self.advance()
            if self.current_tok.keyword == "YR":
                more_arguments_node.children.append(ParseNode(self.current_tok.keyword, parent=more_arguments_node))
                self.advance()
                self.argument(more_arguments_node)
            else:
                raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")  
        else:
            raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")      

    def loop(self, node):
        loop_node = ParseNode("<loop>", parent=node)

        if self.current_tok.keyword == "IM IN YR":
            node.children.append(loop_node)
            loop_node.children.append(ParseNode(self.current_tok.keyword, parent=loop_node))
            self.advance()

            if self.current_tok.token_type != "Identifier":
                raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
            else:
                # self.value(loop_node)
                loop_node.children.append(ParseNode(self.current_tok.keyword, parent=loop_node))
                self.advance()

                if not (self.current_tok.keyword in ["UPPIN", "NERFIN"]):
                    raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
                else:
                    loop_node.children.append(ParseNode(self.current_tok.keyword, parent=loop_node))
                    self.advance()

                    if self.current_tok.keyword != "YR":
                        raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
                    else: 
                        loop_node.children.append(ParseNode(self.current_tok.keyword, parent=loop_node))
                        self.advance()

                        if self.current_tok.token_type != "Identifier":
                            raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
                        else:    
                            self.value(loop_node)
                            # loop_node.children.append(ParseNode(self.current_tok.keyword, parent=loop_node))
                            # self.advance()

                            if not (self.current_tok.keyword in ["TIL", "WILE"]):
                                # raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
                                self.statements(loop_node)
                            else:
                                loop_node.children.append(ParseNode(self.current_tok.keyword, parent=loop_node))
                                self.advance()
                                self.expression(loop_node)
                                self.statements(loop_node)
                                
                            if self.current_tok.keyword != "IM OUTTA YR":
                                raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
                            else:
                                loop_node.children.append(ParseNode(self.current_tok.keyword, parent=loop_node))
                                self.advance()
                                
                                if self.current_tok.token_type != "Identifier":
                                    raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
                                else:
                                    # self.value(loop_node)
                                    loop_node.children.append(ParseNode(self.current_tok.keyword, parent=loop_node))
                                    self.advance()
            

    def switch(self, node):
        switch_node = ParseNode("<switch>", parent=node)
        if self.current_tok.keyword == "WTF?":
            node.children.append(switch_node)
            switch_node.children.append(ParseNode(self.current_tok.keyword, parent=switch_node))
            self.advance()
            self.cases(switch_node)
            if self.current_tok.keyword == "OIC":
                switch_node.children.append(ParseNode(self.current_tok.keyword, parent=switch_node))
                self.advance()
        else:
            raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
    
    def cases(self, node):
        cases_node = ParseNode("<cases>", parent=node)
        
        # If the current token is OMG
        if self.current_tok.keyword == "OMG":
            # Append the cases node to the parent node
            node.children.append(cases_node)
            pass
        
        while self.current_tok.keyword == "OMG":
            self.case(cases_node)
            
        if self.current_tok.keyword == "OMGWTF":
            self.default(cases_node)
            
        if self.current_tok.keyword == "OIC":
            return
        
        raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
    
    def case(self, node):
        case_node = ParseNode("<case>", parent=node)
        if self.current_tok.keyword == "OMG":
            node.children.append(case_node)
            case_node.children.append(ParseNode(self.current_tok.keyword, parent=case_node))
            self.advance()
            self.literal(case_node)
            self.statements(case_node)
        else:
            raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
    
    def default(self, node):
        default_node = ParseNode("<default>", parent=node)
        if self.current_tok.keyword == "OMGWTF":
            node.children.append(default_node)
            default_node.children.append(ParseNode(self.current_tok.keyword, parent=default_node))
            self.advance()
            self.statements(default_node)
        else:
            raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
    
    def value(self, node):
        value_node = ParseNode("<value>", parent=node)

        if self.current_tok.token_type in ["Identifier"]:
            node.children.append(value_node)
            type_node = ParseNode("<identifier>", parent=value_node)
            value_node.children.append(type_node)
            type_node.children.append(ParseNode(self.current_tok.keyword, parent=type_node))
            self.advance()
        elif self.current_tok.token_type in ["String Delimiter", "NUMBR Literal", "NUMBAR Literal", "TROOF Literal", "TYPE Literal"]:
            node.children.append(value_node)
            self.literal(value_node)
        else:
            node.children.append(value_node)
            self.expression(value_node)
        # else:
        #     raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
    
    def literal(self, node):
        literal_node = ParseNode("<literal>", parent=node)

        typeDict = {
            "NUMBR Literal" : "<NUMBR>",
            "NUMBAR Literal" : "<NUMBAR>",
            "TROOF Literal" : "<TROOF>",
            "TYPE Literal": "<TYPE>"
        }

        # <NUMBR> , <NUMBAR>, <TROOF>, <TYPE>
        if self.current_tok.token_type in ["NUMBR Literal", "NUMBAR Literal", "TROOF Literal", "TYPE Literal"]:
            node.children.append(literal_node)
            type_node = ParseNode(typeDict[self.current_tok.token_type], parent=literal_node)
            literal_node.children.append(type_node)
            type_node.children.append(ParseNode(self.current_tok.keyword, parent=type_node))
            self.advance()
        # <STRING>
        elif self.current_tok.token_type in ["String Delimiter"]:
            node.children.append(literal_node)
            type_node = ParseNode("<STRING>", parent=literal_node)
            literal_node.children.append(type_node)
            type_node.children.append(ParseNode(self.current_tok.keyword, parent=type_node))
            self.advance()
            type_node.children.append(ParseNode(self.current_tok.keyword, parent=type_node))
            self.advance()
            type_node.children.append(ParseNode(self.current_tok.keyword, parent=type_node))
            self.advance()
        else:
            raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")
    
    def output(self, node):
        output_node = ParseNode("<output>", parent=node)
        if self.current_tok.keyword == "VISIBLE":
            node.children.append(output_node)
            output_node.children.append(ParseNode(self.current_tok.keyword, parent=output_node))
            self.advance()
            self.value(output_node)
            while self.current_tok.token_type == "Visible Concatenation Symbol":
                output_node.children.append(ParseNode(self.current_tok.keyword, parent=output_node))
                self.advance()
                self.value(output_node)
            if self.current_tok.token_type == "Newline Suppression Symbol":
                output_node.children.append(ParseNode(self.current_tok.keyword, parent=output_node))
                self.advance()

    
    def input(self, node):
        input_node = ParseNode("<input>", parent=node)
        if self.current_tok.keyword == "GIMMEH":
            node.children.append(input_node)
            input_node.children.append(ParseNode(self.current_tok.keyword, parent=input_node))
            self.advance()
            if self.current_tok.token_type == "Identifier":
                input_node.children.append(ParseNode(self.current_tok.keyword, parent=input_node))
                self.advance()
            else:
                raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")

        return
    
    def assignment(self, node):
        assignment_node = ParseNode("<assignment>", parent=node)
        
        if self.current_tok.token_type == "Identifier":
            node.children.append(assignment_node)
            assignment_node.children.append(ParseNode(self.current_tok.keyword, parent=assignment_node))
            self.advance()
            if self.current_tok.keyword == "R":
                assignment_node.children.append(ParseNode(self.current_tok.keyword, parent=assignment_node))
                self.advance()
                self.value(assignment_node)
            else: 
                raise Exception(f"SyntaxError: Missing/Invalid token before or after '{self.current_tok.keyword} {self.check_advance().keyword}'")

       
    
if __name__ == "__main__":
    p = Parser(lexemes)
    p.parse()
    print_tree(p.parse_tree)


