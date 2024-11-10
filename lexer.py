### Main function
def run_lexer(file_path: str) -> list:

    with open(file_path, "r") as file_content:
        buffer = file_content.read()

    # inizialize lexer variables
    token_list = []
    lexer = {
        "buffer" : buffer,
        "buffer_lenght" : len(buffer),
        "read_pos" : 1,
        "current_pos" : 0,
        "current_char" : buffer[0]
    }
    token = ("START")
    while token[0] != "EOF":
        token = advance_to_next_token(lexer)
        token_list.append(token)

    return token_list


### Main components
def advance_to_next_token(lexer: dict) -> tuple[str, str|None, int]:
    token_position = lexer["current_pos"]
    char = lexer["current_char"]

    if char == "\0":
        read_char(lexer)
        return ("EOF", None, token_position)
    elif char == "\n":
        read_char(lexer)
        return ("EOL", None, token_position)
    elif char == " ":
        read_char(lexer)
        return ("SPACE", None, token_position)
    elif char == ":":
        read_char(lexer)
        return ("COLON", None, token_position)
    # brackets
    elif char == "(":
        read_char(lexer)
        return ("L_BRACKET", None, token_position)
    elif char == ")":
        read_char(lexer)
        return ("L_BRACKET", None, token_position)
    elif char == "[":
        read_char(lexer)
        return ("L_S_BRACKET", None, token_position)
    elif char == "]":
        read_char(lexer)
        return ("R_S_BRACKET", None, token_position)
    elif char == "{":
        read_char(lexer)
        return ("L_C_BRACKET", None, token_position)
    elif char == "}":
        read_char(lexer)
        return ("R_C_BRACKET", None, token_position)
    # arithmetic operators
    elif char == "+":
        next_char = peek_char(lexer)
        if next_char == "+":
            read_char(lexer)
            read_char(lexer)
            return ("AUTO_INCREMENT", None, token_position)
        else:
            read_char(lexer)
            return ("PLUS", None, token_position)
    elif char == "-":
        next_char = peek_char(lexer)
        if next_char == "-":
            read_char(lexer)
            read_char(lexer)
            return ("AUTO_DECREMENT", None, token_position)
        elif next_char == ">":
            read_char(lexer)
            read_char(lexer)
            return ("ARROW", None, token_position)
        else:
            read_char(lexer)
            return ("MINUS", None, token_position)
    elif char == "*":
        next_char = peek_char(lexer)
        if next_char == "*":
            read_char(lexer)
            read_char(lexer)
            return ("EXPONENTATION", None, token_position)
        else:
            read_char(lexer)
            return ("MULTIPLICATION", None, token_position)
    elif char == "/":
        next_char = peek_char(lexer)
        if next_char == "/":
            read_char(lexer)
            read_char(lexer)
            return ("FLOOR_DIVISION", None, token_position)
        else:
            read_char(lexer)
            return ("DIVISION", None, token_position)
    elif char == "%":
        read_char(lexer)
        return ("MODULUS", None, token_position)
    # comparison operators  
    elif char == "=":
        next_char = peek_char(lexer)
        if next_char == "=":
            read_char(lexer)
            read_char(lexer)
            return ("EQUAL", None, token_position)
        else:
            read_char(lexer)
            return ("ASSIGN", None, token_position)
    elif char == "<":
        next_char = peek_char(lexer)
        if next_char == "=":
            read_char(lexer)
            read_char(lexer)
            return ("LESS_THAN_EQUAL", None, token_position)
        else:
            read_char(lexer)
            return ("LESS_THAN", None, token_position)
    elif char == ">":
        next_char = peek_char(lexer)
        if next_char == "=":
            read_char(lexer)
            read_char(lexer)
            return ("MORE_THAN_EQUAL", None, token_position)
        else:
            read_char(lexer)
            return ("MORE_THAN", None, token_position)
    # parse identifiers and keywords
    elif is_letter(char):
        slice_lenght = 0
        while is_valid_char(char):
            slice_lenght += 1
            char = read_char(lexer)
        literal = lexer["buffer"][token_position : token_position + slice_lenght]
        return literal_to_token(literal, token_position)
    # parse numbers
    elif is_digit(char):
        slice_lenght = 0
        while (is_digit(char)) or (char == "."):
            slice_lenght += 1
            char = read_char(lexer)
        literal = lexer["buffer"][token_position : token_position + slice_lenght]
        return ("NUMBER_LITERAL", literal, token_position)
    # parse strings
    elif char == '"':
        return string_to_token(lexer)
    else:
        read_char(lexer)
        return ("ILLEGAL", None, token_position)

# Keywords
def literal_to_token(literal: str, token_position: int) -> tuple[str, str, int]:
    if literal == "int":
        return ("INT", None, token_position)
    elif literal == "float":
        return ("FLOAT", None, token_position)
    elif literal == "double":
        return ("DOUBLE", None, token_position)
    elif literal == "if":
        return ("IF", None, token_position)
    elif literal == "elif":
        return ("ELIF", None, token_position)
    elif literal == "else":
        return ("ELSE", None, token_position)
    elif literal == "and":
        return ("AND", None, token_position)
    elif literal == "or":
        return ("OR", None, token_position)
    elif literal == "continue":
        return ("CONTINUE", None, token_position)
    else:
        return ("IDENTIFIER", literal, token_position)

def string_to_token(lexer: dict) -> tuple[str, str, int]:
    token_position = lexer["current_pos"]
    read_char(lexer)
    literal = []
    while lexer["current_char"] != '"':
        char = lexer["current_char"]
        literal.append(char)
        read_char(lexer)
    read_char(lexer)
    return ("STRING_LITERAL", "".join(literal), token_position)

### Lexer movement        
def peek_char(lexer: dict) -> str:
    if lexer["read_pos"] >= lexer["buffer_lenght"]:
        return "\0"
    return lexer["buffer"][lexer["read_pos"]]

def read_char(lexer: dict) -> str:
    lexer["current_char"] = peek_char(lexer)
    lexer["current_pos"] = lexer["read_pos"]
    lexer["read_pos"] += 1
    return lexer["current_char"]
    
def skip_until_space(lexer: dict) -> None:
    while lexer["current_char"] != " " and lexer["current_char"] != "EOF":
        read_char(lexer)
        
def skip_until_newline(lexer: dict) -> None:
    while lexer["current_char"] != "\n" and lexer["current_char"] != "EOF":
        read_char(lexer)
        
### Char utils for building literals
def is_letter(char: str) -> bool:
    return ('a' <= char and char <= 'z') or ('A' <= char and char <= 'Z')

def is_digit(char: str) -> bool:
    return '0' <= char and char <= '9'

def is_new_line(char: str) -> bool:
    return char == '\n'

def is_space(char: str) -> bool:
    return char == ' '

def is_whitespace(char: str) -> bool:
    return char == '\t' or char == "\r"

def is_valid_char(char: str) -> bool:
    return is_letter(char) or is_digit(char) or (char == "_")
