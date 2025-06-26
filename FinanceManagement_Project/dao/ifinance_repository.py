from abc import ABC, abstractmethod
from entity.user import User
from entity.expense import Expense

class IFinanceRepository(ABC):

    @abstractmethod
    def create_user(self, user: User) -> bool:
        pass

    @abstractmethod
    def create_expense(self, expense: Expense) -> bool:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def delete_expense(self, expense_id: int) -> bool:
        pass

    @abstractmethod
    def get_all_expenses(self, user_id: int) -> list:
        pass

    @abstractmethod
    def update_expense(self, user_id: int, expense: Expense) -> bool:
        pass

    @abstractmethod
    def get_all_categories(self) -> list:
        pass
