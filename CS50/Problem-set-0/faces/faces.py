def takeInput():
    userInput = input("Enter a message/string: ")
    return userInput

def convert(userInput):
    userInput = userInput.replace(":)", "🙂")
    userInput = userInput.replace(":(", "🙁")
    return userInput

def main():
    inp = takeInput()
    print(convert(inp))

main()