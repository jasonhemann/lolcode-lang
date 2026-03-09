# LOLCODE Interpreter
# AUTHOR: John Nico T. De Castro
# CREATION DATE: 11/12/2024
# DESCRIPTION: An interpreter for the LOLCODE language. A project for CMSC 124.

import customtkinter as ctk
import re
import decimal as dec

SEMANTIC_ERR = 2

symbol_table = {}
func_table = {}

def semantic_analysis(symbols, parse_tree, print_console, reset_console, semantic_err_handler):
    global symbol_table 
    global func_table
    func_table = {}
    symbol_table = {}
    print("\n==================== PERFORMING SEMANTIC ANALYSIS ====================\n")

    set_or_update_it("NOOB Literal", "", symbol_table)

    # Functions
    for token in parse_tree:
        if token[0] == 'funcdef':
            try:
                process_funcs(token)
            except Exception as e:
                reset_console()
                return semantic_err_handler(f"{e}")

    # handle variable declarations
    for token in parse_tree:
        if token[0] == 'vardecport':
            try:
                process_vardecport(token)
            except Exception as e:
                reset_console()
                return semantic_err_handler(f"{e}")
            break

    # statements
    for token in parse_tree:
        if token[0] == 'statements':
            try:
                process_statements(token[1:], print_console, symbol_table)
            except Exception as e:
                reset_console()
                return semantic_err_handler(f"{e}")
            break

    # append to symbols
    for ident,sym_data in symbol_table.items():
         symbols.append([ident, sym_data['value']])

    print("==================== COMPLETED SEMANTIC ANALYSIS ====================")
    return 0

def process_funcs(statements):
    func_name = statements[1][1]
    params = statements[2][1:]
    func_statements = statements[3][1:]
    return_val = statements[4][1]

    # add params to paramlist
    paramlist = []
    for param in params:
        paramlist.append(param[1])

    # add params to func symbol table
    func_sym_table = {}
    for param in paramlist:
        func_sym_table[param] = {"type": "NOOB Literal", "value": ""}

    # print(f'funcname {func_name}')
    # print(f'paramlist {paramlist}')
    # print(f'funcstatements {func_statements}')
    # print(f'returnval {return_val}')
    # print(f'func_sym_tab {func_sym_table}')
    add_func(func_name, paramlist, func_statements, return_val, func_sym_table)
    

