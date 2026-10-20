import sqlite3

def get_user_info(id):
    """
    Safely retrieves user information from the database using parameterized queries.
    """
    try:
        # Establish connection to the database
        connection = sqlite3.connect('users_database.db')
        cursor = connection.cursor()

        # DEFENSE: Use Parameterized Queries
        # We use a '?' as a placeholder. The database engine will treat 
        # the user input strictly as data, never as executable SQL code.
        query = "SELECT first_name, last_name FROM users WHERE id = ?"
        
        # Execution: Pass the input as a separate tuple
        # This completely prevents SQL injection even if id 
        # contains malicious commands like '1 OR 1=1'
        cursor.execute(query, (id,))
        
        results = cursor.fetchall()

        if results:
            for row in results:
                print(f"ID: {id}")
                print(f"First Name: {row[0]}")
                print(f"Surname: {row[1]}")
        else:
            print("No user found with that ID.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if connection:
            connection.close()

