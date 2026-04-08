import re

'''
NO GIMMEH
NESTED ARITHMETIC ONLY READS OTHER ARITHMETIC EXPRESSIONS
COMPARISON ONLY USES MAX/MIN AND DOES NOT NEST
NESTING BOOLEAN WITH NOT FAILS
'''


class Semantic:
    def __init__(self, tokens):
        self.tokens = tokens
        self.symbol_table = [['IT', 'NOOB']] #JUST VARIABLES
        self.condition_block = [] #CONTAINS IF-ELSE STATEMENTS
        self.loop_block = [] #CONTAINS LOOP STATEMENTS
        self.function_block = [] #CONTAINS FUNCTION STATEMENTS
        self.toprint = []
        self.error = False
        self.end = False

        #list of categories that have an operation associated with it
        self.operation_categories = [
        'variable declaration', 'assignment', 'typecast', 'recast',
        'addition', 'difference', 'multiplication', 'division', 'modulo', 'max', 'min',
        'booland', 'boolor', 'boolxor', 'boolnot', 'boolalland', 'boolallor',
        'compare equal', 'compare diff',
        'concatenation',
        'output']
        
        self.arithmetic_categories = ['addition', 'difference', 'multiplication', 'division', 'modulo', 'max', 'min'] 
        self.comparison_categories = ['compare equal', 'compare diff']
        self.boolean_categories = ['booland', 'boolor', 'boolxor', 'boolnot']
        self.boolean_infinite = ['boolalland', 'boolallor']

    def read_code(self):
        while not self.error and not self.end:
            for line in self.tokens:
                self.check_operation(line)
        
        #do error related stuff here
    
    def check_operation(self, args):
        if args[0][1] in self.operation_categories or args[1][1] in self.operation_categories:
            if args[0][1] == 'variable declaration':
                self.var_dec(args)
            if args[1][1] == 'assignment':
                self.var_assign(args)
            if args[0][1] == 'typecast':
                self.typecast(args)
            if args[1][1] == 'recast':
                self.recast(args)
            if args[0][1] in self.arithmetic_categories:
                self.arithmetic(args)
            if args[0][1] == 'boolean':
                self.boolean(args, False)
            if args[0][1] in self.comparison_categories:
                self.comparison(args)
            if args[0][1] == 'output':
                self.lol_print(args)
            if args[0][1] == 'concatenation':
                self.concatenate(args)

        if args[0][1] == 'program end':
            self.end = True

    def read_symbol_table(self, name):
        for symbol in self.symbol_table:
            if name == symbol[0]: #if match the identifier in symbol table
                return symbol #return the value
        else:
            return False

    def implicit_typecast(self, val, stype, etype): #start type, end type 
        ### NOT YET DONE
        if stype == 'numbar':
            temp = float(val)
            if etype == 'numbr':
                return int(temp)

            if etype == 'troof':
                if temp != 0:
                    return 'WIN'
                else:
                    return 'FAIL'
            if etype == 'yarn':
                return "\"" + str(temp) + "\""
    
        if stype == 'numbr':
            temp = int(val)
            if etype == 'numbar':
                return float(temp)
            if etype == 'troof':
                if temp != 0:
                    return 'WIN'
                else:
                    return 'FAIL'
            if etype == 'yarn':
                return "\"" + str(temp) + "\""
        
        if stype == 'troof':
            if etype == 'numbar':
                if val == 'WIN':
                    return 1.0
                else:
                    return 0.0
            
            if etype == 'numbr':
                if val == 'WIN':
                    return 1
                else:
                    return 0
            
            if etype == 'yarn':
                return "\"" + val + "\""
        
        if stype == 'yarn':
            temp = val[1:-1]
            if temp.isdigit() and (etype == 'numbar' or etype == 'numbr'):
                if etype == 'numbar':
                    return round(float(temp), 2)
                if etype == 'numbr':
                    return int(temp)
            
            elif etype == 'troof':
                return temp
            
            else: #yarn -> numbar/numbr while not a digit
                self.error = True
        
        if stype == 'NOOB':
            if etype == 'troof':
                return 'WIN'
            else: #no typecasting to other types
                self.error = True

    #-----VARIABLE STUFF-----
    def var_dec(self, args):
        if len(args) == 3: #keyword, identifier, linebreak
            temp = [args[1][0], 'NOOB']
            self.symbol_table.append(temp)
        elif len(args) == 5: #keyword, identifier, keyword, init value, linebreak
            #convert numbar and numbr into numeric, troof and yarns stay in string format
            if args[3][1] == 'numbar':
                val = float(args[3][0])
            elif args[3][1] == 'numbr':
                val = int(args[3][0])
            else:
                val = args[3][0]
            temp = [args[1][0], args[3][1], val]
            self.symbol_table.append(temp)
        else: #it has an expression
            
            ###CHECK WHAT KIND OF EXPRESSION
            if args[3][1] in self.arithmetic_categories:
                temp = []
                count = 3
                while args[count][1] != 'linebreak':
                    temp.append(args[count])
                    count += 1
                
                val = self.arithmetic(temp)
                if isinstance(val, float):
                    temp2 = 'numbar'
                else:
                    temp2 = 'numbr'

                temp = [args[1][0], temp2, val]
                self.symbol_table.append(temp)
            
            if args[3][1] in self.comparison_categories:
                temp = []
                count = 3
                while args[count][1] != 'linebreak':
                    temp.append(args[count])
                    count += 1
                
                val = self.comparison(temp)

                temp = [args[1][0], 'troof', val]
                self.symbol_table.append(temp)
            
            if args[3][1] in self.boolean_categories or args[3][1] in self.boolean_infinite:
                temp = []
                count = 3
                while args[count][1] != 'linebreak':
                    temp.append(args[count])
                    count += 1
                
                val = self.boolean(temp)

                temp = [args[1][0], 'troof', val]
                self.symbol_table.append(temp)

    def var_assign(self, args):
        temp = []
        if len(args) == 4: #identifier or raw value
            if args[2][1] == 'identifier':
                symbol = self.read_symbol_table(args[2][0])
                temp = symbol
                temp[0] = args[0][0]
            else: #raw value
                temp = [args[0][0], args[2][1], args[2][0]]

        elif len(args) == 6: #recast
            temp = []
            temp.append(args[2])
            temp.append(args[3])
            temp.append(args[4])
            result = self.typecast(temp)
            temp = [args[0][0], args[4][0].lower(), result]

        else: #expression
            if args[2][1] in self.arithmetic_categories:
                count = 2
                while args[count][1] != 'linebreak':
                    temp.append(args[count])
                    count += 1
                
                val = self.arithmetic(temp)
                if isinstance(val, float):
                    temp2 = 'numbar'
                else:
                    temp2 = 'numbr'

                temp = [args[0][0], temp2, val]
            
            if args[2][1] in self.comparison_categories:
                count = 2
                while args[count][1] != 'linebreak':
                    temp.append(args[count])
                    count += 1
                
                val = self.comparison(temp)

                temp = [args[0][0], 'troof', val]
            
            if args[2][1] in self.boolean_categories or args[2][1] in self.boolean_infinite:
                count = 2
                while args[count][1] != 'linebreak':
                    temp.append(args[count])
                    count += 1
                
                val = self.boolean(temp)

                temp = [args[0][0], 'troof', val]
            
            if args[2][1] == 'concatenation':
                count = 2
                while args[count][1] != 'linebreak':
                    temp.append(args[count])
                    count += 1
                temp.append(args[count])
                val = self.concatenate(temp)

                temp = [args[0][0], 'yarn', val]

        for i in range(0, len(self.symbol_table)):
            if self.symbol_table[i][0] == args[0][0]: #symbol matches name of var to edit
                self.symbol_table[i] = temp
                break

    def typecast(self, args):
        temp = args[2][0].lower()
        symbol = self.read_symbol_table(args[1][0])
        if symbol[1] == 'NOOB':
            if temp == 'yarn':
                result = '""'
            if temp == 'numbr':
                result = 0
            if temp == 'numbar':
                result = 0.0
            if temp == 'troof':
                result = 'FAIL'
        else:
            result = self.implicit_typecast(symbol[2], symbol[1], temp)

        return result
        # self.symbol_table[0] = ['IT', temp, result]

    def recast(self, args):
        temp = args[2][0].lower()
        for i in range(0, len(self.symbol_table)):
            if self.symbol_table[i][0] == args[0][0]: #symbol matches name of var to edit
                temp = [self.symbol_table[i][0], temp, self.implicit_typecast(self.symbol_table[i][2], self.symbol_table[i][1], temp)]
                self.symbol_table[i] = temp
                break
        
    #-------------------------

    #-----ARITHMETIC-----
    def arithmetic(self, args):
        numbar = False
        i = 3 #for nesting

        #check for numbar
        for arg in args:
            if arg[1] == 'identifier':
                symbol = self.read_symbol_table(arg[0])
                if symbol[1] == 'numbar':
                    numbar = True

            if arg[1] == 'numbar':
                numbar = True

        #1st value
        #if a variable, look it up in symbol table
        if args[1][1] == 'identifier':
            symbol = self.read_symbol_table(args[1][0])
            if symbol:
                if symbol[1] == 'numbar':
                    val1 = symbol[2]
                if symbol[1] == 'numbr':
                    if numbar:
                        val1 = self.implicit_typecast(symbol[2], 'numbr', 'numbar')
                    else:
                        val1 = symbol[2]
                if symbol[1] == 'troof':
                    if numbar:
                        val1 = self.implicit_typecast(symbol[2], 'troof', 'numbar')
                    else:
                        val1 = self.implicit_typecast(symbol[2], 'troof', 'numbr')
                if symbol[1] == 'yarn':
                    if numbar:
                        val1 = self.implicit_typecast(symbol[2], 'yarn', 'numbar')
                    else:
                        val1 = self.implicit_typecast(symbol[2], 'yarn', 'numbr')
                #NOOB
                else:
                    self.error = True
            else:
                self.error = True

        elif args[1][1] in self.arithmetic_categories:
            temp = []
            j = 2
            count = 0 #count how many values we've encountered
            #deeper nesting!
            if args[2][1] in self.arithmetic_categories:
                while count < 2:
                    if args[j][1] in self.arithmetic_categories:
                        count -= 1
                    if args[j][1] == 'identifier' or args[j][1] == 'numbar' or args[j][1] == 'numbr' or args[j][1] == 'troof' or args[j][1] == 'yarn':
                        count += 1
                    temp.append(args[j])
                    j += 1
                    i += 1
                i += 1
                val1 = self.arithmetic(temp)
            else:
                temp.append(args[1])
                temp.append(args[2])
                temp.append(args[3])
                temp.append(args[4])

                val1 = self.arithmetic(temp)
                i += 3

        #not a variable, raw value is in the args
        else:
            if args[1][1] == 'numbar':
                val1 = float(args[1][0])
            if args[1][1] == 'numbr':
                if numbar:
                    val1 = self.implicit_typecast(args[1][0], 'numbr', 'numbar')
                else:
                    val1 = int(args[1][0])
            if args[1][1] == 'troof':
                if numbar:
                    val1 = self.implicit_typecast(args[1][0], 'troof', 'numbar')
                else:
                    val1 = self.implicit_typecast(args[1][0], 'troof', 'numbr')
            if args[1][1] == 'yarn':
                if numbar:
                    val1 = self.implicit_typecast(args[1][0], 'yarn', 'numbar')
                else:
                    val1 = self.implicit_typecast(args[1][0], 'yarn', 'numbr')
        
        #2nd value
        if args[i][1] == 'identifier':
            symbol = self.read_symbol_table(args[i][0])
            if symbol:
                if symbol[1] == 'numbar':
                    val2 = symbol[2]
                if symbol[1] == 'numbr':
                    if numbar:
                        val2 = self.implicit_typecast(symbol[2], 'numbr', 'numbar')
                    else:
                        val2 = symbol[2]
                if symbol[1] == 'troof':
                    if numbar:
                        val2 = self.implicit_typecast(symbol[2], 'troof', 'numbar')
                    else:
                        val2 = self.implicit_typecast(symbol[2], 'troof', 'numbr')
                if symbol[1] == 'yarn':
                    if numbar:
                        val2 = self.implicit_typecast(symbol[2], 'yarn', 'numbar')
                    else:
                        val2 = self.implicit_typecast(symbol[2], 'yarn', 'numbr')
            else:
                self.error = True

        elif args[i][1] in self.arithmetic_categories:
            temp = []
            j = i+1
            count = 0 #count how many values we've encountered
            #deeper nesting!
            if args[j][1] in self.arithmetic_categories:
                while count < 2:
                    if args[j][1] in self.arithmetic_categories:
                        count -= 1
                    if args[j][1] == 'identifier' or args[j][1] == 'numbar' or args[j][1] == 'numbr' or args[j][1] == 'troof' or args[j][1] == 'yarn':
                        count += 1
                    temp.append(args[j])
                    j += 1
                val2 = self.arithmetic(temp)

            else:
                temp.append(args[i])
                temp.append(args[i+1])
                temp.append(args[i+2])
                temp.append(args[i+3])

                val2 = self.arithmetic(temp)

        else:
            if args[i][1] == 'numbar':
                val2 = float(args[i][0])
            if args[i][1] == 'numbr':
                if numbar:
                    val2 = self.implicit_typecast(args[i][0], 'numbr', 'numbar')
                else:
                    val2 = int(args[i][0])
            if args[i][1] == 'troof':
                if numbar:
                    val2 = self.implicit_typecast(args[i][0], 'troof', 'numbar')
                else:
                    val2 = self.implicit_typecast(args[i][0], 'troof', 'numbr')
            if args[i][1] == 'yarn':
                if numbar:
                    val2 = self.implicit_typecast(args[i][0], 'yarn', 'numbar')
                else:
                    val2 = self.implicit_typecast(args[i][0], 'yarn', 'numbr')

        if args[0][1] == 'addition':
            return val1 + val2
        elif args[0][1] == 'difference':
            return val1 - val2
        elif args[0][1] == 'multiplication':
            return val1 * val2
        elif args[0][1] == 'division':
            return val1 / val2
        elif args[0][1] == 'modulo':
            return val1 % val2
        elif args[0][1] == 'max':
            if val1 >= val2:
                return val1
            else:
                return val2
        elif args[0][1] == 'min':
            if val1 >= val2:
                return val2
            else:
                return val1
    #--------------------

    #-----BOOLEAN-----
    def boolean(self, args, nest):
        values = []
        #infinite arity
        if not nest and (args[0][1] == 'boolalland' or args[0][1] == 'boolallor'):
            count = 1
            #iterate through all operands and append to values list
            while args[count-1][1] != 'end of operands':
                if args[count][1] == 'identifier':
                    symbol = self.read_symbol_table(args[count][0])
                    if symbol:
                        if symbol[1] == 'numbar':
                            values.append(self.implicit_typecast(symbol[2], 'numbar', 'troof'))
                        if symbol[1] == 'numbr':
                            values.append(self.implicit_typecast(symbol[2], 'numbr', 'troof'))
                        if symbol[1] == 'troof':
                            values.append(symbol[2]) 
                        if symbol[1] == 'yarn':
                            values.append(self.implicit_typecast(symbol[2], 'yarn', 'troof'))
                    else:
                        self.error = True
                
                elif args[count][1] in self.boolean_categories:
                    temp = []
                    j = count+1 #1+1
                    count2 = 0

                    if args[j][1] in self.boolean_categories:
                        if args[j][1] == 'boolnot':
                            limit = 1
                        else:
                            limit = 2
                        while count2 < limit:
                            if args[j][1] in self.boolean_categories:
                                if args[j][1] != 'boolnot':
                                    count2 -= 1
                            if args[j][1] == 'identifier' or args[j][1] == 'numbar' or args[j][1] == 'numbr' or args[j][1] == 'troof' or args[j][1] == 'yarn':
                                count2 += 1
                            temp.append(args[j])
                            j += 1
                            count += 1
                        count += 1
                        values.append(self.boolean(temp, nest))
                    
                    else:
                        if args[count][1] == 'boolnot':
                            temp.append(args[count])
                            temp.append(args[count+1])
                            count += 1
                        else:
                            temp.append(args[count])
                            temp.append(args[count+1])
                            temp.append(args[count+2])
                            temp.append(args[count+3])

                            count += 3

                        values.append(self.boolean(temp, nest))

                else:
                    if args[count][1] == 'numbar':
                        values.append(self.implicit_typecast(args[count][0], 'numbar', 'troof'))
                    if args[count][1] == 'numbr':
                        values.append(self.implicit_typecast(args[count][0], 'numbr', 'troof'))
                    if args[count][1] == 'troof':
                        values.append(args[count][0])
                    if args[count][1] == 'yarn':
                        values.append(self.implicit_typecast(args[count][0], 'yarn', 'troof'))
                count += 2

        #usual, val1
        i = 3
        if args[1][1] == 'identifier':
            symbol = self.read_symbol_table(args[1][0])
            if symbol:
                if symbol[1] == 'numbar':
                    values.append(self.implicit_typecast(symbol[2], 'numbar', 'troof'))
                if symbol[1] == 'numbr':
                    values.append(self.implicit_typecast(symbol[2], 'numbr', 'troof'))
                if symbol[1] == 'troof':
                    values.append(symbol[2]) 
                if symbol[1] == 'yarn':
                    values.append(self.implicit_typecast(symbol[2], 'yarn', 'troof'))
            else:
                self.error = True

        elif args[1][1] in self.boolean_categories:
            temp = []
            j = 2 #1+1
            count2 = 0

            if args[j][1] in self.boolean_categories:
                if args[j][1] == 'boolnot':
                    limit = 1
                else:
                    limit = 2
                while count2 < limit:
                    if args[j][1] in self.boolean_categories:
                        if args[j][1] != 'boolnot':
                            count2 -= 1
                    if args[j][1] == 'identifier' or args[j][1] == 'numbar' or args[j][1] == 'numbr' or args[j][1] == 'troof' or args[j][1] == 'yarn':
                        count2 += 1
                    temp.append(args[j])
                    j += 1
                    i += 1
                i += 1
                values.append(self.boolean(temp, nest))
            
            else:
                if args[1][1] == 'boolnot':
                    temp.append(args[1])
                    temp.append(args[2])
                    i += 1
                else:
                    temp.append(args[1])
                    temp.append(args[2])
                    temp.append(args[3])
                    temp.append(args[4])

                    i += 3

                    values.append(self.boolean(temp, nest))
            
        else:
            if args[1][1] == 'numbar':
                values.append(self.implicit_typecast(args[1][0], 'numbar', 'troof'))
            if args[1][1] == 'numbr':
                values.append(self.implicit_typecast(args[1][0], 'numbr', 'troof'))
            if args[1][1] == 'troof':
                values.append(args[1][0])
            if args[1][1] == 'yarn':
                values.append(self.implicit_typecast(args[1][0], 'yarn', 'troof'))

        #val2
        if args[0][1] != 'boolnot':
            if args[i][1] == 'identifier':
                symbol = self.read_symbol_table(args[i][0])
                if symbol:
                    if symbol[1] == 'numbar':
                        values.append(self.implicit_typecast(symbol[2], 'numbar', 'troof'))
                    if symbol[1] == 'numbr':
                        values.append(self.implicit_typecast(symbol[2], 'numbr', 'troof'))
                    if symbol[1] == 'troof':
                        values.append(symbol[2]) 
                    if symbol[1] == 'yarn':
                        values.append(self.implicit_typecast(symbol[2], 'yarn', 'troof'))
                else:
                    self.error = True
            
            elif args[i][1] in self.boolean_categories:
                temp = []
                j = i+1 
                count2 = 0

                if args[j][1] in self.boolean_categories:
                    if args[j][1] == 'boolnot':
                        limit = 1
                    else:
                        limit = 2
                    while count2 < limit:
                        if args[j][1] in self.boolean_categories:
                            if args[j][1] != 'boolnot':
                                count2 -= 1 
                        if args[j][1] == 'identifier' or args[j][1] == 'numbar' or args[j][1] == 'numbr' or args[j][1] == 'troof' or args[j][1] == 'yarn':
                            count2 += 1
                        temp.append(args[j])
                        j += 1
                    values.append(self.boolean(temp, nest))
                
                else:
                    if args[i][1] == 'boolnot':
                        temp.append(args[i])
                        temp.append(args[i+1])

                    else:
                        temp.append(args[i])
                        temp.append(args[i+1])
                        temp.append(args[i+2])
                        temp.append(args[i+3])

                    values.append(self.boolean(temp, nest))
                
            else:
                if args[i][1] == 'numbar':
                    values.append(self.implicit_typecast(args[i][0], 'numbar', 'troof'))
                if args[i][1] == 'numbr':
                    values.append(self.implicit_typecast(args[i][0], 'numbr', 'troof'))
                if args[i][1] == 'troof':
                    values.append(args[i][0])
                if args[i][1] == 'yarn':
                    values.append(self.implicit_typecast(args[i][0], 'yarn', 'troof'))
        
        if values[0] == 'WIN':
            result = True
        else:
            result = False

        if args[0][1] != 'boolnot':
            for i in range(1, len(values)):
                if values[i] == 'WIN':
                    temp = True
                else:
                    temp = False

                if args[0][1] == 'boolalland' or args[0][1] == 'booland':
                    result = result and temp
                elif args[0][1] == 'boolallor' or args[0][1] == 'boolor':
                    result = result or temp
                elif args[0][1] == 'boolxor':
                    result = (result and not temp) or (not result and temp)
        else:
            result = not result
        if result:
            return 'WIN'
        else:
            return 'FAIL'
   #-----------------

   #-----COMPARISON-----
    #typecasts everthing into numbar, 2 = 2.0 and 3.5 = 3.5 so it shouldnt matter
    def comparison(self, args):
        temp = args
        if args[-1][1] == 'linebreak':
            del temp[-1]
        # not relational, == or !=
        if len(temp) == 4: #keyword identifier keyword identifier
            #get values
            if args[1][1] == 'identifier':
                symbol = self.read_symbol_table(args[1][0])
                if symbol:
                    if symbol[1] == 'numbar':
                        val1 = symbol[2]
                    if symbol[1] == 'numbr':
                        val1 = self.implicit_typecast(symbol[2], 'numbr', 'numbar')
                    if symbol[1] == 'troof':
                        #make an error for now
                        self.error = True
                    if symbol[1] == 'yarn':
                        self.error = True
                else:
                    self.error = True
            else:
                if args[1][1] == 'numbar':
                    val1 = float(args[1][0])
                if args[1][1] == 'numbr':
                    val1 = self.implicit_typecast(args[1][0], 'numbr', 'numbar')
                if args[1][1] == 'troof':
                    self.error = True
                if args[1][1] == 'yarn':
                    self.error = True
            
            if args[3][1] == 'identifier':
                symbol = self.read_symbol_table(args[3][0])
                if symbol:
                    if symbol[1] == 'numbar':
                        val2 = symbol[2]
                    if symbol[1] == 'numbr':
                        val2 = self.implicit_typecast(symbol[2], 'numbr', 'numbar')
                    if symbol[1] == 'troof':
                        #make an error for now
                        self.error = True
                    if symbol[1] == 'yarn':
                        self.error = True
                else:
                    self.error = True
            else:
                if args[3][1] == 'numbar':
                    val2 = float(args[3][0])
                if args[3][1] == 'numbr':
                    val2 = self.implicit_typecast(args[3][0], 'numbr', 'numbar')
                if args[3][1] == 'troof':
                    self.error = True
                if args[3][1] == 'yarn':
                    self.error = True

            if args[0][1] == 'compare equal':
                if val1 == val2:
                    return 'WIN'
                else:
                    return 'FAIL'
            else:
                if val1 != val2:
                    return 'WIN'
                else:
                    return 'FAIL'

        #is relational
        else: #keyword identifier keyword keyword identifier keyword identifier
            if args[1][1] == 'identifier':
                symbol = self.read_symbol_table(args[1][0])
                if symbol:
                    if symbol[1] == 'numbar':
                        val1 = symbol[2]
                    if symbol[1] == 'numbr':
                            val1 = self.implicit_typecast(symbol[2], 'numbr', 'numbar')
                    if symbol[1] == 'troof':
                        #make an error for now
                        self.error = True
                    if symbol[1] == 'yarn':
                        self.error = True
                else:
                    self.error = True

            elif args[1][1] in self.arithmetic_categories:
                temp = []
                temp.append(args[1])
                temp.append(args[2])
                temp.append(args[3])
                temp.append(args[4])

                val1 = self.arithmetic(temp)

            else:
                if args[1][1] == 'numbar':
                    val1 = float(args[1][0])
                if args[1][1] == 'numbr':
                    val1 = self.implicit_typecast(args[1][0], 'numbr', 'numbar')
                if args[1][1] == 'troof':
                    self.error = True
                if args[1][1] == 'yarn':
                    self.error = True
            
            #val 2
            if args[6][1] == 'identifier':
                symbol = self.read_symbol_table(args[6][0])
                if symbol:
                    if symbol[1] == 'numbar':
                        val2 = symbol[2]
                    if symbol[1] == 'numbr':
                        val2 = self.implicit_typecast(symbol[2], 'numbr', 'numbar')
                    if symbol[1] == 'troof':
                        #make an error for now
                        self.error = True
                    if symbol[1] == 'yarn':
                        self.error = True
                else:
                    self.error = True
            
            elif args[3][1] in self.arithmetic_categories:
                temp = []
                temp.append(args[3])
                temp.append(args[4])
                temp.append(args[5])
                temp.append(args[6])

                val2 = self.arithmetic(temp)

            else:
                if args[6][1] == 'numbar':
                    val2 = float(args[6][0])
                if args[6][1] == 'numbr':
                    val2 = self.implicit_typecast(args[6][0], 'numbr', 'numbar')
                if args[6][1] == 'troof':
                    self.error = True
                if args[6][1] == 'yarn':
                    self.error = True
            
            #check if biggr of or smallr of and return proper expression
            if args[0][1] == 'compare equal':
                if args[3][1] == 'max' or args[1][1] == 'max':
                    if val1 >= val2:
                        return 'WIN'
                    else:
                        return 'FAIL'
                else:
                    if val1 <= val2:
                        return 'WIN'
                    else:
                        return 'FAIL'
            else:
                if args[3][1] == 'max' or args[1][1] == 'max':
                    if val1 > val2:
                        return 'WIN'
                    else:
                        return 'FAIL'
                else:
                    if val1 < val2:
                        return 'WIN'
                    else:
                        return 'FAIL'
    #-----------------

    #-----CONCAT-----
    def concatenate(self, args):
        count = 0
        values = []

        while(args[count][1] != 'linebreak'):
            if args[count][1] == 'identifier':
                symbol = self.read_symbol_table(args[count][0])
                if symbol:
                    #only need to typecast numbr/numbar into yarn
                    if symbol[1] == 'numbar':
                        values.append(self.implicit_typecast(symbol[2], 'numbar', 'yarn'))
                    if symbol[1] == 'numbr':
                        values.append(self.implicit_typecast(symbol[2], 'numbr', 'yarn'))
                    if symbol[1] == 'troof': #stored as string, no need to typecast
                        values.append(self.implicit_typecast(symbol[2], 'troof', 'yarn'))
                    if symbol[1] == 'yarn':
                        values.append(symbol[2])
                    if symbol[1] == 'NOOB':
                        values.append("NOOB")
                else:
                    self.error = True

            elif args[count][1] in self.arithmetic_categories:
                temp = []
                while args[count][1] != 'operand separator' and args[count][1] != 'linebreak':
                    temp.append(args[count])
                    count += 1
                count -= 1
                values.append(self.implicit_typecast(self.arithmetic(temp), 'numbar', 'yarn'))
            
            elif args[count][1] in self.comparison_categories:
                temp = []
                while args[count][1] != 'operand separator' and args[count][1] != 'linebreak':
                    temp.append(args[count])
                    count += 1
                count -= 1
                values.append(self.implicit_typecast(self.comparison(temp), 'troof', 'yarn'))
            
            elif args[count][1] in self.boolean_categories or args[count][1] in self.boolean_infinite:
                temp = []
                while args[count][1] != 'operand separator' and args[count][1] != 'linebreak':
                    temp.append(args[count])
                    count += 1
                count -= 1
                values.append(self.implicit_typecast(self.boolean(temp, False), 'troof', 'yarn'))
            
            else: #raw value
                if args[count][1] == 'numbar':
                    values.append(self.implicit_typecast(args[count][0], 'numbar', 'yarn'))
                if args[count][1] == 'numbr':
                    values.append(self.implicit_typecast(args[count][0], 'numbr', 'yarn'))
                if args[count][1] == 'troof':
                    values.append(self.implicit_typecast(args[count][0], 'troof', 'yarn'))
                if args[count][1] == 'yarn':
                    values.append(args[count][0])
            count += 1
        
        string = ''
        for value in values:
            temp = value[1:-1]
            string = string + temp 
        string = "\"" + string + "\""
        return string

    #----------------

    #-----OUTPUT-----
    def lol_print(self, args):
        count = 0
        values = []
        #iterate until find linebreak
        while(args[count][1] != 'linebreak'):
            if args[count][1] == 'identifier':
                symbol = self.read_symbol_table(args[count][0])
                if symbol:
                    #only need to typecast numbr/numbar into yarn
                    if symbol[1] == 'numbar':
                        values.append(self.implicit_typecast(symbol[2], 'numbar', 'yarn'))
                    if symbol[1] == 'numbr':
                        values.append(self.implicit_typecast(symbol[2], 'numbr', 'yarn'))
                    if symbol[1] == 'troof': #stored as string, no need to typecast
                        values.append(self.implicit_typecast(symbol[2], 'troof', 'yarn'))
                    if symbol[1] == 'yarn':
                        values.append(symbol[2])
                    if symbol[1] == 'NOOB':
                        values.append("\"NOOB\"")
                else:
                    self.error = True

            elif args[count][1] in self.arithmetic_categories:
                numbar = False
                for arg in args:
                    if arg[1] == 'identifier':
                        symbol = self.read_symbol_table(arg[0])
                        if symbol[1] == 'numbar':
                            numbar = True
                    
                    if arg[1] == 'division':
                        numbar = True

                    if arg[1] == 'numbar':
                        numbar = True

                temp = []
                while args[count][1] != 'concatenation operator (VISIBLE)' and args[count][1] != 'linebreak':
                    temp.append(args[count])
                    count += 1
                count -= 1
                if numbar:
                    values.append(self.implicit_typecast(self.arithmetic(temp), 'numbar', 'yarn'))
                else:
                    values.append(self.implicit_typecast(self.arithmetic(temp), 'numbr', 'yarn'))
            
            elif args[count][1] in self.comparison_categories:
                temp = []
                while args[count][1] != 'concatenation operator (VISIBLE)' and args[count][1] != 'linebreak':
                    temp.append(args[count])
                    count += 1
                count -= 1
                values.append(self.implicit_typecast(self.comparison(temp), 'troof', 'yarn'))
            
            elif args[count][1] in self.boolean_categories or args[count][1] in self.boolean_infinite:
                temp = []
                while args[count][1] != 'concatenation operator (VISIBLE)' and args[count][1] != 'linebreak':
                    temp.append(args[count])
                    count += 1
                count -= 1
                values.append(self.implicit_typecast(self.boolean(temp, False), 'troof', 'yarn'))
            
            else: #raw value
                if args[count][1] == 'numbar':
                    values.append(self.implicit_typecast(args[count][0], 'numbar', 'yarn'))
                if args[count][1] == 'numbr':
                    values.append(self.implicit_typecast(args[count][0], 'numbr', 'yarn'))
                if args[count][1] == 'troof':
                    values.append(self.implicit_typecast(args[count][0], 'troof', 'yarn'))
                if args[count][1] == 'yarn':
                    values.append(args[count][0])
            count += 1
        
        string = ''
        for value in values:
            temp = value[1:-1]
            string = string + temp 
        string = "\"" + string + "\""

        self.toprint.append(string)
    #----------------

    #-----CONTROL----
    #returns the code block
    def lookup_code(self, codetype, label):
        if codetype == 'loop enter':
            for code in self.loop_block:
                if code[0] == label: #match loop name to code name
                    returncode = code[1]
        
        if codetype == 'function enter':
            for code in self.function_block:
                if code[0] == label: #match func name to code name
                    returncode = code[1]

        return returncode #list of lists

    def save_loop_code(self, label, codeblock):
        self.loop_block.append([label, codeblock])

    def loop_code(self, args):
        #UPPIN n NERFIN
        if args[2][1] == 'increment':
            increment = True
        else:
            increment = False
        
        for i in range(0, len(self.symbol_table)):
            if self.symbol_table[i][0] == args[4][0]: #4th is position of var
                symbol = self.symbol_table[i][0]
                index = i
                break

        codeblock = lookup_code(args[0], args[1][0]) #loop keyword + label

        if args[5][0] == 'TIL': #5th is position of TIL/WILE keyword
            condition = False
        else:
            condition = True
        
        temp = []
        for i in range(6, len(args)-1):
            temp.append(args[i]) #get expression
        condition_code = temp

        while self.comparison(condition_code) != condition:
            for code in codeblock:
                self.check_operation(code) #run the code
            if increment: #increment/decrement
                self.symbol_table[index][2] += 1
            else:
                self.symbol_table[index][2] -= 1


    #----------------