def process_statements(statements, print_console, passed_sym_table):
    symbol_table = passed_sym_table
    for statement in statements:
        print(statement) 
        if statement[0] == 'print':
            print_str = []
            if statement[1][0] == "concat":
                statement = statement[1]
            for i in range(1,len(statement)):
                if statement[i][0] == 'literal':
                    print_type, print_val = typecast((statement[i][1], re.sub(r'\"', '', statement[i][2])), "YARN Literal")
                    set_or_update_it(print_type, print_val, symbol_table)
                    print_str.append(symbol_table["IT"]['value'])
                elif statement[i][0] == 'varident':
                    check_variable(statement[i][1], symbol_table)
                    print_type, print_val = typecast((symbol_table[statement[i][1]]['type'],symbol_table[statement[i][1]]['value']), "YARN Literal")
                    set_or_update_it(print_type, print_val, symbol_table)
                    print_str.append(symbol_table["IT"]['value'])
                    # print_console(symbol_table[statement[i][1]]['value'])
                elif statement[i][0] == 'expr':
                    print_type, print_val = evaluate_expr(statement[i], symbol_table)
                    print_type, print_val = typecast((print_type, print_val), "YARN Literal")
                    set_or_update_it(print_type, print_val, symbol_table)
                    print_str.append(symbol_table["IT"]['value'])
            print_console("".join(print_str))
            set_or_update_it("YARN Literal", "".join(print_str), symbol_table)
        elif statement[0] == 'input':
            dialog = ctk.CTkInputDialog(text="Enter input:", title="Input")
            check_variable(statement[1][1], symbol_table)
            input_type, input_val = typecast(('YARN Literal',dialog.get_input()), 'YARN Literal')
            update_variable(statement[1][1], input_type, input_val)
            set_or_update_it(input_type, input_val, symbol_table)
        elif statement[0] == 'varassign':
            var = statement[1][1]
            new_val = statement[2]  # literal, varident, typecast, concat, expr
            check_variable(var, symbol_table)
            if new_val[0] == 'literal':
                var_type, var_val = typecast((new_val[1], new_val[2]), new_val[1])
                set_or_update_it(var_type, var_val, symbol_table)
                update_variable(var, var_type, var_val)
            elif new_val[0] == 'varident':
                check_variable(new_val[1], symbol_table)
                set_or_update_it(symbol_table[new_val[1]]['type'], symbol_table[new_val[1]]['value'], symbol_table)
                update_variable(var, symbol_table[new_val[1]]['type'], symbol_table[new_val[1]]['value'])
            elif new_val[0] == 'expr':
                var_type, var_val = evaluate_expr(new_val, symbol_table)
                set_or_update_it(var_type, var_val, symbol_table)
                update_variable(var_type, var_val)
            elif new_val[0] == 'concat':
                concat_str = []
                for i in range(1,len(new_val)):
                    if new_val[i][0] == 'literal':
                        concat_type, concat_val = typecast((new_val[i][1], re.sub(r'\"', '', new_val[i][2])), "YARN Literal")
                        set_or_update_it(concat_type, concat_val, symbol_table)
                        concat_str.append(symbol_table["IT"]['value'])
                    elif new_val[i][0] == 'varident':
                        check_variable(new_val[i][1], symbol_table)
                        concat_type, concat_val = typecast((symbol_table[new_val[i][1]]['type'],symbol_table[new_val[i][1]]['value']), "YARN Literal")
                        set_or_update_it(concat_type, concat_val, symbol_table)
                        concat_str.append(symbol_table["IT"]['value'])
                    elif new_val[i][0] == 'expr':
                        concat_type, concat_val = evaluate_expr(new_val[i], symbol_table)
                        concat_type, concat_val = typecast((concat_type, concat_val), "YARN Literal")
                        set_or_update_it(concat_type, concat_val, symbol_table)
                        concat_str.append(symbol_table["IT"]['value'])
                set_or_update_it("YARN Literal", "".join(concat_str), symbol_table)
                update_variable(var, "YARN Literal", "".join(concat_str))
            elif new_val[0] == 'typecast':
                new_var_type, new_var_val = typecast((symbol_table[new_val[1][1]]['type'],symbol_table[new_val[1][1]]['value']),new_val[2][2])
                set_or_update_it(new_var_type, new_var_val, symbol_table)
                update_variable(new_val[1][1], new_var_type, new_var_val)
        elif statement[0] == 'typecast':
            new_var_type, new_var_val = typecast((symbol_table[statement[1][1]]['type'],symbol_table[statement[1][1]]['value']),statement[2][2])
            set_or_update_it(new_var_type, new_var_val, symbol_table)
            update_variable(statement[1][1], new_var_type, float(new_var_val))
        elif statement[0] in ['expr', 'literal', 'varident']:
            new_it = evaluate_expr(statement, symbol_table)  # literal, varident, expr
            set_or_update_it(new_it[0], new_it[1], symbol_table)
        elif statement[0] == "ifelse":
            if symbol_table['IT']['type'] == "TROOF Literal":
                if symbol_table['IT']['value'] == "WIN":
                    process_statements(statement[1][1:], print_console, symbol_table)
                elif symbol_table['IT']['value'] == "FAIL" and statement[-1][0] == 'else':
                    process_statements(statement[2][1:], print_console, symbol_table)
        elif statement[0] == "switchcase":
            cases = statement[1:]
            switch_val = symbol_table["IT"]["value"]
            case_matched = False

            for case in cases:
                if case[0] == "omg":
                    # cmp case val with switch val
                    case_val = evaluate_expr(case[1], symbol_table)

                    # fix int/float
                    case_val = typecast(case_val, case_val[0])

                    # execute code if fall-through or matched case
                    if case_matched or case_val[1] == switch_val:
                        case_matched = True
                        process_statements(case[2:], print_console, symbol_table)

                        if "loopbreak" in case:     # if GTFO found, skip succeeding cases
                            break

                elif case[0] == "omgwtf":
                    # execute default if no match
                    if not case_matched:
                        process_statements(case[1:], print_console, symbol_table)
                        break
        elif statement[0] == "loop":
            operation = statement[2]
            op_var_name = statement[2][2][1]
            loop_type = statement[3][1]
            cond_expr = statement[3][2]
            loop_statements = statement[4]

            # check initial condition
            cond_result = evaluate_expr(cond_expr, symbol_table)
            set_or_update_it(cond_result[0], cond_result[1], symbol_table)
            if cond_result[1] == "FAIL" and loop_type == "TIL":
                while cond_result[1] == "FAIL":
                    # execute loop statements
                    process_statements(loop_statements[1:], print_console, symbol_table)

                    # perform operation and update var
                    op_result = evaluate_expr(operation, symbol_table)
                    update_variable(op_var_name, op_result[0], op_result[1])
                    set_or_update_it(op_result[0], op_result[1], symbol_table)

                    # update condition result
                    cond_result = evaluate_expr(cond_expr, symbol_table)
                    set_or_update_it(cond_result[0], cond_result[1], symbol_table)
            elif cond_result[1] == "WIN" and loop_type == "WILE":
                while cond_result[1] == "WIN":
                    # execute loop statements
                    process_statements(loop_statements[1:], print_console, symbol_table)

                    # perform operation and update var
                    op_result = evaluate_expr(operation, symbol_table)
                    update_variable(op_var_name, op_result[0], op_result[1])
                    set_or_update_it(op_result[0], op_result[1], symbol_table)

                    # update condition result
                    cond_result = evaluate_expr(cond_expr, symbol_table)
                    set_or_update_it(cond_result[0], cond_result[1], symbol_table)
        elif statement[0] == "funcall":
            func_name = statement[1][1]
            args = statement[2][1:]
            params = func_table[func_name]["params"]
            func_sym_table = func_table[func_name]["sym_table"]
            check_func(func_name)

            if len(args) != len(params):
                raise ValueError(f"Function {func_name} expected {len(params)} arguments, got {len(args)}")
            
            # bind values to func local variables
            for index in range(len(params)):
                new_val = evaluate_expr(args[index], symbol_table)
                new_val = typecast(new_val, new_val[0])     # fix int/float vals
                # update function variable
                update_func_variable(func_sym_table, params[index], new_val[0], new_val[1])
            
            func_body = func_table[func_name]["body"]
            # execute func_body but with local variable scope
            process_statements(func_body, print_console, func_sym_table)

            # set return val as IT of local variable symbol table, then set it as IT of global symbol table
            return_val = func_table[func_name]["return_val"]
            if return_val == "NOOB": 
                process_statements([("literal", "NOOB Literal", "")], print_console, func_sym_table)
                func_it = func_sym_table["IT"]
                set_or_update_it(func_it["type"], func_it["value"], symbol_table)
            else:
                process_statements([func_table[func_name]["return_val"]], print_console, func_sym_table)
                func_it = func_sym_table["IT"]
                set_or_update_it(func_it["type"], func_it["value"], symbol_table)

