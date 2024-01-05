from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import queries_connector
import geopy.distance
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

wonder_database = queries_connector.connect_database()
select_queries = queries_connector.SelectQueries(wonder_database)
insert_queries = queries_connector.InsertQueries(wonder_database)
update_queries = queries_connector.UpdateQueries(wonder_database)


def get_serial_numbers_list(condition):
    serial_numbers_query_result = select_queries.select('serial_num', 'airports',
                                                        condition)  # select_queries.select returns a list of tuples
    num_destination_list = [num[0] for num in
                            serial_numbers_query_result]  # selects the element at index [0] from each tuple
    # and creating a list

    return num_destination_list


def get_destinations_num_names_list(condition):
    destinations_query_result = select_queries.select('serial_num, location', 'airports', condition)
    destinations_list_dictionary = [{num[0]: num[1]} for num in destinations_query_result]
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
    print(f"Selected Destination in function: {location_num}")
    result = select_queries.select('location', 'airports', f"serial_num='{location_num}'")
    print(f"SQL Result: {result[0][0]}")

    if result:
        return result[0][0]
    else:
        raise ValueError(f"No location found for serial_num {location_num}")


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


def set_game_win_conditions(player_email, input_difficulty_level):
    difficulty_easy = 10000
    difficulty_medium = 12000
    difficulty_hard = 16000
    game_win_easy = 6
    game_win_medium = 9
    game_win_hard = 13
    difficulty = 0
    game_win_threshold = 0

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


@app.route('/')
def index():
    # Redirect to player_info route
    return render_template('index.html')


@app.route('/player_info', methods=['GET', 'POST'])
def player_info():
    if request.method == 'POST':
        player_email = request.form['email']
        player_name = request.form['name']
        input_difficulty_level = request.form['difficulty']

        existing_player = get_existing_player_info(player_email)

        if existing_player is None:
            default_location = select_queries.select('location', 'airports', f"serial_num='{17}'")[0][0]
            insert_queries.insert_new_player(player_email, player_name, default_location)

        game_win_threshold, difficulty = set_game_win_conditions(player_email, input_difficulty_level)

        session['player_email'] = player_email
        session['difficulty'] = difficulty
        session['game_win_threshold'] = game_win_threshold

        return redirect(url_for('play_game'))

    return render_template('player_info.html', )


@app.route('/play_game', methods=['GET', 'POST'])
def play_game():
    co2_available = 0
    total_co2_spent = None  # Initialize total_co2_spent to None
    distance_in_kilometer = 0

    if 'player_email' not in session:
        return redirect(url_for('index'))

    if 'num_visited_destinations' not in session:
        session['num_visited_destinations'] = 0

    player_email = session['player_email']
    difficulty = session['difficulty']
    game_win_threshold = session['game_win_threshold']
    num_visited_destinations = session['num_visited_destinations']

    # Retrieve co2 budget
    co2_budget = select_queries.select('co2_budget', 'users', f"email='{player_email}'")[0][0]
    player_name = select_queries.select('name', 'users', f"email='{player_email}'")[0][0]

    co2_emission_factor = 0.35
    default_location_num = 17
    current_location_name = select_queries.select('location', 'airports', f"serial_num='{default_location_num}'")[0][0]
    current_player_coordinates = select_queries.select('latitude_deg, longitude_deg', 'airports', f"serial_num='{default_location_num}'")[
        0]
    destinations_list = []
    unvisited_destinations_list = []
    condition = "serial_num < 17"
    select_all_destinations = get_destinations_num_names_list(condition)
    destinations_list.extend(select_all_destinations)
    unvisited_destinations = [item for item in destinations_list if item not in unvisited_destinations_list]
    print(f"unvisited_destinations: {unvisited_destinations}")
    if request.method == 'POST':
        selected_destination = request.json.get('data-destination')
        if selected_destination is not None:
            get_destination_name = get_location_name(selected_destination)
            print(get_destination_name)
        else:
            print("Selected destination is None. Check frontend code or server request.")
        print(f"Selected Destination in play_game: {selected_destination}")
        unvisited_destinations_list.append(selected_destination)
        get_destination_name = get_location_name(selected_destination)
        current_location_name = get_destination_name
        selected_location_coordinates = get_location_coordinates(selected_destination)
        update_new_destination(get_destination_name, player_email)

        num_visited_destinations += 1
        session['num_visited_destinations'] = num_visited_destinations
        print(f"num visited destinations: {num_visited_destinations}")

        distance_in_kilometer = round(calculate_distance(current_player_coordinates, selected_location_coordinates), 2)
        co2_calculated = int(distance_in_kilometer * co2_emission_factor)

        # Retrieve the current total_co2_spent from the database
        current_total_co2_spent = select_queries.select('co2_consumed', 'users', f"email='{player_email}'")[0][0]

        # Update the total_co2_spent with the new value
        total_co2_spent = current_total_co2_spent + co2_calculated
        update_co2_consumed(total_co2_spent, player_email)

        co2_available = difficulty - total_co2_spent
        update_queries.update('users', f"co2_available={co2_available}", f"email='{player_email}'")

        if total_co2_spent > difficulty:
            return jsonify({'status': 'lost', 'co2_budget': co2_budget,
            'co2_available': co2_available,
            'total_co2_spent': total_co2_spent,
            'num_visited_destinations': num_visited_destinations,
            'current_location_name': current_location_name,
            'game_win_threshold': game_win_threshold,
            'distance_in_kilometer': distance_in_kilometer,
            'player_name': player_name})


        if num_visited_destinations >= game_win_threshold:
            return jsonify({'status': 'won', 'co2_budget': co2_budget,
            'co2_available': co2_available,
            'total_co2_spent': total_co2_spent,
            'num_visited_destinations': num_visited_destinations,
            'current_location_name': current_location_name,
            'game_win_threshold': game_win_threshold,
            'distance_in_kilometer': distance_in_kilometer,
            'player_name': player_name})

        return jsonify({
            'co2_budget': co2_budget,
            'co2_available': co2_available,
            'total_co2_spent': total_co2_spent,
            'num_visited_destinations': num_visited_destinations,
            'current_location_name': current_location_name,
            'game_win_threshold': game_win_threshold,
            'distance_in_kilometer': distance_in_kilometer,
            'player_name': player_name})

    return render_template('play_game.html', co2_budget=co2_budget, co2_available=co2_available,
                           total_co2_spent=total_co2_spent, num_visited_destinations=num_visited_destinations,
                           difficulty=difficulty, distance_in_kilometer=distance_in_kilometer,
                           current_location_name=current_location_name, game_win_threshold=game_win_threshold,
                           unvisited_destinations=unvisited_destinations, player_name=player_name)

@app.route('/clear_session', methods=['POST'])
def clear_session():
    try:
        session.pop('player_email', None)
        session.pop('difficulty', None)
        session.pop('game_win_threshold', None)
        session.pop('num_visited_destinations', None)
        session.pop('co2_budget', None)
        session.pop('c02_available', None)
        session.pop('total_co2_spent', None)
        session.pop('current_location_name', None)
        session.pop('player_name', None)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.secret_key = secrets.token_hex(16)
    app.run(debug=True)
