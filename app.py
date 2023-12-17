from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')
import queries_connector
import geopy.distance

# connect to the database queries classes
wonder_database = queries_connector.connect_database()
select_queries = queries_connector.SelectQueries(wonder_database)
insert_queries = queries_connector.InsertQueries(wonder_database)
update_queries = queries_connector.UpdateQueries(wonder_database)

#### Global Variables ###


#### list of destinations

def get_serial_numbers_list(condition):
    serial_numbers_query_result = select_queries.select('serial_num', 'airports',
                                                        condition)  # Assuming select_queries.select returns a list of tuples
    num_destination_list = [num[0] for num in
                            serial_numbers_query_result]  # Extracting the first element from each tuple and creating a list

    return num_destination_list


destinations_list = get_serial_numbers_list('serial_num < 17')

# Display unvisited lists


# check existing player in the database
def get_unvisited_destinations(player_email):
    # Get the list of all destinations
    all_destinations = get_serial_numbers_list('serial_num < 17')

    # Get the list of destinations visited by the player
    visited_destinations = select_queries.select('destination', 'player_visits', f"player_email='{player_email}'")

    # Filter out the visited destinations from the list of all destinations
    unvisited_destinations = [destination for destination in all_destinations if destination not in visited_destinations]

    return unvisited_destinations

def get_existing_player_info(email):
    existing_player = select_queries.select('email', 'users', f"email='{email}'")

    if existing_player:
        return existing_player[0][0]  # Returning the player information
    else:
        return None  # Player not found


# calculate distance

def calculate_distance(location_1, location_2):
    return geopy.distance.distance(location_1, location_2).km


# sub queries
def get_location_coordinates(destination_num):
    result = select_queries.select('latitude_deg, longitude_deg', 'airports',
                                   f"serial_num='{destination_num}'")[0]
    return result

# get location name from database
def get_location_name(location_num):
    result = select_queries.select('location', 'airports', f"serial_num='{location_num}'")
    return result[0][0]


# updates the destination in database

def update_new_destination(location, email):
    #update_queries.update_location('users', 'current_location = %s', 'email = %s', (chosen_num_by_player, player_email))
    update_queries.update_location(location, email)


# get co2 consumed by the player
def get_co2_consumed_by_player(email):
    result = select_queries.select('co2_consumed', 'users', f"email='{email}'")
    return result[0][0]


# update co2 of player in database
def update_co2_consumed(co2_consumed_by_player, player_email):
    update_queries.update('users', f"co2_consumed={co2_consumed_by_player}", f"email='{player_email}'")


# Game difficulty
difficulty = 0
difficulty_easy = 10000
difficulty_medium = 12000
difficulty_hard = 16000
game_win_easy = 7
game_win_medium = 10
game_win_hard = 14
game_win_threshold = 0
# player = None
current_location = 'Helsinki'
current_player_coordinates = select_queries.select('latitude_deg, longitude_deg', 'airports', f"serial_num='{17}'")[0]
select_destination_num = 0
input_destination = 0

num_visited_destinations = 0

@app.route('/index.html')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