def process_vardecport(vardecport):
    for var in vardecport[1:]:
        # get name
        var_name = None
        if var[0] == 'vardec':
            var_name = var[1][1]
        elif var[0] == 'varinit':
            var_name = var[1][1][1]

        # get val & type
        var_val = ''
        var_type = 'NOOB Literal'
        if var[0] == 'varinit':
            if var[2][0] == 'literal':
                var_type = var[2][1]
                var_val = re.sub(r'\"', '', var[2][2])
            elif var[2][0] == 'varident':
                varident_val = var[2][1]
                try:
                    check_variable(varident_val, symbol_table)
                except:
                    raise Exception(f"Variable '{varident_val}' used before declaration.")
                var_val = symbol_table[varident_val]['value']
                var_type = symbol_table[varident_val]['type']
            elif var[2][0] == 'expr':
                var_type, var_val = evaluate_expr(var[2], symbol_table)
            set_or_update_it(var_type, var_val, symbol_table)

        add_variable(var_name, var_type, var_val)

def evaluate_expr(expr, sym_table):
    symbol_table = sym_table
    if expr[0] == "varident":
        check_variable(expr[1], symbol_table)
        return [symbol_table[expr[1]]['type'], symbol_table[expr[1]]['value']]
    elif expr[0] == "literal":
        return expr[1:]
    elif expr[0] == "expr":
        return evaluate_expr(expr[1], symbol_table)
    elif expr[0] == "operation":
        op1 = evaluate_expr(expr[2], symbol_table)
        op2 = evaluate_expr(expr[3], symbol_table)

        if expr[1] in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]:
            # at least one numbar, result is numbar
            if op1[0] == "NUMBAR Literal" or op2[0] == "NUMBAR Literal":
                op1 = typecast(op1, "NUMBAR Literal")
                op2 = typecast(op2, "NUMBAR Literal")
            else:
                try:
                    op1 = typecast(op1, "NUMBR Literal")
                    op2 = typecast(op2, "NUMBR Literal")
                except:
                    op1 = typecast(op1, "NUMBAR Literal")
                    op2 = typecast(op2, "NUMBAR Literal")

            # Perform the operation
            if expr[1] == "SUM OF":
                return op1[0], op1[1] + op2[1]
            elif expr[1] == "DIFF OF":
                return op1[0], op1[1] - op2[1]
            elif expr[1] == "PRODUKT OF":
                return op1[0], op1[1] * op2[1]
            elif expr[1] == "QUOSHUNT OF":
                if op2[1] == 0:
                    raise Exception("Runtime Error: Division by zero.")
                if op1[0] == "NUMBAR Literal" or op2[0] == "NUMBAR Literal":
                    return op1[0], op1[1] / op2[1]
                else:
                    return op1[0], op1[1] // op2[1]
            elif expr[1] == "MOD OF":
                if op2[1] == 0:
                    raise Exception("Runtime Error: Division by zero.")
                else:
                    return op1[0], op1[1] % op2[1]
            elif expr[1] == "BIGGR OF":
                return op1[0], max(op1[1], op2[1])
            elif expr[1] == "SMALLR OF":
                return op1[0], min(op1[1], op2[1])
    elif expr[0] == "compop":
        op1 = evaluate_expr(expr[2], symbol_table)
        op2 = evaluate_expr(expr[3], symbol_table)
        
        if expr[1] in ["BOTH SAEM", "DIFFRINT"]:
            # fix int/float
            op1 = typecast(op1, op1[0])
            op2 = typecast(op2, op2[0])

            if op1[0] != op2[0]:
                raise ValueError(f"Type mismatch in comparison operation ({op1[0]} and {op2[0]})")
            elif expr[1] == "BOTH SAEM":
                if op1[1] == op2[1]:
                    return "TROOF Literal", "WIN"
                else:
                    return "TROOF Literal", "FAIL"
            elif expr[1] == "DIFFRINT":
                if op1[1] == op2[1]:
                    return "TROOF Literal", "FAIL"
                else:
                    return "TROOF Literal", "WIN"
    elif expr[0] == "boolop":
        if expr[1] in ("NOT", "BOTH OF", "EITHER OF", "WON OF"):
            if expr[1] == "NOT":
                op1 = evaluate_expr(expr[2], symbol_table)
                op1 = typecast(op1, "TROOF Literal")
                if op1[1] == "WIN":
                    return op1[0], "FAIL"
                else:
                    return op1[0], "WIN"

            op1 = evaluate_expr(expr[2], symbol_table)
            op2 = evaluate_expr(expr[3], symbol_table)

            op1 = typecast(op1, "TROOF Literal")
            op2 = typecast(op2, "TROOF Literal")

            if expr[1] == "BOTH OF":
                if op1[1] == "WIN" and op2[1] == "WIN":
                    return op1[0], "WIN"
                else:
                    return op1[0], "FAIL"
            elif expr[1] == "EITHER OF":
                if op1[1] == "WIN" or op2[1] == "WIN":
                    return op1[0], "WIN"
                else:
                    return op1[0], "FAIL"
            elif expr[1] == "WON OF":
                if (op1[1] == "WIN") ^ (op2[1] == "WIN"):
                    return op1[0], "WIN"
                else:
                    return op1[0], "FAIL"
    elif expr[0] == "infboolop":
        if expr[1] in ("ANY OF", "ALL OF"):
            oplist = []
            for op in expr[2:]:
                oplist.append(typecast(evaluate_expr(op, symbol_table), "TROOF Literal"))
            
            if expr[1] == "ANY OF":
                if any([True if op[1] == "WIN" else False for op in oplist]):
                    return oplist[0][0], "WIN"
                else:
                    return oplist[0][0], "FAIL"
            elif expr[1] == "ALL OF":
                if all([True if op[1] == "WIN" else False for op in oplist]):
                    return oplist[0][0], "WIN"
                else:
                    return oplist[0][0], "FAIL"
    elif expr[0] == "loopop":
        if expr[1] in ("UPPIN", "NERFIN"):
            # extract varname
            var_name = expr[2][1]
            
            # check if existing
            check_variable(var_name, symbol_table)

            # try typecasting to NUMBR or NUMBAR
            try:
                var = typecast([symbol_table[var_name]["type"], symbol_table[var_name]["value"]], "NUMBR Literal")
            except:
                var = typecast([symbol_table[var_name]["type"], symbol_table[var_name]["value"]], "NUMBAR Literal")

            if expr[1] == "UPPIN":
                return var[0], var[1]+1
            elif expr[1] == "NERFIN":
                return var[0], var[1]-1
    else:
        raise ValueError("Unknown operation")

