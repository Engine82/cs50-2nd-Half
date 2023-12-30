import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.tx")
        return 1

    # TODO: Read database file into a variable
    database = []
    with open(sys.argv[1]) as file:
        database_reader = csv.DictReader(file)
        for name in database_reader:
            database.append(name)

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2]) as file:
        txtsequence = file.read()

    # TODO: Find longest match of each STR in DNA sequence
    subsequences = list(database[0].keys())
    subsequences.pop(0)

    results = {}
    for i in subsequences:
        results[i] = longest_match(txtsequence, i)


    # TODO: Check database for matching profiles
    # Loop through each person in the database
    for person in database:
        person_counter = 0
        # Loop through each STR (which each person has)
        for subsequence in subsequences:
            # If the person's STR count is the same as the test's STR count
            if int(person[subsequence]) == results[subsequence]:
                # Add to person counter
                person_counter += 1
        # If all of the person's STR's match the sample
        if person_counter == len(subsequences):
            # Print that person's name
            print(person["name"])
            return 0

    # If none of the peopne in the database match the sequence
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
