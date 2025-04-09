from fastapi import FastAPI, HTTPException
from datetime import datetime, date
import db_helper
from typing import List
from pydantic import BaseModel

class Expense(BaseModel):
    #expense_date: date
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date

app = FastAPI()

#GET request
@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date: date):
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expenses from the database.")

    return expenses

#POST request
@app.post("/expenses/{expense_date}")
def add_or_update_expenses(expense_date: date, expenses:List[Expense]):
    db_helper.delete_expenses_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)
    return {"message": "Expenses updated successfully"}

# POST request for analytics
@app.post("/analytics/")
def get_analytics(date_range: DateRange):
    data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database.")

    total = sum([row['total'] for row in data])

    breakdown = {}
    for row in data:
        percentage = (row['total']/total)*100 if total != 0 else 0
        breakdown[row['category']] = {
            "total": row['total'],
            "percentage": percentage
        }

    return breakdown

# @app.get("/expenses/{expense_date}")
# def get_expenses(expense_date: date): #here we are specifying the data type, "date" is a type hint.
#     return f"Resieved get_expense request {expense_date}"

# @app.get("/")
# def read_root():
#     return {"message": "FastAPI is working!"}
#
# def get_expenses(expense_date: str):
#     try:
#         parsed_date = datetime.strptime(expense_date, "%Y-%m-%d").date()
#         return {"message": f"Received get_expense request for {parsed_date}"}
#     except ValueError:
#         return {"error": "Invalid date format. Use YYYY-MM-DD."}