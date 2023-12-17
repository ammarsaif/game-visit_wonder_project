import queries_connector
import geopy.distance

# connect to the database queries classes
wonder_database = queries_connector.connect_database()
select_queries = queries_connector.SelectQueries(wonder_database)
insert_queries = queries_connector.InsertQueries(wonder_database)
update_queries = queries_connector.UpdateQueries(wonder_database)

def get_destinations_names_list(condition):
    destinations_query_result = select_queries.select('serial_num, location', 'airports', condition)
    destinations_list = [{'serial_num': num[0], 'name': num[1]} for num in destinations_query_result]
    return destinations_list

destinations_names_list = []
select_all_destinations = get_destinations_names_list('serial_num < 17')
destinations_names_list.extend(select_all_destinations)
print(destinations_names_list)

"""

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
"""
