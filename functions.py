import queries_connector
import geopy.distance

# connect to the database queries classes
wonder_database = queries_connector.connect_database()
select_queries = queries_connector.SelectQueries(wonder_database)
insert_queries = queries_connector.InsertQueries(wonder_database)
update_queries = queries_connector.UpdateQueries(wonder_database)

def get_destinations_num_names_list(condition):
    destinations_query_result = select_queries.select('serial_num, location', 'airports', condition)
    destinations_list_dictionary = [{num[0]: num[1]} for num in destinations_query_result]
    return destinations_list_dictionary


destinations_list = []
unvisited_destinations_list = []
default_location_serial_num = "serial_num < 17"
select_all_destinations = get_destinations_num_names_list(default_location_serial_num)
destinations_list.extend(select_all_destinations)
unvisited_destinations = [item for item in destinations_list if item not in unvisited_destinations_list]

for destination in destinations_list:
    print(f"destination: {destination}")
    for key, value in destination.items():
        print(key)
print(f"destinations List: {destinations_list}")
print(f"unvisited destinations List: {unvisited_destinations_list}")
print(f"unvisited destinations: {unvisited_destinations}")


def get_location_name(location_num):
    print(f"Selected Destination: {location_num}")
    result = select_queries.select('location', 'airports', f"serial_num='{location_num}'")
    print(f"SQL Result: {result}")

    if result:
        return result[0]
    else:
        raise ValueError(f"No location found for serial_num {location_num}")
location = 12

print(f"location: {get_location_name(location)}")

