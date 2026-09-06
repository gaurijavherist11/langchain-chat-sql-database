import sqlite3

# Create a database and connect
connection = sqlite3.connect("ecommerce.db")

# Create a cursor object
cursor = connection.cursor()


# Create the CUSTOMERS table

table_info = """
CREATE TABLE CUSTOMERS(
    CUSTOMER_ID INT,
    FIRST_NAME VARCHAR(50),
    LAST_NAME VARCHAR(50),
    EMAIL VARCHAR(100),
    PHONE VARCHAR(20),
    CITY VARCHAR(50),
    STATE VARCHAR(50),
    REGISTRATION_DATE DATE
)
"""

cursor.execute(table_info)


# Insert records into CUSTOMERS table

cursor.execute("""INSERT INTO CUSTOMERS VALUES
(1, 'Gauri', 'Javheri', 'gauri@gmail.com', '9876543210', 'Mumbai', 'Maharashtra', '2025-01-10')""")

cursor.execute("""INSERT INTO CUSTOMERS VALUES
(2, 'Rahul', 'Sharma', 'rahul@gmail.com', '9876543211', 'Pune', 'Maharashtra', '2025-02-15')""")

cursor.execute("""INSERT INTO CUSTOMERS VALUES
(3, 'Priya', 'Patil', 'priya@gmail.com', '9876543212', 'Thane', 'Maharashtra', '2025-03-20')""")

cursor.execute("""INSERT INTO CUSTOMERS VALUES
(4, 'Amit', 'Verma', 'amit@gmail.com', '9876543213', 'Delhi', 'Delhi', '2025-04-05')""")

cursor.execute("""INSERT INTO CUSTOMERS VALUES
(5, 'Sneha', 'Kulkarni', 'sneha@gmail.com', '9876543214', 'Nashik', 'Maharashtra', '2025-05-12')""")


# Display all the records

print("The inserted records are")

data = cursor.execute("""SELECT * FROM CUSTOMERS""")

for row in data:
    print(row)


# Commit changes in the database

connection.commit()


# Close the database connection

connection.close()