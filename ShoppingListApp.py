"""
This is a python class that will store and update a shopping list including costs and shit in a database so that you can access, view previous
shopping list and compare prices etc for budgeting.
"""
import sqlite3

class ShoppingListApp:

    def __init__(self) -> None:
        self.connector = sqlite3.connect("ShoppingList.db")
        self.cursor = self.connector.cursor()
        self.tableInUse = None

    def returnTables(self) -> list:
        return self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

    def createTable(self, shopName) -> str:
        try:
            self.cursor.execute(f"CREATE TABLE {shopName} (item VARCHAR(20) PRIMARY KEY, quantity INTEGER, unitPrice FLOAT, totalPrice FLOAT, catagory VARCHAR(10), description VARCHAR(80));")
            return None
        except sqlite3.OperationalError:
            return f"Query Rejected: Table '{shopName}' already exists!"
        except Exception as e:
            return e

    def validateItemName(self) -> str:
        while True:
            item = input("Item Name: ")
            if len(item) <= 255:
                return item
            else:
                print("Invalid Input: Length must be 20 characters or less.")
        #ENDWHILE

    def validateQuantity(self) -> int:
        while True:
            quantity = input("Quantity: ")
            if quantity.isdigit():
                return quantity
            else:
                print("Invalid Input: Must be an integer.")
        #ENDWHILE

    def validateUnitPrice(self) -> float:
        while True:
            unitPrice = input("Unit Price: ")
            if unitPrice.replace(".", "").isdigit():
                return unitPrice
            else:
                print("Invalid Input: Must be a non-negative real number.")
        #ENDWHILE

    def validateTotalPrice(self, quantity, unitPrice) -> float:
        while True:
            offer = input("Is there a discount (y/n)? ")
            if offer == "n":
                return float(quantity) * float(unitPrice)
            elif offer == "y":
                while True:
                    totalPrice = input("Total Price: ")
                    if totalPrice.replace(".","").isdigit():
                        return totalPrice
                    else:
                        print("Invalid Input: Must be a non-negative real number.")
                        break
                #ENDWHILE
            else:
                continue
        #ENDWHILE

    def validateCategory(self) -> str:
        while True:
            category = input("Category: ")
            if len(category) <= 10 and category.count(" ") == 0:
                return category
            else:
                print("Invalid Input: Must be one word of 10 characters or less")
        #ENWHILE

    def validateDescription(self) -> str:
        while True:
            description = input("Description: ")
            if len(description) <= 80:
                return description
            else:
                print("Invalid Input: Must be less than 80 characters long.")
                

    def enterTable(self, table) -> None:
        self.tableInUse = table

        while True:
            while True:
                print(f"{self.tableInUse}:")
                print(f"\t 1. View List.")
                print(f"\t 2. Add item to list.")
                print(f"\t 3. Remove item from list.")
                print(f"\t 4. Update value in list.")
                print(f"\t 5. Return to main menu.")
                print(f"\n")
                print(f"Enter number of the desired function...")
                response = input("Input: ")
                if response.isdigit() == False:
                    continue
                else:
                    response = int(response)
                    if response == 1:
                        print(self.viewTableContents())
                        break
                    elif response == 2:
                        print("Enter Details about the item:")
                        itemName = self.validateItemName()
                        quantity = self.validateQuantity()
                        unitPrice = self.validateUnitPrice()
                        totalPrice = self.validateTotalPrice(quantity, unitPrice)
                        category = self.validateCategory()
                        description = self.validateDescription()

                        errorMessage = self.insertIntoTable(itemName, quantity, unitPrice, totalPrice, category, description)
                        if errorMessage == None:
                            print(f"Query Accepted: {itemName} inserted into {self.tableInUse}.")
                            break
                        else:
                            print(errorMessage)
                    elif response == 3:
                        print("\n")
                        itemToRemove = input("Item You would like to remove (just press enter to go back): ")
                        if itemToRemove == "":
                            break
                        else:
                            errorMessage = self.deleteFromTable(itemToRemove)
                            if errorMessage == None:
                                print(f"Query Accepted: {itemToRemove} removed from {self.tableInUse}.")
                                break
                            else:
                                print(errorMessage)
                    elif response == 4:
                        itemToChange = input("What item would you like to update? ")
                        tableContents = self.getTableContents()
                        if itemToChange not in [item[0] for item in tableContents]:
                            print("ERROR: Item not in the list.")
                        else:
                            # Print the item the user desires to change:
                            itemProperties = self.viewItemProperties(itemToChange)[0]
                            seperator = "|______________________________________________________________________________________________________________________________________________________|\n"
                            output = " ______________________________________________________________________________________________________________________________________________________ \n"
                            output += "|{:20s}|{:10s}|{:12s}|{:13s}|{:10s}|{:<80s}|\n".format("Item:", "Quantity:", "Unit Price:", "Total Price:", "Category:", "Description:")
                            output += "|____________________|__________|____________|_____________|__________|________________________________________________________________________________|\n"
                            output += "|{:20s}|{:>10}|{:>12.2f}|{:13.2f}|{:<10}|{:<80s}|\n".format(itemProperties[0], itemProperties[1], itemProperties[2], itemProperties[3], itemProperties[4], itemProperties[5])
                            output += seperator
                            print(output)

                            print("Enter updated values below (to keep old values just press enter):")
                            changedQuantity = self.validateQuantity()
                            changedUnitPrice = self.validateUnitPrice()
                            changedTotalPrice = self.validateTotalPrice(changedQuantity, changedUnitPrice)

                            errorMessage = self.updateTable(itemToChange, changedQuantity, changedUnitPrice, changedTotalPrice)

                            if errorMessage == None:
                                print(f"Update Successful...")
                            else:
                                print(errorMessage)
                                break

                    elif response == 5:
                        self.exitTable()
                        print("Entering Main Menu...")
                        return
                    else:
                        continue
                    #ENDIF
                #ENDIF
        #ENDWHILE
    
    def insertIntoTable(self, item, quantity, unitPrice, totalPrice, catagory, shortDescription) -> int:
        try:
            self.cursor.execute(f"INSERT INTO {self.tableInUse} VALUES('{item}', {quantity}, {unitPrice}, {totalPrice}, '{catagory}', '{shortDescription}')")
            return None
        except sqlite3.OperationalError:
            return f"Query Rejected: Invalid values."
        except Exception as e:
            return e

    def deleteFromTable(self, item) -> int:
        try:
            self.cursor.execute(f"DELETE FROM {self.tableInUse} WHERE id='{item}';")
            return None
        except sqlite3.OperationalError:
            return f"Query Rejected: Item does not exist."
        except Exception as e:
            return e

    def updateTable(self, item, quantity, unitPrice, totalPrice) -> str:
        try:
            self.cursor.execute(f"UPDATE {self.tableInUse} SET quantity={quantity}, unitPrice={unitPrice}, totalPrice={totalPrice} WHERE id='{item}'")
            return None
        except Exception as e:
            return e

    def exitTable(self) -> None:
        self.tableInUse = None

    def dropTable(self, shopName) -> str:
        try:
            self.cursor.execute(f"DROP TABLE {shopName};")
            return None
        except sqlite3.OperationalError:
            return f"Query Rejected: Table '{shopName}' does not exist!"
        except Exception as e:
            return e

    def getTableContents(self) -> list:
        try:
            return self.cursor.execute(f"SELECT * FROM {self.tableInUse}").fetchall()
        except Exception as e:
            return e

    def viewTableContents(self) -> str:
        contents = self.getTableContents()

        if contents == None:
            return "No items in this shop."

        seperator = "|______________________________________________________________________________________________________________________________________________________|\n"
        
        # format Table:
        output = " ______________________________________________________________________________________________________________________________________________________ \n"
        output += "|{:20s}|{:10s}|{:12s}|{:13s}|{:10s}|{:<80s}|\n".format("Item:", "Quantity:", "Unit Price:", "Total Price:", "Category:", "Description:")
        output += "|____________________|__________|____________|_____________|__________|________________________________________________________________________________|\n"
        for i in range(0, len(contents)):
            output += "|{:20s}|{:>10}|{:>12.2f}|{:13.2f}|{:<10}|{:<80s}|\n".format(contents[i][0], contents[i][1], contents[i][2], contents[i][3], contents[i][4], contents[i][5])
        
        output += seperator

        return output

    def viewItemProperties(self, item) -> str:
        try:
            return self.cursor.execute(f"SELECT * FROM {self.tableInUse} WHERE id='{item}';").fetchall()
        except Exception as e:
            return e



    def closeApp(self) -> None:
        print("Closing App...")
        self.connector.commit()
        self.connector.close()
        self.tableInUse = None

    def run(self) -> int:
        print("At Any point to close the app, type 'close' into the input.\n\n")

        while True:
            print("Main Menu: Selet a Shop...")
            tables = self.returnTables()
            if len(tables) != 0:
                tables = [table[0] for table in tables]
                for i, table in enumerate(tables):
                    print(f"\t{i+1}. {table}")
            else:
                print(f"\tThere are no shops yet.")
            #ENDIF
            print("\n")
            print(f"Or:\n\t- 'CREATE [shop name]': Starts a new shop list.\n\t- 'DELETE [shop name]': Deletes the chosen shopping list\n\t- 'close': Save changes and quit.")
            print()

            while True:
                response = input("Input: ")
                if len(response) == 0:
                    continue
                elif response.isdigit():
                    response = int(response)
                    if response <= len(tables) and response >= 1:
                        print(f"Query Accepted: Entering {tables[response-1]}")
                        self.enterTable(tables[response-1])
                        break
                elif response == "close":
                    self.closeApp()
                    return 0
                else:
                    response = response.split(" ", maxsplit=1)
                    if response[0] == "CREATE":
                        errorMessage = self.createTable(response[1])
                        if errorMessage == None:
                            print(f"Query Accepted: Creating {response[1]}")
                            break
                        else:
                            print(errorMessage)
                            continue
                    elif response[0] == 'DELETE':
                        errorMessage = self.dropTable(response[1])
                        if errorMessage == None:
                            print(f"Query Accepted: Deleting {response[1]}")
                            break
                        else:
                            print(errorMessage)
                            continue
                    #ENDIF
                #ENDIF
            #ENDWHILE
            print("\n\n\n")
        #ENDWHILE
    #ENDPROCEDURE
#ENDCLASS

