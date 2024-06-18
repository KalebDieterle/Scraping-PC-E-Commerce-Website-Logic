# moreOptions.py functionalities - 

# 1 - Viewing the users shopping cart
# 2 - Remove items from their shopping cart
# 3 - Adding items to a wishlist
# 4 - Removing items from the wishlist
# 5 - Adding search filters to narrow their options
# 6 - Removing search filters

import classes
import display_functions

filters = []
price_filter = None
brand_filters = None


class Range_Filter:
    def __init__(self, min, max):

        self.min = min
        self.max = max

    def __str__(self):
        return f"${self.min:.2f} - ${self.max:.2f}"
    
class Brand_Filter:
    def __init__(self, brand):

        self.brand = brand

    def __eq__(self, other):
        if isinstance(other, Brand_Filter):
            return self.brand.lower() == other.brand.lower()
        return False

    def __str__(self):
        return self.brand

# Displays the users shopping cart, and displays that it is empty if there is nothing within it.
def view_cart(username, shopping_cart):

    if shopping_cart:

        total_price = 0

        for i, item in enumerate(shopping_cart):
            print(f'{i+1} - {item}')
            total_price += float(item.price)
        
        total_price = total_price * 1.09

        

        print(f'\nUser: {username}')
        print("***************************************\n")
        for i, item in enumerate(shopping_cart):
            print(f'{i+1} - {item}')

        print("\n***************************************")
                    
        print(f"Your total price after tax will be : ${float(total_price):.2f}")

    else:
        print("Shopping cart is empty.")
        return


# Asks the user which item they would like to remove from their shopping cart, and then removes the item accordingly.
def remove_cart(username, shopping_cart):

    if shopping_cart:

        print('Please select out of the list which item you would like to remove - ')
        for i, item in enumerate(shopping_cart):
            print(f'{i+1} - {item}')

    else:

        print("Shopping cart is empty.")
        return


    while True:

        user_choice = input('Enter the number corresponding with the item: ')

        try:
                
                user_choice = int(user_choice)

                if user_choice in range(len(shopping_cart)):
                        
                    del shopping_cart[user_choice-1]

                    print(f"Removed - ")
                    print(f'{user_choice}  - {shopping_cart[user_choice-1]}')
                        
                    return
                    
                else:
                    raise Exception
            
                
        except Exception as e:
            print("Error: " + str(e))
            print("Invalid entry...")
            
            

# Displays the pages of information and allows the user to add items to their wishlist.
def add_wishlist(username, partList):

    try: 
        
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

        wishlist = []

        for i,part in enumerate(partList):
            print(f"{i+1} - {part}")

        item_type = int(input("What kind of item would you like to add to your wishlist: "))

        try:
            if item_type in options:
                page = options[item_type](username, main=False)
                wishlist = []

                try:
                    item_select = int(input("Enter the number corresponding with the wanted item: "))

                    for i, item in enumerate(page):
                        if item_select == i + 1:
                            wishlist.append(item)
                            print("Item added - ")
                            print(item)

                            break  # Exit the loop after adding the item
                    else:

                        print("Invalid item number.")
                        
                except Exception as e:
                    print("Error: " + str(e))
            else:
                raise Exception("Invalid entry.")
        except Exception as e:
            print("Error: " + str(e))
    
    except Exception as e:
        print("Error:" + str(e))

    return wishlist

# Prompts the user and asks which item they would like to remove from their wishlist.
def remove_wishlist(username, wishlist):

    print("*****************************************\n")

    for i, wish in enumerate(wishlist):
        print(f'{i+1} - {wish}')

    remove_choice = input("\nPlease enter the number corresponding to the item you want to remove, or '0' to return back to the previous menu: ")

    remove_index = int(remove_choice) - 1
 

    try:

        if remove_index == -1:
            print("*****************************************\n*****************************************\n")
            return # we return if the enter users '0', it is entered as -1 because we compensate for the index starting at 0 previously

        if 0 <= remove_index < len(wishlist):

            removed_item  = wishlist.pop(remove_index)


            print("\n*****************************************\n")
            print("Removed from your wishlist - ")
            print(str(removed_item) + '\n')
            print("\n*****************************************\n\n")


    except ValueError:
        print("Invalid input. Please enter a number.")

    except Exception as e:

        print('Error: ' + str(e))

    return wishlist


