# TODO
from cs50 import get_float

# prompt user for amount of change
while True:
    dollars = get_float("Change owed: ")
    if dollars > 0.00:
        break

# Convert dollars (from input) into cents
cents = dollars * 100

# Calculate number of quarters
quarters = int(cents / 25)
cents = cents - quarters * 25

# Calculate number of dimes
dimes = int(cents / 10)
cents = cents - dimes * 10

# Calculate number of nickels
nickels = int(cents / 5)
cents = cents - nickels * 5

# Calculate number of pennies (really just convert to an int so
# that the final output is a whole number instead of "0.00")
pennies = int(cents / 1)

# Add up total number of coins and display
coins = quarters + dimes + nickels + pennies
print(f"{coins}")