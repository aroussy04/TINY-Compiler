"""
Parser for the TINY language.

Assumed grammar (based on the token list):

program -> stmt_sequence
stmt_sequence -> statement {; statement}
statement -> if_stmt | repeat_stmt | assign_stmt | read_stmt | write_stmt
if_stmt -> if exp then stmt_sequence end
repeat_stmt -> repeat stmt_sequence until exp
assign_stmt -> identifier := exp
read_stmt -> read identifier
write_stmt -> write exp
exp -> simple_exp [comparison_op simple_exp]
comparison_op -> < | =
simple_exp -> term {addop term}
addop -> + | -
term -> factor {mulop factor}
mulop -> * | /
factor -> (exp) | number | identifier
"""

class Parser:
    def __init__(self):
        self.tokens = []
        self.current_token_index = 0
        self.current_token = None
        self.syntax_tree = None
        
    def parse(self, tokens):
        """
        Parse the tokens and return True if the syntax is correct, False otherwise.
        Also constructs the syntax tree.
        """
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[0] if self.tokens else None
        
        try:
            # Start parsing from the program rule
            self.syntax_tree = self.program()
            
            # Check if we've consumed all tokens
            if self.current_token_index < len(self.tokens):
                raise Exception(f"Unexpected token: {self.current_token}")
                
            return True, self.syntax_tree
        except Exception as e:
            return False, str(e)
            
    def match(self, expected_type):
        """
        Match the current token with the expected type.
        If they match, consume the token and return it.
        Otherwise, raise an exception.
        """
        if self.current_token_index >= len(self.tokens):
            raise Exception("Unexpected end of input")
            
        token_value, token_type = self.current_token
        
        if token_type != expected_type:
            raise Exception(f"Expected {expected_type}, but found {token_type}")
            
        # Consume the token
        consumed_token = self.current_token
        self.current_token_index += 1
        self.current_token = self.tokens[self.current_token_index] if self.current_token_index < len(self.tokens) else None
        
        return consumed_token
        
    def program(self):
        """
        program -> stmt_sequence
        """
        return {'type': 'program', 'body': self.stmt_sequence()}
        
    def stmt_sequence(self):
        """
        stmt_sequence -> statement {; statement}
        """
        statements = [self.statement()]
        
        while self.current_token and self.current_token[1] == 'SEMICOLON':
            self.match('SEMICOLON')
            if self.current_token and self.current_token[1] not in ['END', 'UNTIL']:
                statements.append(self.statement())
            else:
                break
                
        return {'type': 'stmt_sequence', 'statements': statements}
        
    def statement(self):
        """
        statement -> if_stmt | repeat_stmt | assign_stmt | read_stmt | write_stmt
        """
        if not self.current_token:
            raise Exception("Unexpected end of input")
            
        token_value, token_type = self.current_token
        
        if token_type == 'IF':
            return self.if_stmt()
        elif token_type == 'REPEAT':
            return self.repeat_stmt()
        elif token_type == 'READ':
            return self.read_stmt()
        elif token_type == 'WRITE':
            return self.write_stmt()
        elif token_type == 'IDENTIFIER':
            return self.assign_stmt()
        else:
            raise Exception(f"Unexpected token: {token_value}, {token_type}")
            
    def if_stmt(self):
        """
        if_stmt -> if exp then stmt_sequence end
        """
        self.match('IF')
        condition = self.exp()
        self.match('THEN')
        body = self.stmt_sequence()
        self.match('END')
        
        return {'type': 'if_stmt', 'condition': condition, 'body': body}
        
    def repeat_stmt(self):
        """
        repeat_stmt -> repeat stmt_sequence until exp
        """
        self.match('REPEAT')
        body = self.stmt_sequence()
        self.match('UNTIL')
        condition = self.exp()
        
        return {'type': 'repeat_stmt', 'body': body, 'condition': condition}
        
    def assign_stmt(self):
        """
        assign_stmt -> identifier := exp
        """
        identifier = self.match('IDENTIFIER')
        self.match('ASSIGN')
        value = self.exp()
        
        return {'type': 'assign_stmt', 'identifier': identifier, 'value': value}
        
    def read_stmt(self):
        """
        read_stmt -> read identifier
        """
        self.match('READ')
        identifier = self.match('IDENTIFIER')
        
        return {'type': 'read_stmt', 'identifier': identifier}
        
    def write_stmt(self):
        """
        write_stmt -> write exp
        """
        self.match('WRITE')
        value = self.exp()
        
        return {'type': 'write_stmt', 'value': value}
        
    def exp(self):
        """
        exp -> simple_exp [comparison_op simple_exp]
        """
        left = self.simple_exp()
        
        if self.current_token and self.current_token[1] in ['LESSTHAN', 'EQUAL']:
            op = self.current_token
            if op[1] == 'LESSTHAN':
                self.match('LESSTHAN')
            else:
                self.match('EQUAL')
                
            right = self.simple_exp()
            return {'type': 'exp', 'left': left, 'op': op, 'right': right}
            
        return left
        
    def simple_exp(self):
        """
        simple_exp -> term {addop term}
        """
        left = self.term()
        
        while self.current_token and self.current_token[1] in ['PLUS', 'MINUS']:
            op = self.current_token
            if op[1] == 'PLUS':
                self.match('PLUS')
            else:
                self.match('MINUS')
                
            right = self.term()
            left = {'type': 'simple_exp', 'left': left, 'op': op, 'right': right}
            
        return left
        
    def term(self):
        """
        term -> factor {mulop factor}
        """
        left = self.factor()
        
        while self.current_token and self.current_token[1] in ['MULT', 'DIV']:
            op = self.current_token
            if op[1] == 'MULT':
                self.match('MULT')
            else:
                self.match('DIV')
                
            right = self.factor()
            left = {'type': 'term', 'left': left, 'op': op, 'right': right}
            
        return left
        
    def factor(self):
        """
        factor -> (exp) | number | identifier
        """
        if not self.current_token:
            raise Exception("Unexpected end of input")
            
        token_value, token_type = self.current_token
        
        if token_type == 'OPENBRACKET':
            self.match('OPENBRACKET')
            exp_value = self.exp()
            self.match('CLOSEDBRACKET')
            return {'type': 'factor', 'value': exp_value}
        elif token_type == 'NUMBER':
            return {'type': 'factor', 'value': self.match('NUMBER')}
        elif token_type == 'IDENTIFIER':
            return {'type': 'factor', 'value': self.match('IDENTIFIER')}
        else:
            raise Exception(f"Unexpected token: {token_value}, {token_type}")

    def parse_file(self, token_filename):
        """
        Parse a file containing tokens in the format: token_value,token_type
        """
        tokens = []
        with open(token_filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    token_value, token_type = line.split(',')
                    tokens.append((token_value, token_type))
        return self.parse(tokens)

# Example usage
if __name__ == "__main__":
    from scanner import Scanner
    
    scanner = Scanner()
    parser = Parser()
    
    # Example from string
    sample_code = "read x; if x < 0 then x := 0 end; write x"
    tokens = scanner.scan(sample_code)
    
    print("Tokens:")
    for token in tokens:
        print(f"{token[0]},{token[1]}")
    
    success, result = parser.parse(tokens)
    
    if success:
        print("\nParsing successful!")
        print("Syntax tree:")
        print(result)
    else:
        print(f"\nParsing failed: {result}") 