import csv

books = []

# Add books to your shelf by reading from books.csv
with open("books.csv") as file:
    file_reader = csv.reader(file)
    for row in file_reader:
        print(row[0])