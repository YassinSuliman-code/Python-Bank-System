import csv
import re


class InsufficientFundsError(Exception):
    """Raised when a withdrawal would result in a negative balance."""
    pass

class UsernameError(Exception):
    """Raised when a user's username violates username rules."""
    pass

class PasswordError(Exception):
    """Raised when a user's password violates password rules."""


class Account:
    def __init__(self, username, password, money=0):
        self.username = username
        self.password = password
        self.money = money

    def deposit(self, n: int):
        if int(n) <= 0:
            raise ValueError

        user_money = int(self.money) + int(n)
        self.money = user_money

        with open("accounts.csv") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            for account in rows:
                if account["username"] == self.username:
                    account["money"] = user_money
                    break

        with open("accounts.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["username", "password", "money"])
            writer.writeheader()
            writer.writerows(rows) 

    def withdraw(self, n: int):
        if int(n) <= 0:
            raise ValueError

        user_money = int(self.money) - int(n)
        
        if user_money < 0:
            raise InsufficientFundsError
        
        self.money = user_money

        with open("accounts.csv") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            for account in rows:
                if account["username"] == self.username:
                    account["money"] = user_money
                    break

        with open("accounts.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["username", "password", "money"])
            writer.writeheader()
            writer.writerows(rows)

    def change_password(self, new_password: str):
        while(True):
            confirm_new = input("Confirm your new password: ")
            if confirm_new != new_password:
                print("Incorrect. Make sure to write your new password correctly.")
            else:
                break

        while(True):
            old = input("Enter your old password: ")
            if old != self.password:
                print("Incorrect. Make sure you enter your old password correctly.")
            else:
                break
        
        while(True):
            choice = input(f"Are you sure you want to change your password \"{self.password}\" to \"{new_password}\"? (Yes/No)\n")

            if choice == "Yes":
                with open("accounts.csv") as file:
                    reader = csv.DictReader(file)
                    rows = list(reader)
                    for account in rows:
                        if account["username"] == self.username:
                            account["password"] = new_password
                            break

                with open("accounts.csv", "w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=["username", "password", "money"])
                    writer.writeheader()
                    writer.writerows(rows)

                self.password = new_password

                print("Password changed successfully.")
                return

            elif choice == "No":
                print("Action cancelled. Password has not been changed.")
                return

            else:
                print("Please choose either \"Yes\" or \"No\"")


        

def main():
    print("Welcome to Python's Bank!")
    while(True):
        choice = input("Would you like to Log-in or Sign-up?\n")
        if choice.lower() == "sign-up" or choice.lower() == "sign up":
            user = create_account()
            break
        elif choice.lower() == "log-in" or choice.lower() == "log in":
            user = log_in()
            break
        else:
            print("please choose a valid command.")

    print(f"Welcome {user.username}! We are glad to have you with us today!")

    while(True):
        command = input("Enter desired service: ")

        if command.lower() == "deposit":
            try:
                amount = int(input("Enter amount desired to deposit: "))
                identity_check(user)
                user.deposit(amount)
            except ValueError:
                print("Invalid amount. Please enter a positive numeric value.")
            else:
                print("Deposit successful.")
            
        elif command.lower() == "withdraw" or command.lower() == "withdrawal":
            try:
                amount = int(input("Enter amount desired to be withdrawn: "))
                identity_check(user)
                user.withdraw(amount)               
            except ValueError:
                print("Invalid amount. Please enter a positive numeric value.")
            except InsufficientFundsError:
                print("Insufficient funds in your account.")
            else:
                print("Withdrawal successful.")

        elif command.lower() == "get balance" or command.lower() == "show balance":
            identity_check(user)
            print(f"Your current balance is: {user.money} USD")

        elif command.lower() == "change password":
            new_password = verify_new_password(user)
            user.change_password(new_password)

        elif command.lower() == "transfer":
            identity_check(user)
            transfer(user)
            
        elif command.lower() == "exit":
            print("Thank you for using Pythons Bank, have a great day!")
            break
        else:
            print("Please make sure to enter a valid command.")

def create_account():
    while(True):
        try:
            username = get_username(input("Enter your username: "))
        except(UsernameError):
            continue
        else:
            break

    while(True):
        try:
            password = get_password(input("Enter your password: "), username)
        except(PasswordError):
            continue
        else:
            break

    with open("accounts.csv", "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["username", "password", "money"])
        writer.writerow({"username": username, "password": password, "money": 0})

    account = Account(username, password, 0)
    return account


def get_username(username):
    if matches := re.search(r"^(?=^.{6,20}$)[A-Za-z]+[A-Za-z0-9_\.]*[A-Za-z0-9]+$", username):
        pass
    else:
        print("Invalid Username.")
        raise UsernameError

    with open("accounts.csv") as file:
        reader = csv.DictReader(file)
        for account in reader:
            if username == account["username"]:
                print("This username is already used")
                raise UsernameError

    return username


def get_password(password, username):
    if matches := re.search(r"^(?=^.{8,32}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*()_+\-=])(?!.*\s)[A-Za-z0-9!@#$%^&*()_+\-=]+$", password):
        if username.lower() in password.lower():
            print("Username can't be in password.")
            raise PasswordError
        else:
            return password

    else:
        print("Invalid Password.")
        raise PasswordError

def log_in():
    username = input("Enter your username: ")

    username_found = False
    with open("accounts.csv") as file:
        reader = csv.DictReader(file)
        for account in reader:
            if account["username"] == username:
                username_found = True
                user_password = account["password"]
                user_money = account["money"]

    if not username_found:
        print("Invalid Username, please make sure you enter your username correctly.")
        return log_in()

    while(True):
        password = input("Enter your password: ")
        if password == user_password:
            break
        else:
            print("Invalid Password, please make sure you enter your password correctly.")

    return Account(username, password, user_money)

def identity_check(user):
    password = input("Enter your password to verify your identity: ")
    while(user.password != password):
        print("Incorrect Password.")
        password = input("Enter password: ")

def verify_new_password(user):
    new_password = input("Enter new password: ")

    if matches := re.search(r"^(?=^.{8,32}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*()_+\-=])(?!.*\s)[A-Za-z0-9!@#$%^&*()_+\-=]+$", new_password):
        if user.username.lower() in new_password.lower():
            print("Username can't be in password.")
            return verify_new_password(user)
        elif user.password.lower() == new_password.lower():
            print("Password already in use.")
            return verify_new_password(user)
        else:
            return new_password
    else:
        print("Invalid Password.")
        return verify_new_password(user)

def transfer(user):
    while(True):
        try:
            amount = confirm_amount(input("Enter amount to be transferred: "), user)
        except ValueError:
            print("Invalid amount. Please enter a positive numeric value.")
            continue
        except InsufficientFundsError:
            print("Insufficient funds in your account.")
            continue
        else:
            break

    reciever_password, reciever_money, reciever_username = find_reciever(input("Enter username of reciever: "))

    while(True):
        choice = input(f"Are you sure you want to transfer {amount} USD to {reciever_username}? (Yes/No)\n")

        if choice == "Yes":
            reciever = Account(reciever_username, reciever_password, reciever_money)
            user.withdraw(amount)
            reciever.deposit(amount)
            print("Tranfer successful.")
            return
        elif choice == "No":
            print("Action cancelled.")
            return
        else:
            print("Please choose either \"Yes\" or \"No\"")

def confirm_amount(amount, user):
    amount = int(amount)

    if amount > int(user.money):
        raise InsufficientFundsError
    if amount <= 0:
        raise ValueError

    return amount

def find_reciever(reciever_username):
    found = False
    with open("accounts.csv") as file:
        reader = csv.DictReader(file)
        for account in reader:
            if account["username"] == reciever_username:
                reciever_password = account["password"]
                reciever_money = account["money"]
                found = True
                break
    
    if found:
        return reciever_password, reciever_money, reciever_username
    else:
        print("Reciever doesn't exsist, please make sure to enter the reciever's username correctly.")
        return find_reciever(input("Enter username of reciever: "))


if __name__ == "__main__":
    main()
