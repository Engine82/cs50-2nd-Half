# TODO
from cs50 import get_string


def main():
    text = get_string("Text: ")

    # Calculate number of letters, words and sentences
    # Words starts as 1 because we know there is at least one word entered,
    # and there will be one less space between words than there are words.
    letters = 0
    words = 1
    sentences = 0

    # Iterate through each char and add to appropriate counter
    punctuation = ['.', '!', '?']
    for char in text:
        if char.isalpha() == True:
            letters += 1
        elif char.isspace() == True:
            words += 1
        elif char in punctuation:
            sentences += 1

    # Perform Coleman-Liau calculation
    L = letters / words * 100
    S = sentences / words * 100
    index = 0.0588 * L - 0.296 * S - 15.8
    final = round(index)

    # Print result
    if final < 1:
        print("Before Grade 1")

    elif final >= 1 and final < 16:
        print(f"Grade {final}")

    elif final >= 16:
        print("Grade 16+")


main()