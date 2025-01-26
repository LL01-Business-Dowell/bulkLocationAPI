import json
import requests
import os
import pandas as pd
from django.conf import settings
import haversine as hs
import googlemaps
from decouple import config
import json
BASE_DIR = settings.BASE_DIR
static_path = os.path.join(BASE_DIR, 'static')
directory = os.path.join(BASE_DIR, 'json_data')
id_directory = os.path.join(BASE_DIR, 'json__id_data')
plc_id_file_name = os.path.join(id_directory, "id_json_data.json")
api_key = config("API_KEY")
print('api_key ')
try:
    client = googlemaps.Client(key=api_key)

except:
    print('Error occured ', api_key)


class CustomError(Exception):
    pass


def processApikey(api_key):
    url = f'https://100105.pythonanywhere.com/api/v3/process-services/?type=api_service&api_key={api_key}'
    print(api_key)
    print(url)
    payload = {
        "service_id": "DOWELL10009"
    }

    response = requests.post(url, json=payload)
    print("response.status === ", response.status_code)
    print("response === ", response.text)
    # if response.status_code == 400 or response.status_code == "400":
    # raise CustomError
    # else:

    # response.status_code
    res = json.loads(response.text)
    print("res.success", res["success"])
    print("res.success type", type(res["success"]))
    return response


# Insertion of data
def insert_data(data):
    # dowellconnectionfunction

    url = "http://100002.pythonanywhere.com/"
