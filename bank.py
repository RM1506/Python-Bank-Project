# Bank Services
from database import *
import datetime


class Bank:
    def __init__(self, username, account_number):
        self.__username = username
        self.__account_number = account_number

    def create_transaction_table(self):
        db_query(f"CREATE TABLE IF NOT EXISTS {self.__username}_transaction "
                 f"( timedate VARCHAR(30),"
                 f"account_number INTEGER,"
                 f"remarks VARCHAR(30),"
                 f"amount INTEGER )")

    def balance_enquiry(self):
        temp = db_query(
            f"SELECT balance FROM customers WHERE username = '{self.__username}';")
        print(f"{self.__username} Balance is {temp[0][0]}")

    def deposit(self, amount):
        temp = db_query(
            f"SELECT balance FROM customers WHERE username = '{self.__username}';")
        new_balance = amount + temp[0][0]
        db_query(
            f"UPDATE customers SET balance = '{new_balance}' WHERE username = '{self.__username}'; ")
        self.balance_enquiry()
        db_query(f"INSERT INTO {self.__username}_transaction VALUES ("
                 f"'{datetime.datetime.now()}',"
                 f"'{self.__account_number}',"
                 f"'Amount Deposit',"
                 f"'{amount}'"
                 f")")
        print(f"{self.__username} Amount is Successfully Deposited into Your Account {self.__account_number}")

    def withdraw(self, amount):
        temp = db_query(
            f"SELECT balance FROM customers WHERE username = '{self.__username}';")
        if amount > temp[0][0]:
            print("Insufficient Balance Please Deposit Money")
        else:
            new_balance = temp[0][0] - amount
            db_query(
                f"UPDATE customers SET balance = '{new_balance}' WHERE username = '{self.__username}'; ")
            self.balance_enquiry()
            db_query(f"INSERT INTO {self.__username}_transaction VALUES ("
                     f"'{datetime.datetime.now()}',"
                     f"'{self.__account_number}',"
                     f"'Amount Withdraw',"
                     f"'{amount}'"
                     f")")
            print(f"{self.__username} Amount is Successfully Withdrawn from Your Account {self.__account_number}")

    def fund_transfer(self, receive, amount):
        temp = db_query(
            f"SELECT balance FROM customers WHERE username = '{self.__username}';")
        if amount > temp[0][0]:
            print("Insufficient Balance Please Deposit Money")
        else:
            temp2 = db_query(
                f"SELECT balance FROM customers WHERE account_number = '{receive}';")
            if temp2 == []:
                print("Account Number Does Not Exist")
            else:
                new_balance_sender = temp[0][0] - amount
                new_balance_receiver = amount + temp2[0][0]
                db_query(
                    f"UPDATE customers SET balance = '{new_balance_sender}' WHERE username = '{self.__username}'; ")
                db_query(
                    f"UPDATE customers SET balance = '{new_balance_receiver}' WHERE account_number = '{receive}'; ")
                receiver_username = db_query(
                    f"SELECT username FROM customers where account_number = '{receive}';")
                self.balance_enquiry()
                db_query(f"INSERT INTO {receiver_username[0][0]}_transaction VALUES ("
                         f"'{datetime.datetime.now()}',"
                         f"'{self.__account_number}',"
                         f"'Fund Transfer From {self.__account_number}',"
                         f"'{amount}'"
                         f")")
                db_query(f"INSERT INTO {self.__username}_transaction VALUES ("
                         f"'{datetime.datetime.now()}',"
                         f"'{self.__account_number}',"
                         f"'Fund Transfer -> {receive}',"
                         f"'{amount}'"
                         f")")
                print(f"{self.__username} Amount is Successfully Transferred from Your Account {self.__account_number}")

    def show_transactions(self):
        transactions = db_query(f"SELECT * FROM {self.__username}_transaction ORDER BY timedate DESC;")
        if not transactions:
            print("No transactions found.")
        else:
            print(f"\nTransaction History for {self.__username}:")
            for transaction in transactions:
                timedate, account_number, remarks, amount = transaction
                print(f"Date/Time: {timedate}, Account Number: {account_number}, Remarks: {remarks}, Amount: {amount}")
