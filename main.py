import queries_connector
import geopy.distance

# connect to the database queries classes
wonder_database = queries_connector.connect_database()
select_queries = queries_connector.SelectQueries(wonder_database)
insert_queries = queries_connector.InsertQueries(wonder_database)
update_queries = queries_connector.UpdateQueries(wonder_database)


#### list of destinations

def get_serial_numbers_list(condition):
    serial_numbers_query_result = select_queries.select('serial_num', 'airports',
                                                        condition)  # Assuming select_queries.select returns a list of tuples
    num_destination_list = [num[0] for num in
                            serial_numbers_query_result]  # Extracting the first element from each tuple and creating a list

    return num_destination_list


def get_destinations_names_list(condition):
    destinations_query_result = select_queries.select('serial_num, location', 'airports', condition)
    destinations_list_dictionary = [{'serial_num': num[0], 'name': num[1]} for num in destinations_query_result]
    return destinations_list_dictionary


# check existing player in the database
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
    update_queries.update_location(location, email)


# get co2 consumed by the player
def get_co2_consumed_by_player(email):
    result = select_queries.select('co2_consumed', 'users', f"email='{email}'")
    return result[0][0]


# update co2 of player in database
def update_co2_consumed(co2_consumed_by_player, email):
    update_queries.update('users', f"co2_consumed={co2_consumed_by_player}", f"email='{email}'")


# Display unvisited destinations function
def display_destinations(unvisited_destinations):
    print("Available Destinations:")
    for destination in unvisited_destinations:
        print(destination)


def set_game_win_threshold(game_win_threshold, email):
    update_queries.update_game_win_threshold(game_win_threshold, email)


def set_difficulty(difficulty_level, email):
    update_queries.update_difficulty(difficulty_level, email)


# Register player info

def register_player(email, name):
    existing_player = get_existing_player_info(email)

    if existing_player is None:
        default_location = select_queries.select('location', 'airports', f"serial_num='{17}'")[0][0]
        insert_queries.insert_new_player(email, name, default_location)

    return email

# set Game condition

def set_game_win_conditions(player_email, input_difficulty_level):
    difficulty_easy = 10000
    difficulty_medium = 12000
    difficulty_hard = 16000
    game_win_easy = 6
    game_win_medium = 9
    game_win_hard = 13
    game_win_threshold = 0
    difficulty = 0

    if input_difficulty_level == "easy":
        difficulty = difficulty_easy
        set_difficulty(difficulty, player_email)
        game_win_threshold = game_win_easy
        set_game_win_threshold(game_win_threshold, player_email)
    elif input_difficulty_level == "medium":
        difficulty = difficulty_medium
        set_difficulty(difficulty, player_email)
        game_win_threshold = game_win_medium
        set_game_win_threshold(game_win_threshold, player_email)
    elif input_difficulty_level == "hard":
        difficulty = difficulty_hard
        set_difficulty(difficulty, player_email)
        game_win_threshold = game_win_hard
        set_game_win_threshold(game_win_threshold, player_email)

    return game_win_threshold, difficulty
# Play game function

def play_game(player_email, difficulty, game_win_threshold):
    num_visited_destinations = 0

    co2_emission_factor = 0.35
    current_player_coordinates = select_queries.select('latitude_deg, longitude_deg', 'airports', f"serial_num='{17}'")[
        0]
    default_location_serial_num = 17
    destinations_list = []
    unvisited_destinations_list = []
    select_all_destinations = get_serial_numbers_list(default_location_serial_num)
    destinations_list.extend(select_all_destinations)

    while player_email is not None:
        unvisited_destinations = list(set(destinations_list) - set(unvisited_destinations_list))
        print(unvisited_destinations)
        display_destinations(unvisited_destinations)
        co2_consumed = select_queries.select('co2_consumed', 'users', f"email='{player_email}'")[0][0]
        selected_destination = int(input('Please, choose a number from the available destinations: '))
        unvisited_destinations_list.append(selected_destination)
        get_destination_name = get_location_name(selected_destination)

        selected_location_coordinates = get_location_coordinates(selected_destination)
        update_new_destination(get_destination_name, player_email)

        num_visited_destinations += 1

        distance_in_kilometer = calculate_distance(current_player_coordinates, selected_location_coordinates)
        co2_calculated = int(distance_in_kilometer * co2_emission_factor)

        total_co2_spent = co2_calculated + co2_consumed
        update_co2_consumed(total_co2_spent, player_email)
        co2_available = difficulty - total_co2_spent
        update_queries.update('users', f"co2_available={co2_available}", f"email='{player_email}'")

        print(f"Current Destination Name: {get_destination_name}")
        print(f"Number of visited Destinations: {num_visited_destinations}")
        print(f"Co2 spent on this trip: {co2_calculated}")
        print(f"Total co2 spent: {total_co2_spent}")

        print(f"Total CO2 Spent: {total_co2_spent}, Difficulty: {difficulty}")
        if total_co2_spent > difficulty:
            print("You lost the game the game!")
            exit()

        if num_visited_destinations >= game_win_threshold:
            print("You have won the game")
            exit()


########## Main Program ###########
agree_play_game = input('Do you want to play? Type "y" for yes and "n" for no: ')

