from database import Database

def show_menu():
    print("\n===== Personal Expense Tracker =====")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. View Expenses by Category")
    print("4. Show Total Spent")
    print("5. Show Total by Category")
    print("6. Delete Expense")
    print("7. Exit")
    print("====================================")

def main():
    db = Database()

    while True:
        show_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            try:
                amount = float(input("Enter amount: ₹"))
                category = input("Enter category (Food/Travel/Shopping/Bills/Other): ").strip().title()
                description = input("Enter description (optional): ").strip()
                db.add_expense(amount, category, description)
            except ValueError:
                print("❌ Please enter a valid number for amount.")

        elif choice == "2":
            expenses = db.view_all_expenses()
            if expenses:
                print("\nID | Date                | Amount   | Category   | Description")
                print("-" * 70)
                for exp in expenses:
                    print(f"{exp[0]:<3}| {exp[1]:<19}| ₹{exp[2]:<7.2f}| {exp[3]:<10}| {exp[4]}")
            else:
                print("No expenses found.")

        elif choice == "3":
            category = input("Enter category: ").strip().title()
            expenses = db.view_by_category(category)
            if expenses:
                print(f"\nExpenses in '{category}':")
                for exp in expenses:
                    print(f"ID: {exp[0]} | {exp[1]} | ₹{exp[2]:.2f} | {exp[4]}")
            else:
                print(f"No expenses found in category '{category}'.")

        elif choice == "4":
            total = db.get_total_spent()
            print(f"\n💰 Total Spent: ₹{total:.2f}")

        elif choice == "5":
            results = db.get_total_by_category()
            if results:
                print("\nCategory-wise Total:")
                print("-" * 30)
                for category, total in results:
                    print(f"{category:<15}: ₹{total:.2f}")
            else:
                print("No expenses found.")

        elif choice == "6":
            try:
                expense_id = int(input("Enter Expense ID to delete: "))
                db.delete_expense(expense_id)
            except ValueError:
                print("❌ Please enter a valid ID number.")

        elif choice == "7":
            print("👋 Thank you for using Expense Tracker!")
            db.close()
            break

        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()