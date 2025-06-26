import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.finance_repository_impl import FinanceRepositoryImpl
from entity.user import User
from entity.expense import Expense
from myexceptions.user_not_found_exception import UserNotFoundException
from myexceptions.expense_not_found_exception import ExpenseNotFoundException

def main():
    repo = FinanceRepositoryImpl()

    while True:
        print("\n===== Finance Management System =====")
        print("1. Add User")
        print("2. Add Expense")
        print("3. Delete User")
        print("4. Delete Expense")
        print("5. Update Expense")
        print("6. Get All Expenses")
        print("0. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                username = input("Enter username: ")
                password = input("Enter password: ")
                email = input("Enter email: ")
                user = User(None, username, password, email)
                if repo.create_user(user):
                    print("User added successfully!")
                else:
                    print("Failed to add user.")
            
            elif choice == "2":
                print("Available Categories:")
                categories = repo.get_all_categories()
                for cat in categories:
                    print(f"{cat[0]}. {cat[1]}")

                user_id = int(input("Enter user ID: "))
                amount = float(input("Enter amount: "))
                category_id = int(input("Enter category ID from above list: "))
                expense_date = input("Enter date (YYYY-MM-DD): ")
                description = input("Enter description: ")

                expense = Expense(None, user_id, amount, category_id, expense_date, description)
                if repo.create_expense(expense):
                    print("Expense added successfully!")
                else:
                    print("Failed to add expense.")
            
            elif choice == "3":
                user_id = int(input("Enter user ID to delete: "))
                try:
                    if repo.delete_user(user_id):
                        print("User deleted successfully.")
                    else:
                        print("Failed to delete user.")
                except UserNotFoundException as e:
                    print(e)
            
            elif choice == "4":
                expense_id = int(input("Enter expense ID to delete: "))
                try:
                    if repo.delete_expense(expense_id):
                        print("Expense deleted successfully.")
                    else:
                        print("Failed to delete expense.")
                except ExpenseNotFoundException as e:
                    print(e)
    
            elif choice == "5":
                user_id = int(input("Enter your user ID: "))
                expense_id = int(input("Enter expense ID to update: "))
                amount = float(input("Enter new amount: "))
                
                # Show categories
                print("Available Categories:")
                categories = repo.get_all_categories()
                for cat in categories:
                    print(f"{cat[0]}. {cat[1]}")  # category_id, category_name

                category_id = int(input("Enter new category ID: "))
                expense_date = input("Enter new date (YYYY-MM-DD): ")
                description = input("Enter new description: ")

                expense = Expense(expense_id, user_id, amount, category_id, expense_date, description)
                
                try:
                    if repo.update_expense(user_id, expense):
                        print("Expense updated successfully.")
                    else:
                        print("Failed to update expense.")
                except ExpenseNotFoundException as e:
                    print(e)


            elif choice == "6":
                user_id = int(input("Enter your user ID: "))
                expenses = repo.get_all_expenses(user_id)

                if expenses:
                    print(f"\n Expenses for user ID {user_id}:")
                    print("ID\tAmount\tCategory\tDate\t\tDescription")
                    print("-"*60)
                    for exp in expenses:
                        print(f"{exp[0]}\t{exp[1]}\t{exp[2]}\t\t{exp[3]}\t{exp[4]}")
                else:
                    print("No expenses found for this user.")


            elif choice == "0":
                print("Exiting application...")
                break

            else:
                print("Invalid choice. Please try again.")

        except UserNotFoundException as ue:
            print(ue)
        except ExpenseNotFoundException as ee:
            print(ee)
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()

