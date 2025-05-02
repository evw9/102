# Note to self: This app lets users create accounts, log in, deposit, withdraw, check balance, and delete their account.

import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Note to self: Connect to the MySQL database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",  # server name
        user="root",       # your username
        password="MArtum6609065446!",  # your MySQL password
        database="online_banking"  # your database name
    )

# Note to self: Make a new account
def create_account(account_number, pin, name):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO accounts (account_number, pin, balance, name) VALUES (%s, %s, %s, %s)", (account_number, pin, 0.0, name))
    db.commit()
    db.close()

# Note to self: Check login info
def verify_login(account_number, pin):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM accounts WHERE account_number = %s AND pin = %s", (account_number, pin))
    result = cursor.fetchone()
    db.close()
    return result

# Note to self: Add money to balance
def deposit(account_number, amount):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_number = %s", (amount, account_number))
    db.commit()
    db.close()

# Note to self: Take money from balance
def withdraw(account_number, amount):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
    balance = cursor.fetchone()[0]
    if balance >= amount:
        cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_number = %s", (amount, account_number))
        db.commit()
    else:
        messagebox.showerror("Error", "Not enough money")
    db.close()

# Note to self: Check how much money is in the account
def get_balance(account_number):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
    balance = cursor.fetchone()[0]
    db.close()
    return balance

# Note to self: Remove an account
def delete_account(account_number):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM accounts WHERE account_number = %s", (account_number,))
    db.commit()
    db.close()

# Note to self: Show login and create screen
root = tk.Tk()
root.title("Banking App")
root.geometry("300x300")

# Note to self: Switch to banking options after login
def open_dashboard(account_number):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text=f"Welcome {account_number}").pack()

    tk.Button(root, text="Deposit", command=lambda: handle_transaction(account_number, "deposit")).pack(pady=5)
    tk.Button(root, text="Withdraw", command=lambda: handle_transaction(account_number, "withdraw")).pack(pady=5)
    tk.Button(root, text="Check Balance", command=lambda: messagebox.showinfo("Balance", f"Your balance is ${get_balance(account_number):.2f}")).pack(pady=5)
    tk.Button(root, text="Delete Account", command=lambda: handle_delete(account_number)).pack(pady=5)

# Note to self: Show input for money and update

def handle_transaction(account_number, type):
    trans_window = tk.Toplevel(root)
    trans_window.title(type.capitalize())

    tk.Label(trans_window, text="Amount:").pack()
    amount_entry = tk.Entry(trans_window)
    amount_entry.pack()

    def submit():
        try:
            amount = float(amount_entry.get())
            if type == "deposit":
                deposit(account_number, amount)
            else:
                withdraw(account_number, amount)
            messagebox.showinfo("Success", f"{type.capitalize()} successful!")
            trans_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Enter a number")

    tk.Button(trans_window, text="Submit", command=submit).pack()

# Note to self: Ask to confirm and delete

def handle_delete(account_number):
    if messagebox.askyesno("Delete", "Are you sure?"):
        delete_account(account_number)
        messagebox.showinfo("Deleted", "Your account is gone.")
        show_login_screen()

# Note to self: Login function

def login():
    acc = login_acc_entry.get()
    pin = login_pin_entry.get()
    if verify_login(acc, pin):
        open_dashboard(acc)
    else:
        messagebox.showerror("Error", "Wrong info")

# Note to self: Create account function

def create():
    acc = create_acc_entry.get()
    pin = create_pin_entry.get()
    name = name_entry.get()
    if acc and pin and name:
        create_account(acc, pin, name)
        messagebox.showinfo("Created", "Account made!")
        show_login_screen()
    else:
        messagebox.showerror("Error", "Fill all fields")

# Note to self: Show login and create account form

def show_login_screen():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Welcome to the Simple Bank App!", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(root, text="Login").pack()
    tk.Label(root, text="Account #").pack()
    global login_acc_entry
    login_acc_entry = tk.Entry(root)
    login_acc_entry.pack()

    tk.Label(root, text="PIN").pack()
    global login_pin_entry
    login_pin_entry = tk.Entry(root, show="*")
    login_pin_entry.pack()

    tk.Button(root, text="Login", command=login).pack(pady=5)

    tk.Label(root, text="Or Create Account").pack(pady=10)
    tk.Label(root, text="Name").pack()
    global name_entry
    name_entry = tk.Entry(root)
    name_entry.pack()

    tk.Label(root, text="New Account #").pack()
    global create_acc_entry
    create_acc_entry = tk.Entry(root)
    create_acc_entry.pack()

    tk.Label(root, text="New PIN").pack()
    global create_pin_entry
    create_pin_entry = tk.Entry(root, show="*")
    create_pin_entry.pack()

    tk.Button(root, text="Create Account", command=create).pack(pady=5)

show_login_screen()
root.mainloop()