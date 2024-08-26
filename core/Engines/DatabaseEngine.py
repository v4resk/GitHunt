import json
import csv
import sqlite3
import os
from os.path import join as path_join
from core.Config.Config import Config 
from colorama import Fore
import datetime
from colorama import Fore


class DatabaseEngine():
    def __init__(self, available_modules ,db_file="githunt.db"):
        #Init DB
        db_folder = Config().get("FOLDERS", "DB_FOLDER")
        db_path = path_join(db_folder, db_file)

        if not os.path.exists(db_folder):
            os.makedirs(db_folder)
        if not os.path.exists(db_path):
            f"{Fore.YELLOW}[+] {Fore.WHITE} Initializing the database"

        f"{Fore.YELLOW}[+] {Fore.WHITE} Connecting to the database..."
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_tables(available_modules)


    def create_tables(self, available_modules):
        for module in available_modules:
            table_name = module
            # Define the SQL command to create the table
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                value TEXT NOT NULL,
                isValid TEXT NOT NULL,
                lastChecked TEXT NOT NULL
            );
            """
            # Execute the SQL command
            self.cursor.execute(create_table_sql)
        # Commit changes and close the connection
        self.connection.commit()


    def db_value_exists(self,value,module):
        self.cursor.execute(f"SELECT * FROM {module} WHERE value = ?", (value,))
        return self.cursor.fetchone() is not None

    def db_add_value(self,value,isValid,module):
        current_date = datetime.date.today()
        self.cursor.execute(
            f"INSERT INTO {module}(value, isValid, lastChecked) VALUES(?, ?, ?)",
            (value, isValid, current_date),
        )
        self.connection.commit()
        #print(f"{Fore.GREEN}[+] {Fore.WHITE}{value} added to database !")

    def db_delete_value(self,value,module):
        self.cursor.execute(f"DELETE FROM {module} WHERE value = ?", (value,))
        self.connection.commit()
    
    def exportDB(self,module, format, output,exportAll):
        # Determine the query based on exportAll flag
        if exportAll:
            query = f"SELECT * FROM {module}"
        else:
            query = f"SELECT * FROM {module} WHERE isValid LIKE '%YES%'"
        
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # Export to JSON
        if format == "json":
            data = [{"value": row[0], "isValid": row[1], "lastChecked": row[2]} for row in rows]
            with open(output, 'w') as json_file:
                json.dump(data, json_file, indent=4)

        # Export to CSV
        elif format == "csv":
            with open(output, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["value", "isValid", "lastChecked"])  # CSV header
                writer.writerows(rows)

        # Export to TXT
        elif format == "txt":
            with open(output, 'w') as txt_file:
                for row in rows:
                    txt_file.write(f"Value: {row[0]} isValid: {row[1]} LastChecked: {row[2]}\n")

        print(f"{Fore.GREEN}[+] {Fore.WHITE} Database exported successfully to {output} in {format} format.")



    def close(self):
        """Close the database connection."""
        self.connection.close()