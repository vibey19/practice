def shorten(input_string):
    short_string = ''
    
    for char in input_string:
        if char != 'a' and char != 'e' and char != 'i' and char != 'o' and char != 'u' and char != 'A' and char != 'E' and char != 'I' and char != 'O' and char != 'U': 
            short_string += char
    return short_string

def main():
    input_string = input("Enter your word/sentence: ")
    result = shorten(input_string)
    print(result)
    
if __name__ == "__main__":
    main()