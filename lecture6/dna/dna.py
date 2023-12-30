import csv
import sys


def main():

    # TODO: Check for command-line usage
    # Self-explanatory
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.tx")
        return 1

    # TODO: Read database file into a variable
    # Create database variable
    database = []

    # Read database into opened variable as dict
    with open(sys.argv[1]) as file:
        database_reader = csv.DictReader(file)
        for name in database_reader:
            database.append(name)

    # TODO: Read DNA sequence file into a variable
    # Self-explanatory
    with open(sys.argv[2]) as file:
        DNAsequence = file.read()

    # TODO: Find longest match of each STR in DNA sequence
    # Create a list of just the subsequences from the database, and remove the header
    subsequences = list(database[0].keys())
    subsequences.pop(0)

    # Create a dict to store the results. Loop through each STR and find the longest number of repeats
    results = {}
    for str in subsequences:
        results[str] = longest_match(DNAsequence, str)

    # TODO: Check database for matching profiles
    # Loop through each person, and create a counter for that person to count STR matches
    for person in database:
        counter = len(subsequences)

        # Loop through each STR and check for match; if match, decrease counter 1
        for str in subsequences:
            if results[str] == int(person[str]):
                counter -= 1
                # If all STRs match, print person's name and return 0
                if counter == 0:
                    print(person["name"])
                    return 0

    # If none matched, print no match, return 0
    print("No match")
    return 0


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
