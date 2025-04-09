import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

# Name for the setup_logger
logger = setup_logger('db_helper')

###-----------------------------  CRUD OPERATIONS ----------------###

# Context manager for database connection
@contextmanager
# Database Configuration Function
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    print("Closing cursor")
    cursor.close()
    connection.close()

# Create a new expense in a database (C)
def insert_expense(expense_date, amount, category, notes):
    logger.info(f"Insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )

# Read all expenses from database (R)
def fetch_all_records():
    query = "SELECT * from expenses"

    with get_db_cursor() as cursor:
        logger.info(f"fetch_expenses_for_date called with {expense_date}")
        cursor.execute(query)
        expenses = cursor.fetchall()
        for expense in expenses:
            print(expense)


# Read all the expenses of the exact date (R)
def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall() # This should return a list of tuples or dictionaries
        return expenses

# Function for deleting an existing expenses of exact date in a database (D)
def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "DELETE FROM expenses WHERE expense_date = %s",
            (expense_date,)
        )

#Function for expense summary
def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total 
               FROM expenses WHERE expense_date
               BETWEEN %s and %s
               group by category;''',
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data



if __name__ == "__main__":

    #Checking all the expenses of the exact date (R)
    expenses = fetch_expenses_for_date("2024-09-30")
    print(expenses)

    #Adding a new expense in a database (C)
    #insert_expense("2024-08-25", 40, "Food", "Eat tasty pizza")
    #new_expense = fetch_expenses_for_date("2024-08-25")
    #print(new_expense)

    #Update existing expense in a database (U)
    #update_expenses_for_date("2024-08-25", 150, "Food", "Went for a dinner with friends", 69)
    #updated_expense = fetch_expenses_for_date("2024-08-25")
    #print(updated_expense)

    #Deleting all the expenses of the exact date
    #delete_expenses_for_date("2024-08-25")
    #fetch_expenses_for_date("2024-08-25")

    #Expense Summary
    summary = fetch_expense_summary("2024-08-01", "2024-08-25")
    for record in summary:
        print(record)