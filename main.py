from lexer import run_lexer

if __name__ == "__main__":
    
    example_1 = "examples/example_01_variables.txt"
    example_2 = "examples/example_02_comparison.txt"
    
    output_lexer = run_lexer(example_2)
    
    for token in output_lexer:
        print(token)