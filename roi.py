import re

class Property():
    def __init__(self, address, state, rent, coi):
        self.address = address
        self.state = state
        self.rent = rent
        self.coi = coi

    def change_rent(self):
        print("""
*****************************************************************
Rent Data:
        """)
        with open('grossrents.txt') as f:
            data = f.read()

        us_data = re.search('(USA)\)\s+(\$\d+)', data)
        state_data = re.search(f'([A-z ]+)\s+\(({self.state})\)\s+(\$\d+)', data)
        # show median gross rent for USA and the State of the property
        if state_data:
            print(f"The current median gross rent in the United States is {us_data.group(2)}.")
            print(f"The current median gross rent in the State of {state_data.group(1)} is {state_data.group(3)}.")
            print(f"The current rent of {self.address} in {self.state} is ${self.rent}.")
            print('*****************************************************************')

        new_rent = float(input("What is the new rent? $"))
        old_rent = self.rent
        self.rent = new_rent
        print(f"The rent of {self.address} in {self.state} has been updated from ${old_rent} to ${new_rent}.")

    def change_coi(self, new_coi):
        old_coi = self.coi
        self.coi = new_coi
        print(f"The COI of {self.address} in {self.state} has been updated from ${old_coi} to ${new_coi}.")

    def __repr__(self):
        return f"\nProperty: {self.address}\nLocation: {self.state}\nRent: ${self.rent}\nCOI: ${self.coi}"

    

class ROI():
    def __init__(self):
        self.users = {} # key = user, value = property(s) in array

    def add_user(self):
        while True: # double check if username is available
            username = input("Please create an username: ").lower().strip()
            if username in self.users:
                print(f"\nThe username {username} already exists. Please use a different username.")
            else:
                # if the username is available, add it to users dictionary and set the value to an empty arr
                # this arr will be used to store all of the users properties
                self.users[username] = []
                print(f"{username}'s account has been created!")
                break

    def del_user(self):
        username = input("Please input the username you want to delete: ").lower().strip()
        # check if username exists
        if username in self.users:
            del self.users[username]
            print(f"{username}'s account has been deleted.")
        else:
            print(f"\n{username} does not exist. Returning to Main Menu.")

    def view_users(self):
        print(f"""
**************
Current Users:
        """)

        if self.users:
            for user in self.users:
                print(user)
            print("**************")
        else:
            print("NONE\n**************")

    def add_property(self, username):
        # property #, street name, and state are used to check that no duplicate properties are added to current user's property listings
        addy = input("Enter the property number and street name (ex. 123 Main St):\n").title().strip()
        
        # grab all United States State abbreviations and store in a list so we can
        # make sure user enters the correct state abbreviations
        with open('grossrents.txt') as f:
            data = f.readlines()
        state_abbreviations = []
        for line in data:
            found = re.search('\(([A-Z]{2})\)', line)
            if found:
                state_abbreviations.append(found.group(1)) 

        while True:
            state = input("Enter the State where the property resides in abbreviated format (ex. for Maryland, enter MD):\n").upper().strip()
            if len(state) == 2 and state in state_abbreviations:
                break
            else:
                print("Invalid State abbreviation. Please try again.")
        
        # in order to check if the property already exits
        # check arrays are created to hold all of the address/state attributes from our Property class
        check_addy = []
        check_state = []
        for p in self.users[username]:
            check_addy.append(p.address)
            check_state.append(p.state)

        if addy in check_addy and state in check_state:
            print(f"The property: {addy} in {state} already exists in your list of properties.")
        else:
            rent = float(input("Enter the current rent of the property: $"))
            coi = float(input("Enter the cost of investment (COI) of the property: $"))
            self.users[username].append(Property(addy, state, rent, coi))
            print(f"The property: {addy} in {state} has been added to your list of properties!")

    def del_property(self, username):
        # user needs to input both addy and state because property #s/street names are not unique.
        # we need property #, strett name, and state to find the unique property in our list of properties
        addy = input("Enter the property number and street name of the property you wish to remove:\n").title().strip()
        state = input("Enter the State where the property resides in abbreviated format (ex. for Maryland, enter MD):\n").upper().strip()

        # loop through our user's list of properties. if we find a property that matches the addy and state that the user
        # previously entered, then we will delete the property from the user's list of properties
        for p in self.users[username]: # p is a Property object
            if addy == p.address and state == p.state:
                self.users[username].remove(p)
                print(f"Your property at {addy} in {state} has been removed from your list of properties.")
                break
        else:
            print(f"\nThe property: {addy} in {state} is not in your list of properties.")
            

    def view_properties(self, username):
        print(f"""
************************
{username}'s property(s):""")

        if self.users[username]:
            for p in self.users[username]:
                print(p)
                print(f"ROI: {self.cal_roi(p)}%") # users can also view the ROI of each property
            print("************************")
        else:
            print("\nNONE\n************************")

    def cal_roi(self,p):
        net_income = p.rent - p.coi
        roi = int((net_income/p.coi)*100)
        return roi

    def edit_property(self, username):
        addy = input("Enter the property number and street name of the property you want edit:\n").title().strip()
        state = input("Enter the State where the property resides in abbreviated format (ex. for Maryland, enter MD):\n").upper().strip()

        # loop through the user's property list to find a match
        for p in self.users[username]:
            # if the property is found, user can either change the rent or the coi
            if addy == p.address and state == p.state:
                print(f"The property: {addy} in {state} has been found in your list of properties!\n")
                choice = input("Enter 'Rent' to change the rent. Enter 'COI' to change the cost of investment.\n").lower().strip()
                
                if choice in ('rent', 'change rent'):
                    p.change_rent()
                    break
                elif choice in ('coi', 'change coi', 'cost of invesment', 'change cost of invesment'):
                    new_coi = float(input("What is the new cost of investment (COI)? $"))
                    p.change_coi(new_coi)
                    break
                else:
                    print("Invalid input. Returning to User Menu")
                    break
        else:
            print(f"\nThe property: {addy} in {state} is not in your list of properties.")

class Main():
    def print_main_menu():
        print("""
=========
Main Menu
=========

[1] Create New Account
[2] Delete Account
[3] Go to User Menu
[4] View Users
[5] Exit Application
        """) # view users option is used to double check your username's spelling and to let users know which usernames are taken
    
    def print_user_menu(username):
        print(f"""
======================
{username}'s User Menu
======================

[1] Add Property
[2] Remove Property
[3] Edit Property
[4] View Property(s) & View ROI of Each Property
[5] Back to Main Menu
        """)
    
    def run():
        roi = ROI()
        while True:
            Main.print_main_menu()

            choice = input("Please select from the options above: ").strip()
            if choice == '1':
                roi.add_user()
            elif choice == '2':
                roi.del_user()
            elif choice == '3':
                username = input("Enter your username: ").lower().strip()
                if username in roi.users:
                    while True:
                        Main.print_user_menu(username)

                        response = input("Please select from the options above: ").strip()
                        if response == '1':
                            roi.add_property(username)
                        elif response == '2':
                            roi.del_property(username)
                        elif response == '3':
                            roi.edit_property(username)
                        elif response == '4':
                            roi.view_properties(username)
                        elif response == '5':
                            print("Returning to Main Menu")
                            break
                        else:
                            print("Invalid input. Please try again.")
                else:
                    print(f"\nThe username: {username} does not exist. Please double check your spelling or create a new account.")
            elif choice == '4':
                roi.view_users()
            elif choice == '5':
                print("Exiting application.")
                break
            else:
                print("Invalid input. Please try again.")


Main.run()


