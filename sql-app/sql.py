import sqlite3

def create_connection(db_name="college.db"):
    """
    Create a connection to the SQLite database.
    """
    try:
        connection = sqlite3.connect(db_name)
        return connection
    except sqlite3.Error as e:
        print(f"Error creating connection to database: {e}")
        return None

def create_table(cursor):
    """
    Create the COLLEGES table if it doesn't exist.
    """
    table_info = """
    CREATE TABLE IF NOT EXISTS COLLEGES (
        name TEXT NOT NULL,
        courses TEXT NOT NULL,
        rating REAL NOT NULL,
        fee INTEGER NOT NULL,
        UNIQUE(name, courses)  -- Ensures no duplicate entries for the same college with identical courses
    );
    """
    try:
        cursor.execute(table_info)
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

def insert_records(cursor, records):
    """
    Insert records into the COLLEGES table if they do not already exist.
    """
    try:
        cursor.executemany("""
            INSERT OR IGNORE INTO COLLEGES (name, courses, rating, fee) 
            VALUES (?, ?, ?, ?)
        """, records)
    except sqlite3.Error as e:
        print(f"Error inserting records: {e}")

def fetch_data(cursor):
    """
    Fetch all data from the COLLEGES table.
    """
    try:
        cursor.execute("SELECT * FROM COLLEGES")
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Error fetching data: {e}")
        return []

def main():
    # Establish a connection to the SQLite database
    connection = create_connection()

    if connection is None:
        return  # Exit if connection failed

    cursor = connection.cursor()

    # Create the COLLEGES table
    create_table(cursor)

    # Records to be inserted into the COLLEGES table
    records = [
        ('Tech University', 'BTech: Computer Science, Electrical Engineering; Diploma: Mechanical Engineering, Civil Engineering', 4.5, 30000),
        ('Future Tech Institute', 'BTech: Information Technology, Mechanical Engineering; Diploma: Electrical Engineering, Computer Engineering', 4.3, 28000),
        ('Apex College of Engineering', 'BTech: Civil Engineering, Electronics and Communication; Diploma: Mechanical Engineering, Civil Engineering', 4.1, 25000),
        ('Innovate Institute of Technology', 'BTech: Computer Engineering, Electrical and Electronics; Diploma: Electronics Engineering, Mechanical Engineering', 4.4, 32000),
        ('Elite Tech Academy', 'BTech: Software Engineering, Chemical Engineering; Diploma: Chemical Engineering, Electrical Engineering', 4.6, 35000),
        ('CMR Institute of Technology', 'All courses', 4.9, 1000000),
        ('Global Tech College', 'BTech: IT, Mechanical Engineering; Diploma: Electronics, Civil Engineering', 4.2, 29000),
        ('Premier Engineering College', 'BTech: Civil Engineering, Computer Science; Diploma: Mechanical Engineering, Electrical Engineering', 4.0, 27000),
        ('Advanced Tech University', 'BTech: Chemical Engineering, Information Systems; Diploma: Software Development, Network Security', 4.7, 34000),
        ('Innovative College of Engineering', 'BTech: Electrical Engineering, Aerospace Engineering; Diploma: Chemical Engineering, Civil Engineering', 4.3, 31000),
        ('Techno World Institute', 'BTech: Mechanical Engineering, Robotics; Diploma: IT, Mechanical Engineering', 4.4, 33000)
    ]

    # Insert records into the COLLEGES table
    insert_records(cursor, records)

    # Commit the transaction to save changes
    connection.commit()

    # Fetch and display all data from the COLLEGES table
    rows = fetch_data(cursor)

    # Print the fetched rows
    if rows:
        print("COLLEGES Table Data:")
        for row in rows:
            print(row)
    else:
        print("No data found in the COLLEGES table.")

    # Close the connection
    connection.close()

if __name__ == "__main__":
    main()
