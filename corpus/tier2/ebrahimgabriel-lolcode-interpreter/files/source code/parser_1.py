class Node:
    def __init__(self, value):
        self.value = value
        self.children = []
    
    # Print in array form
    #def __str__(self):
    #    return f'[{self.value}, {self.children}]'
    
    #Print in tree form
    def __str__(self, level=0):
        ret = "\t" * level + f"[{repr(self.value)}]\n"
        for child in self.children:
            if isinstance(child, Node):
                ret += child.__str__(level + 1)
            else:
                ret += "\t" * (level + 1) + f"[{repr(child)}]\n"
        return ret
    
    def __repr__(self):
        return f'[{self.value}, {self.children}]'

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        
    def parse(self):
        tree = self.parse_program()
        return tree
    
    def parse_program(self):
        root = Node('program')

        if self.tokens[self.index][0] != 'HAI':
           print('error at line 35')
        
        root.children.append(self.tokens[self.index][0])
        self.index += 1

        if self.tokens[self.index][0] != '\n':
           print('error at line 41')
        root.children.append(self.tokens[self.index][0])   
        self.index += 1

        # if self.tokens[self.index][0] != 'VARDECLARATION':
        #    print('error')
        # self.index += 1

        root.children.append(self.parse_statement())

        # if self.tokens[self.index][0] != 'LINEBREAK':
        #    print('error')
        # self.index += 1    

        if self.tokens[self.index][0] != 'KTHXBYE':
           print('error at line 56')
        root.children.append(self.tokens[self.index][0])
        self.index += 1

        return root
    
    def parse_statement(self):

        # parse expr
        # parse print
        # parse inputstatement
        # parse smooshstatement
        # ....

        tree = Node('statement')
        while self.tokens[self.index][0] != 'KTHXBYE':
            if self.tokens[self.index][1] == 'input':
                tree.children.append(self.parse_input_statement())
            elif self.tokens[self.index][1] == 'output':
                tree.children.append(self.parse_print())
            elif self.tokens[self.index + 1][1] == 'assignment' and self.tokens[self.index][0] != 'number':
                tree.children.append(self.parse_assignment())
            elif self.tokens[self.index][1] == 'arithmetic':
                tree.children.append(self.parse_arithoperation())
            elif self.tokens[self.index][1] == 'concatenation':
                tree.children.append(self.parse_smooshoperation())
            elif self.tokens[self.index][1] == 'boolean':
                tree.children.append(self.parse_booloperation())
            elif self.tokens[self.index][1] == 'typecast':
                tree.children.append(self.parse_typecaststatement())
            elif self.tokens[self.index][1] == 'comparison':
                tree.children.append(self.parse_equality())
            elif self.tokens[self.index][1] == 'ifstart':
                tree.children.append(self.parse_ifstatement())
            elif self.tokens[self.index+1][1] == 'recast' or (self.tokens[self.index][0] == 'number' and self.tokens[self.index+1][1] == 'assignment'):
                tree.children.append(self.parse_recaststatement())
            elif self.tokens[self.index][1] == 'switchstart':
                tree.children.append(self.parse_switchstatement())
            elif self.tokens[self.index][1] == 'function start':
                tree.children.append(self.parse_function())
            elif self.tokens[self.index][1] == 'loopstart':
                tree.children.append(self.parse_loopstatement())
        # tree.children.append(self.parse_expr())
        # tree.children.append(self.smooshstaement())
        return tree

    def parse_input_statement(self):
        tree = Node('inputstatement')
        if self.tokens[self.index][0] != 'GIMMEH':
            print('error at line 105')
        tree.children.append(self.tokens[self.index][0])
        self.index += 1

        tree.children.append(self.tokens[self.index][0])
        self.index += 1

        return tree
    
    def parse_print(self):
        tree = Node('printstatement')
        if self.tokens[self.index][0] != 'VISIBLE':
            print('error at line 117')
        tree.children.append(self.tokens[self.index][0])
        self.index += 1
        tree.children.append(self.parse_literal())
        return tree

    def parse_literal(self):
        tree = Node('literal')
        if self.tokens[self.index][1] == 'numbr' or self.tokens[self.index][1] == 'yarn' or self.tokens[self.index][1] == 'numbar' or self.tokens[self.index][1] == 'troof':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 129')
        return tree

    def parse_assignment(self):
        tree = Node('assignmentstatement')
        tree.children.append(self.tokens[self.index][0])
        self.index += 1
        
        if self.tokens[self.index][0] != 'R':
            print('error at line 138')
        tree.children.append(self.tokens[self.index][0])
        self.index += 1

        tree.children.append(self.parse_literal())

        return tree

    def parse_arithoperation(self):
        tree = Node('arithoperation')

        if self.tokens[self.index][0] != 'SUM OF' and self.tokens[self.index][0] != 'DIFF OF' and self.tokens[self.index][0] != 'PRODUKT OF' and self.tokens[self.index][0] != 'QUOSHUNT OF' and self.tokens[self.index][0] != 'MOD OF' and self.tokens[self.index][0] != 'BIGGR OF' and self.tokens[self.index][0] != 'SMALLR OF':
            print('error at line 150')

        while self.tokens[self.index][0] == 'SUM OF' or self.tokens[self.index][0] == 'DIFF OF' or self.tokens[self.index][0] == 'PRODUKT OF' or self.tokens[self.index][0] == 'QUOSHUNT OF' or self.tokens[self.index][0] == 'MOD OF' or self.tokens[self.index][0] == 'BIGGR OF' or self.tokens[self.index][0] == 'SMALLR OF':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1

        while (self.tokens[self.index][1] == 'numbr' or self.tokens[self.index][1] == 'yarn' or self.tokens[self.index][1] == 'numbar' or self.tokens[self.index][1] == 'troof') and self.tokens[self.index + 1][0] == 'AN':
            tree.children.append(self.parse_literal())
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        
        while self.tokens[self.index][1] == 'identifier' and self.tokens[self.index + 1][0] == 'AN':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
            tree.children.append(self.tokens[self.index][0])
            self.index += 1

        if self.tokens[self.index][1] == 'numbr' or self.tokens[self.index][1] == 'yarn' or self.tokens[self.index][1] == 'numbar' or self.tokens[self.index][1] == 'troof':
            tree.children.append(self.parse_literal())
        elif self.tokens[self.index][1] == 'identifier':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 173')
        
        return tree
    
    def parse_smooshoperation(self):
        tree = Node('concatoperation')
        if self.tokens[self.index][0] == 'SMOOSH':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 183')
        
        if self.tokens[self.index][1] != 'identifier' or self.tokens[self.index + 1][0] != 'AN':
            print('error at line 186')

        while self.tokens[self.index][1] == 'identifier' and self.tokens[self.index + 1][0] == 'AN':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        
        if self.tokens[self.index - 1][0] == 'AN' and self.tokens[self.index][1] == 'identifier':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1

        return tree

    def parse_typecaststatement(self):
        tree = Node('typecaststatement')      

        # MAEK
        if self.tokens[self.index][0] == 'MAEK':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 208')
            
        # varident
        if self.tokens[self.index][1] == 'identifier':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 215')
        
        # A
        if self.tokens[self.index][0] == 'A':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 222')
        
        # TROOF | NUMBAR | NUMBR | YARN 
        if self.tokens[self.index][0] in ['TROOF', 'NUMBAR', 'NUMBR', 'YARN']:
            tree.children.append(self.tokens[self.index][0])  
            self.index += 1
        else:
            print('error at line 229')  
        
        return tree

    def parse_booloperation(self):
        tree = Node('booloperation')
        if self.tokens[self.index][0] == 'BOTH OF' or self.tokens[self.index][0] == 'EITHER OF' or self.tokens[self.index][0] == 'WON OF':
            tree = self.parse_binary()
        elif self.tokens[self.index][0] == 'NOT':
            tree = self.parse_unary()
        elif self.tokens[self.index][0] == 'ALL OF' or self.tokens[self.index][0] == 'ANY OF':
            tree = self.parse_infarity()
        return tree

    def parse_binary(self):
        tree = Node('booloperation')
        if self.tokens[self.index][0] == 'BOTH OF' or self.tokens[self.index][0] == 'EITHER OF' or self.tokens[self.index][0] == 'WON OF':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
            if self.tokens[self.index][1] == 'identifier':
                tree.children.append(self.tokens[self.index][0])
                self.index += 1
            elif self.tokens[self.index][1] == 'numbr' or self.tokens[self.index][1] == 'yarn' or self.tokens[self.index][1] == 'numbar' or self.tokens[self.index][1] == 'troof':
                tree.children.append(self.parse_literal())
            else:
                print('error at line 254')
            
            if self.tokens[self.index][0] == 'AN':
                tree.children.append(self.tokens[self.index][0])
                self.index += 1
            else:
                print('error at line 260')
            
            if self.tokens[self.index][1] == 'identifier':
                tree.children.append(self.tokens[self.index][0])
                self.index += 1
            elif self.tokens[self.index][1] == 'numbr' or self.tokens[self.index][1] == 'yarn' or self.tokens[self.index][1] == 'numbar' or self.tokens[self.index][1] == 'troof':
                tree.children.append(self.parse_literal())
            else:
                print('error at line 269')
        else:
            print('error at line 270')
        
        return tree

    def parse_unary(self):
        tree = Node('booloperation')
        if self.tokens[self.index][0] == 'NOT':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
            if self.tokens[self.index][1] == 'identifier':
                tree.children.append(self.tokens[self.index][0])
                self.index += 1
            elif self.tokens[self.index][1] == 'numbr' or self.tokens[self.index][1] == 'yarn' or self.tokens[self.index][1] == 'numbar' or self.tokens[self.index][1] == 'troof':
                tree.children.append(self.parse_literal())
            else:
                print('error at line 285')
        else:
            print('error at line 287')

        return tree

    def parse_infarity(self):
        tree = Node('booloperation')
        if self.tokens[self.index][0] == 'ALL OF' or self.tokens[self.index][0] == 'ANY OF':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 297')

        while self.tokens[self.index][0] == 'NOT' or self.tokens[self.index][0] == 'BOTH OF' or self.tokens[self.index][0] == 'EITHER OF' or self.tokens[self.index][0] == 'WON OF':
            if self.tokens[self.index][0] == 'NOT':
                tree.children.append(self.parse_unary())
            else:
                tree.children.append(self.parse_binary())

            if self.tokens[self.index][0] == 'AN':
                tree.children.append(self.tokens[self.index][0])
                self.index += 1

        if self.tokens[self.index][0] == 'MKAY':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 313')

        return tree
    
    def parse_equality(self):
        tree = Node('equalityoperation')
        if self.tokens[self.index][0] == 'BOTH SAEM' or self.tokens[self.index][0] == 'DIFFRINT':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        
        if self.tokens[self.index][1] == 'identifier':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        elif self.tokens[self.index][1] == 'numbr' or self.tokens[self.index][1] == 'yarn' or self.tokens[self.index][1] == 'numbar' or self.tokens[self.index][1] == 'troof':
            self.children.append(self.parse_literal)
        else:
            print('error at line 329')
        
        if self.tokens[self.index][0] == 'AN' or self.tokens[self.index][0] == 'AN BIGGR OF' or self.tokens[self.index][0] == 'AN SMALLR OF':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 335')

        if self.tokens[self.index][1] == 'identifier':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        elif self.tokens[self.index][1] == 'numbr' or self.tokens[self.index][1] == 'yarn' or self.tokens[self.index][1] == 'numbar' or self.tokens[self.index][1] == 'troof':
            tree.children.append(self.parse_literal())
        else:
            print('error at line 343')

        return tree
    
    def parse_recaststatement(self):
        tree = Node('recaststatement')      

        if self.tokens[self.index+1][1] == 'recast':
            # varident
            if self.tokens[self.index][1] == 'identifier':
                tree.children.append(self.tokens[self.index][0])
                self.index += 1
            else:
                print('error at line 356')
            
            # IS NOW A
            if self.tokens[self.index][1] == 'recast':
                tree.children.append(self.tokens[self.index][0])
                self.index += 1
            else:
                print('error at line 363')
                
            # TROOF | NUMBAR | NUMBR | YARN 
            if self.tokens[self.index][0] in ['TROOF', 'NUMBAR', 'NUMBR', 'YARN']:
                tree.children.append(self.tokens[self.index][0])  
                self.index += 1
            else:
                print('error at line 370')
        elif self.tokens[self.index][0] == 'number' and self.tokens[self.index+1][1] == 'assignment':
            
            # number R
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
            
            # <typecast>
            tree.children.append(self.parse_typecaststatement())
            
        return tree

    def parse_flow_statement(self):
        tree = Node('flowstatement')
        while True:
            if self.tokens[self.index][1] == 'input':
                tree.children.append(self.parse_input_statement())
                return tree
            elif self.tokens[self.index][1] == 'output':
                tree.children.append(self.parse_print())
                return tree
            elif self.tokens[self.index + 1][0] == 'R':
                tree.children.append(self.parse_assignment())
                return tree
            elif self.tokens[self.index][1] == 'arithmetic':
                tree.children.append(self.parse_arithoperation())
                return tree
            elif self.tokens[self.index][1] == 'concatenation':
                tree.children.append(self.parse_smooshoperation())
                return tree
            elif self.tokens[self.index][1] == 'boolean':
                tree.children.append(self.parse_booloperation())
                return tree
            elif self.tokens[self.index][1] == 'typecast':
                tree.children.append(self.parse_typecaststatement())
                return tree
            elif self.tokens[self.index][1] == 'comparison':
                tree.children.append(self.parse_equality())
                return tree
            elif self.tokens[self.index][1] == 'ifstart':
                tree.children.append(self.parse_ifstatement())
                return tree
            elif self.tokens[self.index][1] == 'switchstart':
                tree.children.append(self.parse_switchstatement())
                return tree
            elif self.tokens[self.index][1] == 'function start':
                tree.children.append(self.parse_function())
                return tree
            elif self.tokens[self.index][1] == 'linebreak':
                tree.children.append(self.tokens[self.index][0])
                self.index += 1
                return tree

    def parse_ifstatement(self):
        tree = Node('ifstatement')
        if self.tokens[self.index][0] == 'O RLY?':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 431')

        if self.tokens[self.index][0] == '\n':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 437')

        if self.tokens[self.index][0] == 'YA RLY':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 443')
        
        if self.tokens[self.index][0] == '\n':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 449')

        tree.children.append(self.parse_flow_statement())

        if self.tokens[self.index][0] == '\n':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 457')


        while self.tokens[self.index][0] == 'MEBBE':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
            if self.tokens[self.index][0] == '\n':
                tree.children.append(self.tokens[self.index][0])
                self.index += 1
            else:
                print('error at line 467')

            tree.children.append(self.parse_flow_statement())
            
            if self.tokens[self.index][0] == '\n':
                tree.children.append(self.tokens[self.index][0])
                self.index += 1
            else:
                print('error at line 475')
        
        if self.tokens[self.index][0] == '\n':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 481')
        
        if self.tokens[self.index][0] == 'NO WAI':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 487')
        
        if self.tokens[self.index][0] == '\n':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 494')

        tree.children.append(self.parse_flow_statement())

        if self.tokens[self.index][0] == '\n':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 501')

        if self.tokens[self.index][0] == 'OIC':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 507')

        if self.tokens[self.index][0] == '\n':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 513')

        return tree

    def parse_switchstatement(self):
        tree = Node('switchstatement')
        if self.tokens[self.index][0] == 'WTF?':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 523')

        if self.tokens[self.index][0] == '\n':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 529')

        while self.tokens[self.index][0] == 'OMG':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1

            if self.tokens[self.index][1] == 'numbr' or self.tokens[self.index][1] == 'yarn' or self.tokens[self.index][1] == 'numbar' or self.tokens[self.index][1] == 'troof':
                tree.children.append(self.parse_literal())
            else:
                print('error at line 539')

            if self.tokens[self.index][0] == '\n':
                tree.children.append(self.tokens[self.index][0])
                self.index += 1
            else:
                print('error at line 544')

            tree.children.append(self.parse_flow_statement())

            if self.tokens[self.index][0] == '\n':
                tree.children.append(self.tokens[self.index][0])
                self.index += 1
            else:
                print('error at line 552')
        
        if self.tokens[self.index][0] == 'OMGWTF':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 558')

        if self.tokens[self.index][0] == '\n':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 564')

        tree.children.append(self.parse_flow_statement())

        if self.tokens[self.index][0] == '\n':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 572')

        if self.tokens[self.index][0] == 'OIC':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 578')

        if self.tokens[self.index][0] == '\n':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 584')

        return tree

    def parse_expression(self):
        tree = Node('expression')
        if self.tokens[self.index][1] == 'arithmetic':
            tree.children.append(self.parse_arithoperation())
        elif self.tokens[self.index][1] == 'boolean':
            tree.children.append(self.parse_booloperation())
        elif self.tokens[self.index][1] == 'comparison':
            tree.children.append(self.parse_equality())
        else:
            print('error at line 597')
        return tree

    def parse_function(self):
        tree = Node('function')
        if self.tokens[self.index][0] == 'HOW IZ I':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 606')


        if self.tokens[self.index][1] == 'identifier':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 613')


        while self.tokens[self.index][0] == 'YR':
            if self.tokens[self.index][0] == 'YR':
                tree.children.append(self.tokens[self.index][0])
                self.index += 1
            else:
                print('error at line 621')
            
            if self.tokens[self.index][1] == 'identifier':
                tree.children.append(self.tokens[self.index][0])
                self.index += 1
            else:
                print('error at line 627')

            if self.tokens[self.index][0] != 'AN':
                break
            else:
                tree.children.append(self.tokens[self.index][0])
                self.index += 1

            print(self.tokens[self.index][0])

            
        
        if self.tokens[self.index][0] == '\n':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 643')

        tree.children.append(self.parse_flow_statement())

        if self.tokens[self.index][0] == '\n':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 651')

        if self.tokens[self.index][0] == 'GTFO':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        elif self.tokense[self.index][0] == 'FOUND YR':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
            tree.children.append(self.parse_expression())
        else:
            print('error at line 661')

        if self.tokens[self.index][0] == '\n':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 667')

        if self.tokens[self.index][0] == 'IF U SAY SO':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 673')

        if self.tokens[self.index][0] == '\n':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 679')
        
        return tree
    
    # <loop> ::= IM IN YR loopident <loopoperation> YR varident <loopcondition> <linebreak> <loopstatement> <linebreak> IM OUTTA YR loopident
    def parse_loopstatement(self):
        tree = Node('loop')

        if self.tokens[self.index][1] == 'loopstart':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else: 
            print('error at line 691')
        
        # loopident
        if self.tokens[self.index][1] == 'identifier':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else: 
            print('error at line 698')
        
        # <loopoperation>
        tree.children.append(self.parse_loopoperation())
        
        # YR
        if self.tokens[self.index][1] == 'params':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 708')
        
        # varident
        if self.tokens[self.index][1] == 'identifier':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 715')
        
        # <loopocondition>
        tree.children.append(self.parse_loopcondition())
        
        # \n
        if self.tokens[self.index][1] == 'linebreak':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 725')
        
        # <loopstatement>
        tree.children.append(self.parse_flow_statement())
        # self.index += 1
        
        # \n
        if self.tokens[self.index][1] == 'linebreak':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 736')
                
        if self.tokens[self.index][1] == 'loopend':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 742')
            
        # loopident
        if self.tokens[self.index][1] == 'identifier':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else: 
            print('error at line 749')
        
        return tree
        
        
    # <loopcondition> ::= UPPIN | NERFIN
    def parse_loopoperation(self):
        tree = Node('loopoperation')
        
        if self.tokens[self.index][1] == 'increment' or self.tokens[self.index][1] == 'decrement':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 762')
        return tree
        
        
    # <loopcondition> ::= loopcondition TIL <boolstatement> | WILE <boolstatement>
    def parse_loopcondition(self):
        tree = Node('loopcondition')
        
        if self.tokens[self.index][1] == 'loop condition':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error at line 774')
            
        # <boolstatement>
        tree.children.append(self.parse_booloperation())

        return tree

        


