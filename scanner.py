import re

# Token definitions
TOKEN_TYPES = {
    # Reserved words
    'if': 'IF',
    'then': 'THEN',
    'end': 'END',
    'repeat': 'REPEAT',
    'until': 'UNTIL',
    'read': 'READ',
    'write': 'WRITE',
    
    # Special symbols
    ';': 'SEMICOLON',
    ':=': 'ASSIGN',
    '<': 'LESSTHAN',
    '=': 'EQUAL',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MULT',
    '/': 'DIV',
    '(': 'OPENBRACKET',
    ')': 'CLOSEDBRACKET',
}

class Scanner:
    def __init__(self):
        self.tokens = []
        
    def scan(self, code):
        """
        Scan the input code and return a list of tokens.
        Each token is a tuple (token_value, token_type).
        """
        self.tokens = []
        position = 0
        
        while position < len(code):
            # Skip whitespace
            if code[position].isspace():
                position += 1
                continue
                
            # Check for identifiers (starts with letter, followed by letters or digits)
            identifier_match = re.match(r'[a-zA-Z][a-zA-Z0-9]*', code[position:])
            if identifier_match:
                value = identifier_match.group(0)
                # Check if it's a reserved word
                if value.lower() in TOKEN_TYPES:
                    token_type = TOKEN_TYPES[value.lower()]
                else:
                    token_type = 'IDENTIFIER'
                self.tokens.append((value, token_type))
                position += len(value)
                continue
                
            # Check for numbers
            number_match = re.match(r'\d+', code[position:])
            if number_match:
                value = number_match.group(0)
                self.tokens.append((value, 'NUMBER'))
                position += len(value)
                continue
                
            # Check for assignment operator (:=)
            if position + 1 < len(code) and code[position:position+2] == ':=':
                self.tokens.append((':=', 'ASSIGN'))
                position += 2
                continue
                
            # Check for other special symbols
            if code[position] in TOKEN_TYPES:
                self.tokens.append((code[position], TOKEN_TYPES[code[position]]))
                position += 1
                continue
                
            # If we get here, we have an unrecognized token
            raise Exception(f"Unrecognized token at position {position}: '{code[position]}'")
            
        return self.tokens
    
    def scan_file(self, filename):
        """
        Scan a file containing TINY code and return a list of tokens.
        """
        with open(filename, 'r') as file:
            code = file.read()
        return self.scan(code)
    
    def save_tokens_to_file(self, tokens, filename):
        """
        Save the tokens to a file in the format: token_value,token_type
        """
        with open(filename, 'w') as file:
            for token_value, token_type in tokens:
                file.write(f"{token_value},{token_type}\n")

# Example usage
if __name__ == "__main__":
    scanner = Scanner()
    
    # Example from string
    sample_code = "read x; if x < 0 then x := 0 end; write x"
    tokens = scanner.scan(sample_code)
    print("Tokens:")
    for token in tokens:
        print(f"{token[0]},{token[1]}") 