# A function that holds 2 different types of filters, allowing the user to sort data by brands, and as well as price ranges to better fit their budget.
def add_filter(username):

 
    global brand_filters
    global price_filter

    # if the price_filter is not yet declared, it is set to None as a placeholder
    if 'price_filter' not in globals():
        price_filter = None

    def price_range():

        global price_filter

        while True:
            try:

                min_price = input("Enter the minimum price for your results you would like: ")
                
                max_price = input("Enter the maximum price for your results you would like: ")
                if float(max_price) <= float(min_price):
                    raise Exception("Maximum must be greater than minimum.")
                else:
                    break

            except ValueError:
                print("Please enter a number.")
            except Exception as e:
                print(e)

        min_price = float(min_price)
        max_price = float(max_price)

         
        price_filter = Range_Filter(min_price, max_price)
        print(f"Items will now only be shown within the range: {price_filter}")
            
      

        return price_filter

    def change_brands():

        global brand_filters

        brands = []
        chosen_brands = []
        data_files = [
            'cpudata.txt', 'gpudata.txt', 'motherboarddata.txt', 'ramdata.txt', 
            'harddrivedata.txt', 'ssddata.txt', 'psudata.txt', 'casedata.txt', 
            'cpucoolerdata.txt', 'keyboarddata.txt', 'mousedata.txt', 'monitordata.txt', 
            'headsetdata.txt'
        ]
        
        for data in data_files:
            with open(data, 'r') as file:
                for line in file:
                    unique = True
                    line = line.split(',')
                    brand = line[0]
                    if brand.lower() in [b.lower() for b in brands]:
                        unique = False
                    if unique:
                        brands.append(brand)

        for i, brand in enumerate(brands):
            print(f'{i+1} - {brand}')
        
        print("This is a list of all unique brands within our data.")
        print("Please enter the number corresponding to the brand you would like, or '0' to finish choosing brands - ")
        
        while True:
            try:
                user_choice = int(input("Enter: "))
                if 1 <= user_choice <= len(brands):

                    brand_object = Brand_Filter(brands[user_choice-1])

                    if brand_object not in chosen_brands and brand_object not in brand_filters:

                        chosen_brands.append(brand_object)

                    else:
                        print("Brand is already within the list.")
                elif user_choice == 0:
                    break
                else:
                    raise Exception("Invalid entry, please enter within the range.")
            except ValueError:
                print("Invalid entry, please enter a number.")
            except Exception as e:
                print("Error: " + str(e))
                     
        print("You chose: ")

        if chosen_brands:

            for i, brand in enumerate(chosen_brands):
                print(f'{i+1} - {brand}')

        else:
            print("No brands added.")
        return chosen_brands
    

    if brand_filters is None:

        brand_filters = []

    filter_options = ['Price-Range', 'Brands']
    for i, filter_option in enumerate(filter_options):
        print(f"{i+1} - {filter_option}")

    while True:
        remove_choice = input("\nPlease enter the number corresponding to the type of filter you want to add, or '0' to finish adding filters: ")

        try:

            remove_choice = int(remove_choice)
            if 0 <= remove_choice <= len(filter_options):

                if remove_choice == 1:
                    
                    price_filter = price_range()


                elif remove_choice == 2:

                    brand_filters.extend(change_brands())
                elif remove_choice == 0:
                    break

            else:
                raise Exception("Entry not in range of list.")
        except ValueError:
            print("Invalid entry, please enter an integer.")
        except Exception as e:
            print("Error: " + str(e))

    print("You chose - ")
    print("\n************************************\n")

    if not price_filter and not brand_filters:
        print("No filters added.")
        #print that there are no filters if there is no values within either filters
    else:

        if price_filter:

            print(f"Price Range: {price_filter}")

        if brand_filters:

            print(f"Brands: {', '.join(str(bf) for bf in brand_filters)}")

    return price_filter, brand_filters

  
    
    

    