def typecast(value, target_type):
    source_type, source_value = value
    
    # Handle typecasting
    if source_type == "NOOB Literal" or source_type == "NOOB":
        if target_type == "TROOF Literal" or target_type == "TROOF":
            return ("TROOF Literal", "FAIL")
        elif target_type == "NUMBR Literal" or target_type == "NUMBR":
            return ("NUMBR Literal", 0)
        elif target_type == "NUMBAR Literal" or target_type == "NUMBAR":
            try:
                return ("NUMBAR Literal", dec.Decimal(0.0))
            except:
                raise Exception(f"Unable to typecast: {source_value} to {target_type}")
        elif target_type == "YARN Literal" or target_type == "YARN":
            return ("YARN Literal", "")
        elif target_type == "NOOB Literal" or target_type == "NOOB":
            return ("NOOB Literal", "")
        else:
            raise Exception(f"Invalid typecast: NOOB Literal to {target_type}")

    elif source_type == "TROOF Literal" or source_type == "TROOF":
        if target_type == "NUMBR Literal" or target_type == "NUMBR":
            return ("NUMBR Literal", 1 if source_value == "WIN" else 0)
        elif target_type == "NUMBAR Literal" or target_type == "NUMBAR":
            return ("NUMBAR Literal", dec.Decimal(1.0) if source_value == "WIN" else dec.Decimal(0.0))
        elif target_type == "YARN Literal" or target_type == "YARN":
            return ("YARN Literal", source_value)
        elif target_type == "TROOF Literal" or target_type == "TROOF":
            return ("TROOF Literal", "WIN" if source_value == "WIN" else "FAIL")
        else:
            raise Exception(f"Invalid typecast: TROOF Literal to {target_type}")

    elif source_type == "NUMBR Literal" or source_type == "NUMBR":
        if target_type == "NUMBAR Literal" or target_type == "NUMBAR":
            return ("NUMBAR Literal", dec.Decimal(float(source_value)))
        elif target_type == "YARN Literal" or target_type == "YARN":
            return ("YARN Literal", str(source_value))
        elif target_type == "NUMBR Literal" or target_type == "NUMBR":
            return ("NUMBR Literal", int(source_value))
        elif (target_type == "TROOF Literal" or target_type == "TROOF"):
            return ("TROOF Literal", "FAIL" if int(source_value) == 0 else "WIN")
        else:
            raise Exception(f"Invalid typecast: NUMBR Literal to {target_type}")

    elif source_type == "NUMBAR Literal" or source_type == "NUMBAR":
        if target_type == "NUMBR Literal" or target_type == "NUMBR":
            return ("NUMBR Literal", int(source_value))  # Truncate decimal part
        elif target_type == "YARN Literal" or target_type == "YARN":
            return ("YARN Literal", str(float(source_value)))
        elif source_type == "NUMBAR Literal":
            return ("NUMBAR Literal", dec.Decimal(source_value))
        elif (target_type == "TROOF Literal" or target_type == "TROOF"):
            return ("TROOF Literal", "FAIL" if source_value == 0 else "WIN")
        else:
            raise Exception(f"Invalid typecast: NUMBAR Literal to {target_type}")

    elif source_type == "YARN Literal" or source_type == "YARN":
        if target_type == "NUMBR Literal" or target_type == "NUMBR":
            try:
                return ("NUMBR Literal", int(re.sub(r'\"', '', source_value)))
            except Exception:
                raise Exception(f"Invalid typecast: YARN Literal '{source_value}' cannot be converted to NUMBR Literal")
        elif target_type == "NUMBAR Literal" or target_type == "NUMBAR":
            try:
                return ("NUMBAR Literal", dec.Decimal(re.sub(r'\"', '', source_value)))
            except Exception:
                raise Exception(f"Invalid typecast: YARN Literal '{source_value}' cannot be converted to NUMBAR Literal")
        elif (target_type == "TROOF Literal" or target_type == "TROOF"):
            return ("TROOF Literal", "FAIL" if source_value == "" or source_value == None else "WIN")
        elif target_type == "YARN Literal" or target_type == "YARN":
            return ("YARN Literal", f"{source_value}")
        else:
            raise Exception(f"Invalid typecast: YARN Literal to {target_type}")

    else:
        raise Exception(f"Unknown source type: {source_type}")

