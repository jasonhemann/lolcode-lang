# parses if-else stmt
def parse_if_else(self):
    cond = self.variables['IT']
    if_keyword = self.current_token()
    has_oic = False

    if not (if_keyword and if_keyword.value == 'YA RLY'):
        raise SyntaxError(f"{self.numline}: in parse_if_else(): Expected 'YA RLY' keyword; Got {if_keyword.value}")
    
    self.next_pos()
    if cond == 1:
        while self.current_token() and self.current_token().value not in ['MEBBE', 'NO WAI', 'OIC']:
            self.parse_statement()
        while self.current_token() and self.current_token().value != 'OIC' and not has_oic:
            if self.current_token() == 'OIC':
                has_oic = True
            self.next_pos()
        self.next_pos()
        return
    elif cond == 0:
        while self.current_token() and self.current_token().value not in ['MEBBE', 'NO WAI', 'OIC']:
            self.next_pos()

        while self.current_token() and self.current_token().value == 'MEBBE':
            self.parse_mebbe()
            
        if self.current_token() and self.current_token().value == 'NO WAI':
            self.next_pos()
            while self.current_token() and self.current_token().value != 'OIC':
                self.parse_statement()
        if self.current_token() and self.current_token().value == 'OIC':
            self.next_pos()
            return
    else:
        raise SyntaxError(f"{self.numline}: in parse_if_else(): Expected 'OIC' Keyword; Got {self.current_token().value}")

# parses mebbe
def parse_mebbe(self):
    has_oic = False
    expression = self.get_next_token()

    if not (expression and expression.type == 'Comparison Operation'):
        raise SyntaxError(f"{self.numline}: in parse_if_else(): Expected valid expression; Got {expression.value}")

    self.parse_comparison()
    cond = self.variables['IT']

    if cond:
        while self.current_token() and self.current_token().value not in ['MEBBE', 'NO WAI', 'OIC']:
            self.parse_statement()
        while self.current_token() and self.current_token().value != 'OIC' and not has_oic:
            if self.current_token() == 'OIC':
                has_oic = True
            self.next_pos()
        self.next_pos()
        return
    else:
        while self.current_token() and self.current_token().value not in ['MEBBE', 'NO WAI', 'OIC']:
            self.next_pos()
        return

# parses switch
def parse_switch(self, variable):
    has_oic = False
    switch_keyword = self.current_token()
    switch_state = 0
    variable_value = self.variables[variable.value]
    
    if not (switch_keyword and switch_keyword.value == 'WTF?'):
        raise SyntaxError(f"{self.numline}: in parse_switch(): Expected 'WTF? Keyword; Got {switch_keyword.value}")
    
    self.next_pos()

    while self.current_token().value != 'OIC' and not has_oic: #repeatedly scan omgs/omgwtf until oic
        #scan for omg
        if self.current_token() == 'OIC':
            has_oic = True
        if self.current_token().value == 'OMG':
            self.next_pos()
            if self.current_token().type in ['NUMBAR Literal', 'NUMBR Literal', 'YARN Delimiter', 'TROOF Literal', 'TYPE Literal']:
                if int(variable_value) == int(self.current_token().value):
                    switch_state = 1
                    self.next_pos()
                    while self.current_token().value not in ['OMG', 'OMGWTF', 'OIC', 'GTFO']:
                        self.parse_statement()
            else:
                 raise SyntaxError(f"{self.numline}: in parse_omg_body(): Expected literal; Got {self.current_token().value}")
        if self.current_token().value == 'OMGWTF':
            self.next_pos()
            if switch_state == 0:
                while self.current_token().value != 'OIC':
                    self.parse_statement()
                break
        self.next_pos()
    self.next_pos()
    return