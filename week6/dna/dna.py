import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py FILENAME(database) FILENAME(sequence)")

    # Read database file into a variable
    database_file = sys.argv[1]

    # Read the STRs from the db into a list. We now have a list of the STRs
    # we need to check for in the sequence file.
    with open(database_file, "r") as f:
        str_list = next(f).strip().split(',')
        str_list.remove('name')

    # Initialize a list to read the contents of the database as dicts. Each
    # item in the list represents a person's name and identifying STRs.
    db_list = []
    # Read the db data into the list, as dicts.
    with open(database_file, "r") as f:
        db_reader = csv.DictReader(f)
        for row in db_reader:
            db_list.append(row)

    # Read DNA sequence file into a variable.
    sequence_file = sys.argv[2]
    with open(sequence_file, "r") as f:
        sequence = f.read()

    # Find longest match of each STR in DNA sequence

    # Initialize a dict to store the returned "longest run" of STRs.
    # Each item will be a "STR: longest run" key/value pair.
    str_lr = {}

    # Run function to return the longest run of each STR in the sequence.
    for short_t_r in str_list:
        lr = longest_match(sequence, short_t_r)
        # Store the longest run in the dict at the corresponding key.
        str_lr[short_t_r] = lr

    # Check database for matching profiles

    # Set `match`, the variable we'll use to print our final result,
    # to "No match" by default. If a match is found later, this variable
    # will be updated.
    match = "No match"

    for person in db_list:
        matches = 0
        for key, value in str_lr.items():
            if int(person[key]) == value:
                matches += 1
            # If the number of matches is equal to the number of STRs in the
            # database, update `match` to the person in the current loop.
            if matches == len(str_list):
                match = person["name"]

    print(match)

    return


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