def set_or_update_it(it_type, it_value, sym_table):
    if 'IT' in sym_table:
        sym_table['IT']['type'] = it_type
        sym_table['IT']['value'] = it_value
    else:
        sym_table['IT'] = {'type': it_type, 'value': it_value}

def add_variable(name, var_type, value=None):
    if name in symbol_table:
        raise Exception(f"Variable '{name}' already declared.")
    symbol_table[name] = {'type': var_type, 'value': value}

def update_variable(name, var_type=None, value=None):
    if name not in symbol_table:
        raise Exception(f"Variable '{name}' not declared.")
    if var_type != None:
        symbol_table[name]['type'] = var_type
    if value != None:
        symbol_table[name]['value'] = value

def check_variable(name, sym_table):
    if name not in sym_table:
        raise Exception(f"Variable '{name}' used before declaration.")
    
def add_func(name, params, body, return_val, sym_table):
    if name in func_table:
        raise Exception(f"Function '{name}' already defined.")
    func_table[name] = {'params': params, 'body': body, 'return_val': return_val, 'sym_table': sym_table}

def update_func_variable(sym_table, name, var_type=None, value=None):
    if name not in sym_table:
        raise Exception(f"Variable '{name}' not declared.")
    if var_type != None:
        sym_table[name]['type'] = var_type
    if value != None:
        sym_table[name]['value'] = value

def check_func(name):
    if name not in func_table:
        raise NameError(f"Function {name} not defined")

# TODO COMMENT! FOR TESTING PURPOSES ONLY!
def print_symbol_table():
    for k,v in symbol_table.items():
        print(f'{k} {v}')