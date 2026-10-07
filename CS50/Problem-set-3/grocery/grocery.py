def main():
    grocery_list = {}

    while True:
        try:
            item = input().lower()

            if item in grocery_list:
                grocery_list[item] += 1
            else:
                grocery_list[item] = 1

        except EOFError:
            break

    for item in sorted(grocery_list):
        print(grocery_list[item], item.upper())


if __name__ == "__main__":
    main()