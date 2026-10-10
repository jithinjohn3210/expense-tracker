from flask import Flask, render_template, request, redirect, url_for
from database import Database

app = Flask(__name__)
db = Database()

@app.route("/")
def index():
    expenses = db.view_all_expenses()
    total = db.get_total_spent()
    category_totals = db.get_total_by_category()
    return render_template("index.html", expenses=expenses, total=total, category_totals=category_totals)

@app.route("/add", methods=["POST"])
def add_expense():
    amount = float(request.form["amount"])
    category = request.form["category"].strip().title()
    description = request.form.get("description", "").strip()
    db.add_expense(amount, category, description)
    return redirect(url_for("index"))

@app.route("/delete/<int:expense_id>")
def delete_expense(expense_id):
    db.delete_expense(expense_id)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)