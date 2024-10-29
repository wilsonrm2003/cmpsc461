import ASTNodeDefs as AST

class Lexer:
    # Write a lexer to tokenize input code into meaningful tokens (e.g., keywords,
    # operators, identifiers, numbers).
    # Handle basic tokens like if, else, while, +, -, *, /, =, !=, ==, <, >, (, ), :, etc.
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.current_char = self.code[self.position]
        self.tokens = []

    # Move to the next position in the code.
    def advance(self):
        # TODO: Students need to complete the logic to advance the position.
        self.position += 1 # changes to next condition 
        self.current_char = self.code[self.position]

    # Skip whitespaces.
    def skip_whitespace(self):
        # TODO: Complete logic to skip whitespaces.
        if self.current_char == " ":
            self.advance()
            self.current_char = self.code[self.position]

    # Tokenize an identifier.
    def identifier(self):
        result = ''
        # TODO: Complete logic for handling identifiers.
        while (self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == '_'):
            result = result + self.current_char
            self.advance()
        return ('IDENTIFIER', result)

    # Tokenize a number.
    def number(self):
        # TODO: Implement logic to tokenize numbers.
        num = 0
        num_place = 1
        while (self.current_char.isdigit()):
            num = self.current_char * num_place
            num_place = num_place * 10
            self.advance()
        return ('NUMBER', num)

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
                return ident
            if self.current_char.isdigit():
                return self.number()

            # TODO: Add logic for operators and punctuation tokens.
            if ident


            raise ValueError(f"Illegal character at position {self.position}: {self.current_char}")

        return ('EOF', None)

    # Collect all tokens into a list.
    def tokenize(self):
        # TODO: Implement the logic to collect tokens.
        return self.tokens

class Parser:
    # Build a parser that converts a token stream into an Abstract Syntax Tree (AST).
    # Implement parsing logic for different constructs like assignment statements (x =
    # expression), binary operations (expression1 + expression2), boolean expressions (x
    # == y), if-else statements, while loops, and function calls.
    # Use recursive descent parsing methods to generate AST nodes for these
    # constructs.
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = tokens.pop(0)  # Start with the first token

    def advance(self):
        # Move to the next token in the list.
        # TODO: Ensure the parser doesn't run out of tokens.
        self.current_token = self.tokens.pop(0)

    def parse(self):
        """
        Entry point for the parser. It will process the entire program.
        TODO: Implement logic to parse multiple statements and return the AST for the entire program.
        """
        return self.program()

    def program(self):
        """
        Program consists of multiple statements.
        TODO: Loop through and collect statements until EOF is reached.
        """
        statements = []
        while self.current_token[0] != 'EOF':
            # TODO: Parse each statement and append it to the list.
            statements += self.current_token
            self.current_token = self.tokens.pop() # update current token by poping the tokens
        # TODO: Return an AST node that represents the program.
        return statements

    def statement(self):
        """
        Determines which type of statement to parse.
        - If it's an identifier, it could be an assignment or function call.
        - If it's 'if', it parses an if-statement.
        - If it's 'while', it parses a while-statement.
        
        TODO: Dispatch to the correct parsing function based on the current token.
        """
        if self.current_token[0] == 'IDENTIFIER':
            if self.peek() == 'EQUALS':  # Assignment
                return self.assign_stmt() #AST of assign_stmt
            elif self.peek() == 'LPAREN':  # Function call
                return self.function_call() #AST of function call
            else:
                raise ValueError(f"Unexpected token after identifier: {self.current_token}")
        elif self.current_token[0] == 'IF':
            return self.if_stmt() #AST of if stmt
        elif self.current_token[0] == 'WHILE':
            return self.while_stmt() #AST of while stmt
        else:
            # TODO: Handle additional statements if necessary.
            raise ValueError(f"Unexpected token: {self.current_token}")

    def assign_stmt(self):
        """
        Parses assignment statements.
        Example:
        x = 5 + 3
        TODO: Implement parsing for assignments, where an identifier is followed by '=' and an expression.
        """
        identifier = self.current_token
        expression = self.current_token
        return AST.Assignment(identifier, expression)

    def if_stmt(self):
        """
        Parses an if-statement, with an optional else block.
        Example:
        if condition:
            # statements
        else:
            # statements
        TODO: Implement the logic to parse the if condition and blocks of code.
        """


    def while_stmt(self):
        """
        Parses a while-statement.
        Example:
        while condition:
            # statements
        TODO: Implement the logic to parse while loops with a condition and a block of statements.
        """

        return AST.WhileStatement(condition, block)

    def block(self):
        """
        Parses a block of statements. A block is a collection of statements grouped by indentation.
        Example:
        if condition:
            # This is a block
            x = 5
            y = 10
        TODO: Implement logic to capture multiple statements as part of a block.
        """
        statements = []
        # write your code here
        return AST.Block(statements)

    def expression(self):
        """
        Parses an expression. Handles operators like +, -, etc.
        Example:
        x + y - 5
        TODO: Implement logic to parse binary operations (e.g., addition, subtraction) with correct precedence.
        """
        left = self.term()  # Parse the first term
        while self.current_token[0] in ['PLUS', 'MINUS']:  # Handle + and -
            op = self.current_token  # Capture the operator
            self.advance()  # Skip the operator
            right = self.term()  # Parse the next term
            left = AST.BinaryOperation(left, op, right)
    
        return left

    def boolean_expression(self):
        """
        Parses a boolean expression. These are comparisons like ==, !=, <, >.
        Example:
        x == 5
        TODO: Implement parsing for boolean expressions.
        """
        # write your code here, for reference check expression function
        return 

    def term(self):
        """
        Parses a term. A term consists of factors combined by * or /.
        Example:
        x * y / z
        TODO: Implement the parsing for multiplication and division.
        """
        # write your code here, for reference check expression function
        return 

    def factor(self):
        """
        Parses a factor. Factors are the basic building blocks of expressions.
        Example:
        - A number
        - An identifier (variable)
        - A parenthesized expression
        TODO: Handle these cases and create appropriate AST nodes.
        """
        if self.current_token[0] == 'NUMBER':
            #write your code here
            return num
        elif self.current_token[0] == 'IDENTIFIER':
            #write your code here
        elif self.current_token[0] == 'LPAREN':
            #write your code here
        else:
            raise ValueError(f"Unexpected token in factor: {self.current_token}")

    def function_call(self):
        """
        Parses a function call.
        Example:
        myFunction(arg1, arg2)
        TODO: Implement parsing for function calls with arguments.
        """
        
        return AST.FunctionCall(func_name, args)

    def arg_list(self):
        """
        Parses a list of arguments in a function call.
        Example:
        arg1, arg2, arg3
        TODO: Implement the logic to parse comma-separated arguments.
        """
        args = []
        return args

    def expect(self, token_type):
       
        if self.current_token[0] == token_type:
            self.advance()  # Move to the next token
        else:
            raise ValueError(f"Expected {token_type} but got {self.current_token[0]}")

    def peek(self):
        if self.tokens:
            return self.tokens[0][0]
        else:
            return None
