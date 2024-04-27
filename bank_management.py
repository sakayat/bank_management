import random


class Bank:
    def __init__(self, name):
        self.name = name
        self.total_bank_balance = 3400
        self.bank_accounts = []
        self.loans = 0
        self.loan_feature_access = ""

    def bank_balance(self):
        if self.total_bank_balance > 0:
            print(f"Current balance: {self.total_bank_balance}")
        if self.total_bank_balance < 0:
            print("The bank is bankrupt")

    def add_account(self, account):
        self.bank_accounts.append(account)


class Account:
    def __init__(self, name, email, address, account_type, bank) -> None:
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.account_number = random.randint(10000, 99999)
        self.transition_history = []
        self.loan_count = 0
        self.bank = bank

    def account_info(self):
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Address: {self.address}")
        print(f"Account Type: {self.account_type}")
        print(f"Balance: {self.balance}")
        print(f"Account Number: {self.account_number}")
        print()

    def deposit(self, amount, account_number):
        if self.account_number == account_number:
            if amount > 0:
                self.balance += amount
                self.transition_history.append(("Deposit", amount))
            else:
                print("Invalid amount to deposit")
        else:
            print("Invalid account number")

    def withdraw(self, amount, account_number):
        if self.account_number == account_number:
            if amount <= self.balance:
                self.balance -= amount
                self.transition_history.append(("Withdraw", amount))
            else:
                print("Withdrawal amount exceeded")
        else:
            print("Invalid account number")

    def check_balance(self):
        print(f"Current balance: {self.balance}")

    def get_loan(self, loan_amount, account_number):
        if self.bank.loan_feature_access:
            if self.loan_count <= 2:
                if self.account_number == account_number:
                    if self.bank.total_bank_balance >= loan_amount:
                        self.balance += loan_amount
                        self.loan_count += 1
                        self.bank.total_bank_balance -= loan_amount
                        self.bank.loans += loan_amount
                        self.transition_history.append(("Loan", loan_amount))
                    else:
                        print("Loan request failed: Insufficient funds in the bank")
                else:
                    print("Invalid account number")
            else:
                print("Loan limit reached")
        else:
            print(f"Loan feature disabled for account {account_number}")

    def transition_info(self, account_number):
        if self.account_number == account_number:
            print("Transaction History:")
            for transaction in self.transition_history:
                print(f"{transaction[0]}: {transaction[1]}")
        else:
            print("Invalid account number")

    def transfer_amount(self, send_account_number, received_account_number, amount):
        send_account_exists = False
        received_account_exists = False

        for user in self.bank.bank_accounts:
            if user.account_number == send_account_number:
                send_account_exists = True
                if user.balance >= amount:
                    user.balance -= amount
                else:
                    print(
                        f"Failed to send money to {received_account_number}: Insufficient balance"
                    )
                    return
            elif user.account_number == received_account_number:
                received_account_exists = True

        if send_account_exists and received_account_exists:
            for user in self.bank.bank_accounts:
                if user.account_number == received_account_number:
                    user.balance += amount
                    print(
                        f"Successfully transferred {amount} to {received_account_number}"
                    )
                    return

        if not send_account_exists:
            print(
                f"Failed to send money to {received_account_number}: Sending account does not exist"
            )
        if not received_account_exists:
            print(
                f"Failed to send money to {received_account_number}: Receiving account does not exist"
            )


class Admin:
    def __init__(self, bank) -> None:
        self.bank = bank

    def add_bank_account(self, account):
        self.bank.add_account(account)

    def delete_account(self, account_number):
        for user in self.bank.bank_accounts:
            if user.account_number == account_number:
                self.bank.bank_accounts.remove(user)
                print(f"Account {account_number} has been deleted.")
            else:
                print("Account not found")

    def show_user_account(self):
        for account in self.bank.bank_accounts:
            print(f"Name: {account.name}")
            print(f"Email: {account.email}")
            print(f"Address: {account.address}")
            print(f"Account Type: {account.account_type}")
            print(f"Balance: {account.balance}")
            print(f"Account Number: {account.account_number}")
            print()

    def total_bank_balance(self):
        print(f"Total Bank Balance: {self.bank.total_bank_balance}")

    def total_loan_amount(self):
        print(f"Total loan amount: {self.bank.loans}")

    def access_loan(self, account_number, enable):
        for user in self.bank.bank_accounts:
            if user.account_number == account_number:
                self.bank.loan_feature_access = enable


def main():
    bank = Bank("My Bank")
    admin = Admin(bank)

    while True:
        print("\n1. Admin Login")
        print("2. User Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            admin_login(admin, bank)
        elif choice == "2":
            user_login(bank)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")


def admin_login(admin, bank):
    while True:
        print("\n1. Add Bank Account")
        print("2. Delete Account")
        print("3. Show User Accounts")
        print("4. Total Bank Balance")
        print("5. Total Loan Amount")
        print("6. Access Loan Feature")
        print("7. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter user name: ")
            email = input("Enter user email: ")
            address = input("Enter user address: ")
            account_type = input("Enter account type: ")
            account = Account(name, email, address, account_type, bank)
            admin.add_bank_account(account)
        elif choice == "2":
            account_number = int(input("Enter account number to delete: "))
            admin.delete_account(account_number)
        elif choice == "3":
            admin.show_user_account()
        elif choice == "4":
            admin.total_bank_balance()
        elif choice == "5":
            admin.total_loan_amount()
        elif choice == "6":
            account_number = int(input("Enter account number: "))
            enable = input("Enable or Disable loan feature (yes/no): ")
            admin.access_loan(account_number, enable.lower() == "yes")
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")


def user_login(bank):
    account_number = int(input("Enter your account number: "))
    for account in bank.bank_accounts:
        if account.account_number == account_number:
            while True:
                print("\n1. Account Info")
                print("2. Deposit")
                print("3. Withdraw")
                print("4. Check Balance")
                print("5. Get Loan")
                print("6. Transaction History")
                print("7. Transfer Amount")
                print("8. Logout")
                choice = input("Enter your choice: ")

                if choice == "1":
                    account.account_info()
                elif choice == "2":
                    amount = float(input("Enter deposit amount: "))
                    account.deposit(amount, account_number)
                elif choice == "3":
                    amount = float(input("Enter withdraw amount: "))
                    account.withdraw(amount, account_number)
                elif choice == "4":
                    account.check_balance()
                elif choice == "5":
                    amount = float(input("Enter loan amount: "))
                    account.get_loan(amount, account_number)
                elif choice == "6":
                    account.transition_info(account_number)
                elif choice == "7":
                    received_account_number = int(
                        input("Enter received account number: ")
                    )
                    amount = float(input("Enter transfer amount: "))
                    account.transfer_amount(
                        account_number, received_account_number, amount
                    )
                elif choice == "8":
                    break
                else:
                    print("Invalid choice. Please try again.")
            return
    print("Account not found.")



main()
