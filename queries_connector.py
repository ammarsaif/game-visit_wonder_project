import mysql.connector


def connect_database():
    return mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='visit_wonder',
        user='root',
        password='1472',
        autocommit=True
    )



class SelectQueries:
    def __init__(self, connection):
        self.connection = connection

    def select(self, query, table, where, additional_query=''):
        sql = f"SELECT {query} FROM {table}"

        if where != '':
            sql += f" WHERE {where}"

        if additional_query != '':
            sql += additional_query

        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()

        return result



    def check_player_exists(self, player_email):
        sql = 'SELECT * FROM users WHERE email = %s;'

        with self.connection.cursor() as cursor:
            cursor.execute(sql, (player_email,))
            existing_player = cursor.fetchall()

        if existing_player:
            # Returning the player information
            return existing_player[0]  # only expect one result
        else:
            # Player not found
            return None

class InsertQueries:
    def __init__(self, connection):
        self.connection = connection

    def insert_new_player(self, player_email, name, location):
        sql = 'INSERT INTO users (email, name, current_location) VALUES (%s, %s, %s);'


        with self.connection.cursor() as cursor:
            cursor.execute(sql, (player_email, name, location))

        self.connection.commit()


class UpdateQueries:
    def __init__(self, connection):
        self.connection = connection

    def update(self, table, field_and_value, where, values=None):
        sql = f"UPDATE {table} SET {field_and_value} WHERE {where}"

        # Using parameterized queries to prevent SQL injection
        with self.connection.cursor() as cursor:
            if values:
                cursor.execute(sql, values)
            else:
                cursor.execute(sql)

        self.connection.commit()

    def update_location(self, location, player_email):
        current_location = 'Helsinki'
        sql = 'UPDATE users SET current_location = %s WHERE email = %s;'
        values = (location, player_email)

        with self.connection.cursor() as cursor:
            cursor.execute(sql, values)

        self.connection.commit()


    def update_difficulty(self, difficulty, player_email):
        table = 'users'
        field_and_value = "co2_budget = %s"
        where = "email = %s"
        values = (difficulty, player_email)

        sql = f"UPDATE {table} SET {field_and_value} WHERE {where}"

        with self.connection.cursor() as cursor:
            cursor.execute(sql, values)

        self.connection.commit()

    def update_game_win_threshold(self, game_win, player_email):
        table = 'users'
        field_and_value = "game_win = %s"
        where = "email = %s"
        values = (game_win, player_email)

        sql = f"UPDATE {table} SET {field_and_value} WHERE {where}"

        with self.connection.cursor() as cursor:
            cursor.execute(sql, values)

        self.connection.commit()

"""
sql = 'SELECT ident, municipality, name FROM airport WHERE ident = "EFHK";'
cursor.execute(sql)
result = cursor.fetchone()
if result:
    icao, municipality, name = result
    print({"ICAO": icao, "Name": name, "Location": municipality})


player_name = "Ammi"
player_email = "Ammi@ammi.com"
player_co2 = 16000

sql = 'insert into user (player_name, email) values (%s, %s);'
cursor.execute(sql, (player_name, player_email))
wonderDatabase.commit()
cursor.close()
wonderDatabase.close()
"""