import unittest
from myexceptions.user_not_found_exception import UserNotFoundException
from myexceptions.expense_not_found_exception import ExpenseNotFoundException

class TestExceptionHandling(unittest.TestCase):
    def test_user_not_found_exception(self):
        with self.assertRaises(UserNotFoundException):
            raise UserNotFoundException("User with ID 9999 not found")

    def test_expense_not_found_exception(self):
        with self.assertRaises(ExpenseNotFoundException):
            raise ExpenseNotFoundException("Expense ID 9999 not found")

if __name__ == '__main__':
    unittest.main()