SAMPLE_CODE = [
    [['HAI', 'program start'], ['\n', 'linebreak']], [['WAZZUP', 'variable declaration area start'], ['\n', 'linebreak']], 
    [['BTW .', 'comment'], ['\n', 'linebreak']], 
    [['I HAS A', 'variable declaration'], ['x', 'identifier'], ['ITZ', 'variable initialization'], ['4', 'numbr'], ['\n', 'linebreak']], 
    [['I HAS A', 'variable declaration'], ['y', 'identifier'], ['ITZ', 'variable initialization'], ['4', 'numbr'], ['\n', 'linebreak']], 
    [['BUHBYE', 'variable declaration area end'], ['\n', 'linebreak']], 
    [['VISIBLE', 'output'], ['BOTH SAEM', 'compare equal'], ['x', 'identifier'], ['AN', 'noonecares'], ['y', 'identifier'], ['\n', 'linebreak']],
    [['VISIBLE', 'output'], ['DIFFRINT', 'compare diff'], ['x', 'identifier'], ['AN', 'noonecares'], ['y', 'identifier'], ['\n', 'linebreak']],
    [['VISIBLE', 'output'], ['BOTH SAEM', 'compare equal'], ['x', 'identifier'], ['AN', 'noonecares'], ['BIGGR OF', 'max'], ['x', 'identifier'], ['AN', 'asdasd'], ['y', 'identifier'], ['\n', 'linebreak']],
    [['VISIBLE', 'output'], ['BOTH SAEM', 'compare equal'], ['x', 'identifier'], ['AN', 'noonecares'], ['SMALLR OF', 'min'], ['x', 'identifier'], ['AN', 'asdasd'], ['y', 'identifier'], ['\n', 'linebreak']],
    [['VISIBLE', 'output'], ['DIFFRINT', 'compare diff'], ['x', 'identifier'], ['AN', 'noonecares'], ['BIGGR OF', 'max'], ['x', 'identifier'], ['AN', 'asdasd'], ['y', 'identifier'], ['\n', 'linebreak']],
    [['VISIBLE', 'output'], ['DIFFRINT', 'compare diff'], ['x', 'identifier'], ['AN', 'noonecares'], ['SMALLR OF', 'min'], ['x', 'identifier'], ['AN', 'asdasd'], ['y', 'identifier'], ['\n', 'linebreak']],
    [['KTHXBYE', 'program end'], ['\n', 'linebreak']]
    ]

# s = Semantic(SAMPLE_CODE)
# s.read_code()
