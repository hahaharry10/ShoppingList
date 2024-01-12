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
            self.cursor.execute(f"CREATE TABLE {shopName} (id item VARCHAR(255) PRIMARY KEY, quantity INTEGER, unitPrice FLOAT(23), totalPrice FLOAT(23), catagory VARCHAR(255), description VARCHAR(255));")
            return None
        except sqlite3.OperationalError:
            return f"Query Rejected: Table '{shopName}' already exists!"
        except Exception as e:
            return e

    def enterTable(self, table) -> None:
        self.tableInUse = table

        while True:
            print(f"{self.tableInUse}:")
            print(f"\t 1. View List.")
            print(f"\t 2. Add item to list.")
            print(f"\t 3. Remove item from ist.")
            print(f"\t 4. Return to main menu.")
            print(f"\n")
            print(f"Enter number of the desired function...")
            
            while True:
                response = input("Input: ")
                if response.isdigit() == False:
                    continue
                else:
                    response = int(response)
                    if response == 1:
                        print(self.viewTableContents())
                        break
                    elif response == 2:
                        while True:
                            item = input("Item: ")
                            if len(item) <= 255:
                                break
                        while True:
                            quantity = input("Quanity: ")
                            if quantity.isdigit():
                                break
                        while True:
                            unitPrice = input("Unit Price: ")
                            if unitPrice.replace(".", "").isdigit():
                                break
                        while True:
                            totalPrice = input("Total Price: ")
                            if totalPrice.replace(".", "").isdigit():
                                break
                        while True:
                            catagory = input("Catagory: ")
                            if len(catagory) < 255 and catagory.count(" ") == 0:
                                break
                            else:
                                print("Only one word of max 255 characters allowed.")
                        while True:
                            shortDescription = input("Total Price: ")
                            if len(shortDescription) < 255:
                                break
                        errorMessage = self.insertIntoTable(item, quantity, unitPrice, totalPrice, catagory, shortDescription)
                        if errorMessage == None:
                            print(f"Query Accepted: {item} inserted into {self.tableInUse}.")
                            break
                        else:
                            print(errorMessage)
                    elif response == 3:
                        pass
                    elif response == 4:
                        self.exitTable()
                        print("Entering Main Menu...")
                        return
                    else:
                        continue
                    #ENDIF
                #ENDIF
            #ENDWHILE
            print("\n\n")
        #ENDWHILE
    
    def insertIntoTable(self, item, quantity, unitPrice, totalPrice, catagory, shortDescription) -> int:
        try:
            self.cursor.execute(f"INSERT INTO {self.tableInUse} VALUES({item}, {quantity}, {unitPrice}, {totalPrice}, {catagory}, {shortDescription})")
            return None
        except sqlite3.OperationalError:
            return f"Query Rejected: Invalid values."
        except Exception as e:
            return e

    def updateTable(self) -> int:
        pass

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

    def viewTableContents(self) -> str:
        try:
            return self.cursor.execute(f"SELECT * FROM {self.tableInUse}").fetchall()
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
            print(f"Or:\n\t- 'CREATE [shop name]': Starts a new shop list.\n\t- 'DELETE [shop name]': Deletes the chosen shopping list")
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