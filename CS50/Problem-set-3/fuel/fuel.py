def convert(fract):
    try:
        x, y = fract.split("/")
        x, y = int(x), int(y)

        if x > y or x < 0 or y == 0:
            return None

        return (x / y) * 100

    except ValueError:
        return None

    except ZeroDivisionError:
        return None


def main():
    while True:
        fract = input("Input Fraction: ")
        percentage = convert(fract)

        if percentage is None:
            continue

        break

    if percentage <= 1:
        print("E")

    elif percentage >= 99:
        print("F")

    else:
        print(f"{round(percentage)}%")


if __name__ == "__main__":
    main()