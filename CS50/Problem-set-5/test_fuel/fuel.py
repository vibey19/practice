def convert(fraction):
    x, y = fraction.split("/")
    x, y = int(x), int(y)

    if y == 0:
        raise ZeroDivisionError("denominator cannot be zero")

    if x < 0 or y < 0 or x > y:
        raise ValueError("fraction must be between 0 and 1")

    return round(x / y * 100)


def gauge(percentage):
    if percentage <= 1:
        return "E"
    elif percentage >= 99:
        return "F"
    else:
        return f"{percentage}%"


def main():
    while True:
        try:
            percentage = convert(input("Fraction: "))
        except (ValueError, ZeroDivisionError):
            pass
        else:
            break

    print(gauge(percentage))


if __name__ == "__main__":
    main()
