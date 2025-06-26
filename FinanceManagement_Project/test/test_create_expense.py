import unittest
from dao.finance_repository_impl import FinanceRepositoryImpl
from entity.expense import Expense

class TestCreateExpense(unittest.TestCase):
    def test_create_expense_successfully(self):
        repo = FinanceRepositoryImpl()
        expense = Expense(None, 6, 200.0, 1, "2025-06-24", "Test Expense Entry")
        result = repo.create_expense(expense)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
