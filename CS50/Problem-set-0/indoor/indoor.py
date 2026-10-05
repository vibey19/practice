def takeInput():
    userInput = input("Enter a message/string: ")
    return userInput
    
def toLowerCase(userInput):
    lower_case_string = userInput.lower()
    print(lower_case_string)
    
inp = takeInput()
toLowerCase(inp)