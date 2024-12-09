import React, { useState, useEffect } from "react";
import styled from "styled-components";
import axios from "axios";

const Container = styled.div`
  background: white;
  border: 1px solid black;
  padding: 16px;
  border-radius: 8px;
  max-width: 400px;
  margin: 0 auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
`;

const BudgetCalculator = () => {
  const [budget, setBudget] = useState(0);
  const [expenses, setExpenses] = useState([]);
  const [expenseName, setExpenseName] = useState("");
  const [expenseAmount, setExpenseAmount] = useState("");

  // Fetch initial data
  useEffect(() => {
    fetchExpenses();
  }, []);

  const fetchExpenses = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/expenses");
      setExpenses(response.data);
    } catch (error) {
      console.error("Error fetching expenses:", error);
    }
  };

  const addExpense = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/expenses", {
        name: expenseName,
        amount: parseFloat(expenseAmount),
        budget_id: 1, // Replace with a dynamic budget ID if needed
      });
      setExpenses([...expenses, response.data.data]);
      setExpenseName("");
      setExpenseAmount("");
    } catch (error) {
      console.error("Error adding expense:", error);
    }
  };

  const totalExpenses = expenses.reduce((total, expense) => total + expense.amount, 0);
  const remainingBudget = budget - totalExpenses;

  return (
    <Container>
      <h1>Budget Calculator</h1>
      <label htmlFor="budget">Set your budget:</label>
      <input
        type="number"
        placeholder="Set Budget"
        value={budget}
        onChange={(e) => setBudget(parseFloat(e.target.value))}
      />
      <div>
        <input
          type="text"
          placeholder="Expense Name"
          value={expenseName}
          onChange={(e) => setExpenseName(e.target.value)}
        />
        <input
          type="number"
          placeholder="Expense Amount"
          value={expenseAmount}
          onChange={(e) => setExpenseAmount(e.target.value)}
        />
        <button onClick={addExpense}>Add Expense</button>
      </div>
      <h2>Total (Monthly) Budget: ${budget}</h2>
      <h2>Total Expenses: ${totalExpenses}</h2>
      <h2>Remaining Budget: ${remainingBudget}</h2>
      <ul>
        {expenses.map((expense) => (
          <li key={expense.id}>
            {expense.name}: ${expense.amount}
          </li>
        ))}
      </ul>
    </Container>
  );
};

export default BudgetCalculator;
