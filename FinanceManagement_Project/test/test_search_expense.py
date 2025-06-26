import unittest
from dao.finance_repository_impl import FinanceRepositoryImpl

class TestSearchExpense(unittest.TestCase):
    def test_search_expenses_for_user(self):
        repo = FinanceRepositoryImpl()
        user_id = 6  
        expenses = repo.get_all_expenses(user_id)
        self.assertIsInstance(expenses, list)
        self.assertGreaterEqual(len(expenses), 0)

if __name__ == '__main__':
    unittest.main()
