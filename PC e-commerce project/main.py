#main.py functionalities - 

# 1 - Greet the user
# 2 - Store user information
# 3 - Holds a login and account creation screen 
# 4 - Store login information
# 5 - Load part data, processes orders and check outs
# 6 - Divides the information into easy to use pages 
# 7 - Displays items accordingly to the entered page number


import classes
import display_functions

userCredentials = []
partList = ["CPU", "GPU", "Motherboard", "RAM", "Hard Drives", "SSD's", "Power Supply", "PC Cases", "Cooling Solutions", "Keyboard",
            "Mouse", "Monitor", "Headset"]

shopping_cart = []


# Loads user data from a file to compare user entered data with old information.
def loadUserLogin():
    with open("savedLogins.txt") as file:
        for line in file:
            username, password = line.strip().split(',')
            customerCredential = classes.CustomerLogin(username, password)
            userCredentials.append(customerCredential)


        return

# Asks for input on their username and password, then compares data to ensure the username and password are correct.
def userLogin():
    enteredUserName = input("Enter your username: ")
    for user in userCredentials:

        if enteredUserName == user.username:
            enteredPassword = input("Enter password: ")
            while enteredPassword != user.password:
                enteredPassword = input("Invalid password, please try again or enter 'quit' to quit: ")
                if enteredPassword == "quit":
                    quit()
            print("Login Successful...")
            break
    else:
        print("No username match found, transfering you to the account creation screen.")
        createNewAcc()
    userMainScreen(enteredUserName)


# Prints out multiple different items and asks for user input on which item they would like to shop for.
def userMainScreen(username):

    print("Welcome! What are you shopping for today? Please enter the number accordingly, or '0' to quit: ")

    print("\nYou may also enter '-1' in order to view more options: ")
    
    for i,part in enumerate(partList):
        print(f"{i+1} - {part}")
    shopChoice = input()
    isInt = checkIfInt(shopChoice)

    if int(shopChoice) == 0:
        quit()

    elif int(shopChoice) == -1:


        from moreOptions import more_options
        more_options(username, shopping_cart, partList)
        return

    while isInt == False or int(shopChoice) not in range(15):
        shopChoice = input("Invalid input, please try again, or enter '0' to quit: ")
        isInt = checkIfInt(shopChoice)

        if shopChoice == '0':

            quit()
            
  
    print(f"You chose: {partList[int(shopChoice)-1]}!")
    print("Redirecting you now...")
    
    processNextPage(shopChoice, username)

# Uses a dictionary to determine which function to call based on the user input from userMainScreen()
def processNextPage(choice, username):

    try: 
        choice = int(choice)
        options = {
            1: display_functions.displayCPUs,
            2: display_functions.displayGPUs,
            3: display_functions.displayMotherboards,
            4: display_functions.displayRAM,
            5: display_functions.displayHardDrives,
            6: display_functions.displaySSDs,
            7: display_functions.displayPowerSupplies,
            8: display_functions.displayCases,
            9: display_functions.displayCoolingSolutions,
            10: display_functions.displayKeyboards,
            11: display_functions.displayMice,
            12: display_functions.displayMonitors,
            13: display_functions.displayHeadsets,
        }
        
        if choice in options:
            options[choice](username, main=True)
        else:
            print("Invalid choice. Please choose a valid option.")

            
    except Exception as e:
        print("Error: " + str(e))


# Asks the user to enter which item they want to order, and then gives them the option to add it to cart or check out now.

def process_order(page, username):

    while True:

        item = input("Enter the number corresponding to the item you would like to purchase, or '0' to exit: ")

        try:
            item = int(item)

            if item in range(len(page)):

                user_item = page[item-1]

                print(f'You chose: {user_item}')

                print("Would you like to add to your shopping cart, or check-out now? ")
                print("1 - Add to Shopping Cart")
                print("2 - Check-Out")

                user_choice = input()
                user_choice = int(user_choice)
                

                if user_choice == 1:
                    import time
                    shopping_cart.append(user_item)

                    print("Transfering back to page selection...\n\n")
                    time.sleep(1)

                    userMainScreen(username)

                
                elif user_choice == 2:
                    shopping_cart.append(user_item)
                    check_out(username)
                    

            elif item == '0':
                quit()

            break

        except ValueError:
            print("Invalid entry, integer is needed.")


# Prints the information of what you will be ordering, and then asks the user one last time if they want to order it.    
def check_out(username):

    print("Your items are - ")

    total_price = 0

    for i, item in enumerate(shopping_cart):
        print(f'{i+1} - {item}')
        total_price += float(item.price)
    
    print(f"Your price before tax will be : ${float(total_price):.2f}")

    total_price = total_price * 1.09

    print(f"Your total price after tax will be : ${float(total_price):.2f}")

    print('Would you like to place your order? - ')
    print('1 - Yes')
    print('2 - No')

    while True:


        order_choice = input()

   

        try:
            order_choice = int(order_choice)

            if order_choice == 1:

                process_receipt(total_price, username)
                break
            elif order_choice == 2:
                
                quit()

            else:
                print('Invalid entry...')
                
    

        except ValueError:
            print("Invalid, please enter an integer corresponding with the 2 options.")


