# parses loops
def parse_loop(self):
    label = self.current_token()

    if not (label and label.type == 'Identifier'): # label
        raise SyntaxError(f"{self.numline}: in parse_loop(): Expected valid variable or label; Got {label.value}")
    
    oper = self.get_next_token()
    if not (oper and oper.type == 'Loop Keyword' and oper.value in ['UPPIN', 'NERFIN']): # uppin or nerfin
        raise SyntaxError(f"{self.numline}: in parse_loop(): Expected loop operation; Got {oper.value}")
    
    yr = self.get_next_token()
    if not (yr and yr.value == 'YR'): # yr
        raise SyntaxError(f"{self.numline}: in parse_loop(): Expected 'YR' Keyword; Got {oper.value}")
    
    var = self.get_next_token()

    if not (var and var.type == 'Identifier' and var.value != label.value): # varident
        raise SyntaxError(f"{self.numline}: in parse_loop(): Expected valid variable; Got {var.value}")
        
    til_wile = self.get_next_token()
    if til_wile and til_wile.type == 'Loop Keyword' and til_wile.value in ['TIL', 'WILE']: # til or wile
        self.next_pos()

        #start of checking condition
    else:
        raise SyntaxError(f"{self.numline}: in parse_loop(): Expected valid loop keyword; Got {til_wile.value}")
    
    #var = variable to be incremented
    #oper = whether var is to be inc or decremented
    #til_wile = while false vs while true
    #result = condition for value of var

    start_of_condition = self.position
    start_of_condition_line = self.numline

    while True:
        cond = self.parse_expression()
        if til_wile.value == 'TIL':
            if cond == 0:
                while self.current_token().value != 'IM OUTTA YR':
                    self.parse_statement()
                if oper.value == 'UPPIN':
                    self.variables[var.value] += 1
                elif oper.value == 'NERFIN':
                    self.variables[var.value] -= 1
                self.position = start_of_condition
                self.numline = start_of_condition_line
            elif cond == 1:
                while self.current_token().value != label.value:
                    self.next_pos()
                self.next_pos()
                return
        elif til_wile.value == 'WILE':
            if cond == 1:
                while self.current_token().value != 'IM OUTTA YR':
                    self.parse_statement()
                if oper.value == 'UPPIN':
                    self.variables[var.value] += 1
                elif oper.value == 'NERFIN':
                    self.variables[var.value] -= 1
                self.position = start_of_condition
                self.numline = start_of_condition_line
            elif cond == 0:
                while self.current_token().value != label.value:
                    self.next_pos()
                self.next_pos()
                return