import pymysql

# Connect to the RDS MySQL database
connection = pymysql.connect(
    host='database-1.cobgmm6euz11.us-east-1.rds.amazonaws.com',  # Replace with your RDS endpoint
    user='jyothi',      # Replace with your RDS username
    password='Janu123456789',  # Replace with your RDS password
    database='blogs',  # Replace with your RDS database name
    port=3306                  # Default MySQL port
)

# Execute the schema.sql file to create the database schema
with open('schema.sql') as f:
    schema = f.read()  # Read the contents of the schema.sql file
    with connection.cursor() as cursor:
        for statement in schema.split(';'):  # Split the file into individual SQL statements
            if statement.strip():  # Skip empty statements
                cursor.execute(statement)  # Execute each statement

# Insert initial data into the posts table
cur = connection.cursor()

try:
    cur.execute("SELECT 1 FROM posts LIMIT 1;")  # Check if the table exists
except pymysql.MySQLError:
    print("Table 'posts' does not exist. Please create it first.")
    exit()

cur.execute("INSERT INTO posts (title, content) VALUES (%s, %s)",
            ('First Post', 'Content for the first post'))

cur.execute("INSERT INTO posts (title, content) VALUES (%s, %s)",
            ('Second Post', 'Content for the second post'))

connection.commit()  # Commit the changes to the database
connection.close()  # Close the connection