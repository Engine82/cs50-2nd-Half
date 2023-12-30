word = "Banana"

letters = ['a', 'b', 'c', 'd', 'e']
count = 0
for c in word:
    if c.isalpha() == True:
        count += 1
    print("cycle")

print(f"{count}")