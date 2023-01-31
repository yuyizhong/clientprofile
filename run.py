"""Client Profile Mgmt Imports"""
# import gspread to access and edit the excelsheet
import gspread

# import google oauth to authorize the access to client-Book through credentials
from google.oauth2.service_account import Credentials

# import tabulate to print the data list in a nice table format
from tabulate import tabulate

# import pyfiglet module for ascii art
import pyfiglet

# import colorama for colour text
import colorama
from colorama import Fore, Back, Style 
colorama.init(autoreset=True)

# import datetime for client date of birth
from datetime import date

# The SCOPE lists the APIs to access to run programme.
# Set up constant variables
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Client-Book')

# clients = SHEET.worksheet('clients')

# data = clients.get_all_values()
# table = tabulate(data, headers="firstrow", tablefmt="grid", colalign="left")

# # print(f"{Back.RED}{table}")
# dob= data[1][2]
# print(type(dob))

def add_client(list):
    """1.Add New Client"""
    # Get Client's name and D.o.B
    fname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}First Name{Style.RESET_ALL}:\n").capitalize()
    lname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Last Name{Style.RESET_ALL}:\n").capitalize()
    dob = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Date of Birth formatted as {Fore.YELLOW}dd/mm/yyyy{Style.RESET_ALL}:\n")
   
    # Check if Client is already in the list.
    exist = False  
    for index in range(len(list)):
        if (list[index][0] == fname and list[index][1] == lname and list[index][2] == dob):
            print(f"{Back.RED}{Fore.WHITE}Client is exist! {Style.BRIGHT}Please enter again!!{Style.RESET_ALL}\n")
            exist = True
            break
    # If not in the list, get client contact number, email and spend
    # If spend enter is valid then update client Type accordingly   
    if not exist:
        tel = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Contact Number{Style.RESET_ALL}:\n")
        email = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Email{Style.RESET_ALL}:\n")
        while True:
            spend = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}client's spend amount in Sterling Pounds{Style.RESET_ALL}:\n")
            if validate_spend(spend):
                break        
        return spend

        new_client = [fname, lname, dob, tel, email, spend]
        # Add the list of new client's information to the clients sheet
        list.append(new_client)
        print(f"{Back.GREEN}{Fore.WHITE}client{fname}{lname} is now added to the Client Book.\n")

def validate_spend(value):
    """
    Inside the try, converts all string values into floats.
    And add the float to the previous total spend
    Raises ValueError if strings cannot be converted into float.
    
    """

    try:
        [float(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values are required, you provided {len(values)}")

    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")
        return False

    return True


