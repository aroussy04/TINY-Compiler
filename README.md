# TINY Compiler

A complete compiler front-end for the TINY programming language, featuring a scanner (lexical analyzer), parser (syntax analyzer), syntax tree visualizer, and a graphical user interface.

## Features

- **Scanner (Lexical Analyzer)**: Tokenizes TINY source code into a list of tokens
- **Parser (Syntax Analyzer)**: Performs syntactic analysis on the token stream and builds a syntax tree
- **Syntax Tree Visualizer**: Visually displays the parsed syntax tree
- **GUI Application**: Windows-compatible application with an intuitive interface

## Installation

### Requirements

- Python 3.6 or higher
- Required Python packages:
  - networkx
  - matplotlib
  - pillow (PIL)

### Setup

1. Clone or download this repository
2. Install the required packages:
   ```
   pip install networkx matplotlib pillow
   ```
3. Run the application:
   ```
   python main.py
   ```

### Building Executable

To build a standalone Windows executable (.exe) file, see the instructions in `build_instructions.md`.

## TINY Language Specification

### Tokens

| Token Type | Example |
|------------|---------|
| SEMICOLON | ; |
| IF | if |
| THEN | then |
| END | end |
| REPEAT | repeat |
| UNTIL | until |
| IDENTIFIER | x, abc, xyz |
| ASSIGN | := |
| READ | read |
| WRITE | write |
| LESSTHAN | < |
| EQUAL | = |
| PLUS | + |
| MINUS | - |
| MULT | * |
| DIV | / |
| OPENBRACKET | ( |
| CLOSEDBRACKET | ) |
| NUMBER | 12, 289 |

### Grammar

```
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
```

## Usage

1. Launch the application using `python main.py`
2. Enter TINY code directly in the text box or load a .tiny file
3. Click "Compile" to process the code
4. View the resulting tokens and syntax tree in their respective tabs

## Example Programs

Sample TINY programs are provided in the `examples` directory:

- `factorial.tiny`: Calculates the factorial of a number
- `sum.tiny`: Calculates the sum from 1 to n

## Project Structure

- `scanner.py`: Implementation of the lexical analyzer
- `parser.py`: Implementation of the syntax analyzer
- `visualizer.py`: Implementation of the syntax tree visualizer
- `gui.py`: Implementation of the graphical user interface
- `main.py`: Main entry point for the application
- `examples/`: Directory containing example TINY programs

## License

This project is released as open-source software. 