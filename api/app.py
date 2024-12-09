from flask import Flask, request, jsonify
from flask_cors import CORS 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Corrected database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


# Database Models
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)  

# Initialize database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Budget App!",
        "endpoints": {
            "POST /budget": "Add a new budget",
            "POST /expenses": "Add a new expense",
            "GET /expenses": "Retrieve all expenses",
            "DELETE /expenses": "Delete an expense",
            "DELETE /budget": "Delete budget",
            "UPDATE /expenses": "Update an expense",
            "UPDATE /budget": "Update a budget",
        }
    })

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Return an empty response with a 204 No Content status

@app.route('/budget', methods=['POST'])
def add_budget():
    data = request.json
    new_budget = Budget(name=data['name'], amount=data['amount'])
    db.session.add(new_budget)
    db.session.commit()
    return jsonify({"message": "Budget added", "data": {"id": new_budget.id, "name": new_budget.name, "amount": new_budget.amount}}), 201

@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.json
    new_expense = Expense(name=data['name'], amount=data['amount'], budget_id=data['budget_id'])
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({"message": "Expense added", "data": {"id": new_expense.id, "name": new_expense.name, "amount": new_expense.amount, "budget_id": new_expense.budget_id}}), 201

@app.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    expenses_list = [
        {"id": expense.id, "name": expense.name, "amount": expense.amount, "budget_id": expense.budget_id}
        for expense in expenses
    ]
    return jsonify(expenses_list)


@app.route('/budget/<int:budget_id>', methods=['PUT'])
def update_budget(budget_id):
    data = request.json
    budget = Budget.query.get_or_404(budget_id)
    budget.name = data.get('name', budget.name)
    budget.amount = data.get('amount', budget.amount)
    db.session.commit()
    return jsonify({"message": "Budget updated", "data": {"id": budget.id, "name": budget.name, "amount": budget.amount}})

@app.route('/expense/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    data = request.json
    expense = Expense.query.get_or_404(expense_id)
    expense.name = data.get('name', expense.name)
    expense.amount = data.get('amount', expense.amount)
    expense.budget_id = data.get('budget_id', expense.budget_id)
    db.session.commit()
    return jsonify({"message": "Expense updated", "data": {"id": expense.id, "name": expense.name, "amount": expense.amount, "budget_id": expense.budget_id}})

@app.route('/budget/<int:budget_id>', methods=['DELETE'])
def delete_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    db.session.delete(budget)
    db.session.commit()
    return jsonify({"message": "Budget deleted"})

@app.route('/expense/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "Expense deleted"})

@app.route('/calculate-budget', methods=['POST'])
def calculate_budget():
    data = request.json
    budget = data['budget']
    expenses = data['expenses']
    total_expenses = sum(expense['amount'] for expense in expenses)
    remaining = budget - total_expenses
    return jsonify({"budget": budget, "total_expenses": total_expenses, "remaining": remaining})


if __name__ == "__main__":
    app.run(debug=True)
