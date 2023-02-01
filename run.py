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

    # # Get Client's name and D.o.B
    # fname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}First Name{Style.RESET_ALL}:\n").capitalize()
    # lname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Last Name{Style.RESET_ALL}:\n").capitalize()
    # dob = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Date of Birth formatted as {Fore.YELLOW}dd/mm/yyyy{Style.RESET_ALL}:\n")
    # list = worksheet.get_all_values()
    # # Check if Client is already in the list.
    # exist = False  
    # for index in range(len(list)):
    #     if (list[index][0] == fname and list[index][1] == lname and list[index][2] == dob):
    #         print(f"{Back.RED}{Fore.WHITE}Client is exist! {Style.BRIGHT}Please enter again!!{Style.RESET_ALL}\n")
    #         exist = True
    #         break
    # # If not in the list, get client contact number, email and spend
    # # If spend enter is valid then update client Type accordingly   

    # if not exist:
    
    exist = check_client(worksheet)    
    if exist == False:
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
            delete_choice = input(f"{Fore.YELLOW}Do you want to delete client {fname} {lname}? Y or N{Fore.RESET}:\n").lower()
            exist = True
            if delete_choice == "y":
                num=index+1
                worksheet.delete_rows(num)
                
                print(f"{Back.YELLOW}{Fore.BLACK}client {fname} {lname} is now deleted from Client Book.\n")
                break
            
            elif delete_choice == "n":
                print(f"{Back.GREEN}{Fore.BLACK}No delete, exit to main menue")
                break
            
            else:
                print(f"{Back.RED}{Fore.WHITE}Not a valid input, please try again!\n")
                delete_client(worksheet)

    
    if not exist:
        print (f"{Back.RED}{Fore.WHITE}Client is not exist!{Style.RESET_ALL}\n")

def check_client(worksheet):
    """Get user input to check if client is exist"""
     # Get Client's name and D.o.B
    fname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}First Name{Style.RESET_ALL}:\n").capitalize()
    lname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Last Name{Style.RESET_ALL}:\n").capitalize()
    dob = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Date of Birth formatted as {Fore.YELLOW}dd/mm/yyyy{Style.RESET_ALL}:\n")
    list = worksheet.get_all_values()
    # Check if Client is already in the list.
    exist = False  
    for index in range(len(list)):
        if (list[index][0] == fname and list[index][1] == lname and list[index][2] == dob):
            print(f"{Back.RED}{Fore.WHITE}Client is exist!{Style.RESET_ALL}\n")
            return True
            break
    
    if not exist:
        print (f"{Back.RED}{Fore.WHITE}Client is not exist!{Style.RESET_ALL}\n")
        return False
        

# add_client(clients)

            


