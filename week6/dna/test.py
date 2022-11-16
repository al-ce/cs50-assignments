import csv
import sys



# TODO: Read database file into a variable
database = "databases/small.csv"

sequences_list = []
with open(database, "r") as f:
    header = next(f).strip().split(',')
    header.remove('name')
print(header)

# Initialize a dictionary for database data.
db_list = []
with open(database, "r") as f:
    d_reader = csv.DictReader(f)
    for row in d_reader:
        db_list.append(row)


print(db_list)

# sequence_file = "sequences/1.txt"
# with open(sequence_file, "r") as f:
#     sequence = f.read()


