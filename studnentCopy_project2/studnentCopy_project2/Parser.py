import ASTNodeDefs as AST
class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.current_char = self.code[self.position]
        self.tokens = []
    
    # Move to the next position in the code increment by one.
    def advance(self):
        self.position += 1
        if self.position >= len(self.code):
            self.current_char = None
        else:
            self.current_char = self.code[self.position]

    # If the current char is whitespace, move ahead.
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    # Tokenize the identifier.
    def identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return ('IDENTIFIER', result)
    

    # Tokenize numbers, including float handling
    def number(self):
        result = ''
        # TODO: Update this code to handle floating-point numbers 
        is_float = 0 # initalizes is float to zero so doesnt go to float if it is an int
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == "."):
            if self.current_char == ".":
                is_float = 1 # updates number to a float if there is a . in the number
            result += self.current_char
            self.advance()
        if is_float:
            return ('FNUMBER', float(result))
        else:
            return ('NUMBER', int(result))

    def token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isalpha():
                ident = self.identifier()
                if ident[1] == 'if':
                    return ('IF', 'if')
                elif ident[1] == 'else':
                    return ('ELSE', 'else')
                elif ident[1] == 'while':
                    return ('WHILE', 'while')
                elif ident[1] == 'int':
                    return ('INT', 'int')
                elif ident[1] == 'float':
                    return ('FLOAT', 'float')
                return ident  # Generic identifier
            if self.current_char.isdigit() or self.current_char == '.':
                return self.number()
            if self.current_char == '+':
                self.advance()
                return ('PLUS', '+')
            if self.current_char == '-':
                self.advance()
                return ('MINUS', '-')
            if self.current_char == '*':
                self.advance()
                return ('MULTIPLY', '*')
            if self.current_char == '/':
                self.advance()
                return ('DIVIDE', '/')
            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return ('EQ', '==')
                return ('EQUALS', '=')
            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return ('NEQ', '!=')
            if self.current_char == '<':
                self.advance()
                return ('LESS', '<')
            if self.current_char == '>':
                self.advance()
                return ('GREATER', '>')
            if self.current_char == '(':
                self.advance()
                return ('LPAREN', '(')
            if self.current_char == ')':
                self.advance()
                return ('RPAREN', ')')
            if self.current_char == ',':
                self.advance()
                return ('COMMA', ',')
            if self.current_char == ':':
                self.advance()
                return ('COLON', ':')
            # TODO: Implement handling for '{' and '}' tokens here (see `tokens.txt` for exact names)
            if self.current_char == "{":
                self.advance()
                return ("LBRACE", "{")
            if self.current_char == "}":
                self.advance()
                return ("RBRACE", "}")
            if self.current_char == '\n':
                self.advance()
                continue

            raise ValueError(f"Illegal character at position {self.position}: {self.current_char}")

        return ('EOF', None)

    # Collect all the tokens in a list.
    def tokenize(self):
        while True:
            token = self.token()
            self.tokens.append(token)
            if token[0] == 'EOF':
                break
        return self.tokens

