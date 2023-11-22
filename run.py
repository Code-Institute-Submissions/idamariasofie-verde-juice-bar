import os
import time
import gspread
from google.oauth2.service_account import Credentials
from termcolor import colored
from pyfiglet import figlet_format, Figlet
from tabulate import tabulate

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('verde_juice_bar')


def clear_console():
    """
    This function clears the console screen.
    The code checks whether the operating system
    is posix (as in Linux or macOS) or not, and runs the
    appropriate command to clear the screen.
    Code taken from geeksforgeeks.org
    """
    if os.name == "posix":
        _ = os.system("clear")
    else:
        _ = os.system("cls")


def welcome():
    """
    Verde Juice bar logo to welcome user
    parts of code from MiguelSanLeon
    Holiday survey
    """
    welcome_message = SHEET.worksheet('other').col_values(1)
    clear_console()
    print("\n")
    print("\n")
    print("\n")
    print(welcome_message[1])
    print("\n")
    print("Press Enter to continue...")
    time.sleep(5)
    clear_console()


def get_juice_selection():
    """
    Displays juice menu for the user to select from.
    Get juice order value input from the user.
    """
    clear_console()

    juices = SHEET.worksheet("menu")
    data = juices.get_all_values()

    # define header names
    col_names = data[0]

    # define menu content and set width for Ingredients column
    menu_data = data[-5:]
    for row in menu_data:
        if len(row[2]) > 45:
            last_space_index = row[2][:45].rfind(" ")
            row[2] = row[2][:last_space_index + 1] + "\n" + row[2][last_space_index + 1:]

    # print juice menu table
    print(tabulate(menu_data, headers=col_names, tablefmt="fancy_grid") + "\n")

    while True:
        print("Welcome to The Juice Bar's order system")
        print("Please enter your juice of choice (1-5)")
        print("Then press Enter when you are ready.\n")

        juice_selection = input("Enter your order here:\n")
        # creates a list with every value inserted by the user
        user_data = juice_selection.split(" ")
        if validate_juice_data(user_data):
            print("Thanks for your order")
            continue
        else:
            print("Your order contains:")
            for order in user_data:
                print(colored(order.get_string(), "yellow"))
                print("\n\n")
            continue

        print("We get you to the next step...")
        break

    return user_data[0]


def validate_juice_data(values):
    """
    This function checks if the values provided by the user,
    in the functions get_juice_selection meet the requirements
    in the validate_juice_data. Also validates if the format is correct.
    If any of the requirements is not fulfilled it throws an
    error to inform the user.
    """
    try:
        if len(values) != 1:
            raise ValueError(f"Please enter 1 value you entered {len(values)}")

        juice_selection = int(values[0])

        if 1 <= juice_selection <= 5:
            return True
        else:
            raise ValueError(
                f"Please enter a number (1-5)\n you entered {int(values)}")
    except ValueError as e:
        print(colored(f"Invalid data: {e}, please try again\n"))
        return False

def get_size_selection():
    """
    Displays juice menu for the user to select from.
    Get juice order value input from the user.
    """
    clear_console()

    sizes = SHEET.worksheet("options")
    sizes_data = sizes.get_all_values()

    # define header names
    col_names = []
    for ind in range(1, 3):
        column = sizes.col_values(ind)
        col_names.append(column[0])

    # define size menu content
    sizes_data = []
    for ind in range(2, 4):
        row = sizes.row_values(ind)
        sizes_data.append(row[:3])

    # print size table
    print(tabulate(sizes_data, headers=col_names, tablefmt="fancygrid") +
          "\n")
    while True:
        print("Please enter your juice size of choice (S, M, L)")
        print("Then press Enter when you are ready.\n")

        size_selection = input("Enter your order here:\n")
        # creates a list with every value inserted by the user
        user_data = size_selection.split(" ")

        if size_selection(user_data, ["S", "M", "L"]):
            print("Thanks for your order...")
        else:
            print("We get you to the next step...")
            time.sleep(1)
        break

    return user_data[0]

def validate_size_data(values):
    """
    This function checks if the values provided by the user, in the functions
    get_size_selection meet the requirements in the validate_size_data.
    Also validates if the format is correct. If any of the requirements is not
    fulfilled it throws an error to inform the user.
    """
    try:
        size_selection = values.upper()
        if size_selection in ['S', 'M', 'L']:
            return True
        else:
            raise ValueError(
                f"Please enter size S, M or L)\n you entered {values}")
    except ValueError as e:
        print(colored(f"Invalid data: {e}, please try again\n", color="red"))
        return False

def get_quantity():
    """
    Get quantity value input from the user
    """
    clear_console()

    while True:
        print("Please insert the quantity that you want, (not more than 10) ")
        print("Then press Enter when you are ready.\n")

        juice_quantity = input("Enter your order here:\n")
        # creates a list with every value inserted by the user
        user_data = juice_quantity.split(" ")

        if validate_data(user_data, ["1", "2", "3", "4", "5", "6", "7", "8",
                                     "9", "10"]):
            print("Thanks for your order")
        else:
            print("We get you to the next step...")
            break

    return user_data[0]

def main():
    """
    Run all program functions
    """
    welcome()
    clear_console()
    get_juice_selection()
    validate_juice_data()
    get_size_selection()

if __name__ == "__main__":
    main()
