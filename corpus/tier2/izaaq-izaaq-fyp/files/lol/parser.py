"""
Parser class - Organises tokens and specifies grammar rules.
"""

from sly import Parser
from lol.lexer import LexerLOL

class ParserLOL(Parser):
    # tokens are passed from lexer to parser
    tokens = LexerLOL.tokens

    # define grammar
    # programs must start with 'HAI' and end with 'KTHXBYE'
    @_('HAI EOL statement_list KTHXBYE',
       'HAI EOL statement_list KTHXBYE EOL')
    def program(self, p):
        return ('start', p.statement_list)

    # inspired by michal zarlok
    @_('statement_list statement EOL',
       'statement EOL')
    def statement_list(self, p):
        if len(p) == 3:
            return (p[0] + [p[1]])
        else:
            return ([p[0]])

    @_('')
    def statement(self, p):
        pass

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('VISIBLE expr "!"',
       'VISIBLE expr')
    def statement(self, p):
        if len(p) == 3:
            return ('print', p.expr)
        return ('printline', p.expr)

    @_('GIMMEH IDENTIFIER')
    def statement(self, p):
        return ('input', p.IDENTIFIER)

    @_('I_HAS_A IDENTIFIER ITZ expr',
       'I_HAS_A IDENTIFIER')
    def statement(self, p):
        if len(p) == 4:
            return ('var_def', p.IDENTIFIER, p.expr)
        return ('var_declare', p.IDENTIFIER)

    @_('IDENTIFIER R expr')
    def statement(self, p):
        return ('assign', p.IDENTIFIER, p.expr)

    @_('IDENTIFIER IS_NOW_A TYPE')
    def statement(self, p):
        return ('convert', p.IDENTIFIER, p.TYPE)

    @_('expr EOL O_RLY "?" EOL YA_RLY EOL statement_list OIC',
       'expr EOL O_RLY "?" EOL YA_RLY EOL statement_list NO_WAI EOL statement_list OIC',
       'expr EOL O_RLY "?" EOL YA_RLY EOL statement_list MEBBE expr EOL statement_list OIC',
       'expr EOL O_RLY "?" EOL YA_RLY EOL statement_list MEBBE expr EOL statement_list NO_WAI EOL statement_list OIC')
    def statement(self, p):
        if len(p) == 9:
            return ('if', p.expr, p.statement_list)
        elif len(p) == 12:
            return ('if-else', p.expr, p.statement_list0, p.statement_list1)
        elif len(p) == 13:
            return ('if-elif', p.expr0, p.statement_list0, p.expr1, p.statement_list1)
        else:
            return ('if-elif-else', p.expr0, p.statement_list0, p.expr1, p.statement_list1, p.statement_list2)

    @_('IM_IN_YR IDENTIFIER EOL statement_list IM_OUTTA_YR IDENTIFIER')
    def statement(self, p):
        return ('loop', p.IDENTIFIER0, p.statement_list, p.IDENTIFIER1)

    @_('IM_IN_YR IDENTIFIER LOOPERATOR YR IDENTIFIER LOOPCONDITION expr EOL statement_list IM_OUTTA_YR IDENTIFIER')
    def statement(self, p):
        return ('counted_loop', p.IDENTIFIER0, p.LOOPERATOR, p.IDENTIFIER1, p.LOOPCONDITION, p.expr, p.statement_list, p.IDENTIFIER2)

    @_('GTFO')
    def statement(self, p):
        return ('break', p[0])

    @_('HOW_IZ_I IDENTIFIER EOL statement_list IF_U_SAY_SO')
    def statement(self, p):
        return ('func_def', p.IDENTIFIER, p.statement_list)

    @_('I_IZ IDENTIFIER MKAY')
    def expr(self, p):
        return ('func_call', p.IDENTIFIER)

    @_('FOUND_YR expr')
    def statement(self, p):
        return ('return', p.expr)

    @_('NOT expr')
    def expr(self, p):
        return ('not', p.expr)

    @_('SUM_OF expr AN expr',       # +
       'DIFF_OF expr AN expr',      # -
       'PRODUKT_OF expr AN expr',   # *
       'QUOSHUNT_OF expr AN expr',  # /
       'MOD_OF expr AN expr')       # %
    def expr(self, p):
        return ('bin_op', p[0], p.expr0, p.expr1)

    @_('BOTH_SAEM expr AN expr',    # ==
       'DIFFRINT expr AN expr',     # !=
       'WON_OF expr AN expr',       # xor
       'BOTH_OF expr AN expr',      # and
       'EITHER_OF expr AN expr',    # or
       'BIGGR_OF expr AN expr',     # max()
       'SMALLR_OF expr AN expr')    # min()
    def expr(self, p):
        return ('comparison_check', p[0], p.expr0, p.expr1)

    @_('FLOAT')
    def expr(self, p):
        return ('float', p.FLOAT)

    @_('INTEGER')
    def expr(self, p):
        return ('int', p.INTEGER)

    @_('BOOLEAN')
    def expr(self, p):
        return ('bool', p.BOOLEAN)

    @_('STRING')
    def expr(self, p):
        return ('str', p.STRING)

    @_('IDENTIFIER')
    def expr(self, p):
        return ('var', p.IDENTIFIER)
