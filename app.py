from flask import Flask, render_template, request, redirect, url_for
import queries_connector
import geopy.distance

app = Flask(__name__, template_folder='templates', static_folder='static')

# connect to the database queries classes
wonder_database = queries_connector.connect_database()
select_queries = queries_connector.SelectQueries(wonder_database)
insert_queries = queries_connector.InsertQueries(wonder_database)
update_queries = queries_connector.UpdateQueries(wonder_database)


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


def get_destinations_names_list(condition):
    destinations_query_result = select_queries.select('serial_num, location', 'airports', condition)
    destinations_list = [{'serial_num': num[0], 'name': num[1]} for num in destinations_query_result]
    return destinations_list


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

    #destinations_names_list = []
    #select_all_destinations = get_destinations_names_list('serial_num < 17')
    #destinations_names_list.extend(select_all_destinations)

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
            game_win_threshold = game_win_easy
        elif input_difficulty_level == "medium":
            difficulty = difficulty_medium
            update_queries.update_difficulty(difficulty, player_email)
            game_win_threshold = game_win_medium
        elif input_difficulty_level == "hard":
            difficulty = difficulty_hard
            update_queries.update_difficulty(difficulty, player_email)
            game_win_threshold = game_win_hard

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
