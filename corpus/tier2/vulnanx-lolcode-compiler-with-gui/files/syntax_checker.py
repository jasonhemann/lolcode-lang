from error import Error
from lexer import Lexer
from token_class import TokenClass
from global_tokens import GlobalTokens

# ============= FLOW =============
#   1. check validity of comments
#   2. clean tokens
#   3. iterate per token in line ; break after a match
#   4. check correctness based off tokens in the line
#   5. perform recursion for checking  



class SyntaxChecker:
    expressions = (
        "arithmetic operation", "logical operation"
    )

    io = (
        "output statement", "input statement"
    )

    binary_operations = (
        "PRODUKT OF", "QUOSHUNT OF", "SMALLR OF", "BIGGR OF", "EITHER OF",
        "SUM OF", "DIFF OF", "MOD OF", "BOTH OF", "WON OF", "BOTH SAEM",
        "DIFFRINT"
    )

    nary_operations = (
        "ALL OF", "ANY OF", "SMOOSH"
    )

    literals = (
        "NUMBAR", "NUMBR", "TROOF", "YARN"
    )


    def __init__(self, program):
        self.lexer = Lexer(program)
        self.tokens = self.lexer.tokenize()
        self.cleaned_tokens = self._clean_tok()
        self.paired_tags_stack = []
        self.errors = []
        self.var_table = {"IT": ["NOOB", None, 0]} # IT variable will always be here, but initially set to no value (NOOB)

        if self.cleaned_tokens:
            self.first_line = min(self.cleaned_tokens.keys())
            self.second_line = list(self.cleaned_tokens.keys())[1]
            self.last_line = max(self.cleaned_tokens.keys())
        else:
            self.first_line = 0
            self.second_line = 0
            self.last_line = 0
    
    def check_syntax(self):

        # STEP 1 : CHECK FOR THE CORRECTNESS OF COMMENTS
        for line_number, tokens_in_line in self.tokens.items():
            for token in tokens_in_line:
                if token.value in ("OBTW", "TLDR"):
                    self._comment_handler(line_number, tokens_in_line, token)

        # STEP 2 : CHECK FOR THE VALIDITY OF EACH TOKEN
        for line_number, tokens_in_line in self.cleaned_tokens.items():
            for token in tokens_in_line:

                if token.type == "program delimiter":
                    self._program_delimiter_handler(line_number, tokens_in_line, token)
                    break

                if token.type == "variable declaration":
                    self._variable_declaration_handler(line_number, tokens_in_line, token)
                    break

                if token.type == "function declaration":
                    self._function_declaration_handler(line_number, tokens_in_line, token)
                    break

                if token.type == "function call":
                    self._function_call_handler(line_number, tokens_in_line, token)
                    break

                if token.type == "if-then statement":
                    self._if_then_handler(line_number, tokens_in_line, token)
                    break

                if token.type == "switch-case statement":
                    self._switch_case_handler(line_number, tokens_in_line, token)
                    break

                if token.type == "loop statement":
                    self._loop_handler(line_number, tokens_in_line, token)
                    break

                if token.type == "return statement":
                    self._return_handler(line_number, tokens_in_line, token)
                    break

                if token.type == "typecasting statement":
                    self._typecast_handler(GlobalTokens(line_number, tokens_in_line, token))
                    break

                if token.type == "reassignment statement":
                    self._reassignment_handler(GlobalTokens(line_number, tokens_in_line, token))
                    break

                if token.type in self.io:
                    self._io_handler(line_number, tokens_in_line, token)
                    break

                if token.value == "NOT":
                    self._unary_handler(GlobalTokens(line_number, tokens_in_line, token))
                    break

                if token.value in self.binary_operations:
                    self._binary_operations_handler(GlobalTokens(line_number, tokens_in_line, token))
                    break

                if token.value in self.nary_operations:
                    self._nary_operations_handler(GlobalTokens(line_number, tokens_in_line, token))
                    break

                if self.paired_tags_stack and token.type == "closing statement" and token.value not in ("MKAY", "GTFO"):
                    self._closing_tag_handler(line_number, tokens_in_line, token)
                    break

                if token.type == "variable":
                    self._variable_handler(line_number, token)
                    break

                if token.type == "unknown":
                    self._add_err(line_number)._invalid_variable(token)
                    break

        # STEP 3: CHECK FOR UNRESOLVED PAIRED TAGS
        if self.paired_tags_stack:
            self._add_err(self._pt_tos()["line number"])._tag_mismatch(self._pt_tos()["token"])

        return self.errors, self.cleaned_tokens



    # SYNTAX HANDLER FUNCTIONS

    def _comment_handler(self, line_num, tokens, token):
        error_found = False

        if len(tokens) > 1:
            self._add_err(line_num)._operand_count_mismatch(token)
            error_found = True

        if token.value == "OBTW":
            if not error_found:
                self._add_pt(line_num, token, "comment")

        if token.value == "TLDR":
            if not self.paired_tags_stack or self._pt_tos()["token value"] != "OBTW":
                self._add_err(line_num)._tag_mismatch(token)
                error_found = True

            if not error_found:
                self.paired_tags_stack.pop()

    def _expression_handler(self, global_tokens):
        token = global_tokens.get_tok_at_pos()
        line_num = global_tokens.line_num

        if token.type in self.literals:
            return token
        elif token.type == "variable":
            return self._variable_handler(line_num, token)
        elif token.type == "typecasting statement":
            return self._typecast_handler(global_tokens)
        elif token.value in self.binary_operations:
            return self._binary_operations_handler(global_tokens)
        elif token.value in self.nary_operations:
            return self._nary_operations_handler(global_tokens)
        elif token.value == "NOT":
            return self._unary_handler(global_tokens)
        else:
            self._add_err(global_tokens.line_num)._invalid_variable(token)
            return

    def _variable_handler(self, line_num, token):
        if self.paired_tags_stack and self._pt_tos()["token value"] == "HOW IZ I":
            return False
        if token.value not in self.var_table:   # ignores variables in functions for now since global symbol table pa lang kinukuha
            self._add_err(line_num)._var_undeclared(token)
            return True
        return False
        
    def _program_delimiter_handler(self, line_num, tokens, token):
        error_found = False

        if token.value == "HAI":
            if line_num != self.first_line:
                self._add_err(line_num)._program_delimiter_mismatch(token)
                error_found = True
            if len(tokens) > 1:
                self._add_err(line_num)._operand_count_mismatch(token)
                error_found = True

            if not error_found:
                self._add_pt(line_num, token, "start of program")

        elif token.value == "KTHXBYE":
            if line_num != self.last_line:
                self._add_err(line_num)._program_delimiter_mismatch(token)
                error_found = True
            if len(tokens) > 1:
                self._add_err(line_num)._operand_count_mismatch(token)
                error_found = True
            if not self.paired_tags_stack or self._pt_tos()["token value"] != "HAI":
                self._add_err(line_num)._tag_mismatch(token)
                error_found = True

            if not error_found:
                self.paired_tags_stack.pop()

    def _variable_declaration_handler(self, line_num, tokens, token):
        error_found = False

        if token.value == "WAZZUP":
            if line_num != self.second_line:
                self._add_err(line_num)._program_delimiter_mismatch(token)
                error_found = True
            if len(tokens) > 1:
                self._add_err(line_num)._operand_count_mismatch(token)
                error_found = True

            if not error_found:
                self._add_pt(line_num, token, "start of var dec")

        elif token.value == "I HAS A":
            if self._pt_tos()["token value"] != "WAZZUP":
                self._add_err(line_num)._declared_outside(token)
                return

            if len(tokens) < 2:
                self._add_err(line_num)._operand_count_mismatch(token)
                return
            elif len(tokens) == 2:
                variable = tokens[1]
                if variable.type != "variable":
                    self._add_err(line_num)._invalid_variable(variable)
                    return
                self.var_table[variable.value] = ["NOOB", None, line_num]
            elif len(tokens) >= 4:
                variable = tokens[1]
                itz = tokens[2]
                value = tokens[3:]

                if variable.type != "variable":
                    self._add_err(line_num)._invalid_variable(variable)
                    return
                if itz.value != "ITZ":
                    self._add_err(line_num)._word_mismatch("ITZ", itz)
                    return
                if value[0].type in self.expressions:
                    self._expression_handler(GlobalTokens(line_num, value, value[0]))
                elif value[0].type not in ("variable",) + self.literals:
                    self._add_err(line_num)._invalid_variable(value[0])
                    return
                self.var_table[variable.value] = [value[0].type, value, line_num] # store value as tokens muna for easier evaluation

    def _closing_tag_handler(self, line_num, tokens, token):
        if not self.paired_tags_stack:
            self._add_err(line_num)._tag_mismatch(token)
            return

        tos = self._pt_tos()
        opening_tag = ()
        max_length = 1
        
        if token.value == "IM OUTTA YR":
            opening_tag = ("IM IN YR")
            max_length = 2
        if token.value == "OIC":
            opening_tag = ("O RLY?", "WTF?")
        if token.value == "MKAY":
            opening_tag = ("I IZ", "ALL OF", "ANY OF", "SMOOSH")
        if token.value == "IF U SAY SO":
            opening_tag = ("HOW IZ I")
        if token.value == "BUHBYE":
            opening_tag = ("WAZZUP")
            
        if tos["token value"] not in opening_tag:
            self._add_err(line_num)._tag_mismatch(token)
            return
        if token.value != "MKAY" and len(tokens) != max_length:
            self._add_err(line_num)._operand_count_mismatch(token)
            return
        if token.value == "IM OUTTA YR":
            label = tokens[1]
            if label.value != self._pt_tos()["label"]:
                self._add_err(line_num)._label_mismatch(self._pt_tos()["label"], label.value)
                return

        self.paired_tags_stack.pop()

    def _unary_handler(self, global_tokens):
        valid_operands = ("variable",) + self.literals
        line_num = global_tokens.line_num
        tokens = global_tokens.tokens
        token = global_tokens.operation

        operation = global_tokens.get_tok_at_pos()
        global_tokens.consume()

        operand = global_tokens.get_tok_at_pos()
        if not operand:
            self._add_err(line_num)._operand_count_mismatch(token)
            return
        
        if operand.type in self.expressions:
            self._expression_handler(global_tokens)
        elif operand.type in valid_operands:
            if operand.type == "variable" and self._variable_handler(line_num, operand):
                return
            global_tokens.consume()
        else:
            self._add_err(line_num)._invalid_variable(token)

        if operation == token and global_tokens.pos < len(tokens):
            self._add_err(line_num)._operand_count_mismatch(token)

    def _binary_operations_handler(self, global_tokens):
        valid_operands = ("variable",) + self.literals
        line_num = global_tokens.line_num
        tokens = global_tokens.tokens
        token = global_tokens.operation

        operation = global_tokens.get_tok_at_pos()
        global_tokens.consume()

        left = global_tokens.get_tok_at_pos()
        if not left:
            self._add_err(line_num)._operand_count_mismatch(token)
            return

        if left.type in self.expressions:
            # if operation.type == "arithmetic operation" and left.type == "logical operation":
            #     self._add_err(line_num)._invalid_variable(left)
            #     return
            # global_tokens.operation = left
            self._expression_handler(global_tokens)
        elif left.type in valid_operands:
            if left.type == "variable" and self._variable_handler(line_num, left):
                return
            global_tokens.consume()
        else:
            self._add_err(line_num)._invalid_variable(token)
        
        an = global_tokens.consume(TokenClass("conjunction", "AN", False))
        if isinstance(an, Error):
            self.errors.append(an)
            return
        
        right = global_tokens.get_tok_at_pos()
        if not right:
            self._add_err(line_num)._operand_count_mismatch(token)
            return
    
        if right.type in self.expressions:
            # if operation.type == "arithmetic operation" and right.type == "logical operation":
            #     self._add_err(line_num)._invalid_variable(right)
            #     return
            # global_tokens.operation = right
            self._expression_handler(global_tokens)
        elif right.type in valid_operands:
            if right.type == "variable" and self._variable_handler(line_num, right):
                return
            global_tokens.consume()
        else:
            self._add_err(line_num)._invalid_variable(token)

        if operation == token and global_tokens.pos < len(tokens):
            self._add_err(line_num)._operand_count_mismatch(token)

    def _nary_operations_handler(self, global_tokens):
        valid_operands = ("variable",) + self.literals
        line_num = global_tokens.line_num
        tokens = global_tokens.tokens
        token = global_tokens.operation

        if global_tokens.get_tok_at_pos() == token:
            operation = global_tokens.get_tok_at_pos()
            global_tokens.consume()

        while True:
            operand = global_tokens.get_tok_at_pos()
            if not operand:
                self._add_err(line_num)._operand_count_mismatch(token)
                return
            
            if operand.type in self.expressions and operand.value not in self.nary_operations:
                self._expression_handler(global_tokens)
            elif operand.type in valid_operands:
                if operand.type == "variable" and self._variable_handler(line_num, operand):
                    return
                global_tokens.consume()
            else:
                self._add_err(line_num)._invalid_variable(token)

            an = global_tokens.consume(TokenClass("conjunction", "AN", False))
            if isinstance(an, Error):   # line did not end with AN
                if token.value != "SMOOSH":
                    mkay = global_tokens.consume(TokenClass("closing statement", "MKAY", False))
                    if isinstance(mkay, Error):
                        self.errors.append(mkay)
                        return
                    break
                if global_tokens.pos >= len(tokens):
                    break
                self.errors.append(an)
                return

    def _parameter_handler(self, global_tokens):
        valid_parameters = ("variable", "parameter") + self.literals
        line_num = global_tokens.line_num
        tokens = global_tokens.tokens
        token = global_tokens.operation

        actual_tokens = tokens
        expects_mkay = token.value == "I IZ"
        if expects_mkay and tokens[-1].value == "MKAY":
            actual_tokens = tokens[:-1]
        elif expects_mkay and tokens[-1].value != "MKAY":
            self._add_err(line_num)._word_mismatch(TokenClass("closing statement", "MKAY", False), tokens[-1])
            return False

        yr_count = self._count_yr(actual_tokens)
        
        for counter in range(yr_count):
            yr = global_tokens.consume(TokenClass("variable reference", "YR", False))
            if isinstance(yr, Error):
                self.errors.append(yr)
                return False
            
            parameter = global_tokens.get_tok_at_pos()
            if not parameter:
                self._add_err(line_num)._operand_count_mismatch(token)
                return False
            
            if parameter.type in self.expressions:
                next_an_yr_pos = self._find_next_an_yr(global_tokens.pos, actual_tokens)
                
                if next_an_yr_pos is not None:
                    temp_tokens = actual_tokens[global_tokens.pos:next_an_yr_pos]
                else:
                    temp_tokens = actual_tokens[global_tokens.pos:]
                
                temp_global_tokens = GlobalTokens(line_num, temp_tokens, parameter)
                self._expression_handler(temp_global_tokens)
                global_tokens.pos += temp_global_tokens.pos

            elif parameter.type in valid_parameters:
                global_tokens.consume()
            else:
                self._add_err(line_num)._invalid_variable(parameter)
                return False
            
            if counter < yr_count - 1:
                an = global_tokens.consume(TokenClass("conjunction", "AN", False))
                if isinstance(an, Error):
                    self.errors.append(an)
                    return False
        
        if global_tokens.pos < len(actual_tokens):
            self._add_err(line_num)._operand_count_mismatch(token)
            return False
                    
        return True

    def _function_declaration_handler(self, line_num, tokens, token):
        if len(tokens) < 2:
            self._add_err(line_num)._operand_count_mismatch(token)
            return
        
        label = tokens[1]
        if label.type != "function label":
            self._add_err(line_num)._invalid_variable(label)
            return
        
        if len(tokens) >= 4:
            valid = self._parameter_handler(GlobalTokens(line_num, tokens[2:], token))
        else:
            self._add_err(line_num)._operand_count_mismatch(token)
            return
        
        if valid:
            self._add_pt(line_num, token, label.value)

    def _function_call_handler(self, line_num, tokens, token):
        if len(tokens[:-1]) < 2:
            self._add_err(line_num)._operand_count_mismatch(token)
            return
        
        label = tokens[1]
        if label.type != "function label":
            self._add_err(line_num)._invalid_variable(label)
            return
        
        if len(tokens) >= 4:
            self._parameter_handler(GlobalTokens(line_num, tokens[2:], token))
        else:
            self._add_err(line_num)._operand_count_mismatch(token)
            return

    def _if_then_handler(self, line_num, tokens, token):
        # if self.var_table['IT'] == ["NOOB", None, 0]:
        #     self._add_err(line_num)._nothing_to_compare(token)

        if token.value == "O RLY?":
            self._add_pt(line_num, token, "start of if-then")

        if token.value != "O RLY?":
            if self.paired_tags_stack and self._pt_tos()["token value"] != "O RLY?":
                self._add_err(line_num)._declared_outside(token)
                return
        
        if token.value != "MEBBE":
            if len(tokens) > 1:
                self._add_err(line_num)._operand_count_mismatch(token)
                return
            
        if token.value == "MEBBE":
            global_tokens = GlobalTokens(line_num, tokens, token)
            global_tokens.consume() # consume MEBBE

            operand = global_tokens.get_tok_at_pos()
            if isinstance(operand, Error) or not operand:
                self._add_err(line_num)._operand_count_mismatch(token)
                return
            else:
                if operand.type == "logical operation":
                    self._expression_handler(global_tokens)
                else:
                    self._add_err(line_num)._invalid_variable(operand)

    def _switch_case_handler(self, line_num, tokens, token):
        # if self.var_table['IT'] == ["NOOB", None, 0]:
        #     self._add_err(line_num)._nothing_to_compare(token)

        if token.value == "WTF?":
            self._add_pt(line_num, token, "start of if-then")
        
        elif token.value == "OMG":
            if len(tokens) != 2:
                self._add_err(line_num)._operand_count_mismatch(token)
                return
            operand = tokens[1]
            if operand.type not in self.literals:
                self._add_err(line_num)._invalid_variable(operand)
                return
            
        elif token.value == "OMGWTF":
            if len(tokens) != 1:
                self._add_err(line_num)._operand_count_mismatch(token)
                return

    def _loop_handler(self, line_num, tokens, token):
        if token.value == "IM IN YR":
            if len(tokens) < 6:
                self._add_err(line_num)._operand_count_mismatch(token)
                return

            label = tokens[1]
            operation = tokens[2]
            yr = tokens[3]
            variable = tokens[4]
            loop_type = tokens[5]
            expression = tokens[6:]

            if label.type != "loop label":
                self._add_err(line_num)._invalid_variable(label)
                return
            if operation.value not in ("UPPIN", "NERFIN"):
                self._add_err(line_num)._word_mismatch(TokenClass("loop statement", "UPPIN", False), operation)
                return
            if yr.value != "YR":
                self._add_err(line_num)._word_mismatch(TokenClass("variable reference", "YR", False), yr)
                return
            if variable.type != "variable":
                self._add_err(line_num)._invalid_variable(variable)
                return
            if variable.type == "variable" and self._variable_handler(line_num, variable):
                return
            if loop_type.value not in ("TIL", "WILE"):
                self._add_err(line_num)._word_mismatch(TokenClass("loop statement", "TIL", False), loop_type)
                return
            if expression[0].type not in self.expressions:
                self._add_err(line_num)._invalid_variable(expression[0])
                return

            self._expression_handler(GlobalTokens(line_num, expression, expression[0]))
            self._add_pt(line_num, token, label.value)

    def _return_handler(self, line_num, tokens, token):        
        if token.value == "FOUND YR":
            if self.paired_tags_stack and self._pt_tos()["token value"] != "HOW IZ I":
                self._add_err(line_num)._declared_outside(token)
                return
                
            valid_expressions = ("variable",) + self.literals

            if len(tokens) < 2:
                self._add_err(line_num)._operand_count_mismatch(token)
                return
            
            return_value = tokens[1:]
            if return_value[0].type in self.expressions:
                self._expression_handler(GlobalTokens(line_num, return_value, return_value[0]))
            elif return_value[0].type not in valid_expressions:
                self._add_err(line_num)._invalid_variable(return_value[0])
                return
        
        if token.value == "GTFO":
            if len(tokens) != 1:
                self._add_err(line_num)._operand_count_mismatch(token)
                return

    def _typecast_handler(self, global_tokens):
        line_num = global_tokens.line_num
        tokens = global_tokens.tokens
        token = global_tokens.operation

        if token.value == "MAEK":
            if len(tokens) == 3:
                variable = tokens[1]
                new_type = tokens[2]

                if variable.type != "variable":
                    self._add_err(line_num)._invalid_variable(variable)
                    return
                if variable.type == "variable" and self._variable_handler(line_num, variable):
                    return
                if new_type.value not in self.literals:
                    self._add_err(line_num)._invalid_variable(new_type)
                    return
            elif len(tokens) == 4:
                variable = tokens[1]
                a = tokens[2]
                new_type = tokens[3]

                if variable.type != "variable":
                    self._add_err(line_num)._invalid_variable(variable)
                    return
                if variable.type == "variable" and self._variable_handler(line_num, variable):
                    return
                if a.value != "A":
                    self._add_err(line_num)._word_mismatch(TokenClass("typecasting statement", "A", False), a)
                    return
                if new_type.value not in self.literals:
                    self._add_err(line_num)._invalid_variable(new_type)
                    return
            else:
                self._add_err(line_num)._operand_count_mismatch(token)
                return

        elif token.value == "IS NOW A":
            if len(tokens) != 3:
                self._add_err(line_num)._operand_count_mismatch(token)
                return
            
            variable = tokens[0]
            new_type = tokens[2]

            if variable.type != "variable":
                self._add_err(line_num)._invalid_variable(variable)
                return
            if variable.type == "variable" and self._variable_handler(line_num, variable):
                return
            if new_type.value not in self.literals:
                self._add_err(line_num)._invalid_variable(new_type)
                return

    def _reassignment_handler(self, global_tokens):
        line_num = global_tokens.line_num
        tokens = global_tokens.tokens
        token = global_tokens.operation

        operation = global_tokens.get_tok_at_pos()
        if operation.type == "variable":
            if self._variable_handler(line_num, operation):
                return
            global_tokens.consume()
        else:
            self._add_err(line_num)._invalid_variable(operation)
            return

        r = global_tokens.consume(TokenClass("reassignment statement", "R", False))
        if isinstance(r, Error):
            self.errors.append(r)
            return
        
        temp_tokens = tokens[global_tokens.pos:]
        self._expression_handler(GlobalTokens(line_num, temp_tokens, temp_tokens[0]))

    def _io_handler(self, line_num, tokens, token):
        if token.value == "VISIBLE":
            valid_operands = ("variable",) + self.literals
            global_tokens = GlobalTokens(line_num, tokens, token)
            global_tokens.consume()

            operand = global_tokens.get_tok_at_pos()
            if not operand:
                self._add_err(line_num)._operand_count_mismatch(token)
                return
                
            if operand.type in self.expressions:
                global_tokens.operation = operand
                self._expression_handler(global_tokens)
            elif operand.type in valid_operands:
                if operand.type == "variable" and self._variable_handler(line_num, operand):
                    return
                global_tokens.consume()
            else:
                self._add_err(line_num)._invalid_variable(operand)
                return
            
            while global_tokens.pos < len(tokens):
                concat = global_tokens.consume(TokenClass("output concat", "+", False))
                if isinstance(concat, TokenClass):
                    if concat.get_type_value() == ("output concat", "+"):
                        next_operand = global_tokens.get_tok_at_pos()
                        if not next_operand:
                            self._add_err(line_num)._operand_count_mismatch(token)
                            return
                        
                        if next_operand.type in self.expressions:
                            next_plus_pos = self._find_next_plus(global_tokens.pos, tokens)
                            
                            if next_plus_pos is not None:
                                temp_tokens = tokens[global_tokens.pos:next_plus_pos]
                            else:
                                temp_tokens = tokens[global_tokens.pos:]
                            
                            temp_global_tokens = GlobalTokens(line_num, temp_tokens, next_operand)
                            self._expression_handler(temp_global_tokens)
                            
                            global_tokens.pos += temp_global_tokens.pos
                            
                        elif next_operand.type in valid_operands:
                            if next_operand.type == "variable" and self._variable_handler(line_num, next_operand):
                                return
                            global_tokens.consume()
                        else:
                            self._add_err(line_num)._invalid_variable(next_operand)
                            return
                    else:
                        self._add_err(line_num)._invalid_variable(concat)
                        return
                else:
                    remaining = global_tokens.get_tok_at_pos()
                    if remaining:
                        self._add_err(line_num)._word_mismatch(TokenClass("output concat", "+", False), remaining)
                        return
                    break 
            
        elif token.value == "GIMMEH":
            if len(tokens) != 2:
                self._add_err(line_num)._operand_count_mismatch(token)
                return
            
            operand = tokens[1]
            if operand.type != "variable":
                self._add_err(line_num)._invalid_variable(operand)
                return
            if operand.type == "variable" and self._variable_handler(line_num, operand):
                return



    # HELPER FUNCTIONS

    def _clean_tok(self):
        cleaned_tokens = {}
        for line_number, tokens in self.tokens.items():
            if not tokens:
                continue
            non_comment_tokens = [t for t in tokens if t.type != "comment"]
            if non_comment_tokens:
                cleaned_tokens[line_number] = non_comment_tokens
        return cleaned_tokens
    
    def _clean_err(self):
        final_errors = []
        seen = set()
        
        for error in self.errors:
            key = (error.line_number, repr(error))
            if key not in seen:
                seen.add(key)
                final_errors.append(error)

        return final_errors

    def _count_yr(self, tokens):
        yr_count = 0
        for token in tokens:
            if token.value == "YR":
                yr_count += 1

        return yr_count

    def _find_next_an_yr(self, start_pos, tokens):
        i = start_pos
        while i < len(tokens) - 1:
            if tokens[i].value == "AN" and tokens[i + 1].value == "YR":
                return i
            i += 1
        return None
    
    def _find_next_plus(self, start_pos, tokens):
        for i in range(start_pos, len(tokens)):
            if tokens[i].value == "+":
                return i
        return None

    def _add_err(self, line_number):
        new_err = Error(line_number)
        self.errors.append(new_err)
        return new_err
    
    def _add_pt(self, line_number, token, label):
        paired_tag_info = {
            "line number": line_number,
            "token": token,
            "token type": token.type,
            "token value": token.value,
            "label": label
        }
        self.paired_tags_stack.append(paired_tag_info)

    def _pt_tos(self):
        return self.paired_tags_stack[-1]
    
    def _print_err(self):
        if not self.errors:
            return
        
        print("============ ERRORS ============")
        final_errors = self._clean_err()
        for error in final_errors:
            print(repr(error))

    def _print_var_table(self):
        print("========= SYMBOL TABLE =========")
        for key, value in self.var_table.items():
            print(f"{key:<15}{value}")
                


# FOR TESTING PURPOSES
file = open("test_cases/04_smoosh_assign.lol")
syntax_checker = SyntaxChecker(file)
syntax_checker.check_syntax()
syntax_checker._print_err()
syntax_checker._print_var_table()
file.close()