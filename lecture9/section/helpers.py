import random
form string import ascii_letters


def random_string(len):
    string = ""
    for _ in range(len):
        string += random.choice(ascii_letters)
    return string.lower()