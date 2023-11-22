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

class JuiceOrder:
    def __init__(self, juice, size, quantity, price):
        self.juice = juice
        self.size = size
        self.quantity = quantity
        self.price = price

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
        if validate_juice_data(juice_selection):
            print("Thanks for your order")
            break
        
        print("Your order contains:")
        print(colored(juice_selection, "yellow"))
        print("\n\n")

    return juice_selection

def validate_juice_data(values):
    """
    This function checks if the values provided by the user,
    in the functions get_juice_selection meet the requirements
    in the validate_juice_data. Also validates if the format is correct.
    If any of the requirements is not fulfilled it throws an
    error to inform the user.
    """
    try:
        juice_selection = int(values)

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
    for ind in range(1, 4):
        column = sizes.col_values(ind)
        col_names.append(column[0])

    # define size menu content
    sizes_data = []
    for ind in range(1, 4):
        row = sizes.row_values(ind)
        sizes_data.append(row[:4])

    # print size table
    print(tabulate(sizes_data, headers=col_names, tablefmt="fancygrid") +
          "\n")
    
    while True:
        print("Please enter your juice size of choice (S, M, L)")
        print("Then press Enter when you are ready.\n")

        size_selection = input("Enter your order here:\n")
        if validate_size_data(size_selection):
            print("Thanks for your order")
            break
        
        print("Your order contains:")
        print(colored(size_selection, "yellow"))
        print("\n\n")

    return size_selection

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

        quantity_selection = input("Enter your order here:\n")
        if validate_quantity_data(quantity_selection):
            print("Thanks for your order")
            break

        print("Your order contains:")
        print(colored(quantity_selection, "yellow"))
        print("\n\n")

    return quantity_selection

def validate_quantity_data(values):
    """
    This function checks if the values provided by the user, in the functions
    get_quanity function meet the requirements in the validate_quantity_data.
    Also validates if the format is correct. If any of the requirements is not
    fulfilled it throws an error to inform the user.
    """
    try:
        quantity_selection = int(values)
        if 1 <= quantity_selection <= 10:
            return True
        else:
            raise ValueError(
                f"Please enter a number (1-10)\n you entered {values}")
    except ValueError as e:
        print(colored(f"Invalid data: {e}, please try again\n", color="red"))
        return False

def update_order_worksheet(juice, size, quantity):
    """
    Update order worksheet with juice, size and quantity
    selection, add new row with the list data provided
    """
    print("Updating order...\n")
    order_worksheet = SHEET.worksheet("order")
    order = []
    order.append(juice)
    order.append(size)
    order.append(quantity)
    order_worksheet.append_row(order)
    print("Order updated successfully.\n")

def get_orders():
    """
    Get all order from worksheet and display
    these to customer 
    """
    orders = SHEET.worksheet("order")
    show_orders = orders.get_all_values()

    print(show_orders)

def main():
    """
    Run all program functions
    """
    welcome()
    clear_console()
    juice_selection = get_juice_selection()
    validate_juice_data(juice_selection)
    size_selection = get_size_selection()
    validate_size_data(size_selection)
    quantity = get_quantity()
    validate_quantity_data(quantity)
    update_order_worksheet(juice_selection, size_selection, quantity)
    get_orders()

if __name__ == "__main__":
    main()
