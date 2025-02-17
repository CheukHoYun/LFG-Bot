import mysql.connector
from mysql.connector import Error

class DataHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataHandler, cls).__new__(cls)
            cls._instance.connection = cls._instance.connect_to_db()
        return cls._instance
    def connect_to_db(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',  # or your host, e.g., remote database server
                database='GameDB',
                user='lfg_db_user',  # your database username
                password='your_password'  # your database password
            )
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def check_connection(self):
        try:
            # Attempt a simple operation that requires an active connection.
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return True
        except:
            # If the operation fails, the connection is not active.
            return False


    def get_game_id(self, discord_user_id, game_name, logging=True):
        try:
            if not self.check_connection():
                self.connection = self.connect_to_db()
            connection = self.connection
            cursor = connection.cursor()
            query = f"SELECT game_id FROM UserGameIDs WHERE discord_user_id = {discord_user_id} AND game_name = '{game_name}'"
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            # print(f"[DB] Retrieving game id: discord_user_id={discord_user_id}, game_name={game_name}, result={result}")
            if logging:
                print(f"[DataBase]\tRetrieving:({discord_user_id}, {game_name}). ")
                if result is None:
                    print(f"[DataBase]\tNo result found.")
                else:
                    print(f"[DataBase]\tFound name: {result[0]}")
            return result
        except Error as e:
            print(f"Error while interacting with MySQL: {e}")
            return None




    def add_game_id(self, discord_user_id, game_name, game_id):
        try:
            if not self.check_connection():
                self.connection = self.connect_to_db()
            connection = self.connection
            cursor = connection.cursor()
            query = "INSERT INTO UserGameIDs (discord_user_id, game_name, game_id) VALUES (%s, %s, %s)"
            cursor.execute(query, (discord_user_id, game_name, game_id))
            connection.commit()
            cursor.close()
            connection.close()
            print(f"[DataBase]\tEntry added: ({discord_user_id, game_name} -> {game_id})")
        except Error as e:
            print(f"Error while interacting with MySQL: {e}")

    def edit_game_id(self, discord_user_id, game_name, new_game_id):
        try:
            if not self.check_connection():
                self.connection = self.connect_to_db()
            connection = self.connection
            cursor = connection.cursor()
            query = """
            UPDATE UserGameIDs 
            SET game_id = %s 
            WHERE discord_user_id = %s AND game_name = %s
            """
            cursor.execute(query, (new_game_id, discord_user_id, game_name))
            connection.commit()
            cursor.close()
            connection.close()
            # print(f"[DB] Modifying entry: Updated game ID for user {discord_user_id} for game {game_name} to {new_game_id}")
        except Error as e:
            print(f"Error while interacting with MySQL: {e}")

    def try_edit_or_add_game_id(self, discord_user_id, game_name, new_game_id):
        # Try to edit the game ID first
        print(f"[DataBase]\tModification attempt: ({discord_user_id, game_name} -> {new_game_id})")
        self.edit_game_id(discord_user_id, game_name, new_game_id)

        # Check if the edit was successful
        if self.get_game_id(discord_user_id, game_name, logging=False) is None:
            print(f"[DataBase]\tModification failed. Adding instead.")
            # If the entry doesn't exist, add it
            self.add_game_id(discord_user_id, game_name, new_game_id)
        else:
            print(f"[DataBase]\tModification Successful.")