import ASTNodeDefs as AST

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = tokens.pop(0)
        # Use these to track the variables and their scope
        self.symbol_table = {'global': {}}
        self.scope_counter = 0
        self.scope_stack = ['global']
        self.messages = []

    def error(self, message):
        self.messages.append(message)
    
    def advance(self):
        if self.tokens:
            self.current_token = self.tokens.pop(0)

    # TODO: Implement logic to enter a new scope, add it to symbol table, and update `scope_stack`
    def enter_scope(self):
        self.scope_counter += 1
        scope_name = "scope" + (str)(self.scope_counter) # set unique scope name for each scope 
        self.scope_stack.append(scope_name)


    # TODO: Implement logic to exit the current scope, removing it from `scope_stack`
    def exit_scope(self):
        if self.scope_stack:
            self.scope_stack.pop(-1) # remove last item from scope if scope_stack exists

    # Return the current scope name
    def current_scope(self):
        return self.scope_stack[-1]

    # TODO: Check if a variable is already declared in the current scope; if so, log an error
    def checkVarDeclared(self, identifier):
        if self.current_scope() in self.symbol_table: # checks if scope has been added to symbol table yet
            for item in self.symbol_table[self.current_scope()]:
                if identifier == item:
                    self.error(f"Variable {identifier} has already been declared in the current scope")

    # TODO: Check if a variable is declared in any accessible scope; if not, log an error
    def checkVarUse(self, identifier):
        var_notpresent = 1 
        for scope in self.scope_stack: # check the scopes in the scope stack
            if scope in self.symbol_table: # check if the current scope is actually in the symbol table yet
                for item in self.symbol_table[scope]:
                    if identifier == item:
                        var_notpresent = 0 # changes value if variable is not present 
        if (var_notpresent): #if the variable is not present throw the error
            self.error(f"Variable {identifier} has not been declared in the current or any enclosing scopes")

    # TODO: Check type mismatch between two entities; log an error if they do not match
    def checkTypeMatch2(self, vType, eType, var, exp):      
        # print(var, "   ???   ", exp)
        # print(vType, "   ???   ", eType)
        if (vType == "int" and eType == "float") or (vType == "float" and eType == "int"): # only checks for float and int mismatch
            self.error(f"Type Mismatch between {vType} and {eType}")
        
    # TODO: Implement logic to add a variable to the current scope in `symbol_table`
    def add_variable(self, name, var_type):
        if self.current_scope() not in self.symbol_table:
            self.symbol_table[self.current_scope()] = {}
        self.symbol_table[self.current_scope()].update({name : var_type})

    # TODO: Retrieve the variable type from `symbol_table` if it exists
    def get_variable_type(self, name):
        var_type = None # initialize to None in case variable isnt found
        for scope in self.scope_stack:
            if scope in self.symbol_table: # checks if the scope is inside the symbol table before looking for value so doesnt exit scope stack
                for item in self.symbol_table[scope]:
                    if item == name:
                        var_type = self.symbol_table[scope][name].value_type
                        if self.current_scope() == scope:
                            return var_type # return the current variable type in the scope
        return var_type # returns variable type so most recent scope is the valuetype 

    def parse(self):
        return self.program()

    def program(self):
        statements = []
        while self.current_token[0] != 'EOF':
            statements.append(self.statement())
        return AST.Block(statements)

    # TODO: Modify the `statement` function to dispatch to declare statement
    def statement(self):
        if self.current_token[0] == 'IDENTIFIER':
            if self.peek() == 'EQUALS':
                return self.assign_stmt()
            elif self.peek() == 'LPAREN':
                return self.function_call()
            else:
                raise ValueError(f"Unexpected token after identifier: {self.current_token}")
        elif self.current_token[0] == 'IF':
            return self.if_stmt()
        elif self.current_token[0] == 'WHILE':
            return self.while_stmt()
        elif self.current_token[0] == "INT" or self.current_token[0] == "FLOAT":
            return self.decl_stmt()
        elif self.current_token[0] == "LBRACE":
            self.advance()
            self.enter_scope()
            return self.block()
        else:
            raise ValueError(f"Unexpected token: {self.current_token}")

    # TODO: Implement the declaration statement and handle adding the variable to the symbol table
    def decl_stmt(self):
        """
        Parses a declaration statement.
        Example:
        int x = 5
        float y = 3.5
        TODO: Implement logic to parse type, identifier, and initialization expression and also handle type checking
        """
        var_type = self.current_token[1]
        self.advance()
        var_name = self.current_token[1]
        self.expect("IDENTIFIER")
        self.expect("EQUALS")
        expression = self.expression()
        self.checkVarDeclared(var_name) # check if the variable has already been declared in scope before adding it 
        self.checkTypeMatch2(var_type, expression.value_type, var_name, expression) 
        self.add_variable(var_name, expression) # add variable to the sybol table
        return AST.Declaration(var_type, var_name, expression)

    # TODO: Parse assignment statements, handle type checking
    def assign_stmt(self):
        """
        Parses an assignment statement.
        Example:
        x = 10
        x = y + 5
        TODO: Implement logic to handle assignment, including type checking.
        """
        var_name = self.current_token[1]
        self.checkVarUse(var_name)
        self.advance()
        self.expect("EQUALS")
        expression = self.expression()
        self.checkTypeMatch2(self.get_variable_type(var_name), expression.value_type, var_name, expression)
        self.add_variable(var_name, expression)
        return AST.Assignment(var_name, expression)

    # TODO: Implement the logic to parse the if condition and blocks of code
    def if_stmt(self):
        """
        Parses an if-statement, with an optional else block.
        Example:
        if condition {
            # statements
        }
        else {
            # statements
        }
        TODO: Implement the logic to parse the if condition and blocks of code.
        """
        self.expect("IF")
        condition = self.boolean_expression()
        self.expect("LBRACE")
        self.enter_scope()
        then_block = self.block()
        if self.current_token[0] == "ELSE":
            self.expect("ELSE")
            self.enter_scope
            else_block = self.block()
        else: 
            else_block = None
        return AST.IfStatement(condition, then_block, else_block)

    # TODO: Implement the logic to parse while loops with a condition and a block of statements
    def while_stmt(self):
        """
        Parses a while-statement.
        Example:
        while condition {
            # statements
        }
        TODO: Implement the logic to parse while loops with a condition and a block of statements.
        """
        self.expect("WHILE")
        condition = self.boolean_expression()
        self.expect("LBRACE")
        self.enter_scope()
        block = self.block()
        return AST.WhileStatement(condition, block)

    # TODO: Implement logic to capture multiple statements as part of a block
    def block(self):
        """
        Parses a block of statements. A block is a collection of statements grouped by `{}`.
        Example:
        
        x = 5
        y = 10
        
        TODO: Implement logic to capture multiple statements as part of a block.
        """
        statements = []
        while (self.current_token[0] != "EOF" and self.current_token[0] != "RBRACE"):
            statements.append(self.statement())
        if self.current_token[0] != "EOF":
            self.expect("RBRACE")
        self.exit_scope()
        return AST.Block(statements)

    # TODO: Implement logic to parse binary operations (e.g., addition, subtraction) with correct precedence and type checking
    def expression(self):
        """
        Parses an expression. Handles operators like +, -, etc.
        Example:
        x + y - 5
        TODO: Implement logic to parse binary operations (e.g., addition, subtraction) with correct precedence and type checking.
        """
        left = self.term()
        while self.current_token[0] in ['PLUS', 'MINUS']:
            op = self.current_token[0]
            self.advance()
            right = self.term()
            self.checkTypeMatch2(left.value_type, right.value_type, left, right)
            left = AST.BinaryOperation(left, op, right, value_type=left.value_type)

        return left

    # TODO: Implement parsing for boolean expressions and check for type compatibility
    def boolean_expression(self):
        """
        Parses a boolean expression. These are comparisons like ==, !=, <, >.
        Example:
        x == 5
        TODO: Implement parsing for boolean expressions and check for type compatibility.
        """
        left = self.term() # parse first term
        while (self.current_token[0] in ["EQ", "NEQ", "LESS", "GREATER"]):
            op = self.current_token # capture operator
            self.advance() # skip the operator
            right = self.term() # parse the next term
            self.checkTypeMatch2(left.value_type, right.value_type, left, right)
            left = AST.BooleanExpression(left, op, right) # do the boolean operations
        return left
        

    # TODO: Implement parsing for multiplication and division and check for type compatibility
    def term(self):
        """
        Parses a term. A term consists of factors combined by * or /.
        Example:
        x * y / z
        TODO: Implement parsing for multiplication and division and check for type compatibility.
        """
        left = self.factor() # parse first factor
        while (self.current_token[0] in ["MULTIPLY", "DIVIDE"]):
            op = self.current_token # caputre operator
            self.advance()
            right = self.factor() # parse next factor
            self.checkTypeMatch2(left.value_type, right.value_type, left, right)
            left = AST.BinaryOperation(left, op, right, value_type=left.value_type) # do operations
        return left
        
    def factor(self):
        if self.current_token[0] == 'NUMBER':
            # handle int
            num = self.current_token[1]
            self.advance()
            return AST.Factor(num, 'int')
        elif self.current_token[0] == 'FNUMBER':
            # handle float
            num = self.current_token[1]
            self.advance()
            return AST.Factor(num, 'float')
        elif self.current_token[0] == 'IDENTIFIER':
            # TODO: Ensure that you parse the identifier correctly, retrieve its type from the symbol table, and check if it has been declared in the current or any enclosing scopes.
            var_name = self.current_token[1]
            self.checkVarUse(var_name) # check if variable has been declared
            var_type = self.get_variable_type(var_name)
            self.advance()
            return AST.Factor(var_name, var_type)
        elif self.current_token[0] == 'LPAREN':
            self.advance()
            expr = self.expression()
            self.expect('RPAREN')
            return expr
        else:
            raise ValueError(f"Unexpected token in factor: {self.current_token}")

    def function_call(self):
        func_name = self.current_token[1]
        self.advance()
        self.expect('LPAREN')
        args = self.arg_list()
        self.expect('RPAREN')

        return AST.FunctionCall(func_name, args)

    def arg_list(self):
        """
        Parses a list of function arguments.
        Example:
        (x, y + 5)
        """
        args = []
        if self.current_token[0] != 'RPAREN':
            args.append(self.expression())
            while self.current_token[0] == 'COMMA':
                self.advance()
                args.append(self.expression())

        return args

    def expect(self, token_type):
        if self.current_token[0] == token_type:
            self.advance()
        else:
            raise ValueError(f"Expected token {token_type}, but got {self.current_token[0]}")

    def peek(self):
        return self.tokens[0][0] if self.tokens else None
