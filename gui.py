import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector as sql
from random import randint
import datetime

# Connect to the database
mydb = sql.connect(
    host="localhost",
    user="root",
    passwd="1506@Rishu",
    database="bank"
)
cursor = mydb.cursor()

def db_query(query):
    """Execute a SQL query and return the results."""
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except sql.Error as err:
        print(f"Error: {err}")
        return None

class Bank:
    def __init__(self, username, account_number):
        self.__username = username
        self.__account_number = account_number

    def create_transaction_table(self):
        db_query(f"CREATE TABLE IF NOT EXISTS {self.__username}_transaction "
                 f"(timedate VARCHAR(30),"
                 f"account_number INTEGER,"
                 f"remarks VARCHAR(30),"
                 f"amount INTEGER)")

    def balance_enquiry(self):
        temp = db_query(f"SELECT balance FROM customers WHERE username = '{self.__username}';")
        return temp[0][0]

    def deposit(self, amount):
        temp = db_query(f"SELECT balance FROM customers WHERE username = '{self.__username}';")
        new_balance = amount + temp[0][0]
        db_query(f"UPDATE customers SET balance = '{new_balance}' WHERE username = '{self.__username}'; ")
        db_query(f"INSERT INTO {self.__username}_transaction VALUES ("
                 f"'{datetime.datetime.now()}',"
                 f"'{self.__account_number}',"
                 f"'Amount Deposit',"
                 f"'{amount}'"
                 f")")
        mydb.commit()
        return new_balance

    def withdraw(self, amount):
        temp = db_query(f"SELECT balance FROM customers WHERE username = '{self.__username}';")
        if amount > temp[0][0]:
            return None  # Insufficient balance
        new_balance = temp[0][0] - amount
        db_query(f"UPDATE customers SET balance = '{new_balance}' WHERE username = '{self.__username}'; ")
        db_query(f"INSERT INTO {self.__username}_transaction VALUES ("
                 f"'{datetime.datetime.now()}',"
                 f"'{self.__account_number}',"
                 f"'Amount Withdraw',"
                 f"'{amount}'"
                 f")")
        mydb.commit()
        return new_balance

    def fund_transfer(self, receiver_account_number, amount):
        temp = db_query(f"SELECT balance FROM customers WHERE username = '{self.__username}';")
        if amount > temp[0][0]:
            return None  # Insufficient balance

        temp2 = db_query(f"SELECT balance FROM customers WHERE account_number = '{receiver_account_number}';")
        if not temp2:
            return False  # Receiver account does not exist

        new_sender_balance = temp[0][0] - amount
        new_receiver_balance = temp2[0][0] + amount
        db_query(f"UPDATE customers SET balance = '{new_sender_balance}' WHERE username = '{self.__username}'; ")
        db_query(f"UPDATE customers SET balance = '{new_receiver_balance}' WHERE account_number = '{receiver_account_number}'; ")

        receiver_username = db_query(f"SELECT username FROM customers WHERE account_number = '{receiver_account_number}';")[0][0]
        db_query(f"INSERT INTO {receiver_username}_transaction VALUES ("
                 f"'{datetime.datetime.now()}',"
                 f"'{self.__account_number}',"
                 f"'Fund Transfer from {self.__account_number}',"
                 f"'{amount}'"
                 f")")
        db_query(f"INSERT INTO {self.__username}_transaction VALUES ("
                 f"'{datetime.datetime.now()}',"
                 f"'{self.__account_number}',"
                 f"'Fund Transfer -> {receiver_account_number}',"
                 f"'{amount}'"
                 f")")
        mydb.commit()
        return True
    def show_transactions(self):
        transactions = db_query(f"SELECT * FROM {self.__username}_transaction;")
        return transactions

class Customer:
    def __init__(self, username, password, name, age, city, account_number):
        self.__username = username
        self.__password = password
        self.__name = name
        self.__age = age
        self.__city = city
        self.__account_number = account_number

    def create_user(self):
        db_query(f"INSERT INTO customers VALUES ('{self.__username}', '{self.__password}', '{self.__name}', '{self.__age}', '{self.__city}', 0 , '{self.__account_number}', 1);")
        mydb.commit()

def sign_up():
    username = input("Create Username: ")
    temp = db_query(f"SELECT username FROM customers WHERE username = '{username}';")
    if temp:
        print("Username Already Exists")
        sign_up()
    else:
        print("Username is Available. Please Proceed.")
        password = input("Enter Your Password: ")
        name = input("Enter Your Name: ")
        age = input("Enter Your Age: ")
        city = input("Enter Your City: ")
        while True:
            account_number = randint(10000000, 99999999)
            temp = db_query(f"SELECT account_number FROM customers WHERE account_number = '{account_number}';")
            if temp:
                continue
            else:
                print("Your Account Number:", account_number)
                break
        customer = Customer(username, password, name, age, city, account_number)
        customer.create_user()
        bank = Bank(username, account_number)
        bank.create_transaction_table()
        return username

