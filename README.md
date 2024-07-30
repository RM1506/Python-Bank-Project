# Bank Management System

Welcome to the Bank Management System, a Python and MySql(RDBMS) based application designed to manage bank accounts efficiently. This system allows users to sign in, sign up, manage their accounts, perform transactions, and check their account details. It features both a command-line interface and a graphical user interface (GUI) built using Tkinter.

## Features

- **Sign In / Sign Up**
  - Check if User is Registered
  - No User Registration

- **Account Management**
  - Same Account
    - Credit / Withdraw
    - Send Money to Another Account
  - Account Details Update
  - Transaction History

- **Banking Facilities**
  - Account Details
  - Registration
  - Account Management
  - Transaction History
  - Balance Enquiry
  - Credit / Withdraw
  - Funds Transfer
  - Date/Time Functions
  - Separate Account Number

## Getting Started

### Prerequisites

Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Installation
1. Install MySQL Connector:
    ```bash
    pip install mysql-connector-python
    ```
2. Clone the repository:
    ```bash
    git clone https://github.com/mohitprajapat2001/Python-Bank-Project
    ```
3. Navigate to the project directory:
    ```bash
    cd Python-Bank-Project
    ```

### Usage
1. Run the Database File Once to Create Required Tables:
    ```bash
    python database.py
    ```
2. Run the application:
    ```bash
    python main.py
    ```
3. Follow the on-screen instructions to navigate through the menu and use the various features of the bank management system.
4. Run the gui.py to start interacting with the GUI:
    ```bash
    gui.py
    ```

## Detailed Features

### Registration

- New users can register by providing personal details and creating an account.

### Sign In / Sign Up

- Users can sign in using their account credentials.
- New users can sign up and create a new account.

### Account Management

- Update account details.
- View and manage the transaction history.
- Enquire about account balance.

### Transactions

- Credit or withdraw money from the account.
- Transfer funds to another account.

### Banking Facilities

- Provides various banking functionalities like balance enquiry, funds transfer, and viewing transaction history.
- Implements object-oriented programming (OOP) for better code management and scalability.
- Each account has a unique account number.

### Date/Time Functions

- Utilizes date and time functions to keep track of transactions and account activities.