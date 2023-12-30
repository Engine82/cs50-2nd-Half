# TODO

def main():
    # Get height from user until in range
    while True:
        try:
            height = int(input("Height: "))
            if 0 < height < 9:
                break
        except ValueError:
            print("Not an integer")

    # Loop until specified number of rows have been printed
    for i in range(height):

        # Print space
        print_spaces(height, i)

        # Print left blocks
        print_blocks(i + 1)

        # Print center space
        print("  ", end="")

        # Print right blocks
        print_blocks(i + 1)

        # Print newline
        print("", end="\n")


def print_spaces(width, i):
    spaces = 0
    while spaces < (width - i - 1):
        print(" ", end="")
        spaces += 1


def print_blocks(width):
    for blocks in range(width):
        print("#", end="")


main()