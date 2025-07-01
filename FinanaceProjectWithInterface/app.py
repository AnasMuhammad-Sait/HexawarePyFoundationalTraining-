from flask import Flask, render_template, request, redirect, url_for, flash
from dao.finance_repository_impl import FinanceRepositoryImpl
from entity.user import User
from entity.expense import Expense
from util.db_conn_util import DBConnUtil
from myexceptions.user_not_found_exception import UserNotFoundException
from flask import Flask, session, redirect, url_for, render_template, request, flash
from functools import wraps
from fpdf import FPDF
from flask import send_file
import io


app = Flask(__name__)
app.secret_key = 'thisisAnasApplication' 
repo = FinanceRepositoryImpl()

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

@app.route("/")
@login_required
def home():
    total_expenses = 0
    category_data = []
    monthly_data = []

    try:
        conn = DBConnUtil.get_connection()
        cursor = conn.cursor()
        user_id = session["user_id"]

        # Total expenses for current user
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = %s", (user_id,))
        total_expenses = cursor.fetchone()[0] or 0

        # Category-wise for current user
        cursor.execute("""
            SELECT ec.category_name, SUM(e.amount)
            FROM expenses e
            JOIN expensecategories ec ON e.category_id = ec.category_id
            WHERE e.user_id = %s
            GROUP BY ec.category_name
        """, (user_id,))
        category_data = cursor.fetchall()

        # Monthly-wise for current user
        cursor.execute("""
            SELECT DATE_FORMAT(date, '%b %Y') AS month, SUM(amount)
            FROM expenses
            WHERE user_id = %s
            GROUP BY month
            ORDER BY STR_TO_DATE(month, '%b %Y')
        """, (user_id,))
        monthly_data = cursor.fetchall()

    except Exception as e:
        print(f"Dashboard error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template("home.html",
                           total_expenses=total_expenses,
                           category_data=category_data,
                           monthly_data=monthly_data)



@app.route("/add-user", methods=["GET", "POST"])
@login_required
def add_user():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        user = User(None, username, password, email)
        success = repo.create_user(user)

        if success:
            flash("User added successfully!")
            return redirect(url_for("add_user"))
        else:
            flash("Failed to add user.")
            return redirect(url_for("add_user"))

    return render_template("add_user.html")


@app.route("/add-expense", methods=["GET", "POST"])
@login_required
def add_expense():
    categories = repo.get_all_categories()

    if request.method == "POST":
        try:
            user_id = session["user_id"]
            amount = float(request.form.get("amount"))
            category_id = int(request.form.get("category_id"))
            expense_date = request.form.get("expense_date")
            description = request.form.get("description")

            expense = Expense(None, user_id, amount, category_id, expense_date, description)
            success = repo.create_expense(expense)

            if success:
                flash("Expense added successfully!")
            else:
                flash("Failed to add expense.")

        except Exception as e:
            flash(f"Error adding expense: {str(e)}")

        return redirect(url_for("add_expense"))

    return render_template("add_expense.html", categories=categories)


@app.route("/view-expenses", methods=["GET", "POST"])
@login_required
def get_expenses():
    expenses = []
    if request.method == "POST":
        user_id = session["user_id"]
        try:
            expenses = repo.get_all_expenses(user_id)
            if not expenses:
                flash("No expenses found for this user.")
        except Exception as e:
            flash(f"Error fetching expenses: {str(e)}")

    return render_template("view_expenses.html", expenses=expenses)

@app.route("/update-expense", methods=["GET", "POST"])
@login_required
def update_expense():
    categories = repo.get_all_categories()
    expenses = []
    selected_expense = None
    user_id = None

    if request.method == "POST":
        if "load" in request.form:
            user_id = session["user_id"]
            if user_id:
                expenses = repo.get_all_expenses(user_id)
            else:
                flash("Please enter a User ID.")

        elif "edit" in request.form:
            expense_id = int(request.form.get("expense_id"))
            user_id = request.form.get("user_id")
            all_expenses = repo.get_all_expenses(user_id)
            for e in all_expenses:
                if e[0] == expense_id:
                    selected_expense = e + (user_id,)
                    break
            expenses = all_expenses

        elif "update" in request.form:
            try:
                user_id = int(request.form.get("user_id"))
                expense_id = int(request.form.get("expense_id"))
                amount = float(request.form.get("amount"))
                category_id = int(request.form.get("category_id"))
                expense_date = request.form.get("expense_date")
                description = request.form.get("description")

                from entity.expense import Expense
                updated_expense = Expense(expense_id, user_id, amount, category_id, expense_date, description)

                success = repo.update_expense(user_id, updated_expense)
                if success:
                    flash("Expense updated successfully!")
                else:
                    flash("Failed to update expense.")

                expenses = repo.get_all_expenses(user_id)

            except Exception as e:
                flash(f"Error: {str(e)}")

    return render_template("update_expense.html", categories=categories, expenses=expenses, selected_expense=selected_expense, user_id=user_id)

