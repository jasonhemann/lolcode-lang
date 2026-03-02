TT_STRING =             'String Literal'
TT_TYPE =               'Type Literal'
TT_BOOLEAN =            'Boolean Literal'
TT_FLOAT =              'Float Literal'
TT_INTEGER =            'Integer Literal'
TT_NULL =               'Null Literal'

#Keywords
#START
TT_CODE_STRT =          'Code Delimiter'
TT_FUNC_STRT =          'Function Declaration'
TT_LOOP_STRT =          'Loop Start Keyword'

#END
TT_FUNC_END =           'Function Closing Keyword'
TT_LOOP_END =           'Loop Closing Keyword'
TT_CODE_END =           'Code End Delimiter'

#Operators
TT_VAR_DEC =            'Variable Declaration'
TT_TYPECAST_1 =         'Typecast Keyword'
TT_TYPECAST_2 =         'Typecast Keyword'
TT_VAR_ASSIGN =         'Value Assignment On Declaration Operator'
TT_VAR_VAL_ASSIGN =     'Value Assignment Operator'

#Arithmetic
TT_DIV_OP =             'Division Operator'
TT_MUL_OP =             'Multiplication Operator'
TT_SUB =                'Subtraction Operator'
TT_MOD =                'Modulo Operator'
TT_DEC =                'Decrement Keyword'
TT_INC =                'Increment Keyword'

TT_SUMMATION =          'Summation Keyword'

#Relational
TT_AND =                'And Operator'
TT_AND_INF =            'Infinite Arity And Operator'
TT_OR_OP =              'Or Operator'
TT_OR_INF =             'Infinite Arity Or Operator'
TT_EQU_OP =             'Equality Operator'
TT_NEQU =               'Not Equal Operator'
TT_XOR =                'XOR Operator'
TT_NOT =                'Not Operator'

#Control
TT_IF =                 'If conditional'
TT_ELIF =               'Else If Keyword'
TT_ELSE =               'Else Keyword'
TT_SWITCH =             'Switch Case Keyword'
TT_TRUTH =              'Truth Codeblock keyword'
TT_BREAK =              'Break Default Keyword'
TT_CASEBREAK =          'Case Break Keyword'
TT_CONTROL_END =        'End of control statement'
TT_CASE =               'Case Keyword'

TT_WHILE =              'While Keyword'
TT_UNTIL =              'Until Keyword'

TT_RETURN =             'Return Keyword'
TT_FUNCALL =            'Function Call'
TT_RETURN_NOVAL =       'Return Keyword with no value'

#OPERATION
TT_OUTPUT =             'Output Keyword'
TT_READ =               'Read Keyword'
TT_CONCAT =             'Concatenation Keyword'
TT_MIN =                'Return Minimum Keyword'
TT_MAX =                'Return Maximum Keyword'

#Others
TT_COMMENT_MULTI_STRT = 'Multiline Comment Start Delimiter'
TT_COMMENT_MULTI_END =  'Multiline Comment End Delimiter'
TT_COMMENT_STRT =       'Comment Delimiter'
TT_ARG_SEP =            'Argument Separator'
TT_YR =                 'YR Keyword'
TT_A =                  'A Keyword'
TT_MKAY =               'MKAY Keyword'

TT_STR_DELIMITER =      'String Delimiter'
TT_IDENTIFIER =         'Identifier'
TT_EOF =                'EOF'
TT_NEWLINE =            'New Line'
TT_SUPPRESS_NEWLINE =   'Visible Suppress Next Line'

#GROUPS
GP_LITERAL =            (TT_STRING, TT_FLOAT, TT_INTEGER, TT_TYPE, TT_BOOLEAN)
GP_ARITHMETIC =         (TT_SUMMATION, TT_SUB, TT_MUL_OP, TT_DIV_OP, TT_MOD, TT_DEC, TT_MAX, TT_MIN)
GP_COMPARISON =         (TT_EQU_OP, TT_NEQU)
GP_BOOLEAN_SHORT =      (TT_NOT)
GP_BOOLEAN_LONG =       (TT_AND, TT_OR_OP, TT_XOR)
GP_BOOLEAN_INF =        (TT_AND_INF, TT_OR_INF)
