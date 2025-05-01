import mysql.connector

# connects to the database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="bank_user",       # our mysql user
        password="1234",        # password set earlier
        database="online_banking"  # database we're using
    )

# lets a user make a new account
def create_account():
    try:
        account_number = int(input("Enter account number: "))  # ask for account number
        pin = int(input("Enter PIN: "))                        # ask for pin
        name = input("Enter your name: ")                      # ask for name
        balance = float(input("Enter initial deposit: "))     # ask for first deposit

        connection = connect_to_db()
        cursor = connection.cursor()

        # insert info into database
        query = "INSERT INTO accounts (account_number, pin, name, balance) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (account_number, pin, name, balance))

        connection.commit()
        cursor.close()
        connection.close()

        print("Account created successfully!")
    except Exception as e:
        print(f"Error: {e}")

# logs the user in
def login():
    try:
        account_number = int(input("Enter your account number: "))
        pin = int(input("Enter your PIN: "))

        connection = connect_to_db()
        cursor = connection.cursor()

        # check if account exists
        query = "SELECT * FROM accounts WHERE account_number = %s AND pin = %s"
        cursor.execute(query, (account_number, pin))
        account = cursor.fetchone()

        cursor.close()
        connection.close()

        if account:
            print("Login successful!\n")
            return account_number
        else:
            print("Invalid account number or PIN.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# shows account info
def view_account(account_number):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        query = "SELECT * FROM accounts WHERE account_number = %s"
        cursor.execute(query, (account_number,))
        account = cursor.fetchone()

        cursor.close()
        connection.close()

        if account:
            print(f"Account Number: {account[0]}")
            print(f"Name: {account[2]}")
            print(f"Balance: ${account[3]:.2f}")
        else:
            print("Account not found.")
    except Exception as e:
        print(f"Error: {e}")

# lets user put in money
def deposit(account_number):
    try:
        pin = int(input("Enter your PIN: "))
        amount = float(input("Enter amount to deposit: "))

        connection = connect_to_db()
        cursor = connection.cursor()

        query = "SELECT balance FROM accounts WHERE account_number = %s AND pin = %s"
        cursor.execute(query, (account_number, pin))
        account = cursor.fetchone()

        if account:
            new_balance = account[0] + amount  # update balance
            update_query = "UPDATE accounts SET balance = %s WHERE account_number = %s"
            cursor.execute(update_query, (new_balance, account_number))
            connection.commit()
            print(f"Deposit successful. New balance: ${new_balance:.2f}")
        else:
            print("Invalid PIN.")

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error: {e}")

# lets user take out money
def withdraw(account_number):
    try:
        pin = int(input("Enter your PIN: "))
        amount = float(input("Enter amount to withdraw: "))

        connection = connect_to_db()
        cursor = connection.cursor()

        query = "SELECT balance FROM accounts WHERE account_number = %s AND pin = %s"
        cursor.execute(query, (account_number, pin))
        account = cursor.fetchone()

        if account:
            if amount <= account[0]:  # check for enough money
                new_balance = account[0] - amount
                update_query = "UPDATE accounts SET balance = %s WHERE account_number = %s"
                cursor.execute(update_query, (new_balance, account_number))
                connection.commit()
                print(f"Withdrawal successful. New balance: ${new_balance:.2f}")
            else:
                print("Insufficient funds.")
        else:
            print("Invalid PIN.")

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error: {e}")

# the main menu loop
def main():
    while True:
        print("\nWelcome to the Online Banking System")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            create_account()
        elif choice == '2':
            account_number = login()
            if account_number:
                while True:
                    print("\nMain Menu")
                    print("1. View Account")
                    print("2. Deposit Money")
                    print("3. Withdraw Money")
                    print("4. Logout")

                    menu_choice = input("Choose an option: ")

                    if menu_choice == '1':
                        view_account(account_number)
                    elif menu_choice == '2':
                        deposit(account_number)
                    elif menu_choice == '3':
                        withdraw(account_number)
                    elif menu_choice == '4':
                        print("Logging out...\n")
                        break
                    else:
                        print("Invalid option. Please try again.")
        elif choice == '3':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

# starts the program if this file is run
if __name__ == "__main__":
    main()
