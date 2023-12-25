import os
from datetime import datetime
import calendar
import pytz

from cs50 import SQL
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    jsonify,
    send_from_directory,
)
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import apology, login_required, decimal, allowed_file

# for uploading files
UPLOAD_FOLDER = "/workspaces/147018502/project/file_uploads"

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["decimal"] = decimal

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///expense_tracker.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # get submissions from user
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username, password and confirmation was submitted
        if not username or not password or not confirmation:
            return apology("missing data", 400)

        # check if username already exists
        row = db.execute("SELECT username FROM users WHERE username = ?", username)
        try:
            if row[0]["username"] == username:
                return apology("username already exists", 400)
        except:
            # Ensure password and confirmation match and then add to db
            if password == confirmation:
                db.execute(
                    "INSERT INTO users (username,hash) VALUES (?,?)",
                    username,
                    generate_password_hash(password),
                )
            else:
                return apology("confirmation password different", 400)

        id = db.execute("SELECT id FROM users WHERE username=?", username)
        session["user_id"] = id[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Settings of the user"""
    if request.method == "GET":
        username = db.execute(
            "SELECT username FROM users WHERE id=?", session["user_id"]
        )
        currency = db.execute(
            "SELECT currency FROM users WHERE id=?", session["user_id"]
        )
        return render_template(
            "settings.html",
            name=username[0]["username"].title(),
            currency=currency[0]["currency"],
        )


@app.route("/change_password", methods=["POST"])
@login_required
def change_password():
    try:
        # Get the new password from the request
        new_password = request.json["new_password"]

        # Perform the password update
        hashed_password = generate_password_hash(new_password)
        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?",
            hashed_password,
            session["user_id"],
        )

        # Return a success message
        return (
            jsonify({"status": "success", "message": "Password changed successfully"}),
            200,
        )

    except Exception as e:
        # Handle errors and return an error message
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/delete_account", methods=["POST"])
@login_required
def delete_account():
    try:
        db.execute("DELETE FROM expenses WHERE user_id = ?", session["user_id"])
        db.execute("DELETE FROM income WHERE user_id = ?", session["user_id"])
        db.execute("DELETE FROM categories WHERE user_id = ?", session["user_id"])
        db.execute("DELETE FROM debt WHERE user_id = ?", session["user_id"])
        db.execute("DELETE FROM users WHERE id = ?", session["user_id"])

        # Return a success message
        return (
            jsonify({"status": "success", "message": "Account deleted successfully"}),
            200,
        )

    except Exception as e:
        # Handle errors and return an error message
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/change_currency", methods=["POST"])
@login_required
def change_currency():
    try:
        # Get the new currency from the request
        currency = request.json["currency"]

        db.execute(
            "UPDATE users SET currency = ? WHERE id = ?", currency, session["user_id"]
        )

        # Return a success message
        return (
            jsonify({"status": "success", "message": "Currency changed successfully"}),
            200,
        )

    except Exception as e:
        # Handle errors and return an error message
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/expenses", methods=["GET", "POST"])
@login_required
def expenses():
    """Add new expense"""
    if request.method == "POST":
        # get submissions from user
        date = request.form.get("datePurchased")
        date_split = date.split("-")
        amount = request.form.get("amount")
        item = request.form.get("item")
        category = request.form.get("expense_category")
        description = request.form.get("itemDescription")

        # Ensure all data was submitted
        if not date or not amount or not item or not category:
            return apology("missing data", 400)

        filename = None

        if "receipt" in request.files:
            file = request.files["receipt"]

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        # add data to db
        db.execute(
            "INSERT INTO expenses (user_id, date, day, month, year, item, description, category, amount, receipt, time) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            session["user_id"],
            date,
            date_split[2],
            date_split[1],
            date_split[0],
            item,
            description,
            category,
            amount,
            filename,
            datetime.now(pytz.utc),
        )

        # reload the expense page
        return redirect("/expenses")

    else:
        income_total = db.execute(
            "SELECT SUM(amount) as total FROM income WHERE user_id = ? and month = ? and year = ?",
            session["user_id"],
            datetime.now().month,
            datetime.now().year,
        )
        expense_total = db.execute(
            "SELECT SUM(amount) as total FROM expenses WHERE user_id = ? and month = ? and year = ?",
            session["user_id"],
            datetime.now().month,
            datetime.now().year,
        )
        expense_data = db.execute(
            "SELECT expenses_id, date, day, item, amount, category, receipt, description FROM expenses WHERE user_id = ? and month = ? and year = ?",
            session["user_id"],
            datetime.now().month,
            datetime.now().year,
        )
        categories = db.execute(
            "SELECT category_name FROM categories WHERE user_id = ? AND mode = ?",
            session["user_id"],
            "expense",
        )
        budget = db.execute("SELECT budget FROM users WHERE id = ?", session["user_id"])
        currency = db.execute(
            "SELECT currency FROM users WHERE id = ?", session["user_id"]
        )
        if (
            expense_total is None
            or expense_total[0]["total"] is None
            or not expense_data
        ):
            income_total = 0
            expense_total = 0
            income_consumed = 0
            budget_consumed = 0
        else:
            if income_total is None or income_total[0]["total"] is None:
                income_consumed = 0
                expense_total = int(expense_total[0]["total"])
                budget_consumed = round(
                    (expense_total / int(budget[0]["budget"])) * 100)
            else:
                expense_total = int(expense_total[0]["total"])
                income_total = int(income_total[0]["total"])

                income_consumed = round((expense_total / income_total) * 100)
                budget_consumed = round(
                    (expense_total / int(budget[0]["budget"])) * 100
                )


        return render_template(
            "expenses.html",
            budget=budget[0]["budget"],
            currency=currency[0]["currency"],
            categories=categories,
            month=calendar.month_name[datetime.now().month],
            expense_data=expense_data,
            expense_total=expense_total,
            budget_consumed=budget_consumed,
            income_consumed=income_consumed,
        )


@app.route("/expensecategory", methods=["POST"])
@login_required
def expense_category():
    try:
        # Get the new category from the request
        expense_category = request.json["expenseCategory"]

        # check the available categories
        available = db.execute(
            "SELECT category_name FROM categories WHERE user_id = ? AND mode = ?",
            session["user_id"],
            "expense",
        )

        if (expense_category not in ["Groceries", "Shopping", "Utilities"]) and (
            not any(expense_category in row["category_name"] for row in available)
        ):
            db.execute(
                "INSERT INTO categories (user_id, category_name, mode) VALUES (?,?,?)",
                session["user_id"],
                expense_category,
                "expense",
            )

            # Return a success message
            return (
                jsonify(
                    {"status": "success", "message": "Category added successfully"}
                ),
                200,
            )

        else:
            # Handle errors and return an error message
            return (
                jsonify({"status": "error", "message": "Category already available"}),
                500,
            )

    except Exception as e:
        # Handle errors and return an error message
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/budget", methods=["POST"])
@login_required
def budget():
    try:
        # Get the budget from the request
        budget = request.json["budget"]

        db.execute(
            "UPDATE users SET budget = ? WHERE id = ?", budget, session["user_id"]
        )

        # Return a success message
        return (
            jsonify({"status": "success", "message": "Budget changed successfully"}),
            200,
        )

    except Exception as e:
        # Handle errors and return an error message
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/ehistory")
@login_required
def ehistory():
    """Expenses History"""
    expenses_data = db.execute(
        "SELECT date, item, description, category, amount, receipt FROM expenses WHERE user_id = ? ORDER BY date DESC",
        session["user_id"],
    )

    return render_template("ehistory.html", expenses_data=expenses_data)


@app.route("/delete_expense_log", methods=["POST"])
@login_required
def delete_expense_log():
    try:
        # Get the new category from the request
        id = request.json["id_value"]

        db.execute("DELETE FROM expenses WHERE expenses_id = ?", id)

        # Return a success message
        return jsonify({"status": "success", "message": "Deleted successfully"}), 200

    except Exception as e:
        # Handle errors and return an error message
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/expenses_chart", methods=["GET"])
@login_required
def expenses_chart():
    expenses_data = db.execute(
        "SELECT SUM(amount) as total, category FROM expenses WHERE user_id = ? and month = ? and year = ? GROUP BY category",
        session["user_id"],
        datetime.now().month,
        datetime.now().year,
    )
    return jsonify(expenses_data)


@app.route("/update_expenses", methods=["POST"])
@login_required
def update_expenses():
    """Edit expense"""
    # get submissions from user
    id = request.form.get("expenses_id")
    date = request.form.get("datepurchased")
    date_split = date.split("-")
    amount = request.form.get("amount")
    item = request.form.get("item")
    category = request.form.get("select_expense_category")
    description = request.form.get("itemdescription")

    receipt = db.execute("SELECT receipt FROM expenses WHERE expenses_id = ?", id)

    # Ensure all data was submitted
    if not date or not amount or not item or not category:
        return apology("missing data", 400)

    if receipt or receipt[0]["receipt"] is not None:
        filename = receipt[0]["receipt"]
    else:
        filename = None

    if "receipt" in request.files:
        file = request.files["receipt"]

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    # update the db
    db.execute(
        "UPDATE expenses SET user_id = ? , date = ? , day = ? , month = ? , year = ? , item = ? , description = ? , category = ? , amount = ? , receipt = ? , time = ? WHERE expenses_id = ?",
        session["user_id"],
        date,
        date_split[2],
        date_split[1],
        date_split[0],
        item,
        description,
        category,
        amount,
        filename,
        datetime.now(pytz.utc),
        id,
    )

    # reload the expense page
    return redirect("/expenses")


@app.route("/income", methods=["GET", "POST"])
@login_required
def income():
    """Add new income"""
    if request.method == "POST":
        # get submissions from user
        date = request.form.get("dateReceived")
        date_split = date.split("-")
        amount = request.form.get("amount")
        source = request.form.get("source")
        category = request.form.get("income_category")
        description = request.form.get("sourceDescription")

        # Ensure all data was submitted
        if not date or not amount or not source or not category:
            return apology("missing data", 400)

        filename = None

        if "payslip" in request.files:
            file = request.files["payslip"]

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        # add data to db
        db.execute(
            "INSERT INTO income (user_id, date, day, month, year, source, description, category, amount, payslip, time) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            session["user_id"],
            date,
            date_split[2],
            date_split[1],
            date_split[0],
            source,
            description,
            category,
            amount,
            filename,
            datetime.now(pytz.utc),
        )

        # reload the income page
        return redirect("/income")

    else:
        income_total = db.execute(
            "SELECT SUM(amount) as total FROM income WHERE user_id = ? and month = ? and year = ?",
            session["user_id"],
            datetime.now().month,
            datetime.now().year,
        )
        income_data = db.execute(
            "SELECT income_id, date, day, source, amount, payslip, description, category FROM income WHERE user_id = ? and month = ? and year = ?",
            session["user_id"],
            datetime.now().month,
            datetime.now().year,
        )
        categories = db.execute(
            "SELECT category_name FROM categories WHERE user_id = ? AND mode = ?",
            session["user_id"],
            "income",
        )
        goal = db.execute(
            "SELECT income_goal FROM users WHERE id = ?", session["user_id"]
        )
        currency = db.execute(
            "SELECT currency FROM users WHERE id = ?", session["user_id"]
        )

        if income_total is None or income_total[0]["total"] is None or not income_data:
            income_total = 0
            goal_reached = 0
        else:
            income_total = income_total[0]["total"]
            goal_reached = round(
                (int(income_total) / int(goal[0]["income_goal"])) * 100
            )

        return render_template(
            "income.html",
            goal=goal[0]["income_goal"],
            currency=currency[0]["currency"],
            categories=categories,
            month=calendar.month_name[datetime.now().month],
            income_data=income_data,
            income_total=income_total,
            goal_reached=goal_reached,
        )


@app.route("/goal", methods=["POST"])
@login_required
def goal():
    try:
        # Get the budget from the request
        goal = request.json["goal"]

        db.execute(
            "UPDATE users SET income_goal = ? WHERE id = ?", goal, session["user_id"]
        )

        # Return a success message
        return (
            jsonify(
                {"status": "success", "message": "Income goal changed successfully"}
            ),
            200,
        )

    except Exception as e:
        # Handle errors and return an error message
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/incomecategory", methods=["POST"])
@login_required
def income_category():
    try:
        # Get the new category from the request
        income_category = request.json["incomeCategory"]

        # check if category already available
        available = db.execute(
            "SELECT category_name FROM categories WHERE user_id = ? AND mode = ?",
            session["user_id"],
            "income",
        )

        if (income_category not in ["Employer", "Passive Income", "Captal Gains"]) and (
            not any(income_category in row["category_name"] for row in available)
        ):
            db.execute(
                "INSERT INTO categories (user_id, category_name, mode) VALUES (?,?,?)",
                session["user_id"],
                income_category,
                "income",
            )

            # Return a success message
            return (
                jsonify(
                    {"status": "success", "message": "Category added successfully"}
                ),
                200,
            )

        else:
            # Handle errors and return an error message
            return (
                jsonify({"status": "error", "message": "Category already available"}),
                500,
            )

    except Exception as e:
        # Handle errors and return an error message
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/ihistory")
@login_required
def ihistory():
    """Income History"""
    income_data = db.execute(
        "SELECT date, source, description, category, amount, payslip FROM income WHERE user_id = ? ORDER BY date DESC",
        session["user_id"],
    )

    return render_template("ihistory.html", income_data=income_data)


@app.route("/delete_income_log", methods=["POST"])
@login_required
def delete_income_log():
    try:
        # Get the new category from the request
        id = request.json["id_value"]

        db.execute("DELETE FROM income WHERE income_id = ?", id)

        # Return a success message
        return jsonify({"status": "success", "message": "Deleted successfully"}), 200

    except Exception as e:
        # Handle errors and return an error message
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/income_chart", methods=["GET"])
@login_required
def income_chart():
    income_data = db.execute(
        "SELECT SUM(amount) as total, category FROM income WHERE user_id = ? and month = ? and year = ? GROUP BY category",
        session["user_id"],
        datetime.now().month,
        datetime.now().year,
    )
    return jsonify(income_data)


@app.route("/update_income", methods=["POST"])
@login_required
def update_income():
    """Edit income"""
    # get submissions from user
    id = request.form.get("income_id")
    date = request.form.get("datereceived")
    date_split = date.split("-")
    amount = request.form.get("amount")
    source = request.form.get("source")
    category = request.form.get("select_income_category")
    description = request.form.get("sourcedescription")

    payslip = db.execute("SELECT payslip FROM income WHERE income_id = ?", id)

    # Ensure all data was submitted
    if not date or not amount or not source or not category:
        return apology("missing data", 400)

    if payslip or payslip[0]["payslip"]:
        filename = payslip[0]["payslip"]
    else:
        filename = None

    if "payslip" in request.files:
        file = request.files["payslip"]

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    # update the db
    db.execute(
        "UPDATE income SET user_id = ? , date = ? , day = ? , month = ? , year = ? , source = ? , description = ? , category = ? , amount = ? , payslip = ? , time = ? WHERE income_id = ?",
        session["user_id"],
        date,
        date_split[2],
        date_split[1],
        date_split[0],
        source,
        description,
        category,
        amount,
        filename,
        datetime.now(pytz.utc),
        id,
    )

    # reload the expense page
    return redirect("/income")


@app.route("/")
@login_required
def index():
    """Show summary of user's finances"""
    date = datetime.now().date()
    currency = db.execute("SELECT currency FROM users WHERE id = ?", session["user_id"])
    total_income = db.execute(
        "SELECT SUM(amount) as total FROM income WHERE user_id = ? and month = ? and year = ?",
        session["user_id"],
        datetime.now().month,
        datetime.now().year,
    )
    total_expenses = db.execute(
        "SELECT SUM(amount) as total FROM expenses WHERE user_id = ? and month = ? and year = ?",
        session["user_id"],
        datetime.now().month,
        datetime.now().year,
    )
    total_balance_income = db.execute(
        "SELECT SUM(amount) as total FROM income WHERE user_id = ?", session["user_id"]
    )
    total_balance_expenses = db.execute(
        "SELECT SUM(amount) as total FROM expenses WHERE user_id = ?",
        session["user_id"],
    )
    income_data = db.execute(
        "SELECT month, day, category, amount FROM income WHERE user_id = ? ORDER BY date DESC LIMIT 5",
        session["user_id"],
    )
    expenses_data = db.execute(
        "SELECT month, day, category, amount FROM expenses WHERE user_id = ? ORDER BY date DESC LIMIT 5",
        session["user_id"],
    )
    debt_data = db.execute(
        "SELECT day, month, debt, creditor FROM debt WHERE user_id = ? AND done = 'Pending' ORDER BY date DESC LIMIT 5",
        session["user_id"],
    )
    budget = db.execute("SELECT budget FROM users WHERE id = ?", session["user_id"])
    goal = db.execute("SELECT income_goal FROM users WHERE id = ?", session["user_id"])

    if total_income is None or total_income[0]["total"] is None or not income_data:
        total_income = 0
        goal_reached = 0
        income_consumed = 0
    else:
        total_income = int(total_income[0]["total"])
        goal_reached = round((total_income / int(goal[0]["income_goal"])) * 100)

    if (
        total_expenses is None
        or total_expenses[0]["total"] is None
        or not expenses_data
    ):
        total_expenses = 0
        budget_consumed = 0
    else:
        total_expenses = int(total_expenses[0]["total"])
        budget_consumed = round((total_expenses / int(budget[0]["budget"])) * 100)

    if total_balance_income is None or total_balance_income[0]["total"] is None:
        total_balance_income = 0
    else:
        total_balance_income = int(total_balance_income[0]["total"])

    if total_balance_expenses is None or total_balance_expenses[0]["total"] is None:
        total_balance_expenses = 0
    else:
        total_balance_expenses = int(total_balance_expenses[0]["total"])

    total_balance = total_balance_income - total_balance_expenses

    if total_income != 0:
        income_consumed = round((int(total_expenses) / int(total_income)) * 100)

    return render_template(
        "index.html",
        date=date,
        currency=currency[0]["currency"],
        total_income=total_income,
        total_expenses=total_expenses,
        total_balance=total_balance,
        income_data=income_data,
        expenses_data=expenses_data,
        budget_consumed=budget_consumed,
        income_consumed=income_consumed,
        goal_reached=goal_reached,
        debt_data=debt_data,
    )


@app.route("/line_chart_data", methods=["GET"])
@login_required
def get_line_chart_data():
    expenses_data = db.execute(
        "SELECT SUM(amount) as total, month FROM expenses WHERE user_id = ? AND year = ? GROUP BY month",
        session.get("user_id"),
        datetime.now().year,
    )
    income_data = db.execute(
        "SELECT SUM(amount) as total, month FROM income WHERE user_id = ? AND year = ? GROUP BY month",
        session.get("user_id"),
        datetime.now().year,
    )

    # format suitable for the line chart
    line_chart_data = [["Month", "Income", "Expenses"]]
    for month in range(1, 13):
        income_total = next(
            (item["total"] for item in income_data if item["month"] == month), 0
        )
        expenses_total = next(
            (item["total"] for item in expenses_data if item["month"] == month), 0
        )

        line_chart_data.append(
            [f"{calendar.month_name[month]}", income_total, expenses_total]
        )

    return jsonify(line_chart_data)


@app.route("/file_uploads/<name>", methods=["GET"])
@login_required
def download_file(name):
    # Construct the full file path using os.path.join
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], name)

    # Check if the file exists before attempting to send it
    if os.path.isfile(file_path):
        return send_from_directory(app.config["UPLOAD_FOLDER"], name)
    else:
        # Handle the case where the file does not exist
        return jsonify({"error": "File not found"}), 404


