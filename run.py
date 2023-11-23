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
        """
        Initialize JuiceOrder with juice, size, quantity, and price.
        """
        self.juice = juice
        self.size = size
        self.quantity = quantity
        self.price = price


def clear_console():
    """
    Clear the console screen based on the operating system.
    Code taken from geeksforgeeks.org
    """
    if os.name == "posix":
        _ = os.system("clear")
    else:
        _ = os.system("cls")


def welcome():
    """
    Display the welcome message and loading screen.
    Part of code taken from GitHub,
    user MiguelSanLeon.
    """
    welcome_message = SHEET.worksheet('other').col_values(1)
    clear_console()
    print("\n")
    print(welcome_message[1])
    print("Loading...")
    time.sleep(5)
    clear_console()


def get_juice_selection():
    """
    Display the juice menu in a grid.
    And get the user's juice selection.
    Validates the selection.
    Parts of code taken from GitHub,
    user useriasminna.
    """
    clear_console()

    juices = SHEET.worksheet("menu")
    data = juices.get_all_values()

    col_names = data[0]
    menu_data = data[-5:]
    for row in menu_data:
        if len(row[2]) > 45:
            last_space_index = row[2][:45].rfind(" ")
            row[2] = (row[2][:last_space_index + 1] +
                      "\n" +
                      row[2][last_space_index + 1:])

    print(tabulate(menu_data, headers=col_names, tablefmt="fancy_grid") + "\n")

    while True:
        print("Welcome to The Juice Bar's order system")
        print("Please enter your juice of choice (1-5)")
        print("Then press Enter when you are ready.\n")

        juice_selection = input("Enter your order here:\n")
        if validate_juice_data(juice_selection):
            print("Thanks for your order")
            break
        else:
            print("Invalid juice selection. Please try again.")

    return juice_selection


def validate_juice_data(values):
    """
    Validate the user's juice selection.
    And raise error message if not valid.
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
    Display the size menu and get the user's size selection.
    And validates the selection.
    Parts of code taken from GitHub,
    user useriasminna.
    """
    clear_console()

    sizes = SHEET.worksheet("options")
    sizes_data = sizes.get_all_values()

    col_names = sizes_data[0][:3]
    sizes_data = sizes_data[1:4]

    print(tabulate(sizes_data, headers=col_names, tablefmt="fancygrid") + "\n")

    while True:
        print("Please enter your juice size of choice (S, M, L)")
        print("Then press Enter when you are ready.\n")

        size_selection = input("Enter your order here:\n")
        if validate_size_data(size_selection):
            print("Thanks for your order")
            break
        else:
            print("Invalid size selection. Please try again.")

    return size_selection


def validate_size_data(values):
    """
    Validate the user's size selection.
    Raise error message if not valid.
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
    Get the quantity value input from the user.
    And validates it.
    """
    clear_console()

    while True:
        print("Please insert the quantity that you want, (not more than 10) ")
        print("Then press Enter when you are ready.\n")

        quantity_selection = input("Enter your order here:\n")
        if validate_quantity_data(quantity_selection):
            print("Thanks for your order")
            break
        else:
            print("Invalid quantity selection. Please try again.")

    return quantity_selection


def validate_quantity_data(values):
    """
    Validate the user's quantity selection.
    Raise error message if not valid.
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
    Update the order worksheet with juice, size, and quantity selection.
    Part of code taken from GitHub,
    user useriasminna.
    """
    print("Updating order...\n")
    order_worksheet = SHEET.worksheet("order")
    order = [juice, size, quantity]
    order_worksheet.append_row(order)
    print("Order updated successfully.\n")


def get_orders(juice_selection, size_selection, quantity):
    """
    Get all orders from the worksheet and displays
    them to the user.
    """
    juices = {
        1: "Green Green Goddess",
        2: "Energized",
        3: "Fruits and veggies",
        4: "Iron woman",
        5: "Keep the doctor away"
    }

    juice_selection = int(juice_selection)

    selected_juice = juices.get(juice_selection)
    if selected_juice:
        print(f"You selected juice {selected_juice}")
    else:
        print("Invalid juice selection")

    sizes = ['S', 'M', 'L']
    quantities = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    size_selection = size_selection
    quantity_selection = int(quantity)

    if size_selection in sizes:
        print(f"You selected size {size_selection}")
    else:
        print("Invalid size selection")

    if quantity_selection in quantities:
        print(f"You have added {quantity_selection} to your order")
    else:
        print("Invalid quantity")

    return quantity_selection


def calculate_price(size_selection, quantity_selection):
    """
    Calculate the total price of the juices
    added to the order.
    """
    juice_price = 0

    if size_selection == "S":
        juice_price = 4
    elif size_selection == "M":
        juice_price = 5
    elif size_selection == "L":
        juice_price = 6
    else:
        juice_price = 6

    print(f"Total price: {juice_price * quantity_selection} €")
    return juice_price * quantity_selection


def goodbye():
    """
    Displays the thank you message and end the order.
    Part of code taken from GitHub,
    user MiguelSanLeon.
    """
    goodbye_message = SHEET.worksheet('other').col_values(2)
    print("\n")
    print(goodbye_message[1])
    print("\n")
    print("Welcome back...")


def main():
    """
    Run all program functions.
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
    quantity_selection = get_orders(juice_selection, size_selection, quantity)
    total_price = calculate_price(size_selection, quantity_selection)
    time.sleep(5)
    goodbye()
    time.sleep(10)


main()
