from lexer import run_lexer

if __name__ == "__main__":
    
    example_1 = "examples/example_01_variables.txt"
    example_2 = "examples/example_02_comparison.txt"
    example_3 = "examples/example_03_functions.txt"
    
    output_lexer = run_lexer(example_3)
    
    for token in output_lexer:
        print(token)