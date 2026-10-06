def convert_to_snake_case(var):
    snake_case = ''
    
    for char in var:
        if char.islower():
            snake_case += char
        elif char.isupper():
            snake_case += '_'
            snake_case += char.lower()
    return snake_case

def main():
    var = input("Enter the variable: ")
    snake_case = convert_to_snake_case(var)
    print(snake_case)
    
if __name__ == "__main__":
    main()