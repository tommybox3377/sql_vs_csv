import csv
import sqlite3
from random import random, randint, choice
import timeit
import os

# Create a connection to the SQLite database
conn = sqlite3.connect('my_db.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table
create_table_query = '''
    CREATE TABLE IF NOT EXISTS science_stuff (
        id INTEGER PRIMARY KEY,
        group_id TEXT,
        sensor_id TEXT,
        v1 REAL,
        v2 REAL,
        v3 REAL,
        v4 REAL,
        v5 REAL,
        v6 REAL,
        v7 INTEGER,
        v8 INTEGER,
        v9 INTEGER
    )
'''

cursor.execute(create_table_query)

# Commit the changes and close the connection
conn.commit()
conn.close()


# Generate data
groups = ["ABC1", "ABC2", "XYZ1", "XYZ2"]
sensors = ["g1", "g2", "m1", "m2"]

data = [
    (
        i,
        choice(groups),
        choice(sensors),
        random() * 10,
        random() * 10,
        random() * 10,
        random() * 10,
        random() * 10,
        random() * 10,
        randint(0, int(1e10)),
        randint(0, int(1e10)),
        randint(0, int(1e10)),
    ) for i in range(1, 1000000)
]



conn = sqlite3.connect('my_db.db')
cursor = conn.cursor()

# Define the SQL statement for the insert operation
sql = "INSERT INTO science_stuff (id, group_id, sensor_id, v1, v2, v3, v4, v5, v6, v7, v8, v9) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

# Execute the insert statement
cursor.executemany(sql, data)

# Commit the changes to the database
conn.commit()

# Close the cursor and the database connection
cursor.close()
conn.close()


csv_file = 'my_csv.csv'

# Write the list of tuples to the CSV file
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
        "id", "group_id", "sensor_id", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9"
    ])
    writer.writerows(data)


# The database is more space efficient, will vary by data types, set up, etc... but in this case about half as large

sql_lite_file_size = os.path.getsize("my_db.db") / (1024 * 1024)
csv_file_size = os.path.getsize("my_csv.csv") / (1024 * 1024)

print(f"SQLite size: {sql_lite_file_size:.2f} MB")
print(f"CSV size: {csv_file_size:.2f} MB")


sql_code_snippet = """
import sqlite3

conn = sqlite3.connect('my_db.db')
cursor = conn.cursor()

# Define the SQL statement for the insert operation
sql = '''{sql}'''

# Fetch the data
cursor.execute(sql)
data = cursor.fetchall()

# Close the connection
cursor.close()
conn.close()"""

csv_code_snippet = """
import csv

csv_file = 'my_csv.csv'

data = []

# Open the CSV file for reading
with open(csv_file, 'r') as file:
    # Create a CSV reader object
    reader = csv.DictReader(file)

    # Iterate over each row in the CSV file
    for row in reader:
        {conditional}:
            data.append(row)"""



# Getting the data will also be faster

# We get all teh data that are in the group ABC1

execution_time = timeit.timeit(sql_code_snippet.format(sql="SELECT * FROM science_stuff WHERE group_id = 'ABC1';"), number=1)
print("SQL Execution time:", execution_time, "seconds")

execution_time = timeit.timeit(csv_code_snippet.format(conditional="if row['group_id'] == 'ABC1'"), number=1)
print("CSV Execution time:", execution_time, "seconds")


# Some searches will be even faster, such as where we get all the data from sensor g1 on group ABC1

execution_time = timeit.timeit(sql_code_snippet.format(sql="SELECT * FROM science_stuff WHERE group_id = 'ABC1' AND sensor_id = 'g1';"), number=1)
print("SQL Execution time:", execution_time, "seconds")

execution_time = timeit.timeit(csv_code_snippet.format(conditional="if row['group_id'] == 'ABC1' and row['sensor_id'] == 'g1'"), number=1)
print("CSV Execution time:", execution_time, "seconds")


# Other ones will be less so such as getting all the rows where the value of v3 is greater than 1

execution_time = timeit.timeit(sql_code_snippet.format(sql="SELECT * FROM science_stuff WHERE v3 > 1;"), number=1)
print("SQL Execution time:", execution_time, "seconds")

execution_time = timeit.timeit(csv_code_snippet.format(conditional="if float(row['v3']) > 1."), number=1)
print("CSV Execution time:", execution_time, "seconds")


# Some searches, the comparison isn't even fair

execution_time = timeit.timeit(sql_code_snippet.format(sql="SELECT * FROM science_stuff WHERE id = 42069;"), number=1)
print("SQL Execution time:", execution_time, "seconds")

execution_time = timeit.timeit(csv_code_snippet.format(conditional="if int(row['id']) == 1"), number=1)
print("CSV Execution time:", execution_time, "seconds")

