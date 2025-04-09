from backend import db_helper

import os
import sys

print(__file__)

def test_fetch_expenses_for_date_15aug():
    expenses = db_helper.fetch_expenses_for_date("2024-08-15")

    assert len(expenses) == 1
    assert expenses[0]['amount'] == 10.0
    assert expenses[0]['category'] == "Shopping"
    assert expenses[0]['notes'] == "Bought potatoes"

def test_fetch_expense_summary_invalid_range():
    summary = db_helper.fetch_expense_summary("2099-09-05", "2051-05-05")
    assert len(summary) == 0