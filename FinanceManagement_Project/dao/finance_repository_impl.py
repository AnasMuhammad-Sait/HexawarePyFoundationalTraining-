from dao.ifinance_repository import IFinanceRepository
from entity.user import User
from entity.expense import Expense
from util.db_conn_util import DBConnUtil
from myexceptions.user_not_found_exception import UserNotFoundException
from myexceptions.expense_not_found_exception import ExpenseNotFoundException


class FinanceRepositoryImpl(IFinanceRepository):

    def create_user(self, user: User) -> bool:
        try:
            conn = DBConnUtil.get_connection()
            cursor = conn.cursor()
            query = "INSERT INTO Users (username, password, email) VALUES (%s, %s, %s)"
            values = (user.get_username(), user.get_password(), user.get_email())
            cursor.execute(query, values)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def create_expense(self, expense: Expense) -> bool:
        conn = None
        cursor = None
        try:
            conn = DBConnUtil.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO Expenses (user_id, amount, category_id, date, description)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                expense.get_user_id(),
                expense.get_amount(),
                expense.get_category_id(),
                expense.get_expense_date(),
                expense.get_description()
            )

            cursor.execute(query, values)
            conn.commit()
            return True

        except Exception as e:
            print(f"Error adding expense: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def get_all_categories(self) -> list:
        conn = None
        cursor = None
        try:
            conn = DBConnUtil.get_connection()
            cursor = conn.cursor()

            query = "SELECT category_id, category_name FROM ExpenseCategories"
            cursor.execute(query)
            results = cursor.fetchall()
            return results

        except Exception as e:
            print(f"Error fetching categories: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    # Placeholder/dummy methods to avoid abstract class error


    def delete_user(self, user_id: int) -> bool:
        conn = None
        cursor = None
        try:
            conn = DBConnUtil.get_connection()
            cursor = conn.cursor()

            # 1. Check if user exists
            cursor.execute("SELECT * FROM Users WHERE user_id = %s", (user_id,))
            if cursor.fetchone() is None:
                raise UserNotFoundException(user_id)

            # 2. Delete all expenses for that user
            cursor.execute("DELETE FROM Expenses WHERE user_id = %s", (user_id,))

            # 3. Now delete the user
            cursor.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
            conn.commit()
            return True

        except UserNotFoundException as ue:
            raise ue
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def delete_expense(self, expense_id: int) -> bool:
        conn = None
        cursor = None
        try:
            conn = DBConnUtil.get_connection()
            cursor = conn.cursor()

            # Check if expense exists
            cursor.execute("SELECT * FROM Expenses WHERE expense_id = %s", (expense_id,))
            if cursor.fetchone() is None:
                raise ExpenseNotFoundException(expense_id)

            # Delete the expense
            cursor.execute("DELETE FROM Expenses WHERE expense_id = %s", (expense_id,))
            conn.commit()
            return True

        except ExpenseNotFoundException as ee:
            raise ee
        except Exception as e:
            print(f"Error deleting expense: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def get_all_expenses(self, user_id: int) -> list:
        conn = None
        cursor = None
        try:
            conn = DBConnUtil.get_connection()
            cursor = conn.cursor()

            # Get all expenses for a user
            query = """
                SELECT expense_id, amount, category_id, date, description
                FROM Expenses
                WHERE user_id = %s
            """
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()

            return results

        except Exception as e:
            print(f"Error fetching expenses: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def update_expense(self, user_id: int, expense: Expense) -> bool:
        conn = None
        cursor = None
        try:
            conn = DBConnUtil.get_connection()
            cursor = conn.cursor()

            # Check if the expense exists and belongs to the user
            cursor.execute(
                "SELECT * FROM Expenses WHERE expense_id = %s AND user_id = %s",
                (expense.get_expense_id(), user_id)
            )
            if cursor.fetchone() is None:
                raise ExpenseNotFoundException(expense.get_expense_id())

            # Perform the update
            query = """
                UPDATE Expenses
                SET amount = %s,
                    category_id = %s,
                    date = %s,
                    description = %s
                WHERE expense_id = %s AND user_id = %s
            """
            values = (
                expense.get_amount(),
                expense.get_category_id(),
                expense.get_expense_date(),
                expense.get_description(),
                expense.get_expense_id(),
                user_id
            )
            cursor.execute(query, values)
            conn.commit()
            return True

        except ExpenseNotFoundException as ee:
            raise ee
        except Exception as e:
            print(f"Error updating expense: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
