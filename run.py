"""Client Profile Mgmt Imports"""
# import gspread to access and edit the excelsheet
import gspread

# import google oauth to authorize the access to client-Book through credentials
from google.oauth2.service_account import Credentials

# import os to clear terminal when user runs a new programme
import os

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

def clear():
    """
    Clear screen when user running a new programme
    """
    os.system("clear")

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


def check_client(worksheet, fname, lname, dob, list):

    """Get user input to check if client is exist"""
   
    exist = False  
    for index in range(len(list)):
        if (list[index][0] == fname and list[index][1] == lname and list[index][2] == dob):
            print(f"{Back.RED}{Fore.WHITE}Client {fname} {lname} is in the system{Style.RESET_ALL}\n")
            
            return True, index
            break
    
    if not exist:
        print (f"{Back.RED}{Fore.WHITE}Client {fname} {lname} is not in the system{Style.RESET_ALL}\n")
        return False

def add_client(worksheet):

    """1.Add New Client"""
    
    # Get Client's name and D.o.B    
    fname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}First Name{Style.RESET_ALL}:\n").capitalize()
    lname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Last Name{Style.RESET_ALL}:\n").capitalize()
    dob = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Date of Birth formatted as {Fore.YELLOW}dd/mm/yyyy{Style.RESET_ALL}:\n")
    list = worksheet.get_all_values()

    # Check if Client is already in the list.    
    # if not exist: get personal information and add to the list
    # Auto set the client status according to the spend amount
    
    exist = check_client(worksheet, fname, lname, dob, list)    
    if exist == False:
        tel = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Contact Number{Style.RESET_ALL}:\n")
        email = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Email{Style.RESET_ALL}:\n").lower()
        while True:
            spend = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}client's spend amount in Sterling Pounds{Style.RESET_ALL}:\n")
            if validate_spend(spend):
               break        
        fspend = float(spend) 
        if fspend >= 35000.0:
            status = "Vip"
        else:
            status = "Regular"
        new_client = [fname, lname, dob, tel, email, fspend, status]
        # Add the list of new client's information to the clients sheet
        worksheet.append_row(new_client)        
        print(f"{Back.YELLOW}{Fore.BLACK}client {fname} {lname} is now added to the Client Book.\n")

def search_clients(worksheet):

    """2. Search clients and display all the information"""
    
    # Get user to input client's name
    print(f"{Fore.CYAN}Provide the below information for the client which you want to search{Fore.RESET}:\n")
    fname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}First Name{Style.RESET_ALL}:\n").capitalize()
    lname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Last Name{Style.RESET_ALL}:\n").capitalize()    
    list = worksheet.get_all_values()

    # Search client, if exist display the information, otherwise print error message 
    client_exist = False    
    client_info = []    
    for index in range(len(list)):                   
        if fname == list[index][0] and lname == list[index][1]:            
            client_info.append(list[index])             
            client_exist = True   
            
    if not client_exist:
        print (f"{Back.RED}{Fore.WHITE}Client {fname} {lname} you searched is not fund in the system!{Style.RESET_ALL}\n")

    table = tabulate(client_info, tablefmt="grid")            
    print(f"{Back.RED}{table}")
     

def delete_client(worksheet): 

    """3. Delete client"""
    
    # Get user to input client's name and D.o.B
    print(f"{Fore.CYAN}Provide the below information for the client which you want to delete{Fore.RESET}:\n")
    fname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}First Name{Style.RESET_ALL}:\n").capitalize()
    lname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Last Name{Style.RESET_ALL}:\n").capitalize()
    dob = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Date of Birth formatted as {Fore.YELLOW}dd/mm/yyyy{Style.RESET_ALL}:\n")
    list = worksheet.get_all_values()

    # Search client, confirm delete decision and delete client, otherwise print error message
    exist = check_client(worksheet, fname, lname, dob, list)    
    if exist[0] == True:          
    
        delete_choice = input(f"{Fore.YELLOW}Do you want to delete client {fname} {lname}? Y or N{Fore.RESET}:\n").lower()
        
        if delete_choice == "y":
            index = exist[1]
            num=index+1
            worksheet.delete_rows(num)
                
            print(f"{Back.YELLOW}{Fore.BLACK}client {fname} {lname} is now deleted from Client Book.\n")            
            
        elif delete_choice == "n":
            print(f"{Back.GREEN}{Fore.BLACK}No delete, exit to main menue")    
            
        else:
            print(f"{Back.RED}{Fore.WHITE}Not a valid input, please try again!\n")
            delete_client(worksheet)

    # if not exist[0]:
    #     print (f"{Back.RED}{Fore.WHITE}Client is not exist!{Style.RESET_ALL}\n")