@app.route("/debt_tracker", methods=["GET", "POST"])
@login_required
def debt_tracker():
    if request.method == "POST":
        # get submissions from user
        date = request.form.get("datedue")
        date_split = date.split("-")
        debt = request.form.get("debt")
        creditor = request.form.get("creditor")
        info = request.form.get("description")

        # Ensure all data was submitted
        if not date or not debt or not creditor:
            return apology("missing data", 400)

        # add data to db
        db.execute(
            "INSERT INTO debt (user_id, date, day, month, year, debt, info, creditor, time) VALUES (?,?,?,?,?,?,?,?,?)",
            session["user_id"],
            date,
            date_split[2],
            date_split[1],
            date_split[0],
            debt,
            info,
            creditor,
            datetime.now(pytz.utc),
        )

        # reload the expense page
        return redirect("/debt_tracker")

    else:
        currency = db.execute(
            "SELECT currency FROM users WHERE id = ?", session["user_id"]
        )

        debt_data = db.execute(
            "SELECT user_id, debt_id, date, debt, creditor, info FROM debt WHERE user_id = ? AND done = ? ORDER BY date ",
            session["user_id"],
            "Pending",
        )
        return render_template(
            "debt_tracker.html", currency=currency[0]["currency"], debt_data=debt_data
        )


