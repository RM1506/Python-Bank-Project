from register import *
from bank import *

status = False
print("Welcome to Rishabh Banking Project")
while True:
    try:
        register = int(input("1. SignUp\n"
                             "2. SignIn\n"
                             "Enter your choice: "))
        if register == 1 or register == 2:
            if register == 1:
                SignUp()
            if register == 2:
                user = SignIn()
                status = True
                break
        else:
            print("Please Enter Valid Input From Options")

    except ValueError:
        print("Invalid Input Try Again with Numbers")

account_number = db_query(f"SELECT account_number FROM customers WHERE username = '{user}';")

while status:
    print(f"\nWelcome {user.capitalize()} Choose Your Banking Service\n")
    try:
        facility = int(input("1. Balance Enquiry\n"
                             "2. Cash Deposit\n"
                             "3. Cash Withdraw\n"
                             "4. Fund Transfer\n"
                             "5. Show Transactions\n"
                             "6. Exit\n "
                             "Enter your choice: "))
        if facility >= 1 and facility <= 6:
            bobj = Bank(user, account_number[0][0])
            if facility == 1:
                bobj.balance_enquiry()
            elif facility == 2:
                while True:
                    try:
                        amount = int(input("Enter Amount to Deposit: "))
                        bobj.deposit(amount)
                        mydb.commit()
                        break
                    except ValueError:
                        print("Enter Valid Input i.e. Number")
                        continue
            elif facility == 3:
                while True:
                    try:
                        amount = int(input("Enter Amount to Withdraw: "))
                        bobj.withdraw(amount)
                        mydb.commit()
                        break
                    except ValueError:
                        print("Enter Valid Input i.e. Number")
                        continue
            elif facility == 4:
                while True:
                    try:
                        receive = int(input("Enter Receiver Account Number: "))
                        amount = int(input("Enter Money to Transfer: "))
                        bobj.fund_transfer(receive, amount)
                        mydb.commit()
                        break
                    except ValueError:
                        print("Enter Valid Input i.e. Number")
                        continue
            elif facility == 5:
                bobj.show_transactions()
            elif facility == 6:
                print("Thanks For Using Banking Services")
                status = False
        else:
            print("Please Enter Valid Input From Options")
            continue

    except ValueError:
        print("Invalid Input Try Again with Numbers")
        continue
