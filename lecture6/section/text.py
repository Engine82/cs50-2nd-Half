text = "In the great green room"
words = text.split()

# Round 1
print("Round 1")
for word in words:
    print(word)
print()

# In
# the
# great
# green
# room


# Round 2
print("Round 2")
for word in words:
    for c in word:
        print(c)
print()

# I
# n
# t
# h
# e
# .....
# ^no spaces once text is split


# Round 3
print("Round 3")
for word in words:
    if "g" in word:
        print(word)
print()

# great
# green


# Round 4
print("Round 4")
for word in words[2:]:
    print(word)
print()

# great
# green
# room

# Round 5
print("Round 5")
for _ in words:
    print("Goodnight Moon")
print()

# Goodnight moon
# Goodnight moon
# Goodnight moon
# Goodnight moon
# Goodnight moon