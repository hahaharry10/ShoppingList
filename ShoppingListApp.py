"""
This is a python class that will store and update a shopping list including costs and shit in a database so that you can access, view previous
shopping list and compare prices etc for budgeting.
"""
import sqlite3

class ShoppingListApp:
    def __init__(self) -> None:
        self.connector = sqlite3.connect("ShoppingList.db")
        self.cursor = self.connector.cursor()
    #ENDINITIALISATION

    def returnTables(self) -> list:
        return self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

    def createTable(self, shopName) -> int:
        try:
            self.cursor.execute(f"CREATE TABLE {shopName} (id item VARCHAR(255) PRIMARY KEY, quantity INTEGER, unitPrice FLOAT(23), totalPrice INTEGER, catagory VARCHAR(255), description VARCHAR(255));")
            return 0
        except sqlite3.OperationalError:
            print(f"Query Rejected: Table '{shopName}' already exists!")
            return 1
        except Exception as e:
            print(f"ERROR: {e}")
            return 1
        #ENDEXCEPTION

    def enterTable(self, table) -> int:
        pass

    def exitTable(self) -> None:
        pass

    def dropTable(self, tableName) -> int:
        try:
            self.cursor.execute(f"DROP TABLE {tableName};")
            return 0
        except Exception as e:
            print(f"ERROR: {e}")
            return 1

    def insertIntoTable(self, row) -> int:
        pass

    def updateTable(self) -> int:
        pass

    def closeApp(self) -> None:
        print("Closing App...")
        self.connector.commit()
        self.connector.close()

    def run(self) -> int:
        print("At Any point to close the app, type 'close' into the input.\n\n")

        while True:
            print("Main Menu: Selet a Shop...")
            tables = self.returnTables()
            if len(tables) != 0:
                for i, table in enumerate(self.returnTables()):
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
                        break
                elif response == "close":
                    self.closeApp()
                    return 0
                else:
                    response = response.split(" ", maxsplit=1)
                    print(response)
                    if response[0] == "CREATE":
                        self.createTable(response[1])
                        break
                    elif response[0] == 'DELETE':
                        self.dropTable(response[1])
                        break
                #ENDIF
            #ENDWHILE
            
            print("\n\n\n")
        #ENDWHILE
    #ENDPROCEDURE
#ENDCLASS