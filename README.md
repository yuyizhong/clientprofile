# **Clients Profile**

Clients Profile is a Python terminal App that runs on Heroku. 

![User Platform](assets/images/menu.png)

As a data management system, it is supposed to help user to easily access and manipulate data to provide efficiency to their work. The targeted users are sales person, account managers and whoever managing a large client base. With Clients Profile App, they can now add, delete, search, edit and view clients through the interactive terminal with any device. Furthermore, when each time user updating a new sale, the system will automatically review the client's status and change it accordingly.
A live project can be viewed [Here](https://client-profile-system.herokuapp.com/).

## How To Operate

Clients Profile App is easy to operate. Users will start with a menu of 6 options. They can choose any given option by entering 1 to 6 to run the specific program to manage the client database. 

After each selection of the options, users only need to follow the computer instruction for each step to complete the task. 

At the end of each program, it will go back to the main menu and ready to run another program chosen by users. If users finish what they need to do, simply enter 6 at main menu and exit the Clients Profile system.

## User Experience (UX)

### User Stories

As a sales person or account manager, users would like to have an easy access to client database:
* Simple platform and smooth operation
* Clear instruction and easy to follow
* Easy to allocate the information needed
* Easy to add and delete clients and update their details 
* Automatically calculate the total spend for each client 
* Automatically classify the clients into the appropriate group when certain criteria is reached.

### Site Goal
* This App was designed based on user stores to provide the best dynamic experience. 
* Further efforts were made to eliminate certain user input error which may interrupt normal programming.
* Improved site readability and user friendly interface. 

## Features

**App Title and Main Menu:**
* [Pyfiglet](https://www.geeksforgeeks.org/python-ascii-art-using-pyfiglet-module/#:~:text=pyfiglet%20takes%20ASCII%20text%20and,pyfiglet%20module%20%3A%20pip%20install%20pyfiglet) was installed and imported to generate ASCII art for App Title.

* For the sake of it's large font size and simple style, Doom Font was used to the title. It was centred to prominent it's professionalism and clean layout.

![App Title](assets/images/title.png)

* Green colored operation menu is right underneath the App title. 
* Number listed operation options are clearly specified in short words.
* A friendly message instructs the user to start the program.

![App Title](assets/images/main-menu.png)

* If users didn't enter what required by instruction message (eg: anything rather than number 1 - 6), an error message with read background appears.
* Users will be asked to enter again until a number representing one of the menu options is entered.

![App Title](assets/images/menu1.png)