def sign_in():
    username = input("Enter Username: ")
    temp = db_query(f"SELECT username FROM customers WHERE username = '{username}';")
    if temp:
        while True:
            password = input(f"Welcome {username.capitalize()}. Enter Password: ")
            temp = db_query(f"SELECT password FROM customers WHERE username = '{username}';")
            if temp[0][0] == password:
                print("Sign In Successfully")
                return username
            else:
                print("Wrong Password. Try Again.")
    else:
        print("Username does not exist. Please Sign Up.")
        sign_up()

class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking System")
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="NSEW")

        ttk.Label(main_frame, text="Banking System", font=("Helvetica", 20)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Button(main_frame, text="Sign Up", command=self.sign_up_screen).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(main_frame, text="Sign In", command=self.sign_in_screen).grid(row=1, column=1, padx=10, pady=10)

    def sign_up_screen(self):
        self.clear_screen()
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="NSEW")
        
        ttk.Label(main_frame, text="Sign Up", font=("Helvetica", 20)).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(main_frame, text="Username").grid(row=1, column=0, sticky="E")
        self.username_entry = ttk.Entry(main_frame)
        self.username_entry.grid(row=1, column=1, pady=5)

        ttk.Label(main_frame, text="Password").grid(row=2, column=0, sticky="E")
        self.password_entry = ttk.Entry(main_frame, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)

        ttk.Label(main_frame, text="Name").grid(row=3, column=0, sticky="E")
        self.name_entry = ttk.Entry(main_frame)
        self.name_entry.grid(row=3, column=1, pady=5)

        ttk.Label(main_frame, text="Age").grid(row=4, column=0, sticky="E")
        self.age_entry = ttk.Entry(main_frame)
        self.age_entry.grid(row=4, column=1, pady=5)

        ttk.Label(main_frame, text="City").grid(row=5, column=0, sticky="E")
        self.city_entry = ttk.Entry(main_frame)
        self.city_entry.grid(row=5, column=1, pady=5)

        ttk.Button(main_frame, text="Submit", command=self.sign_up).grid(row=6, column=0, columnspan=2, pady=10)

    def sign_up(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        city = self.city_entry.get().strip()

        # Validation for empty fields
        if not username or not password or not name or not age or not city:
            messagebox.showerror("Error", "All fields are required")
            return

        temp = db_query(f"SELECT username FROM customers WHERE username = '{username}';")
        if temp:
            messagebox.showerror("Error", "Username Already Exists")
        else:
            while True:
                account_number = randint(10000000, 99999999)
                temp = db_query(f"SELECT account_number FROM customers WHERE account_number = '{account_number}';")
                if temp:
                    continue
                else:
                    break

            customer = Customer(username, password, name, age, city, account_number)
            customer.create_user()
            bank = Bank(username, account_number)
            bank.create_transaction_table()
            messagebox.showinfo("Success", f"Sign Up Successful. Your Account Number: {account_number}")
            self.create_login_screen()

    def sign_in_screen(self):
        self.clear_screen()
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="NSEW")
        
        ttk.Label(main_frame, text="Sign In", font=("Helvetica", 20)).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(main_frame, text="Username").grid(row=1, column=0, sticky="E")
        self.username_entry = ttk.Entry(main_frame)
        self.username_entry.grid(row=1, column=1, pady=5)

        ttk.Label(main_frame, text="Password").grid(row=2, column=0, sticky="E")
        self.password_entry = ttk.Entry(main_frame, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)

        ttk.Button(main_frame, text="Submit", command=self.sign_in).grid(row=3, column=0, columnspan=2, pady=10)

    def sign_in(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        temp = db_query(f"SELECT username FROM customers WHERE username = '{username}';")
        if temp:
            temp_password = db_query(f"SELECT password FROM customers WHERE username = '{username}';")
            if temp_password[0][0] == password:
                messagebox.showinfo("Success", "Sign In Successfully")
                self.create_main_screen(username)
            else:
                messagebox.showerror("Error", "Wrong Password. Try Again.")
        else:
            messagebox.showerror("Error", "Username does not exist. Please Sign Up.")
            self.create_login_screen()

    def create_main_screen(self, username):
        self.clear_screen()
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="NSEW")

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(main_frame, text=f"Welcome, {username.capitalize()}", font=("Helvetica", 20)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Button(main_frame, text="Balance Enquiry", command=lambda: self.balance_enquiry(username)).grid(row=1, column=0, padx=10, pady=10, sticky="EW")
        ttk.Button(main_frame, text="Deposit", command=lambda: self.deposit_screen(username)).grid(row=1, column=1, padx=10, pady=10, sticky="EW")
        ttk.Button(main_frame, text="Withdraw", command=lambda: self.withdraw_screen(username)).grid(row=2, column=0, padx=10, pady=10, sticky="EW")
        ttk.Button(main_frame, text="Fund Transfer", command=lambda: self.fund_transfer_screen(username)).grid(row=2, column=1, padx=10, pady=10, sticky="EW")
        ttk.Button(main_frame, text="View Transactions", command=lambda: self.view_transactions_screen(username)).grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="EW")
        ttk.Button(main_frame, text="View Account Number", command=lambda: self.view_account_number(username)).grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="EW")
        ttk.Button(main_frame, text="Exit", command=self.root.quit).grid(row=5, column=0, columnspan=2, pady=10, sticky="EW")

    def view_transactions_screen(self, username):
        self.clear_screen()

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="NSEW")

        bank = Bank(username, db_query(f"SELECT account_number FROM customers WHERE username = '{username}';")[0][0])
        transactions = bank.show_transactions()

        ttk.Label(main_frame, text="Transaction History", font=("Helvetica", 20)).grid(row=0, column=0, pady=10)

        columns = ("Date", "Account Number", "Remarks", "Amount")
        tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        tree.grid(row=1, column=0, padx=10, pady=10)

        for trans in transactions:
            tree.insert("", tk.END, values=trans)

        ttk.Button(main_frame, text="Back", command=lambda: self.create_main_screen(username)).grid(row=2, column=0, pady=10)
    def view_account_number(self, username):
        account_number = db_query(f"SELECT account_number FROM customers WHERE username = '{username}';")[0][0]
        messagebox.showinfo("Account Number", f"Your Account Number is: {account_number}")

    def balance_enquiry(self, username):
        bank = Bank(username, db_query(f"SELECT account_number FROM customers WHERE username = '{username}';")[0][0])
        balance = bank.balance_enquiry()
        messagebox.showinfo("Balance Enquiry", f"Your current balance is: {balance}")

    def deposit_screen(self, username):
        self.clear_screen()
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="NSEW")
        
        ttk.Label(main_frame, text="Deposit", font=("Helvetica", 20)).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(main_frame, text="Amount").grid(row=1, column=0, sticky="E")
        self.amount_entry = ttk.Entry(main_frame)
        self.amount_entry.grid(row=1, column=1, pady=5)

        ttk.Button(main_frame, text="Submit", command=lambda: self.deposit(username)).grid(row=2, column=0, columnspan=2, pady=10)

    def deposit(self, username):
        try:
            amount = int(self.amount_entry.get().strip())
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
            return

        bank = Bank(username, db_query(f"SELECT account_number FROM customers WHERE username = '{username}';")[0][0])
        new_balance = bank.deposit(amount)
        messagebox.showinfo("Deposit", f"Deposit Successful. Your new balance is: {new_balance}")
        self.create_main_screen(username)

    def withdraw_screen(self, username):
        self.clear_screen()
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="NSEW")
        
        ttk.Label(main_frame, text="Withdraw", font=("Helvetica", 20)).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(main_frame, text="Amount").grid(row=1, column=0, sticky="E")
        self.amount_entry = ttk.Entry(main_frame)
        self.amount_entry.grid(row=1, column=1, pady=5)

        ttk.Button(main_frame, text="Submit", command=lambda: self.withdraw(username)).grid(row=2, column=0, columnspan=2, pady=10)

    def withdraw(self, username):
        try:
            amount = int(self.amount_entry.get().strip())
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
            return

        bank = Bank(username, db_query(f"SELECT account_number FROM customers WHERE username = '{username}';")[0][0])
        new_balance = bank.withdraw(amount)
        if new_balance is None:
            messagebox.showerror("Error", "Insufficient balance")
        else:
            messagebox.showinfo("Withdraw", f"Withdraw Successful. Your new balance is: {new_balance}")
        self.create_main_screen(username)

    def fund_transfer_screen(self, username):
        self.clear_screen()
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="NSEW")
        
        ttk.Label(main_frame, text="Fund Transfer", font=("Helvetica", 20)).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(main_frame, text="Receiver Account Number").grid(row=1, column=0, sticky="E")
        self.receiver_account_entry = ttk.Entry(main_frame)
        self.receiver_account_entry.grid(row=1, column=1, pady=5)

        ttk.Label(main_frame, text="Amount").grid(row=2, column=0, sticky="E")
        self.amount_entry = ttk.Entry(main_frame)
        self.amount_entry.grid(row=2, column=1, pady=5)

        ttk.Button(main_frame, text="Submit", command=lambda: self.fund_transfer(username)).grid(row=3, column=0, columnspan=2, pady=10)

    def fund_transfer(self, username):
        try:
            receiver_account_number = int(self.receiver_account_entry.get().strip())
            amount = int(self.amount_entry.get().strip())
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter valid details")
            return

        bank = Bank(username, db_query(f"SELECT account_number FROM customers WHERE username = '{username}';")[0][0])
        success = bank.fund_transfer(receiver_account_number, amount)
        if success is None:
            messagebox.showerror("Error", "Insufficient balance")
        elif not success:
            messagebox.showerror("Error", "Receiver account does not exist")
        else:
            messagebox.showinfo("Fund Transfer", "Fund Transfer Successful")
        self.create_main_screen(username)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()