# searchstring="ObjectId"+"("+"'"+"6139bd4969b0c91866e40551"+"'"+")"
    payload = json.dumps({
        "cluster": "dowellmap",
        "database": "dowellmap",
        "collection": "my_map",
        "document": "my_map",
        "team_member_ID": "1164",
        "function_ID": "ABCDE",
        "command": "insert",
        "field": data,
        # "test_data" : "test_data",
        "update_field": {
            "order_nos": 21
        },
        "platform": "bangalore"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    response_dict = json.loads(response.text)
    print(response.text)
    return response_dict
# 3
######

# Fetch Data From Mongo


def fetch_from_mongo(field={}):
    url = "http://uxlivinglab.pythonanywhere.com/"
    headers = {'content-type': 'application/json'}

    payload = {
        "cluster": "dowellmap",
        "database": "dowellmap",
        "collection": "my_map",
        "document": "my_map",
        "team_member_ID": "1164",
        "function_ID": "ABCDE",
        "command": "fetch",
        "field": field,
        "update_field": {
            "order_nos": 21
        },
        "platform": "bangalore"
    }
    data = json.dumps(payload)
    response = requests.request("POST", url, headers=headers, data=data)
    # print(response.text)
    result = json.loads(response.text)
    result = json.loads(result)
    # print(result['isSuccess'])
    # print(type(result['data']))
    print("===========================")
    # print(response.text)
    return result['data']
# Fetch Data from Json


def fetch_from_json():

    # file_path = 'json_data\sample.json'
    n = len(os.listdir(directory))
    # isExist = os.path.exists(file_path)
    # print(isExist)
    # print(n)
    json_data_lists = list()
    for i in range(1, n+1):
        temp_file_name = os.path.join(directory, "rec"+str(i)+".json")
        isTempExist = os.path.exists(temp_file_name)
        sizee = os.path.getsize(temp_file_name)
        file_stats = os.stat(temp_file_name)
        print("i ", i)
        # print("sizee",sizee)
        # print(f"file_stats in bytes is {file_stats.st_size}")
        # print(f"file_stats in megabytes is {file_stats.st_size / (1024 * 1024)}")
        if isTempExist:
            with open(temp_file_name, 'r') as openfile:
                # Reading from json file
                json_object = json.load(openfile)
                print("Round ==========start=========")
                df = pd.DataFrame(json_object[:10])
                print(df.head(5))
                print("Round =========end==========")

            json_data_lists.append(json_object)
    # print(json_data_lists)
    return json_data_lists


def fetch_from_registered_json():

    # file_path = 'json_data\sample.json'
    # n= len(os.listdir(directory))
    # isExist = os.path.exists(file_path)
    # print(isExist)
    # print(n)
    json_data_lists = list()
    my_reg_list = []
#     for i in range(1,n+1):
#         temp_file_name =  os.path.join(directory, "rec"+str(i)+".json")
#         isTempExist = os.path.exists(temp_file_name)
#         sizee = os.path.getsize(temp_file_name)
#         file_stats = os.stat(temp_file_name)
#         print("i ", i)
#         # print("sizee",sizee)
#         # print(f"file_stats in bytes is {file_stats.st_size}")
#         # print(f"file_stats in megabytes is {file_stats.st_size / (1024 * 1024)}")
#         if isTempExist:
#             with open(temp_file_name, 'r') as openfile:
#             # Reading from json file
#                 json_object = json.load(openfile)
#                 print("Round ==========start=========")
#                 print("type of json_object[0] == ", type(json_object[0]))
#                 my_reg_list += [
#     my_dict for my_dict in json_object if"type_of_data" in my_dict and my_dict['type_of_data'] == 'scraped'
# ]
#                 print("length of my_reg_list == ", len(my_reg_list))
#                 print("type of my_reg_list[-1] == ", type(my_reg_list[-1]))
#                 print("my_reg_list[0] == ", my_reg_list[0])
#                 print("Round =========end==========")

    # json_data_lists.append(json_object)
    # print(json_data_lists)
    url = "http://100002.pythonanywhere.com/"
    headers = {'content-type': 'application/json'}

    payload = {
        "cluster": "dowellmap",
        "database": "dowellmap",
        "collection": "my_map",
        "document": "my_map",
        "team_member_ID": "1164",
        "function_ID": "ABCDE",
        "command": "fetch",
        "field": {

        },
        "update_field": {
            "order_nos": 21
        },
        "platform": "bangalore"
    }
    data = json.dumps(payload)
    response = requests.request("POST", url, headers=headers, data=data)
    # print(response.text)
    result = json.loads(response.text)
    print("Round ==========start=========")
    print("type of result['data']] == ", type(result['data'][0]))
    my_reg_list += [
        my_dict for my_dict in result['data'] if "type_of_data" in my_dict and my_dict['type_of_data'] == 'registered'
    ]
    print("length of my_reg_list == ", len(my_reg_list))
    print("type of my_reg_list[-1] == ", type(my_reg_list[-1]))
    print("my_reg_list[0] == ", my_reg_list[0])
    print("Round =========end==========")

    # print(result['isSuccess'])
    # print(type(result['data']))
    # print(result['data'])
    return my_reg_list
# Wtiter to json


def write_json_data(file_name, new_data):
    try:
        isExist = os.path.exists(file_name)
        data = list()
        data_ids = list()
        if isExist:
            # get old data and combine
            with open(file_name, 'r') as openfile:

                #     # Reading from json file
                old_data = json.load(openfile)
            old_data_list = old_data
            data = old_data_list + new_data

        else:
            data = new_data
        for i in data:
            if 'placeId' in i:
                if i['placeId'] not in data_ids:
                    data_ids.append(i['placeId'])
            if 'place_id' in i:
                if i['place_id'] not in data_ids:
                    data_ids.append(i['place_id'])
            # insert in new file
        json_object = json.dumps(data, indent=4)
        with open(file_name, "w") as outfile:
            outfile.write(json_object)
        if len(data_ids):
            id_data = {"data": data_ids}
            json_object = json.dumps(id_data, indent=4)
            with open(plc_id_file_name, "w") as outfile:
                outfile.write(json_object)

        return True
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return False


# Create Data to Json
def create_json_data():
    # Check for number of records

    n = len(os.listdir(directory))
    print("n==", n)

    # Collect Present ids in Json
    json_data_lists = list()
    json_data_sizes = dict()
    if n:
        for i in range(1, n+1):
            temp_file_name = os.path.join(directory, "rec"+str(i)+".json")
            sizee = os.path.getsize(temp_file_name)
            file_stats = os.stat(temp_file_name)
            print("i ", i)
            print("sizee", sizee)
            print(f"file_stats in bytes is {file_stats.st_size}")
            print(
                f"file_stats in megabytes is {file_stats.st_size / (1024 * 1024)}")
            json_data_sizes[temp_file_name] = file_stats.st_size / \
                (1024 * 1024)

            with open(temp_file_name, 'r') as openfile:
                # Reading from json file
                json_object = json.load(openfile)
                # print("Round ===================")
                # print(json_object)
                # print("Round ===================")

            json_data_lists.append(json_object)
        # print("json data", json_data_lists)
        # print("json data sizess", json_data_sizes)
    json_data_ids = list()
    for i in json_data_lists:
        for t in i:
            json_data_ids.append(t['_id'])
    # print("json ids",json_data_ids)
    # Collect Present ids in Mongo
    mongo_data = fetch_from_mongo()
    mongo_df = pd.DataFrame.from_dict(mongo_data)
    mongo_data_ids = [i['_id'] for i in mongo_data]
    # Get missing numbers
    missing_ids = set(mongo_data_ids).difference(set(json_data_ids))
    print("missing ids", missing_ids)
    # print(mongo_df.head())
    missing_data_df = mongo_df.loc[mongo_df['_id'].isin(mongo_data_ids)]
    missing_data_list = missing_data_df.to_dict('records')
    # print(missing_data_df)
    # print("------------------------------------------------->>>>>>>>>>>>>>>>>>>>>>")
    # print(missing_data_list)
    # Write on last json
    culprit_file_name = os.path.join(directory, "rec"+str(n)+".json")
    new_file_name = ""
    if n == 0 or json_data_sizes[culprit_file_name] >= 100:
        new_file_name = os.path.join(directory, "rec"+str(n+1)+".json")
    else:
        new_file_name = culprit_file_name

    isHandled = write_json_data(new_file_name, missing_data_list)
    print("ishHandled =====> ", isHandled)
    return isHandled


def get_unique(place_id_list):
    # Fetch all place ids
    isExist = os.path.exists(plc_id_file_name)
    if isExist:
        with open(plc_id_file_name, 'r') as openfile:
            # Reading from json file
            json_object_ids = json.load(openfile)
        json_id_list = json_object_ids['data']
        # Do difference in sets
        distinct_list = list(set(place_id_list).difference(set(json_id_list)))
        # return list distince

        return distinct_list
    else:
        return []


def get_unique_from_mongo(place_id_list):
    # Fetch all place ids
    distinct_list = list()
    for i in place_id_list:
        field = {
            'placeId': i,
            # 'place_id': i
        }
        print("field = ", field)
        retrieve_id = fetch_from_mongo(field)
        print("retrieve_id = ", retrieve_id)
        if retrieve_id is None or len(retrieve_id) == 0:
            # if len(retrieve_id) == 0:
            print("retrieve_id = ", retrieve_id)
            distinct_list.append(i)

    return distinct_list

# Get differremce in distances


def get_difference(latt1, lonn1, latt2, lonn2):
    loc1 = (latt1, lonn1)
    loc2 = (latt2, lonn2)
    distance = hs.haversine(loc1, loc2, unit=hs.Unit.METERS)
    return distance


def split_string(loc_str1, loc_str2):
    # print("loc_str 1", loc_str1)
    # print("loc_str 2", loc_str2)

    if loc_str1 == '' or loc_str1 == ' ' or loc_str1 == 'nul':
        loc_str1 = '0 , 0'
    if loc_str2 == '' or loc_str2 == ' ' or loc_str2 == 'nul':
        loc_str2 = '0 , 0'
    offset1 = loc_str1.find(',')
    try:
        latt1 = float(loc_str1[:offset1].strip())
        # lonn1 = float(loc_str1[offset1+1:].strip())
    except ValueError:
        latt1 = 0
    try:
        # latt1 = float(loc_str1[:offset1].strip())
        lonn1 = float(loc_str1[offset1+1:].strip())
    except ValueError:
        lonn1 = 0
    offset2 = loc_str2.find(',')
    try:
        latt2 = float(loc_str2[:offset2].strip())
    except ValueError:
        latt2 = 0
    try:
        lonn2 = float(loc_str2[offset2+1:].strip())
    except ValueError:
        lonn2 = 0

    # print("latt ",latt1)
    # print("lonn ",lonn1)

    # latt2 = float(loc_str2[:offset2].strip())
    # lonn2 = float(loc_str2[offset2+1:].strip())
    # print("latt ",latt2)
    # print("lonn ",lonn2)
    hav_distance = get_difference(latt1, lonn1, latt2, lonn2)
    return hav_distance


def get_distance(loc_str1, loc_str2):
    # print("loc_str 1", loc_str1)
    # print("loc_str 2", loc_str2)

    if loc_str1 == '' or loc_str1 == ' ':
        loc_str1 = '0 , 0'
    if loc_str2 == '' or loc_str2 == ' ':
        loc_str2 = '0 , 0'
    offset1 = loc_str1.find(',')
    latt1 = float(loc_str1[:offset1].strip())
    lonn1 = float(loc_str1[offset1+1:].strip())
    # print("latt ",latt1)
    # print("lonn ",lonn1)
    offset2 = loc_str2.find(',')
    latt2 = float(loc_str2[:offset2].strip())
    lonn2 = float(loc_str2[offset2+1:].strip())
    # print("latt ",latt2)
    # print("lonn ",lonn2)
    origins = [{'lat': latt1, 'lng': lonn1}]  # street, zip code, town
# #     destination = street zip code, town, arrival/departure, time, best guess pessi/optimistic
    destinations = [{'lat': latt2, 'lng': lonn2}]

    matrix = client.distance_matrix(
        origins, destinations,
        mode="driving",
        # mode= "transit",
        # departure_time = datetime.now(),
        # traffic_model = "optimistic",
    )
    # print("matrix", matrix)
    # print("matrix type",type( matrix))
    # print("----------------------------------------------------------")
    # print(matrix['rows'][0]['elements'][0]['distance']['value'])
    # hav_distance = get_difference(latt1,lonn1, latt2,lonn2)
    return matrix['rows'][0]['elements'][0]['distance']['value']


def retrieve_details(results_1, plc_id, is_test_data, center_loc="", change_to_utf_8=False):
    place_id_ = plc_id
    place_name = 'None'
    category = 'None'
    address = 'None'
    lng = 'None'
    lat = 'None'
    types = 'None'
    website = 'None'
    open_hrs = 'None'
    int_number = 'None'
    photo_reference = 'None'
    rating = 'None'
    distance_from_center = 'None'
    error = False
    eventId = ""
    if results_1['status'] == 'OK':
        results = results_1['result']
        status = results_1['status']
        if 'place_id' in results:
            # print(results['place_id'])
            place_id_ = results['place_id']
        if 'name' in results:
            # print(results['name'])
            place_name = results['name']
        if 'formatted_address' in results:
            # print(results['formatted_address'])
            address = results['formatted_address']
        if 'geometry' in results:
            # print(results['geometry']['location']['lng'])
            lng = results['geometry']['location']['lng']
            lat = results['geometry']['location']['lat']
            # loc_str = str(lat)+ " , "+str(lng)
            # if center_loc != '':
            # distance_from_center = dh.split_string(loc_str, center_loc)
            # distance_from_center = dh.get_distance(loc_str, center_loc)
        if 'types' in results:
            # print(results['types'])
            types = results['types']
            category = results['types']
        if 'website' in results:
            # print(results['website'])
            website = results['website']
        if 'international_phone_number' in results:
            # print(results['international_phone_number'])
            int_number = results['international_phone_number']
        if 'opening_hours' in results:
            # print(results['opening_hours']["weekday_text"])
            open_hrs = results['opening_hours']["weekday_text"]
        if 'photos' in results:
            # print(results['place_id'])
            photo_reference = results['photos'][0]['photo_reference']
        if "rating" in results:
            # print(results['place_id'])
            rating = results["rating"]

    else:
        error = True
    if change_to_utf_8:
        template = {
            "placeId": place_id_.encode('utf-8'),
            'place_name': place_name.encode('utf-8'),
            'category': category.encode('utf-8'),
            'address': address.encode('utf-8'),
            'location_coord': str(lat) + " , "+str(lng),
            'day_hours': open_hrs.encode('utf-8'),
            'phone': int_number.encode('utf-8'),
            'website': website.encode('utf-8'),
            "photo_reference": photo_reference,
            "rating": rating,
            "type_of_data": "scraped",
            # "distance_from_center":distance_from_center,
            "is_test_data": is_test_data,
            "eventId": eventId,
            "error": error

        }
    else:

        template = {
            "placeId": place_id_,
            'place_name': place_name,
            'category': category,
            'address': address,
            'location_coord': str(lat) + " , "+str(lng),
            'day_hours': open_hrs,
            'phone': int_number,
            'website': website,
            "photo_reference": photo_reference,
            "rating": rating,
            "type_of_data": "scraped",
            # "distance_from_center":distance_from_center,
            "is_test_data": is_test_data,
            "eventId": eventId,
            "error": error

        }
    return template
# fetch_from_mongo()
# fetch_from_json()
# create_json_data()
