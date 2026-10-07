import emoji

def main():
    inp = input("Input: ").strip()
    print(emoji.emojize(inp, language='alias'))
    
    
if __name__ == "__main__":
    main()