# Prints out a reciept after the user checks out, displaying all items and total price after tax.
def process_receipt(total_price, username):

    print("Thank you for your order, here is your reciept - ")


    print(f'\nUser: {username}')
    print("***************************************\n")
    for i, item in enumerate(shopping_cart):
        print(f'{i+1} - {item}')

    print("\n***************************************")
                
    print(f"Your total price after tax will be : ${float(total_price):.2f}")
    


# After the user picks which item they want to shop for, this function will divide the file that holds the item data into pages for the user to browse through.
def get_page(page_number, data):
    import math

    page_size = 20
    
    #we subtract page_size by 1 due to the list going off of index of 0, this therefore makes sure there is a total of 20 instead of 21 in the list.

    num_pages = math.ceil(len(data) / page_size)

    try:
        #ensure that page_number is within the range of total pages
        page_number = int(page_number)
        if page_number < 1 or page_number > num_pages:
            return None

        #the starting index for the requested page.
        start_index = (page_number - 1) * page_size
        #the ending index for the requested page.
        end_index = start_index + page_size

        return data[start_index:end_index]
    except ValueError:
        return None


# Displays the pages and allows the user to choose which page to display.
def item_display(username, data):
    import math
    
    try: 

        from moreOptions import load_filters
        from moreOptions import get_filters

        try:        
            price_filter, brand_filters = get_filters()
        except:
            price_filter, brand_filters = None, None
        

        # Check to see if there are any items within the data after applying filters, if not we skip this function in order to keep the old data.

        if price_filter or brand_filters:
            data = load_filters(data)

        if not data:
            return


        page_number = input(f"Please enter the page number you would like to go to, or '0' to go back to the menu, there are {math.ceil(len(data)/20)} page(s): ")
            
            
        page = get_page(page_number, data)

        if page is not None:
            print(f"Page {page_number}:")
                
            for i, line in enumerate(page):
                print(f"{i+1} - {line}")

        elif int(page_number) == 0: 
            
            userMainScreen(username)
            return
            

        else:
            print("Page number out of range. Please try again.")

            
        while True:

            print('**********************************************************\n')
            print("Please enter another page number to continue browsing, or enter 'buy' to be able to select an item from the page\nYou may also enter 'quit' to quit: ")

            user_input = input("\nYou may also enter '-1' in order to view more options: ").lower()

    
            print("\n\n*********************************************\n\n")


            if user_input == 'buy':
                process_order(page, username)
                break

            elif user_input == 'quit':
                quit()

            elif user_input == '0': 

                userMainScreen(username)
                break

            elif user_input == '-1':

                from moreOptions import more_options

                more_options(username, shopping_cart, partList)
                break




            try:
                
                if 1 <= int(user_input) <= math.ceil(len(data)/20):

                    page = get_page(user_input, data)

                    if page is not None:
                        print(f"Page {user_input}:")
                        
                    for i, line in enumerate(page):
                        print(f"{i+1} - {line}")
                    print("\n\n*********************************************\n\n")
                else:

                    print("Invalid Entry...")
            except ValueError:
                    print("Invalid entry. Please enter a valid page number or 'buy' to proceed.")


    except Exception as e:
        print("Error: " + str(e))



# Checks if a variable is of type int (number)
def checkIfInt(entered):
    
    try:
        int(entered)
        return True
    except ValueError:
        return False

# A function that the user will enter if they do not have an account.
def createNewAcc():
    newUserName = input("Enter your desired username: ")
    used = checkIfUsed(newUserName)
    if used == True:
        print("Username is already used, please try again.")
        createNewAcc()
    if used == False: #another if statement to ensure the 'new password' is only asked for once if the user enters a invalid username the first time.
        newPassword = input("Enter your desired password: ")
    saveUserCredentials(newUserName, newPassword)
    print("You will now be re-directed to the login page.")
    userLogin()


# Saves the user information to a file.
def saveUserCredentials(username, password):
    with open("savedLogins.txt", 'r+') as file:
        file.seek(0)

        if len(file.read()) > 0:
            file.write('\n')
        
        file.write(f"{username},{password}")
        file.truncate()
    print("Saved data successfully.")
    customer = classes.CustomerLogin(username,password)
    userCredentials.append(customer)

# Checks to see if the entered username matches any within the saved data
def checkIfUsed(entered):
    used = False 
    for customer in userCredentials:
        if entered == customer.username: 
            used = True
            break
    return used

# Greets the user, the first screen that appears within the program and asks if thery want to create an account or login.
def greeting():
    userEntry = input("Would you like to make a new account or login?: ").lower()

    if userEntry == "new account":
        createNewAcc()
    elif userEntry == "login":
        userLogin()
    elif userEntry == "quit":
        quit()
    else:
        print("Invalid entry, try again or enter 'quit' to quit.")
        greeting()


# Quickly exits the program.
def quit():
    import sys
    print("Thank you for using this program.")
    print("Exiting...")
    sys.exit()

# Ensures this code is only ran at the beginning of main, not when main.py is imported on other files
if __name__ == "__main__":

    loadUserLogin()
    greeting()