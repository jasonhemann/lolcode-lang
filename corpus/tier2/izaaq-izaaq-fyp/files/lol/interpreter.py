"""
Metaclasses - Mainly needed for "GTFO" and "FOUND YR" to work as intended.
"""
class Break(Exception):
    pass

class Return(Exception):
    pass

"""
Interpreter
Responsible for functionality and logic of the language 
"""
class InterpreterLOL:

    def __init__(self, tree, env):
        self.env = env          # environment to store variables and functions
        self.walkTree(tree)     # recursively walk the parse tree

    # execute every statement in statement list
    def executeStatements(self, statements):
        if statements:
            try:
                for statement in statements:
                    self.walkTree(statement)
            except Break:
                raise Break
            except Return:
                raise Return
            except Exception as e:
                raise e

    # return value of variable
    def getVariable(self, name):
        try:
            return self.env[name]
        except KeyError:
            raise Exception(f"Error - No variable named '{name}' found.'")

    def setVariable(self, name, value):
        if name in self.env:
            self.env[name] = value
        else:
            raise Exception(f"Error - No variable named '{name}' found.'")

    # make a new variable - value to None
    def declareVariable(self, name):
        if name not in self.env:
            self.env[name] = None
        else:
            raise Exception(f"Name '{name}' already taken.")

    # delete variable - really only for 'return' to work as intended
    def deleteVariable(self, name):
        try:
            self.env.pop(name)
        except KeyError:
            raise Exception(f"Error - No variable named '{name}' found.")

    def walkTree(self, node):

        # untyped data
        if node is None:
            return 'NOOB'

        elif node[0] == 'int':
            return node[1]

        elif node[0] == 'float':
            return node[1]

        elif node[0] == 'str':
            return node[1]

        elif node[0] == 'bool':
            return node[1]

        elif node[0] == 'print':
            toPrint = self.walkTree(node[1])
            # print "WIN" if expr == True, and "FAIL" if false.
            if isinstance(toPrint, bool):
                if toPrint:
                    print("WIN", end='')
                else:
                    print("FAIL", end='')
            elif toPrint is None:
                print("NOOB", end='')
            else:
                print(toPrint, end='')
        elif node[0] == 'printline':
            toPrint = self.walkTree(node[1])
            if isinstance(toPrint, bool):
                if toPrint:
                    print("WIN")
                else:
                    print("FAIL")
            elif toPrint is None:
                print("NOOB")
            else:
                print(toPrint)

        elif node[0] == 'input':
            self.declareVariable(node[1])
            self.setVariable(node[1], input())

        elif node[0] == 'var_def':
            self.declareVariable(node[1])
            self.setVariable(node[1], self.walkTree(node[2]))

        elif node[0] == 'var_declare':
            self.declareVariable(node[1])

        elif node[0] == 'assign':
            self.setVariable(node[1], self.walkTree(node[2]))

        elif node[0] == 'convert':
            if node[2] == 'YARN':
                try:
                    self.setVariable(node[1], str(self.getVariable(node[1])))
                except ValueError:
                    raise Exception(f"Cannot convert {node[1]} to string.")
                except TypeError:
                    self.setVariable(node[1], "")
            elif node[2] == 'NUMBR':
                try:
                    self.setVariable(node[1], int(self.getVariable(node[1])))
                except ValueError:
                    raise Exception(f"Cannot convert identifier '{node[1]}' to integer.")
                except TypeError:
                    self.setVariable(node[1], 0)
            elif node[2] == 'NUMBAR':
                try:
                    self.setVariable(node[1], float(self.getVariable(node[1])))
                except ValueError:
                    raise Exception(f"Cannot convert identifier '{node[1]}' to float.")
                except TypeError:
                    self.setVariable(node[1], 0.0)
            elif node[2] == 'TROOF':
                try:
                    self.setVariable(node[1], bool(self.getVariable(node[1])))
                except ValueError:
                    raise Exception(f"Cannot convert identifier '{node[1]}' to boolean.")
                except TypeError:
                    self.setVariable(node[1], False)
            elif node[2] == 'NOOB':
                try:
                    self.setVariable(node[1], None)
                except ValueError:
                    raise Exception(f"Cannot convert identifier '{node[1]}' to None.")
            else:
                raise Exception(f"Type '{node[2]}' is not a defined data type.")

        elif node[0] == 'if':
            if self.walkTree(node[1]):
                self.executeStatements(node[2])
        elif node[0] == 'if-else':
            if self.walkTree(node[1]):
                self.executeStatements(node[2])
            else:
                self.executeStatements(node[3])
        elif node[0] == 'if-elif':
            if self.walkTree(node[1]):
                self.executeStatements(node[2])
            elif self.walkTree(node[3]):
                self.executeStatements(node[4])
        elif node[0] == 'if-elif-else':
            if self.walkTree(node[1]):
                self.executeStatements(node[2])
            elif self.walkTree(node[3]):
                self.executeStatements(node[4])
            else:
                self.executeStatements(node[5])

        # LOLCODE - loops execute forever until 'GTFO' reached.
        elif node[0] == 'loop':
            if node[1] != node[3]:
                raise Exception("Error - Loop opener and closer must have same name.")
            try:
                while True:
                    self.executeStatements(node[2])
            except Break:
                pass

        elif node[0] == 'counted_loop':
            if node[1] != node[7]:
                raise Exception("Error - Loop opener and closer must have same name.")
            change = 1
            index = self.getVariable(node[3])
            if node[2] == 'decrement':
                change = -1
            if node[4] == 'TIL':
                try:
                    while not self.walkTree(node[5]):
                        index += change
                        self.setVariable(node[3], index)
                        self.executeStatements(node[6])
                except Break:
                    pass
            elif node[4] == 'WILE':
                try:
                    while self.walkTree(node[5]):
                        index += change
                        self.setVariable(node[3], index)
                        self.executeStatements(node[6])
                except Break:
                    pass

        elif node[0] == 'break':
            raise Break()

        elif node[0] == 'func_def':
            self.declareVariable(node[1])
            self.setVariable(node[1], node[2])

        elif node[0] == 'func_call':
            function = self.getVariable(node[1])
            try:
                self.declareVariable('ret')         # make temporary variable for return variable
                self.executeStatements(function)
            except LookupError:
                print(f"No function named '{node[1]}'")
            except Break:
                ret = None
            except Return:
                ret = self.getVariable('ret')
            finally:
                self.deleteVariable('ret')          # delete variable - not needed
            return ret

        elif node[0] == 'return':
            self.setVariable('ret', self.walkTree(node[1]))
            raise Return()

        elif node[0] == 'not':
            return not self.walkTree(node[1])

        elif node[0] == 'bin_op':
            if isinstance(self.walkTree(node[2]), str) or isinstance(self.walkTree(node[3]), str):
                raise Exception("Error - Cannot perform math on strings")
            elif node[1] == 'SUM OF':
                return self.walkTree(node[2]) + self.walkTree(node[3])
            elif node[1] == 'DIFF OF':
                return self.walkTree(node[2]) - self.walkTree(node[3])
            elif node[1] == 'PRODUKT OF':
                return self.walkTree(node[2]) * self.walkTree(node[3])
            elif node[1] == 'QUOSHUNT OF':
                if self.walkTree(node[3]) == 0:
                    raise Exception(f"Error - Division by zero")
                return self.walkTree(node[2]) / self.walkTree(node[3])
            elif node[1] == 'MOD OF':
                if self.walkTree(node[3]) == 0:
                    raise Exception(f"Error - Division by zero")
                return self.walkTree(node[2]) % self.walkTree(node[3])

        elif node[0] == 'comparison_check':
            if node[1] == 'BOTH SAEM':
                return self.walkTree(node[2]) == self.walkTree(node[3])
            elif node[1] == 'DIFFRINT':
                return self.walkTree(node[2]) != self.walkTree(node[3])
            elif node[1] == 'WON OF':
                return self.walkTree(node[2]) ^ self.walkTree(node[3])
            elif node[1] == 'BOTH OF':
                return self.walkTree(node[2]) and self.walkTree(node[3])
            elif node[1] == 'EITHER OF':
                return self.walkTree(node[2]) or self.walkTree(node[3])
            elif node[1] == 'BIGGR OF':
                return max(self.walkTree(node[2]), self.walkTree(node[3]))
            elif node[1] == 'SMALLR OF':
                return min(self.walkTree(node[2]), self.walkTree(node[3]))

        elif node[0] == 'var':
            return self.getVariable(node[1])

        elif node[0] == 'start':
            self.executeStatements(node[1])
