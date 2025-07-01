class ExpenseNotFoundException(Exception):
    def __init__(self, expense_id):
        super().__init__(f"Expense with ID {expense_id} not found in the database.")