lexemes = [['HAI', 'program start'], ['\n', 'linebreak'], ['GIMMEH', 'input'], ['x', 'identifier'], ['VISIBLE', 'output'], ['7', 'numbr'], 
            ['y', 'identifier'], ['R', 'assignment'], ['2', 'numbr'], ['SUM OF', 'arithmetic'], ['QUOSHUNT OF', 'arithmetic'], ['4', 'numbr'], ['AN', 'operand separator'], ['6', 'numbr'], 
            ['GIMMEH', 'input'], ['x', 'identifier'], ['SUM OF', 'arithmetic'], ['QUOSHUNT OF', 'arithmetic'], 
            ['PRODUKT OF', 'arithmetic'], ['3', 'numbr'], ['AN', 'operand separator'], ['4', 'numbr'], ['AN', 'operand separator'], ['2', 'numbr'], ['AN', 'operand separator'], ['1', 'numbr'],
            ['SMOOSH', 'concatenation'], ['a', 'identifier'], ['AN', 'operand separator'], ['b', 'identifier'],
            ['AN', 'operand separator'], ['c', 'identifier'], ['EITHER OF', 'boolean'], ['x', 'identifier'], ['AN', 'operand separator'], ['3', 'numbr'],
            ['MAEK', 'typecast'], ['varident', 'identifier'], ['A', 'opsep'], ['TROOF', 'datatype'], 
            ['NOT', 'boolean'], ['3', 'numbr'],
            ['ALL OF', 'boolean'], ['NOT', 'boolean'], ['x', 'identifier'], ['AN', 'operand separator'], ['BOTH OF', 'boolean'], ['y', 'identifier'],
            ['AN', 'operand separator'], ['z', 'identifier'], ['AN', 'operand separator'], ['EITHER OF', 'boolean'], ['x', 'identifier'],
            ['AN', 'operand separator'], ['y', 'identifier'], ['MKAY', 'end of operands'],
            ['BOTH SAEM', 'comparison'], ['y', 'identifier'], ['AN BIGGR OF', 'operand separator'], ['3', 'numbar'],
            ['O RLY?', 'ifstart'], ['\n', 'linebreak'], ['YA RLY', 'ifif'], ['\n', 'linebreak'], ['SUM OF', 'arithmetic'], ['x', 'identifier'], ['AN', 'operand separator'], ['3', 'numbr'], ['\n', 'linebreak'],
            ['MEBBE', 'elseif'], ['\n', 'linebreak'], ['SMOOSH', 'concatenation'], ['x', 'identifier'], ['AN', 'operand separator'], ['b', 'identifier'], ['\n', 'linebreak'],
            ['MEBBE', 'elseif'], ['\n', 'linebreak'], ['GIMMEH', 'input'], ['x', 'identifier'], ['\n', 'linebreak'],
            ['NO WAI', 'elsekey'], ['\n', 'linebreak'], ['VISIBLE', 'output'], ['7', 'numbr'], ['\n', 'linebreak'],
            ['OIC', 'flowend'], ['\n', 'linebreak'],
            ['xxx', 'identifier'], ['IS NOW A', 'recast'], ['TROOF', 'datatype'],
            ['number', 'idk'], ['R', 'assignment'],['MAEK', 'typecast'], ['varident', 'identifier'], ['A', 'opsep'], ['TROOF', 'datatype'],
            ['WTF?', 'switchstart'], ['\n', 'linebreak'], ['OMG', 'switchcase'], ['3', 'numbr'], ['\n', 'linebreak'], ['GIMME', 'input'], ['3', 'numbr'], ['\n', 'linebreak'],
            ['OMG', 'switchcase'], ['10', 'numbr'], ['\n', 'linebreak'], ['SMOOSH', 'concatenation'], ['a', 'identifier'], ['AN', 'operand separator'], ['b', 'identifier'], ['\n', 'linebreak'],
            ['OMGWTF', 'switchdef'], ['\n', 'linebreak'], ['SUM OF', 'arithmetic'], ['2', 'numbr'], ['AN', 'operand separator'], ['1', 'numbr'], ['\n', 'linebreak'],
            ['OIC', 'flowend'], ['\n', 'linebreak'],
            ['HOW IZ I', 'function start'], ['hello', 'identifier'], ['YR', 'parameter'], ['x', 'identifier'], ['AN', 'operand separator'], ['YR', 'parameter'], ['y', 'identifier'], ['\n', 'linebreak'],
            ['SUM OF', 'arithmetic'], ['2', 'numbr'], ['AN', 'operand separator'], ['1', 'numbr'], ['\n', 'linebreak'],
            ['GTFO', 'break'], ['\n', 'linebreak'],
            ['IM IN YR', 'loopstart'], 
            ['loopident', 'identifier'], 
            ['UPPIN', 'increment'], 
            ['YR', 'params'], ['varident', 'identifier'], 
            ['TIL', 'loop condition'], ['NOT', 'boolean'], ['3', 'numbr'],
            ['\n', 'linebreak'], 
            ['GIMMEH', 'input'], ['x', 'identifier'],
            ['\n', 'linebreak'], ['IM OUTTA YR', 'loopend'], ['loopident', 'identifier'], 
            ['KTHXBYE', 'program end']]

p = Parser(lexemes)
t = p.parse()
print(t)