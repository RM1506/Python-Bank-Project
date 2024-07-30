import mysql.connector as sql

# Connect to the database
mydb = sql.connect(
    host="localhost",
    user="root",
    passwd="1506@Rishu",
    database="bank"
)

cursor = mydb.cursor()

def db_query(query):
    """Execute a SQL query and return the results."""
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except sql.Error as err:
        print(f"Error: {err}")
        return None

def createcustomertable():
    """Create the 'customers' table if it does not exist."""
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                username VARCHAR(20) NOT NULL,
                password VARCHAR(20) NOT NULL,
                name VARCHAR(20) NOT NULL,
                age INTEGER NOT NULL,
                city VARCHAR(20) NOT NULL,
                balance INTEGER NOT NULL,
                account_number INTEGER NOT NULL,
                status BOOLEAN NOT NULL
            )
        ''')
        # Commit changes after table creation
        mydb.commit()
        print("Table 'customers' created or already exists.")
    except sql.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    createcustomertable()
    cursor.close()
    mydb.close()
