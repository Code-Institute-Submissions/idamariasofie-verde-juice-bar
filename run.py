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
        if validate_data(juice_selection):
            print("Thanks for your order")
            break
    return juice_selection

def get_size_selection():
    """
    Get size order value input from the user
    """
    while True:
        print("Please enter your juice size of choice (S, M, L)")
        print("Then press Enter when you are ready.\n")

        size_selection = input("Enter your order here:\n")
        if validate_data(size_selection):
            print("Thanks for your order")
            break
    return size_selection

def get_quantity():
    """
    Get quantity value input from the user
    """
    while True:
        print("Please insert the quantity that you want, (not more than 10) ")
        print("Then press Enter when you are ready.\n")

        quantity = input("Enter your order here:\n")
        if validate_data(quantity):
            print("Thanks for your order")
            break
    return quantity

def validate_data(values):
    """
    This function checks if the values provided by the user, in the functions
    get_juice_selection, get_size_selection and get_quanity meet the
    requirements in the values_required. Also validates if the format
    is correct. If any of the requirements is not fulfilled it throws
    an error to inform the user.
    """
    print(values)
        


get_juice_selection()
get_size_selection()
get_quantity()
validate_data()