def update_options(worksheet, fname, lname, index, num):

    """ options for user to choose when updating client's basic information"""
    list = worksheet.get_all_values()
    option = list[0][num-1] 
            
    edit_choice = input(f"{Fore.YELLOW}Do you want to edit client {fname} {lname}'s {option}? Y or N{Fore.RESET}:\n").lower()
            
    if edit_choice == "y":
        new_data = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}updated {option} {Fore.YELLOW}(date please formatted as dd/mm/yyyy){Style.RESET_ALL}:\n")
        row = index + 1
        if num == 1 or 2:
            worksheet.update_cell(row,num, new_data.capitalize())
        else:
            worksheet.update_cell(row,num, new_data)

        print(f"{Back.YELLOW}{Fore.BLACK}client's {option} is now updated as {new_data} at Client Book.\n")
                
            
    elif edit_choice == "n":
        print(f"{Back.GREEN}{Fore.BLACK}You select N, move to next option")
                
            
    else:
        print(f"{Back.RED}{Fore.WHITE}Not a valid input, please try again!\n")
        update_client(worksheet)

def update_client(worksheet):

    """4. Update client personal information"""
    
    # Get user to input client's name and D.o.B
    print(f"{Fore.CYAN}Provide the below information for client which you want to update{Fore.RESET}:\n")
    fname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}First Name{Style.RESET_ALL}:\n").capitalize()
    lname = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Last Name{Style.RESET_ALL}:\n").capitalize()
    dob = input(f"{Fore.CYAN}Please enter {Style.BRIGHT}Date of Birth formatted as {Fore.YELLOW}dd/mm/yyyy{Style.RESET_ALL}:\n")
    list = worksheet.get_all_values()

    # Search client, if exist, confirm edit options and update client information accordingly, otherwise print error message
   
    check_results = check_client(worksheet, fname, lname, dob, list)   
    
    if check_results[0] == True:
        index = check_results[1]
        # Option to edit client's name
        update_options(worksheet, fname, lname, index, 1)
        update_options(worksheet, fname, lname, index, 2)
        # Option to edit client's date of birth
        update_options(worksheet, fname, lname, index, 3)
        # Option to edit client's Contact Number
        update_options(worksheet, fname, lname, index, 4)
        # Option to edit client's Email
        update_options(worksheet, fname, lname, index, 5)

        # Option to update client's spend by adding the new spend to the total spend        
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

            # Update the client status according to new total spend
            if total_spend >= 35000:
                status = "Vip"
            else:
                status = "Regular"
            worksheet.update_cell(row,7, status)
            print(f"{Back.YELLOW}{Fore.BLACK}{status} client's Total Spend is now updated as {total_spend} at Client Book.\n")
            
        elif edit_spend == "n":
            print(f"{Back.GREEN}{Fore.BLACK}You select N, no other option to update!")            
            
        else:
            print(f"{Back.RED}{Fore.WHITE}Not a valid input, please try again!\n")
            update_client(worksheet)            
   
    if not check_results[0]:
        print (f"{Back.RED}{Fore.WHITE}Client is not exist!{Style.RESET_ALL}\n")


def get_all_clients(worksheet):

    """5. List all the clients' details"""    
    # Option to list Regular clients
    # Option to list Vip clients
    # Option to list All clients

    status = input(f"{Fore.YELLOW}Please choose the status of the clients you like to view? Enter Regular, Vip or All{Fore.RESET}:\n").capitalize()
    list = worksheet.get_all_values()        
    
    if status == "Regular" or status == "Vip":
        data = []
        print("-------------------")
        for index in range(len(list)):        
           
            if list[index][6] == status:                      
                row=list[index]            
                data.append(row)                
        table = tabulate(data, tablefmt="grid")
        print(f"{Back.RED}{table}")        
        print("-------------------")
    elif status == "All":
        print("-------------------")
        all_table = tabulate(list, tablefmt="grid")
        print(f"{Back.RED}{all_table}")
        print("-------------------")
    else:
        print(f"{Back.RED}{Fore.WHITE}Not a valid input, please try again!\n")
        get_all_clients(worksheet)
    
def operation (worksheet):
    """link the management functions to the operation menu"""
    while True:        
        title = pyfiglet.figlet_format("Clients Management System", font="doom", justify="center")
        print(title)     
        print("=======================================================================")
        system_menu = '''
        1. Add new client to the system
        2. Search clients by name and display their information
        3. Delete client from the system
        4. Edit the client's information 
        5. Display all the clients on the system (Option to select client Type)    
        6. Exit the system
        '''     
        print(f"{Fore.GREEN}{system_menu}")
        print("========================================================================")
        option = input(f"{Fore.MAGENTA}Please enter the number between 1 - 6 to run your choice:")
        # Check if user entered the correct value as required
        if option not in ["1","2","3","4","5","6"]:
            print(f"{Back.RED}{Fore.WHITE}Not a valid input, please try again!\n")
        else:
            if option == "1":
                add_client(worksheet)
            elif option == "2":
                search_clients(worksheet)
            elif option == "3":
                delete_client(worksheet)
            elif option == "4":
                update_client(worksheet)
            elif option == "5":
                get_all_clients(worksheet)            
            elif option == "6":
                # Exit the operation system
                print(f"{Fore.MAGENTA}Thank you for using the clients management system! Hope to See you soon!")
                break
            
def main ():
    """Run programm according to users' choices"""    
    clients = SHEET.worksheet('clients')    
    operation(clients)

if __name__ == "__main__":
    main()