@app.route("/all", methods=["GET", "POST"])
@login_required
def all():
    debt_data = db.execute(
        "SELECT user_id, debt_id, date, debt, creditor, info, done, done_time FROM debt WHERE user_id = ? ORDER BY date DESC",
        session["user_id"],
    )
    return render_template("all.html", debt_data=debt_data)


@app.route("/completed", methods=["GET", "POST"])
@login_required
def completed():
    debt_data = db.execute(
        "SELECT user_id, debt_id, date, debt, creditor, done_time FROM debt WHERE user_id = ? AND done='Done' ORDER BY date DESC",
        session["user_id"],
    )
    return render_template("completed.html", debt_data=debt_data)


@app.route("/delete_note", methods=["POST"])
@login_required
def delete_note():
    try:
        # Get the new category from the request
        id = request.json["id_value"]

        db.execute("DELETE FROM debt WHERE debt_id = ?", id)

        # Return a success message
        return jsonify({"status": "success", "message": "Deleted successfully"}), 200

    except Exception as e:
        # Handle errors and return an error message
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/checked", methods=["POST"])
@login_required
def checked():
    try:
        # Get the new category from the request
        id = request.json["id_value"]

        db.execute(
            "UPDATE debt SET done = ?, done_time = ? WHERE debt_id = ?",
            "Done",
            datetime.now().date(),
            id,
        )

        # enter into expenses
        debt_data = db.execute(
            "SELECT debt, creditor, info FROM debt WHERE debt_id= ?", id
        )

        date = datetime.now().strftime("%Y-%m-%d")
        date_split = date.split("-")
        item = debt_data[0]["creditor"]
        description = debt_data[0]["info"]
        debt = debt_data[0]["debt"]
        receipt = None

        db.execute(
            "INSERT INTO expenses (user_id, date, day, month, year, item, description, category, amount, receipt, time) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            session["user_id"],
            date,
            date_split[2],
            date_split[1],
            date_split[0],
            item,
            description,
            "Debt",
            debt,
            receipt,
            datetime.now(pytz.utc),
        )

        # Return a success message
        return jsonify({"status": "success", "message": "Deleted successfully"}), 200

    except Exception as e:
        # Handle errors and return an error message
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
