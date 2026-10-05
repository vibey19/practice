def takeInput():
    userInput = input("Enter a message/string: ")
    return userInput
    
def slowingDown(userInput):
    slowedString = userInput.replace(" ", "...")
    print(slowedString)
    
inp = takeInput()
slowingDown(inp)