if agree_play_game == 'y':
    player_exists = get_existing_player_info(player_email)  # returns player at index 1
    player_exists = get_existing_player_info(player_email)
    player_email = input("Enter your email? ")
    player_name = input("Enter your name? ")
    input_difficulty_level = input("Enter your difficulty: ")

    register_player(player_email, player_name)
    set_game_win_conditions(player_email, input_difficulty_level)
    game_win_threshold, difficulty = set_game_win_conditions(player_email, input_difficulty_level)

    play_game(player_email, difficulty, game_win_threshold)

    # print
    print(f"player_email: {player_email}")
    print(f"player_name: {player_name}")
    print(f"Selected difficulty: {input_difficulty_level}")
    print(f"game_difficulty: {difficulty}")
    print(f"Game winning threshold: {game_win_threshold}")
    print(f"Game difficulty: {difficulty}")
    # returns player at index 1



# display_destinations(unvisited_destinations_list)


"""

################## working difficulty and while loop ###########


if agree_play_game == 'y':
    player_exists = get_existing_player_info(player_email)  # returns player at index 1

    if player_exists is None:
        player_name = input("Enter your name? ")
        insert_queries.insert_new_player(player_email, player_name, current_location)  # insert new player in database
        player_exists = get_existing_player_info(player_email)
        player_email = player_exists
        # print(f"not existing player: {player_email}")
    else:
        player_email = player_exists
        # print(f"existing player: {player_email}")
        # Move the call here

    input_difficulty_level = input("Difficulty level: Select easy, medium, or hard: ")
    
    if input_difficulty_level == "easy":
        difficulty = difficulty_easy
        set_game_win_threshold(difficulty, player_email)
        game_win_threshold = game_win_easy
        set_game_win_threshold(game_win_threshold, player_email)
    elif input_difficulty_level == "medium":
        difficulty = difficulty_medium
        set_game_win_threshold(difficulty, player_email)
        game_win_threshold = game_win_medium
        set_game_win_threshold(game_win_threshold, player_email)
    elif input_difficulty_level == "hard":
        difficulty = difficulty_hard
        set_game_win_threshold(difficulty, player_email)
        game_win_threshold = game_win_hard
        set_game_win_threshold(game_win_threshold, player_email)

        display_destinations(unvisited_destinations_list)

    while player_email is not None:
        unvisited_destinations = set(destinations_list) - set(unvisited_destinations_list)
        display_destinations(unvisited_destinations)
        co2_consumed = select_queries.select('co2_consumed', 'users', f"email='{player_email}'")[0][0]
        selected_destination = int(input('Please, choose a number from the available destinations: '))
        unvisited_destinations_list.append(selected_destination)
        get_destination_name = get_location_name(selected_destination)

        selected_location_coordinates = get_location_coordinates(selected_destination)
        update_new_destination(get_destination_name, player_email)

        num_visited_destinations += 1

        distance_in_kilometer = calculate_distance(current_player_coordinates, selected_location_coordinates)
        co2_calculated = int(distance_in_kilometer * 0.35)

        total_co2_spent = co2_calculated + co2_consumed
        update_co2_consumed(total_co2_spent, player_email)
        co2_available = difficulty - total_co2_spent
        update_queries.update('users', f"co2_available={co2_available}", f"email='{player_email}'")

        print(f"Current Destination Name: {get_destination_name}")
        print(f"Number of visited Destinations: {num_visited_destinations}")
        print(f"Co2 spent on this trip: {co2_calculated}")
        print(f"Total co2 spent: {total_co2_spent}")

        print(f"Total CO2 Spent: {total_co2_spent}, Difficulty: {difficulty}")
        if total_co2_spent > difficulty:
            print("You lost the game the game!")
            exit()

        if num_visited_destinations >= game_win_threshold:
            print("You have won the game")
            exit()

else:
    print('Goodbye!')


#################################

def register_player(email, name):
    
    location = select_queries.select('location', 'airports', f"serial_num='{17}'")[0][
        0]  # select Helsinki as default location at 17
    insert_queries.insert_new_player(email, name, location)
    email = select_queries.select('email AS last_item', 'users', 'id = (SELECT MAX(id) FROM users)')[0][0]
    name = select_queries.select('name AS last_item', 'users', 'id = (SELECT MAX(id) FROM users)')[0][0]

    return email, name, location

chosen_location = get_location_coordinates(input_destination)
print(f"Your current location is: {all_destinations.get(input_destination)}")

distance_in_kilometer = calculate_distance(current_player_coordinates, chosen_location)
co2_consumed_by_player = int(distance_in_kilometer * 0.2) + int(player_email['co2_consumed'])
update_co2_consumed(co2_consumed_by_player, player_email)

num_visited_destinations += 1
print(f"Number of visited Destinations: {num_visited_destinations}")
print(f"Distance traveled: {distance_in_kilometer} km")
print(f"CO2 consumed: {co2_consumed_by_player} units")

if num_visited_destinations >= game_win_threshold:
    print("Congratulations! You've visited enough destinations to win the game!")
    exit()
if co2_consumed_by_player > difficulty:
    print("Game Over. You've consumed too much CO2!")
    exit()

"""

"""
class players:
    def __init__(self, player_name, player_email):
        self.player_name = player_name
        self.player_email = player_email


def choose_difficulty(input_difficulty_level, game_win_easy, game_win_medium, game_win_hard, set_difficulty_method,
                      player_email, game_win_threshold):

    else:
        # Handle invalid input or provide a default value
        print("Invalid difficulty level. Using default values.")
        difficulty = 0
        game_win_threshold = 0

    return game_win_threshold
    
    
def to_visit_destinations(locations, chosen_destination):
    visited_destinations = []

    for num, destination in locations.items():
        if num != chosen_destination:
            visited_destinations.append(num)
            print(f"{num}: {destination}", end=" ")

    return visited_destinations


destinations_dictionary = to_visit_destinations(destinations, input_destination)
"""
