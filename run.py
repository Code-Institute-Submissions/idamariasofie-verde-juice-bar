import gspread
from google.oauth2.service_account import Credentials

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
    Get juice order value input from the user
    """
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
                f"Please enter a number (1-5)\n you entered {len(values)}")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")
        return False

def get_size_selection():
    """
    Get size order value input from the user
    """
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
        if len(values) != 1:
            raise ValueError(f"Please enter 1 value you entered {len(values)}")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
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
                f"Please enter a number (1-5)\n you entered {quantity}")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")
        return False

get_juice_selection()
get_size_selection()
get_quantity()
