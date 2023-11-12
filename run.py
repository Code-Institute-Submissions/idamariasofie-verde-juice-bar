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
        if len(juice_selection) == 1:
            print(f'You entered juice number: {juice_selection}')
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
        if len(size_selection) == 1:
            print(f'You entered size: {size_selection}')
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
        if len(quantity) <= 10:
            print(f'You entered size: {quantity}')
            break
    return quantity





get_juice_selection()
get_size_selection()
get_quantity()
