# Importing all the required libraries
from email import header
from colorama import init
init()
from colorama import Fore, Back, Style

# Creating a pseudo front-end view for the project
def header_1():
    print(Fore.GREEN + '''
    ****************************************************************************************************
                                    Let's get the search started            
    ****************************************************************************************************
    ''')

def header_2():
    print(Fore.CYAN + '''
    ****************************************************************************************************
                            Searching for the best location of your company           
    ****************************************************************************************************
    ''')

def header_money():
    print(Fore.CYAN + '''
    ****************************************************************************************************
            Expected turnover of the companies present in the near by vicinity of your location
    ****************************************************************************************************
    ''')
    print(Fore.RED + '''                           Taking your requirement into consideration...''')
   
def header_year():
    print(Fore.CYAN + '''
    ****************************************************************************************************
               Expected age of the companies present in the near by vicinity of your location
    ****************************************************************************************************
    ''')
    print(Fore.RED + '''                           Taking your requirement into consideration...''')

def header_coffee():
    print(Fore.CYAN + '''
    ****************************************************************************************************
                Taking into consideration the distance of all the starbucks in your vicinity
    ****************************************************************************************************
    ''')
    print(Fore.RED + '''                                            Loading the information...''')

def header_school():
    print(Fore.CYAN + '''
    ****************************************************************************************************
                Taking into consideration the distance of all the schools in your vicinity
    ****************************************************************************************************
    ''')
    print(Fore.RED + '''                                            Loading the information...''')

def header_airports():
    print(Fore.CYAN + '''
    ****************************************************************************************************
            Taking into consideration the distance of all the airpots closest to your location
    ****************************************************************************************************
    ''')
    print(Fore.RED + '''                                            Loading the information...''')


print(Style.RESET_ALL)