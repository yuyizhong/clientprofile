import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate
# import pyfiglet module for ascii art
import pyfiglet

# import colorama for adding colour
import colorama
from colorama import Fore, Back, Style 
colorama.init(autoreset=True)


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

data = clients.get_all_values()
table = tabulate(data, headers="firstrow", tablefmt="grid", colalign="left")

print(f"{Back.RED}{table}")