# Prompts the user to ask which type of filter they would like to remove
def remove_filter():

    global brand_filters
    global price_filter

    print("1 - Price Filter")
    print("2 - Brand Filter")

    while True:

        try:

            choice = int(input("Enter the coorelated number in order to remove the filter of that category, or '0' to return: "))

            if choice == 1:

                if not price_filter:
                    print("No price filters active.")
                else:

                    price_filter = None
                    print("Succesfully removed price filters.")

            elif choice == 2:

                if not brand_filters:
                    print("No brand filters active.")
                else:
                    brand_filters = None
                    print("Succesfully removed brand filters.")

            elif choice == 0:
                break

            else:
                raise Exception("Please enter a valid number.")

        except ValueError:
            print("Invalid entry, please enter an integer")
    
    return


# Returns the filters to a different function, allowing it to check whether or not load_filters() needs to be ran.
def get_filters():
    global price_filter, brand_filters
    return price_filter, brand_filters

# This is ran in the event that there are filters in place, in which then it sorts through the data, appending to a list named modified_data and then returning that list, replacing the old list of data.
def load_filters(data):
    print("Loading Filters.")
    
    global price_filter
    global brand_filters

    modified_data = data

    
    if price_filter:
        print("Applying price filters.")
        modified_data = [item for item in modified_data if price_filter.min <= float(item.price) <= price_filter.max]


   
    if brand_filters:
        print("Applying brand filters.")
        modified_data = [item for item in modified_data if item.brand in [brand.brand for brand in brand_filters]]

   
    if not modified_data:
        print("No items found with the applied filters.")


    return modified_data

# Displays the items again, but allows the user to add an item to their wishlist as well as check out
def item_display(username, data):

    import math

    placeholder = None
    page_number = None

    try:        
        price_filter, brand_filters = get_filters()
    except:
        price_filter, brand_filters = None, None

    
    if price_filter or brand_filters:
        data = load_filters(data)

    if not data:
        return
    
    while True:

        try: 

            
            print("\n**********************************************************\n")

            placeholder = page_number

            page_number = input(f"Please enter the page number you would like to go to, or '0' to go back to the menu, there are {math.ceil(len(data)/20)} pages: ")

            print("\n**********************************************************\n")

            #we use a if statement here to pass by the get_page() function if the user enters -1, because otherwise it will result in the page returning as 'None'

            if int(page_number) == -1:

                page_number = placeholder
                break #break out of the while loop in order to retain page_number and return the proper page.

            else:


                from main import get_page
                    
                    
                page = get_page(page_number, data)

            if page is not None:
                print(f"Page {page_number}:")
                        
                for i, line in enumerate(page):
                    print(f"{i+1} - {line}")

                print("\n**********************************************************\n")

                print("To add an item to the wishlish, enter -1 instead: ")


            elif int(page_number) == 0: 

                from main import userMainScreen
                    
                userMainScreen(username)
                break

            else:
                print("Page number out of range. Please try again.")
            


        except Exception as e:
            print("Error: " + str(e))
    
    
    return page

# Prompts the user with a list of extra options, including viewing their shopping cart, removing from shopping cart, adding items to wishlist, removing items from wishlist, and adding and removing search filters.
def more_options(username, shopping_cart, partList):

    

    options = ["View Shopping Cart", "Remove Items From Shopping Cart", "Add Item to Wishlist", "Remove From Wishlist", "Add Search Filter", "Remove Search Filter"]

    wishlist = []

    #we initialize here so that we can check if it is empty later.

    while True:

        print("\nHere is a list of more options - ")
        print('\n')

        for i, option in enumerate(options):
            print(f"{i+1} - {option}")

        print('\n********************************\n')
        user_choice = input("Please enter the needed options number, or '0' to return back to the original menu: ")


        try:

            user_choice = int(user_choice)
            

            if user_choice == 1:
                view_cart(username, shopping_cart)
                

            elif user_choice == 2:
                remove_cart(username, shopping_cart)
                

            elif user_choice == 3:
                wishlist = add_wishlist(username, partList)
                

            elif user_choice == 4:
    
                if not wishlist:
                    print("Wishlist is empty.")

                else:

                    wishlist = remove_wishlist(username, wishlist)
                

            elif user_choice == 5:
                global filters

                filters = add_filter(username)

                

            elif user_choice == 6:

                if filters:

                    filters = remove_filter()
                else:
                    print("No active filters.")
                

            elif user_choice == 0:
                from main import userMainScreen

                userMainScreen(username)
                break

            else: 
                raise Exception




        except ValueError as e:
            import time
            
            print("Invalid input...")
            time.sleep(.5)
            print("Please try again - ")
            time.sleep(.5)