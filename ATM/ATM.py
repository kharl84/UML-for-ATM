import sqlite3
import random

class Bank:
    def __init__(self, bank_name):
        self.bank_name = bank_name

class Customer:
    def __init__(self, username, pin, name, account_number=None, balance=0):
        self.username = username
        self.pin = pin
        self.name = name
        self.account_number = account_number if account_number else self.generate_account_number()
        self.balance = balance

    def generate_account_number(self):
        return str(random.randint(10000000, 99999999))

    def deposit(self, amount):
        self.balance += amount
        return True

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True
        else:
            print("Insufficient funds.")
            return False

class ATM:
    def __init__(self, bank, customers):
        self.bank = bank
        self.customers = customers

    def authenticate_customer(self, username, pin):
        customer = next((cust for cust in self.customers if cust.username == username and cust.pin == pin), None)
        return customer is not None

    def create_customer(self, username, pin, name):
        new_customer = Customer(username, pin, name)
        self.customers.append(new_customer)
        return new_customer
    
    def check_balance(self, customer):
        return customer.balance

    def deposit_funds(self, customer, amount):
        return customer.deposit(amount)

    def withdraw_cash(self, customer, amount):
        return customer.withdraw(amount)

def load_customers_from_database():
    customers = []
    with sqlite3.connect("bank.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                username TEXT PRIMARY KEY,
                pin TEXT,
                name TEXT,
                account_number TEXT,
                balance REAL
            )
        """)
        cursor.execute("SELECT username, pin, name, account_number, balance FROM customers")
        rows = cursor.fetchall()
        for row in rows:
            customers.append(Customer(*row))
    return customers

class Technician:
    def perform_maintenance(self, atm):
        # Placeholder for maintenance actions
        print("Technician performing maintenance on the ATM.")

    def perform_repairs(self, atm):
        # Placeholder for repair actions
        print("Technician performing repairs on the ATM.")

    def replenish_cash(self, atm, amount):
        # Placeholder for cash replenishment actions
        print(f"Technician replenishing ATM with ${amount}.")

    def upgrade_hardware(self, atm):
        # Placeholder for hardware upgrade actions
        print("Technician upgrading hardware on the ATM.")

    def upgrade_firmware(self, atm):
        # Placeholder for firmware upgrade actions
        print("Technician upgrading firmware on the ATM.")

def technician_operations(atm, technician):
     print("\nTechnician Operations:")
     print("1 - Perform Maintenance \t 2 - Perform Repairs \t 3 - Replenish Cash \t 4 - Upgrade Hardware \t 5 - Upgrade Firmware")
    
     operation = input("\nEnter technician operation (1-5): ")

     if operation == "1":
        technician.perform_maintenance(atm)
     elif operation == "2":
        technician.perform_repairs(atm)
     elif operation == "3":
        amount = float(input("Enter amount to replenish: "))
        technician.replenish_cash(atm, amount)
     elif operation == "4":
        technician.upgrade_hardware(atm)
     elif operation == "5":
        technician.upgrade_firmware(atm)
     else:
        print("Invalid technician operation. Try again.")

def main():
    bank = Bank("Example Bank")
    customers = load_customers_from_database()
    atm = ATM(bank, customers)
    technician = Technician()

    username = input("Set Your Username: ")
    pin = input("Set Your PIN: ")
    name = input("Enter Your Full Name: ")

    if atm.authenticate_customer(username, pin):
        print(f" Logging in...")
        customer = next(cust for cust in customers if cust.username == username)
    else:
        customer = atm.create_customer(username, pin, name)
        print(f"New customer account created for {customer.username}")

    while True:
        print(f"\nWelcome {customer.name}! \n1 - Check Balance \t 2 - Deposit Funds \t 3 - Withdraw Cash \t 4 - Technician Operations \t 5 - Quit ")

        selection = input("\nEnter your selection (1-5): ")

        if selection == "1":
            balance = atm.check_balance(customer)
            print("Customer Account Number:", customer.account_number)
            print("Customer Name:", customer.name)
            print("Your Balance is:", balance)
        elif selection == "2":
            amount = float(input("Enter amount to deposit: "))
            success = atm.deposit_funds(customer, amount)
            if success:
                print("Deposit successfully. New Balance is:", customer.balance)
        elif selection == "3":
            amount = float(input("Enter amount to withdraw: "))
            success = atm.withdraw_cash(customer, amount)
            if success:
                print("Withdrawal successful. Updated Balance:", customer.balance)
        elif selection == "4":
            technician_operations(atm, technician)
        elif selection == "5":
            print("Thank you for using our ATM.")
            with sqlite3.connect("bank.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT OR REPLACE INTO customers VALUES (?, ?, ?, ?, ?)",
                               (customer.username, customer.pin, customer.name, customer.account_number, customer.balance))
                conn.commit()
            exit()
        else:
            print("Invalid selection. Try again.")

if __name__ == "__main__":
    main()