@app.route("/delete-expense", methods=["GET", "POST"])
@login_required
def delete_expense():
    expenses = []
    user_id = None

    if request.method == "POST":
        if "load" in request.form:
            user_id = session["user_id"]
            if user_id:
                expenses = repo.get_all_expenses(user_id)
            else:
                flash("Please enter a valid User ID.")

        elif "delete" in request.form:
            try:
                expense_id = int(request.form.get("expense_id"))
                from myexceptions.expense_not_found_exception import ExpenseNotFoundException

                success = repo.delete_expense(expense_id)
                if success:
                    flash(f"Expense ID {expense_id} deleted successfully.")
                else:
                    flash("Failed to delete expense.")
            except ExpenseNotFoundException as e:
                flash(str(e))
            except Exception as e:
                flash(f"Error: {str(e)}")

            # Refresh expense list after deletion
            user_id = request.form.get("user_id")
            expenses = repo.get_all_expenses(user_id)

    return render_template("delete_expense.html", expenses=expenses, user_id=user_id)

@app.route("/delete-user", methods=["GET", "POST"])
@login_required
def delete_user():
    user = None

    if request.method == "POST":
        if "load" in request.form:
            user_id = request.form.get("user_id")
            try:
                conn = DBConnUtil.get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT user_id, username, email FROM users WHERE user_id = %s", (user_id,))
                user = cursor.fetchone()
                if not user:
                    raise UserNotFoundException(user_id)
            except UserNotFoundException as e:
                flash(str(e))
            except Exception as e:
                flash(f"Error: {str(e)}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        elif "confirm_delete" in request.form:
            user_id = request.form.get("user_id")
            try:
                success = repo.delete_user(int(user_id))
                if success:
                    flash("User deleted successfully.")
                else:
                    flash("Failed to delete user.")
            except Exception as e:
                flash(f"Error: {str(e)}")

    return render_template("delete_user.html", user=user)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            conn = DBConnUtil.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, username FROM users WHERE email = %s AND password = %s", (email, password))
            result = cursor.fetchone()

            if result:
                session["user_id"] = result[0]
                session["username"] = result[1]
                flash(f"Welcome, {result[1]} 👋")
                return redirect(url_for("home"))
            else:
                flash("Invalid credentials. Try again.")
        except Exception as e:
            flash(f"Error: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for("login"))


@app.route("/generate-report")
@login_required
def generate_report():
    user_id = session["user_id"]
    username = session["username"]

    try:
        expenses = repo.get_all_expenses(user_id)

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Expense Report for {username}", ln=1, align='C')
        pdf.ln(10)

        # Table Header
        pdf.cell(40, 10, "Category ID", 1)
        pdf.cell(40, 10, "Expense ID", 1)
        pdf.cell(50, 10, "Amount", 1)
        pdf.cell(60, 10, "Date", 1)
        pdf.ln()

        for e in expenses:
            print("DEBUG:", e, "Length:", len(e))

            try:
                amount = f"{e[0]}"
                category = str(e[1])
                date = str(e[2])
                desc = str(e[3])[:30]
            except IndexError:
                amount = "N/A"
                category = "-"
                date = "-"
                desc = "Corrupted"

            pdf.cell(40, 10, date, 1)
            pdf.cell(40, 10, amount, 1)
            pdf.cell(50, 10, category, 1)
            pdf.cell(60, 10, desc, 1)
            pdf.ln()

        # Write to byte stream
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        return send_file(
            io.BytesIO(pdf_bytes),
            as_attachment=True,
            download_name="expense_report.pdf",
            mimetype='application/pdf'
        )

    except Exception as e:
        flash(f"Error generating report: {str(e)}")
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
