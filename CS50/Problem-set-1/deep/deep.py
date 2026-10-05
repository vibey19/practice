def checkIfAnswerExists(inputString):
    inputString = inputString.lower()
    if '42' in inputString:
        return 'Yes'
    elif 'forty-two' in inputString:
        return 'Yes'
    elif 'forty two' in inputString:
        return 'Yes'
    else:
        return 'No'
    
def main():
    inputString = input("What is the Answer to the Great Question of Life, the Universe, and Everything?: ")
    answer = checkIfAnswerExists(inputString)
    print(answer)
    
main()