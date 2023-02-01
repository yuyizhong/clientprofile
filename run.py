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

clients = SHEET.worksheet('clients')




# table = tabulate(data, headers="firstrow", tablefmt="grid", colalign="left")

# # print(f"{Back.RED}{table}")
# dob= data[1][2]
# print(type(dob))

def add_client(worksheet):

    """1.Add New Client"""

    # Get Client's name and D.o.B
    fname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}First Name{Style.RESET_ALL}:\n").capitalize()
    lname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Last Name{Style.RESET_ALL}:\n").capitalize()
    dob = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Date of Birth formatted as {Fore.YELLOW}dd/mm/yyyy{Style.RESET_ALL}:\n")
    list = worksheet.get_all_values()
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
        email = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Email{Style.RESET_ALL}:\n").lower()
        while True:
            spend = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}client's spend amount in Sterling Pounds{Style.RESET_ALL}:\n")
            if validate_spend(spend):
               break        
        fspend = float(spend) 
        if fspend >= 35000.0:
            type = "VIP"
        else:
            type = "Regular"
        new_client = [fname, lname, dob, tel, email, fspend, type]
        # Add the list of new client's information to the clients sheet
        worksheet.append_row(new_client)        
        print(f"{Back.YELLOW}{Fore.BLACK}client {fname} {lname} is now added to the Client Book.\n")

def validate_spend(value):
    """
    Inside the try, converts value into float.
    Raises ValueError if string cannot be converted into float.
    
    """
    try:
        spend_num = float(value)
        print(f"{Back.GREEN}{Fore.BLACK}Number entered is valid.")
    except ValueError as e:
        print(f"{Back.RED}{Fore.WHITE}Not a number: {e}, please try again\n")
        return False

    return True



def delete_client(worksheet): 

    """2. Delete client"""

     # Get user to input client's name and D.o.B
    fname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}First Name{Style.RESET_ALL}:\n").capitalize()
    lname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Last Name{Style.RESET_ALL}:\n").capitalize()
    dob = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Date of Birth formatted as {Fore.YELLOW}dd/mm/yyyy{Style.RESET_ALL}:\n")
    list = worksheet.get_all_values()

    # Search client, confirm delete decision and delete client, otherwise print error message
    exist = False  
    for index in range(len(list)):
        if (list[index][0] == fname and list[index][1] == lname and list[index][2] == dob):
            choice = input(f"{Fore.YELLOW}Do you want to delete client {fname} {lname}? Y or N{Fore.RESET}:\n").lower()
            exist = True
            if choice == "y":
                num=index+1
                worksheet.delete_rows(num)
                
                print(f"{Back.YELLOW}{Fore.BLACK}client {fname} {lname} is now deleted from Client Book.\n")
                break
            
            elif choice == "n":
                print(f"{Back.GREEN}{Fore.BLACK}No delete, exit to main menue")
                break
            
            else:
                print(f"{Back.RED}{Fore.WHITE}Not a valid input, please try again!\n")
                delete_client(worksheet)

    
    if not exist:
        print (f"{Back.RED}{Fore.WHITE}Client is not exist!{Style.RESET_ALL}\n")

delete_client(clients)