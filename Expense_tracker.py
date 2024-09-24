import streamlit as st
import pandas as pd
import os

# Load the existing expenses from CSV
def load_expenses():
    if os.path.exists("expenses.csv"):
        return pd.read_csv("expenses.csv")
    else:
        return pd.DataFrame(columns=["Description", "Amount", "Date"])

# Save new expenses to CSV
def save_expense(description, amount, date):
    new_data = pd.DataFrame([[description, amount, date]], columns=["Description", "Amount", "Date"])
    new_data.to_csv("expenses.csv", mode='a', header=False, index=False)

# Main Streamlit App
def main():
    st.title("Expense Tracker")

    # Load existing expenses
    expenses = load_expenses()

    # Display the expenses table
    st.header("Current Expenses")
    st.dataframe(expenses)

    st.subheader("Add New Expense")
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    date = st.date_input("Date")

    if st.button("Add Expense"):
        if description and amount:
            save_expense(description, amount, date)
            st.success(f"Added {description} - {amount} on {date}")
        else:
            st.error("Please enter a valid description and amount.")

    # Reload the updated expenses
    expenses = load_expenses()
    st.dataframe(expenses)

if __name__ == "__main__":
    main()
