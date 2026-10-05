def greetinChecker(greeting):
    greeting = greeting.lower().strip()
    if greeting.startswith("hello"):
        return '$0'
    elif greeting.startswith("h"):
        return '$20'
    else:
        return '$100'
    
def main():
    greeting = input("Greeting: ")
    fine = greetinChecker(greeting)
    print(fine)
    
main()