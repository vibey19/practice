def extensionChecker(filename):
    filename = filename.lower().strip()
    
    if filename.endswith(".gif"):
            return 'image/gif'
    elif filename.endswith(".jpg"):
            return 'image/jpeg'
    elif filename.endswith(".jpeg"):
            return 'image/jpeg'
    elif filename.endswith(".png"):
            return 'image/png'
    elif filename.endswith(".pdf"):
        return 'application/pdf'
    elif filename.endswith(".txt"):
        return 'text/plain'
    elif filename.endswith(".zip"):
        return 'application/zip'
    else:
        return 'application/octet-stream'
    
def main():
    filename = input("Enter a filename: ")
    extensionType = extensionChecker(filename)
    print(extensionType)
    
main()