"""

def get_serial_numbers_list(condition):
    serial_numbers_query_result = select_queries.select('serial_num', 'airports',
                                                        condition)  # select_queries.select returns a list of tuples
    num_destination_list = [num[0] for num in
                            serial_numbers_query_result]  # Extracting the first element from each tuple and creating a list

    return num_destination_list


def get_destinations_num_names_list(condition):
    destinations_query_result = select_queries.select('serial_num, location', 'airports', condition)
    destinations_list_dictionary = [{num[0]: num[1]} for num in destinations_query_result]
    return destinations_list_dictionary


destinations_list = []
unvisited_destinations_list = []
default_location_serial_num = "serial_num < 17"
select_all_destinations = get_destinations_num_names_list(default_location_serial_num)
destinations_list.extend(select_all_destinations)
unvisited_destinations = [item for item in destinations_list if item not in unvisited_destinations_list]

for destination in destinations_list:
    for key, value in destination.items():
        print(key, value)
print(f"destinations List: {destinations_list}")
print(f"unvisited destinations List: {unvisited_destinations_list}")
print(f"unvisited destinations: {unvisited_destinations}")

########################################################

def register_player(email, name, location):
    location = select_queries.select('location', 'airports', f"serial_num='{17}'")[0][0]
    insert_queries.insert_new_player(email, name, location)
    email = select_queries.select('email AS last_item', 'users', 'id = (SELECT MAX(id) FROM users)')[0][0]
    name = select_queries.select('name AS last_item', 'users', 'id = (SELECT MAX(id) FROM users)')[0][0]

    return email, name, location


#############################


def set_game_win_threshold(game_win_threshold, email):
    update_queries.update_game_win_threshold(game_win_threshold, email)

def set_difficulty(difficulty_level, email):
    update_queries.update_difficulty(difficulty_level, email)
def set_game_win_conditions(player_email, input_difficulty_level):
    difficulty_easy = 10000
    difficulty_medium = 12000
    difficulty_hard = 16000
    game_win_easy = 6
    game_win_medium = 9
    game_win_hard = 13

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
    return game_win_threshold, difficulty, player_email

player_email = "rrr"
input_difficulty_level = "hard"

game_difficulty = set_game_win_conditions(player_email, input_difficulty_level)
print(game_difficulty[2])

################################

current_location = select_queries.select('location', 'airports', f"serial_num='{17}'")[0][0]
print(current_location)

player_email = "ammar"

co2_consumed = select_queries.select('co2_available', 'users', f"email='{player_email}'")[0][0]
print(f"co2 consumed = {co2_consumed}")


def get_location_coordinates(destination_num):
    result = select_queries.select('latitude_deg, longitude_deg', 'airports',
                                   f"serial_num='{destination_num}'")[0]
    return result

current_player_coordinates = select_queries.select('latitude_deg, longitude_deg', 'airports', f"serial_num='{17}'")[0]
num = 2
location_coordinated = get_location_coordinates(num)
print(f"first location: {location_coordinated}")
print(current_player_coordinates)

location_num = 3
player_email = 'ammar'
def get_location_name(location_num):
    result = select_queries.select('location', 'airports', f"serial_num='{location_num}'")
    return ', '.join(map(str, result[0]))

location = get_location_name(location_num)
print(location)
email = 'vvv'
def get_co2_consumed_by_player(email):
    result = select_queries.select('co2_consumed', 'users', f"email='{email}'")
    return result[0][0]
carbon_result = get_co2_consumed_by_player(email)
print(f"carbon spent: {carbon_result}")

#################

input_player_email = "ammar"
player_exists = select_queries.check_player_exists(input_player_email)

print(player_exists)


def get_existing_player_info(player_email):
    existing_player = select_queries.select('email', 'users', f"email='{player_email}'")

    if existing_player:
        return existing_player  # Returning the player information
    else:
        return None  # Player not found

player_email = 'ammar'
existing_player = get_existing_player_info(player_email)
print(existing_player)


#### get location and insert into database

location_num = 3
player_email = 'ammar'
def get_location_name(location_num):
    result = select_queries.select('location', 'airports', f"serial_num='{location_num}'")
    return ', '.join(map(str, result[0]))

location_name = get_location_name()
def update_new_destination(location, player_email):
    #update_queries.update_location('users', 'current_location = %s', 'email = %s', (chosen_num_by_player, player_email))
    update_queries.update_location(location, player_email)

update_new_destination(location_name, player_email)
print(get_location_name)


##### update location in data base ####

def update_new_destination(location, player_email):
    #update_queries.update_location('users', 'current_location = %s', 'email = %s', (chosen_num_by_player, player_email))
    update_queries.update_location(location, player_email)



### update co2 consumption is working

def update_co2_consumed(co2_consumed_by_player, player_email):
    update_queries.update('users', f"co2_consumed={co2_consumed_by_player}", f"email='{player_email}'")

### Location function is working

location_1 = select_queries.select('latitude_deg, longitude_deg', 'airports', f"serial_num='{1}'")
location_2 = select_queries.select('latitude_deg, longitude_deg', 'airports', f"serial_num='{3}'")

#location_1 = (location_1[0], location_1[1])
#location_2 = (location_2[0], location_2[1])

print("Location 1:", location_1)
print("Location 2:", location_2)

def calculate_distance(location_1, location_2):
    return geopy.distance.distance(location_1, location_2).km

distance = calculate_distance(location_1, location_2)
print("Distance:", distance, "km")

get_location_coordinates = select_queries.select('latitude_deg, longitude_deg', 'airports', f"serial_num='{1}'")


##################

# all destinations function is working
 
 def get_serial_numbers_list(condition):
    # Assuming select_queries.select returns a list of tuples
    serial_numbers_query_result = select_queries.select('serial_num', 'airports', condition)

    # Extracting the first element from each tuple and creating a list
    num_destination_list = [num[0] for num in serial_numbers_query_result]

    return num_destination_list


# Example usage
condition = 'serial_num < 17'
result_list = get_serial_numbers_list(condition)
print(result_list)
 
 
 ##### old code ####
def update_new_destination(chosen_num_by_player, player_email):
    new_location = destinations.get(chosen_num_by_player)
    connect_database.update('user', 'location = %s', 'email = %s', (new_location, player_email))
    return new_location

# list of numbers old function

serial_numbers_query_result = select_queries.select('serial_num', 'airports', 'serial_num < 17')
num_destination_list = []
for num in serial_numbers_query_result:
    num_destination_list.append(num[0])
print(num_destination_list)







# Global Variables


# list of destinations
def get_serial_numbers_list(condition):
    serial_numbers_query_result = select_queries.select('serial_num', 'airports',
                                                        condition)
    num_destination_list = [num[0] for num in
                            serial_numbers_query_result]
    return num_destination_list


# Display unvisited lists
def get_destinations_names_list(condition):
    destinations_query_result = select_queries.select('serial_num, location', 'airports', condition)
    destinations_list_dictionary = [{'serial_num': num[0], 'name': num[1]} for num in destinations_query_result]
    return destinations_list_dictionary


def get_existing_player_info(email):
    existing_player = select_queries.select('email', 'users', f"email='{email}'")
    if existing_player:
        return existing_player[0][0]
    else:
        return None


def calculate_distance(location_1, location_2):
    return geopy.distance.distance(location_1, location_2).km


def get_location_coordinates(destination_num):
    result = select_queries.select('latitude_deg, longitude_deg', 'airports',
                                   f"serial_num='{destination_num}'")[0]
    return result


def get_location_name(location_num):
    result = select_queries.select('location', 'airports', f"serial_num='{location_num}'")
    return result[0][0]


def update_new_destination(location, email):
    update_queries.update_location(location, email)


def get_co2_consumed_by_player(email):
    result = select_queries.select('co2_consumed', 'users', f"email='{email}'")
    return result[0][0]


def update_co2_consumed(co2_consumed_by_player, player_email):
    update_queries.update('users', f"co2_consumed={co2_consumed_by_player}", f"email='{player_email}'")


def display_destinations(unvisited_destinations):
    print("Available Destinations:")
    for destination in unvisited_destinations:
        print(destination)

def set_game_win_threshold(game_win_threshold, email):
    update_queries.update_difficulty(game_win_threshold, email)

def set_difficulty(difficulty, email):
    update_queries.update_difficulty(difficulty, email)


def get_destinations_names_list(condition):
    destinations_query_result = select_queries.select('serial_num, location', 'airports', condition)
    destinations_list = [{'serial_num': num[0], 'name': num[1]} for num in destinations_query_result]
    return destinations_list

#######################################################################
@app.route('/')
def home():
    return render_template('index.html', unvisited_destinations=[])


@app.route('/play_game', methods=['POST'])
def play_game():
    difficulty = 0
    difficulty_easy = 10000
    difficulty_medium = 12000
    difficulty_hard = 16000
    game_win_easy = 7
    game_win_medium = 10
    game_win_hard = 14
    current_location = 'Helsinki'
    current_player_coordinates = select_queries.select('latitude_deg, longitude_deg', 'airports', f"serial_num='{17}'")[
        0]

    # List of numbers
    destinations_list = []
    unvisited_destinations_list = []
    select_all_destinations = get_serial_numbers_list('serial_num < 17')
    destinations_list.extend(select_all_destinations)
    print(destinations_list)

    # List of locations with num and name

    # destinations_names_list = []
    # select_all_destinations = get_destinations_names_list('serial_num < 17')
    # destinations_names_list.extend(select_all_destinations)

    num_visited_destinations = 0

    if request.method == 'POST':
        player_email = request.form['player_email']
        player_name = request.form['player_name']
        input_difficulty_level = request.form['difficulty_level']
        game_win_threshold = request.form['game_win_threshold']
        player_exists = get_existing_player_info(player_email)

        #unvisited_destinations = get_unvisited_destinations(player_email)

        if player_exists is None:
            insert_queries.insert_new_player(player_email, player_name, current_location)
            player_exists = get_existing_player_info(player_email)
            player_email = player_exists
        else:
            player_email = player_exists

        if input_difficulty_level == "easy":
            difficulty = difficulty_easy
            update_queries.update_difficulty(difficulty, player_email)
            game_win = game_win_easy
            update_queries.update_difficulty(game_win, player_email)
        elif input_difficulty_level == "medium":
            difficulty = difficulty_medium
            update_queries.update_difficulty(difficulty, player_email)
            game_win = game_win_medium
            update_queries.update_difficulty(game_win, player_email)
        elif input_difficulty_level == "hard":
            difficulty = difficulty_hard
            update_queries.update_difficulty(difficulty, player_email)
            game_win = game_win_hard
            update_queries.update_difficulty(game_win, player_email)

        game_win_threshold = game_win_threshold

        while player_email is not None:
            unvisited_destinations = set(destinations_list) - set(unvisited_destinations_list)
            display_destinations(unvisited_destinations)
            co2_consumed = select_queries.select('co2_consumed', 'users', f"email='{player_email}'")[0][0]
            selected_destination = request.form.get('selected_destination')
            unvisited_destinations_list.append(selected_destination)
            get_destination_name = get_location_name(selected_destination)

            selected_location_coordinates = get_location_coordinates(selected_destination)
            update_new_destination(get_destination_name, player_email)

            num_visited_destinations += 1

            distance_in_kilometer = calculate_distance(current_player_coordinates, selected_location_coordinates)
            co2_calculated = int(distance_in_kilometer * 0.25)

            total_co2_spent = co2_calculated + co2_consumed
            update_co2_consumed(total_co2_spent, player_email)
            co2_available = difficulty - total_co2_spent
            update_queries.update('users', f"co2_available={co2_available}", f"email='{player_email}'")

            game_data = {
                'difficulty': difficulty,
                'current_destination_name': get_destination_name,
                'num_visited_destinations': num_visited_destinations,
                'co2_calculated': co2_calculated,
                'co2_available': co2_available,
                'total_co2_spent': total_co2_spent
            }

            if total_co2_spent > difficulty:
                print("You lost the game!")
                exit()

            if num_visited_destinations >= game_win_threshold:
                print("You have won the game")
                exit()
            return render_template('index.html', unvisited_destinations=unvisited_destinations)

    else:
        print('Goodbye!')

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

"""
