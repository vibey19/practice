def calculate(expression):
    expression = expression.split()
    
    x = int(expression[0])
    y = expression[1]
    z = int(expression[2])
    
    if y == '+':
        return x+z
    elif y == '-':
        return x-z
    elif y == '*':
        return x*z
    elif y == '/':
        if z != 0:
            return x/z    
    return 'Enter Valid Expression'

def main():
    expression = input("Enter the expression: ")
    result = calculate(expression)
    print(float(result))
    
    
main()