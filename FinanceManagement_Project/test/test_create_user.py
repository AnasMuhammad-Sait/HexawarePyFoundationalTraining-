import unittest
from dao.finance_repository_impl import FinanceRepositoryImpl
from entity.user import User

class TestCreateUser(unittest.TestCase):
    def test_create_user_successfully(self):
        repo = FinanceRepositoryImpl()
        user = User(None, "test_user", "test_pass", "test_user@example.com")
        result = repo.create_user(user)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
