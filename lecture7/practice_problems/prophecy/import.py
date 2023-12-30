import csv
import sys
from cs50 import SQL



db = SQL("sqlite:///roster.db")

# Open students.csv and read in.
with open(sys.argv[1]) as file:
    reader = csv.DictReader(file)

    # Create variables for house assignments
    
    # Loop through students in CSV
    for student in reader:

        # Add student name into db
        db.execute("INSERT INTO students_new (student_name) VALUES (student_name)")

        # Check if house is already in houses. If not, add house and head.
        houses = db.execute("SELECT * FROM houses (house))
        if student["house"] not in houses:
            db.execute("INSERT INTO houses (house) FROM ?", student["house"])
            db.execute("INSERT INTO houses (head) FROM ?", student["head"])

        # Associate student with proper house and head
