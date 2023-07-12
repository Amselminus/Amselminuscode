import sys
import csv
import re
import random
import os
from datetime import date
import time
from encryption import encrypt, decrypt, get_key


class Account:
    def __init__(self):
        # account_number; password
        self._login_information = {}
        self._personal_information = {}

    def login(self):
        while True:
            account_number = input("Account number (8-Digits): ")
            if login_information := self.read_login_information(account_number):
                self._login_information = login_information
                break
        # check if password is correct and then decodes individual personal information, there are 3 tries possiblie before programm shuts down
        counter = 0
        while True:
            if counter == 3:
                sys.exit("Access denied! Too many wrong login-attempts.")
            password = input("Password: ")
            counter += 1
            if password == login_information["password"]:
                # append account number and password to new dict for further use
                self._login_information = {
                    "account_number": account_number,
                    "password": password,
                }
                # decode individual personal information
                self.decode(password, login_information["account_number"] + ".csv")
                self._personal_information = self.read_personal_information(
                    self._login_information["account_number"] + ".csv"
                )
                return True

    def read_login_information(self, account_number):
        # decodes the login_information.csv to get access to passwords + numbers
        self.decode("GLOBAL", "login_information.csv")
        with open("login_information.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if account_number == row["account_number"]:
                    # returns row (dict of password + number)
                    return row

    def logout(self):
        # encrypt personal information with inidvidual password
        self.safe_personal_information(
            str(self._login_information["account_number"]) + ".csv",
            self._personal_information,
        )
        self.encode(
            self._login_information["password"],
            str(self._login_information["account_number"]) + ".csv",
        )
        os.remove(str(self._login_information["account_number"]) + ".csv")
        # encrypt login information with global password
        self.encode("GLOBAL", "login_information.csv")
        os.remove("login_information.csv")

    def delete_line(self, birth):
        filenames = ["personal_information.csv", "login_information.csv"]
        for file in filenames:
            with open(file, "r") as f:
                lines = f.readlines()
            with open(file, "w") as f:
                for line in lines:
                    information = line.split(",")
                    #personal_information not deleted!!
                    if file == "personal_information.csv":
                        if information[4] != birth:
                            f.write(line)
                    else:
                        if information[0] != self._login_information["account_number"]:
                            f.write(line)

    def delete_account(self, birth):
        self.delete_line(birth)
        self.encode("GLOBAL", "login_information.csv")
        os.remove("login_information.csv")
        os.remove(str(self._login_information["account_number"]) + ".csv")
        os.remove("encrypted-" + str(self._login_information["account_number"]) + ".csv")

    def encode(self, password, filename):
        encrypt(get_key(password), "/workspaces/126971925/final_project/" + filename)

    def decode(self, password, filename):
        decrypt(get_key(password), "/workspaces/126971925/final_project/encrypted-" + filename)

    def read_personal_information(self, filename):
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                return row

    def safe_personal_information(self, filename, dict):
        with open(filename, "w", newline="") as file:
            key_list = list(dict.keys())
            csv_writer = csv.DictWriter(file, key_list)
            csv_writer.writeheader()
            csv_writer.writerow(dict)

    def withdraw(self):
        while True:
            try:
                withdrawel = int(input("Withdraw: "))
                break
            except ValueError:
                pass
        new_balance = int(self._personal_information["balance"]) - withdrawel
        if new_balance < 0:
            # maybe get dept?
            print("Invalid Input")
        else:
            self._personal_information["balance"] = new_balance
            print("Transaction successful")

    def deposit(self):
        while True:
            try:
                deposition = int(input("Deposit: "))
                break
            except ValueError:
                pass
        new_balance = int(self._personal_information["balance"]) + deposition
        self._personal_information["balance"] = new_balance
        print("Transaction successful")

    def show_balance(self):
        print(f"Balance: {self._personal_information['balance']} $")

    def test_birth(self, birth):
        if self._personal_information["birth"] == birth:
            return True

    def transfer(self):
        while True:
            transfer_money = input(
                "Transfer ('amount-of-money', '8-digit-account-number'): "
            )
            # test validity of money, account-number input
            if transfer_money := re.search(r"^([0-9]+), ([0-9]{8})$", transfer_money):
                #test if its the own account number
                if transfer_money.group(2) != self._login_information["account_number"]:
                    # test new login information and then get dict of (account_number, password)
                    if new_login_information := self.read_login_information(
                        transfer_money.group(2)
                    ):
                        # dict of personal information (first, last, address, etc.)
                        new_personal_information = {}
                        # decode personal information of other customer
                        self.decode(
                            new_login_information["password"],
                            new_login_information["account_number"] + ".csv",
                        )
                        # add values to dict
                        new_personal_information = self.read_personal_information(
                            new_login_information["account_number"] + ".csv"
                        )
                        # add money to balance of other customer
                        new_balance = int(new_personal_information["balance"]) + int(
                            transfer_money.group(1)
                        )
                        new_personal_information["balance"] = new_balance

                        my_balance = int(self._personal_information["balance"]) - int(
                            transfer_money.group(1)
                        )
                        if my_balance < 0:
                            print("Not enough money")
                            os.remove(new_login_information["account_number"] + ".csv")
                            return True
                        self._personal_information["balance"] = my_balance
                        # override old personal information file
                        self.safe_personal_information(
                            new_login_information["account_number"] + ".csv",
                            new_personal_information,
                        )
                        # encrypt file
                        self.encode(
                            new_login_information["password"],
                            str(new_login_information["account_number"]) + ".csv",
                        )
                        # delete decoded account
                        os.remove(new_login_information["account_number"] + ".csv")
                        print("Transaction successful")
                        return True
            print("Invalid input")

    @property
    def login_information(self):
        return self._login_information

    @property
    def personal_information(self):
        return self._personal_information


class Create_Account:
    def __init__(self):
        self._customer = {}
        self._login = {}

    def get_personal_inforamtion(self):
        first, last = self.get_name()
        # safe information in dict
        self._customer = {
            "first": first,
            "last": last,
            "address": self.get_address(),
            "birth": self.get_birth(),
            "email": self.get_email(),
            "balance": 0,
        }

    def get_login_information(self):
        # safe information in dict
        self._login = {
            "account_number": self.generate_account_number(),
            "password": self.get_password(),
        }
        print("Your account number is: " + str(self.login["account_number"]))

    def safe_personal_information_overview(self):
        # write personal information in csv file
        with open("personal_information.csv", "a", newline="") as file:
            key_list = list(self._customer.keys())
            csv_writer = csv.DictWriter(file, key_list)
            csv_writer.writerow(self._customer)
        # encode csv file
        # self.encode("personal_information.csv", "GLOBAL")

    def safe_personal_information_individual(self):
        # write personal information in csv file
        with open(str(self._login["account_number"]) + ".csv", "a", newline="") as file:
            key_list = list(self._customer.keys())
            csv_writer = csv.DictWriter(file, key_list)
            csv_writer.writeheader()
            csv_writer.writerow(self._customer)
        # encode personal_information_individual.csv file with individual set password
        self.encode(
            str(self._login["account_number"]) + ".csv", self._login["password"]
        )
        os.remove(str(self._login["account_number"]) + ".csv")

    def safe_login_information(self):
        # write login information in csv file
        with open("login_information.csv", "a", newline="") as file:
            key_list = ["account_number", "password"]
            csv_writer = csv.DictWriter(file, key_list)
            csv_writer.writerow(self._login)
        # encode login_information.csv file with global password: GLOBAL
        self.encode("login_information.csv", "GLOBAL")

    def encode(self, filename, password):
        encrypt(get_key(password), "/workspaces/126971925/final_project/" + filename)

    def get_password(self):
        # print rules for password
        print("\nThe password"
              "\n  - must include at least 1 lower-case letter."
              "\n  - must include at least 1 upper-case letter."
              "\n  - must include at least 1 number."
              "\n  - must include at least 1 special character (!#%)."
        )
        # check if rules for password are being followed
        while True:
            password = input("Password: ")
            if re.search(
                r"^(?=[^a-z]*[a-z])(?=[^A-Z]*[A-Z])(?=\D*\d)(?=[^_!#%]*[_!#%])[A-Za-z0-9_!#%]{8,32}$",
                password,
            ):
                confirm_password = input("Confirm password: ")
                if password == confirm_password:
                    return password


    def generate_account_number(self):
        # create list with every customer´s account number
        decrypt(get_key("GLOBAL"), "/workspaces/126971925/final_project/encrypted-login_information.csv")
        numbers = []
        with open("login_information.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                numbers.append(row["account_number"])

        # check if new account number already exists in list
        while True:
            account_number = str(random.randrange(10000000, 99999999))
            if account_number not in numbers:
                return account_number

    def get_name(self):
        while True:
            name = input("Full name (first, last): ").strip().title()
            if name := re.search(r"^([a-z]+)\, ([a-z]+)$", name, re.IGNORECASE):
                return name.group(1), name.group(2)

    def get_address(self):
        while True:
            address = (
                input("Full address ('street' 'number', 'zip' 'town'): ")
                .strip()
                .title()
            )
            if address := re.search(
                r"^([a-z]+ .+\, [\d]+ [a-z]+)$", address, re.IGNORECASE
            ):
                return address.group(1)

    def get_birth(self):
        while True:
            birth = input("Date of birth ('yyyy-mm-dd'): ").strip()
            if valid_birth := re.search(
                r"^([0-9]+)-([0-9]+)-([0-9]+)$", birth, re.IGNORECASE
            ):
                try:
                    date(
                        int(valid_birth.group(1)),
                        int(valid_birth.group(2)),
                        int(valid_birth.group(3)),
                    )
                    return birth
                except ValueError:
                    continue

    def get_email(self):
        while True:
            email = input("Email: ").strip().lower()
            if email := re.search(
                r"^([a-z0-9]+[.-_]*[a-z0-9]+@[a-z0-9-]+\.[a-z]{2,})+$", email
            ):
                return email.group(1)

    @property
    def customer(self):
        return self._customer

    @property
    def login(self):
        return self._login


def main():
    while True:
        start = input("Do you have an account (Yes/No)? Do you want to delete an account (Delete)? ")
        if start == "Yes":
            take_action()
        elif start == "No":
            registration()
            take_action()
        elif start == "Delete":
            delete_account()
        else:
            print("Invalid input")


def registration():
    c = Create_Account()
    c.get_personal_inforamtion()
    c.get_login_information()
    c.safe_personal_information_overview()
    c.safe_personal_information_individual()
    c.safe_login_information()
    return True


def take_action():
    a = Account()
    if a.login():
        start = time.time()
        print("Now you are ready to go!")
        while True:
            end = time.time()
            if (int(end)-int(start) > 60):
                print("New Login required! Timelimit exeeded.")
                a.logout()
                break
            print(
                "\nYou can select the following options: "
                "\n1. Deposit"
                "\n2. Withdraw"
                "\n3. Transfer"
                "\n4. Balance"
                "\n5. Logout"
            )
            action = input("\nType in one option from above: ").strip()
            if action == "Deposit":
                a.deposit()
            elif action == "Withdraw":
                a.withdraw()
            elif action == "Transfer":
                if a.transfer():
                    continue
            elif action == "Balance":
                a.show_balance()
            elif action == "Logout":
                a.logout()
                break
            else:
                print("Invalid Input")


def delete_account():
    a = Account()
    if a.login():
        while True:
            final_confirmation = input("Do you really want to delete your account (Yes/No)? ")
            if final_confirmation == "No":
                break
            elif final_confirmation == "Yes":
                birth = input("Date of birth ('yyyy-mm-dd'): ")
                if a.test_birth(birth):
                    a.delete_account(birth)
                    break
                else:
                    print("Birthday does not match!")
                    continue
            else:
                print("Invalid Input")


if __name__ == "__main__":
    main()