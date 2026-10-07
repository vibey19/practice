from pyfiglet import Figlet
import sys
import random


def main():
    figlet = Figlet()

    if len(sys.argv) != 1 and len(sys.argv) != 3:
        sys.exit("Invalid usage")

    if len(sys.argv) == 1:
        fonts = figlet.getFonts()
        font = random.choice(fonts)
        figlet.setFont(font=font)

    else:
        if sys.argv[1] != "-f" and sys.argv[1] != "--font":
            sys.exit("Invalid usage")

        fonts = figlet.getFonts()

        if sys.argv[2] not in fonts:
            sys.exit("Invalid usage")

        figlet.setFont(font=sys.argv[2])

    inp = input()

    print(figlet.renderText(inp))


if __name__ == "__main__":
    main()