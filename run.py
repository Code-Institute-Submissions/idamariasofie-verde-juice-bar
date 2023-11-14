import os
import gspread
from google.oauth2.service_account import Credentials
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

def get_juice_selection():
    """
    Displays juice menu for the user to select from.
    Get juice order value input from the user.
    """
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

    juices = SHEET.worksheet("menu")
    data = juices.get_all_values()

    # define header names
    col_names = data[0]

    # define menu content and set width for Ingredients column
    menu_data = data[-5:]
    for row in menu_data:
        if (len(row[2]) > 45):
            last_space_index = row[2][:45].rfind(" ")
            row[2] = row[2][:last_space_index + 1] + "\n" \
                + row[2][last_space_index + 1:]

    # print juice menu table
    print(tabulate(menu_data, headers=col_names, tablefmt="fancy_grid") +
          "\n")

    while True:
        print("Welcome to The Juice Bar's order system")
        print("Please enter your juice of choice (1-5)")
        print("Then press Enter when you are ready.\n")

        juice_selection = input("Enter your order here:\n")
        if validate_juice_data(juice_selection):
            print("Thanks for your order")
            break
    return juice_selection

def validate_juice_data(values):
    """
    This function checks if the values provided by the user, in the functions
    get_juice_selection meet the requirements in the validate_juice_data.
    Also validates if the format is correct. If any of the requirements is not
    fulfilled it throws an error to inform the user.
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
        print(f"Invalid data: {e}, please try again\n")
        return False

def get_size_selection():
    """
    Displays juice menu for the user to select from.
    Get juice order value input from the user.
    """
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

    sizes = SHEET.worksheet("size")
    data = sizes.get_all_values()

    # define header names
    col_names = data[0]

    # define menu content and set width for Ingredients column
    menu_data = data[-5:]
    for row in menu_data:
        if (len(row[2]) > 45):
            last_space_index = row[2][:45].rfind(" ")
            row[2] = row[2][:last_space_index + 1] + "\n" \
                + row[2][last_space_index + 1:]

    # print juice menu table
    print(tabulate(menu_data, headers=col_names, tablefmt="fancy_grid") +
          "\n")
    while True:
        print("Please enter your juice size of choice (S, M, L)")
        print("Then press Enter when you are ready.\n")

        size_selection = input("Enter your order here:\n")
        if validate_size_data(size_selection):
            print("Thanks for your order")
            break
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
                f"Please enter size S, M or L)\n you entered {int(values)}")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")
        return False

def get_quantity():
    """
    Get quantity value input from the user
    """
    while True:
        print("Please insert the quantity that you want, (not more than 10) ")
        print("Then press Enter when you are ready.\n")

        quantity = input("Enter your order here:\n")
        if validate_quantity_data(quantity):
            print("Thanks for your order")
            break
    return quantity

def validate_quantity_data(values):
    """
    This function checks if the values provided by the user, in the functions
    get_quanity function meet the requirements in the validate_quantity_data.
    Also validates if the format is correct. If any of the requirements is not
    fulfilled it throws an error to inform the user.
    """
    try:
        quantity = int(values)
        if 1 <= quantity <= 10:
            return True
        else:
            raise ValueError(
                f"Please enter a number (1-10)\n you entered {quantity}")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")
        return False

def update_order_worksheet(juice, size, quantity):
    """
    Update order worksheet with juice selection,
    add new row with the list data provided
    """
    print("Updating order...\n")
    order_worksheet = SHEET.worksheet("order")
    order = []
    order.append(juice)
    order.append(size)
    order.append(quantity)
    order_worksheet.append_row(order)
    print("Order updated successfully.\n")

def order_summary(order_row):
    """
    Create a summary of the order, with juice selection, size and quantity
    """
    print("Calculating order summary...\n")
    print("Your order contains:")
    order = SHEET.worksheet("order").get_all_values()

    if len(order) > 1:
        order_row = order[-1]
        print(order_row)

def main():
    """
    Run all program functions
    """
    juice = get_juice_selection()
    size = get_size_selection()
    quantity = get_quantity()
    sales_data = [int(num) for num in juice and quantity]
    update_order_worksheet(juice, size, quantity)
    order_summary(sales_data)

main()
