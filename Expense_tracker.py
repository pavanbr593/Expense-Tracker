import streamlit as st
import pandas as pd
import os

# Load the existing expenses from CSV
def load_expenses():
    if os.path.exists("expenses.csv"):
        expenses = pd.read_csv("expenses.csv")
        expenses["Amount"] = pd.to_numeric(expenses["Amount"], errors="coerce")  # Convert 'Amount' to numeric
        expenses["Date"] = pd.to_datetime(expenses["Date"], errors="coerce")  # Convert 'Date' to datetime
        return expenses
    else:
        return pd.DataFrame(columns=["Description", "Amount", "Date"])

# Save new expenses to CSV
def save_expense(description, amount, date):
    new_data = pd.DataFrame([[description, amount, date]], columns=["Description", "Amount", "Date"])
    if os.path.exists("expenses.csv"):
        new_data.to_csv("expenses.csv", mode='a', header=False, index=False)
    else:
        new_data.to_csv("expenses.csv", mode='w', index=False)

# Remove expense and update CSV
def remove_expense(index):
    expenses = load_expenses()
    expenses = expenses.drop(index)
    expenses.to_csv("expenses.csv", index=False)

# Filter expenses
def filter_expenses(expenses, description_filter, amount_filter, date_range):
    filtered_expenses = expenses.copy()
    
    # Filter by description
    if description_filter:
        filtered_expenses = filtered_expenses[filtered_expenses['Description'].str.contains(description_filter, case=False, na=False)]
    
    # Filter by amount
    if amount_filter > 0:
        filtered_expenses = filtered_expenses[filtered_expenses['Amount'] <= amount_filter]
    
    # Filter by date range
    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_expenses = filtered_expenses[
            (filtered_expenses['Date'] >= pd.to_datetime(start_date)) &
            (filtered_expenses['Date'] <= pd.to_datetime(end_date))
        ]

    return filtered_expenses

# Main Streamlit App
def main():
    st.title("Expense Tracker")

    # Load existing expenses
    expenses = load_expenses()

    # Display the expenses table
    st.header("Current Expenses")
    if not expenses.empty:
        st.dataframe(expenses)
        selected_expense = st.selectbox("Select an expense to remove", expenses.index)
        if st.button("Remove Expense"):
            remove_expense(selected_expense)
            st.success("Expense removed successfully!")
            expenses = load_expenses()
            st.dataframe(expenses)
    else:
        st.write("No expenses found.")

    st.subheader("Add New Expense")
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    date = st.date_input("Date")

    if st.button("Add Expense"):
        if description and amount > 0:
            save_expense(description, amount, date)
            st.success(f"Added: {description} - {amount} on {date}")
            expenses = load_expenses()
            st.dataframe(expenses)
        else:
            st.error("Please enter a valid description and amount.")

    st.subheader("Filter Expenses")
    description_filter = st.text_input("Filter by Description")
    amount_filter = st.number_input("Filter by Maximum Amount", min_value=0.0, format="%.2f")
    date_range = st.date_input("Filter by Date Range", [])

    if st.button("Apply Filter"):
        filtered_expenses = filter_expenses(expenses, description_filter, amount_filter, date_range)
        st.write(f"Filtered Expenses:")
        st.dataframe(filtered_expenses)

if __name__ == "__main__":
    main()