def update_client(worksheet):

    """3. Update client personal information"""

    # Get user to input client's name and D.o.B
    print(f"{Fore.CYAN}Provide the below information for client you want to update{Fore.RESET}:\n")
    fname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}First Name{Style.RESET_ALL}:\n").capitalize()
    lname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Last Name{Style.RESET_ALL}:\n").capitalize()
    dob = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Date of Birth formatted as {Fore.YELLOW}dd/mm/yyyy{Style.RESET_ALL}:\n")
    list = worksheet.get_all_values()

    # Search client, if exist, confirm edit options and update client informatio accordingly, otherwise print error message
    exist = False  
    for index in range(len(list)):
        if (list[index][0] == fname and list[index][1] == lname and list[index][2] == dob):
            exist = True

            # Option to edit client's name
            edit_name = input(f"{Fore.YELLOW}Do you want to edit client {fname} {lname}'s name? Y or N{Fore.RESET}:\n").lower()
            
            if edit_name == "y":
                new_fname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT} updated First Name{Style.RESET_ALL}:\n").capitalize()
                new_lname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT} updated Last Name{Style.RESET_ALL}:\n").capitalize()
                row = index + 1
                worksheet.update_cell(row,1, new_fname)
                worksheet.update_cell(row,2, new_lname)
                print(f"{Back.YELLOW}{Fore.BLACK}client {new_fname} {new_lname} is now updated at Client Book.\n")
                
            
            elif edit_name == "n":
                print(f"{Back.GREEN}{Fore.BLACK}You select N, move to next option")
                
            
            else:
                print(f"{Back.RED}{Fore.WHITE}Not a valid input, please try again!\n")
                update_client(worksheet)
            
            # Option to edit client's date of birth
            edit_dob = input(f"{Fore.YELLOW}Do you want to edit client {fname} {lname}'s Date of Birth? Y or N{Fore.RESET}:\n").lower()
            
            if edit_dob == "y":
                new_dob = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}updated Date of Birth formatted as {Fore.YELLOW}dd/mm/yyyy{Style.RESET_ALL}:\n")
                row = index + 1
                worksheet.update_cell(row,3, new_dob)                
                print(f"{Back.YELLOW}{Fore.BLACK}client's Date of Birth is now updated as {new_dob} at Client Book.\n")
                
            
            elif edit_dob == "n":
                print(f"{Back.GREEN}{Fore.BLACK}You select N, move to next option")
                
            
            else:
                print(f"{Back.RED}{Fore.WHITE}Not a valid input, please try again!\n")
                update_client(worksheet)

            # Option to edit client's Contact Number
            edit_tel = input(f"{Fore.YELLOW}Do you want to edit client {fname} {lname}'s Contact Number? Y or N{Fore.RESET}:\n").lower()
            
            if edit_tel == "y":
                new_tel = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}updated Contact Number{Style.RESET_ALL}:\n")
                row = index + 1
                worksheet.update_cell(row,4, new_tel)                
                print(f"{Back.YELLOW}{Fore.BLACK}client's Contact Number is now updated as {new_tel} at Client Book.\n")
                
            
            elif edit_tel == "n":
                print(f"{Back.GREEN}{Fore.BLACK}You select N, move to next option")
                
            
            else:
                print(f"{Back.RED}{Fore.WHITE}Not a valid input, please try again!\n")
                update_client(worksheet)

            # Option to edit client's Email
            edit_email = input(f"{Fore.YELLOW}Do you want to edit client {fname} {lname}'s Email? Y or N{Fore.RESET}:\n").lower()
            
            if edit_email == "y":
                new_email = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}updated Email{Style.RESET_ALL}:\n")
                row = index + 1
                worksheet.update_cell(row,5, new_email)                
                print(f"{Back.YELLOW}{Fore.BLACK}client's Email is now updated as {new_email} at Client Book.\n")
                
            
            elif edit_email == "n":
                print(f"{Back.GREEN}{Fore.BLACK}You select N, move to next option")
                
            
            else:
                print(f"{Back.RED}{Fore.WHITE}Not a valid input, please try again!\n")
                update_client(worksheet)

            # Option to update client's spend by adding the new spend to the total spend
            # Update the client type according to new total spend
            edit_spend = input(f"{Fore.YELLOW}Do you want to add client {fname} {lname}'s New Spend? Y or N{Fore.RESET}:\n").lower()
            
            if edit_spend == "y":
                while True:
                    new_spend= input(f"{Fore.CYAN}Please enter {Style.BRIGHT}the new Spend amount{Style.RESET_ALL}:\n")
                    if validate_spend(new_spend):
                        break 
                old_total_spend = list[index][5]
                total_spend = float(old_total_spend) + float(new_spend)
                row = index + 1
                worksheet.update_cell(row,6, total_spend)
                if total_spend >= 35000:
                    type = "VIP"
                else:
                    type = "Regular"
                worksheet.update_cell(row,7, type)

                print(f"{Back.YELLOW}{Fore.BLACK}client's Total Spend is now updated as {total_spend} at Client Book.\n")

                break
            
            elif edit_spend == "n":
                print(f"{Back.GREEN}{Fore.BLACK}You select N, no other option to update!")
                break
            
            else:
                print(f"{Back.RED}{Fore.WHITE}Not a valid input, please try again!\n")
                update_client(worksheet)
            
    
    if not exist:
        print (f"{Back.RED}{Fore.WHITE}Client is not exist!{Style.RESET_ALL}\n")




def update_options(num):

    """ options for user to choose when updating client information"""     

            
    edit_choice = input(f"{Fore.YELLOW}Do you want to edit client {fname} {lname}'s {option}? Y or N{Fore.RESET}:\n").lower()
            
    if edit_choice == "y":
        new_data = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}updated option {Fore.YELLOW}if it is a date please formatted as dd/mm/yyyy{Style.RESET_ALL}:\n")
        row = index + 1
        worksheet.update_cell(row,num, new_data)                
        print(f"{Back.YELLOW}{Fore.BLACK}client's option is now updated as {new_data} at Client Book.\n")
                
            
    elif edit_dob == "n":
        print(f"{Back.GREEN}{Fore.BLACK}You select N, move to next option")
                
            
    else:
        print(f"{Back.RED}{Fore.WHITE}Not a valid input, please try again!\n")
        update_client(worksheet)


update_client(clients)