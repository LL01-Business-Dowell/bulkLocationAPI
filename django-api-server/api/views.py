from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import googlemaps
from decouple import config
import traceback
from django.http import Http404, JsonResponse
from rest_framework import status
import requests
import json
import time
from . import data_handlers as dh
import os
# Create your views here.
# api_key = config("API_KEY")
api_key = os.getenv('API_KEY')
# api_key_samanta = config("API_KEY_SAMANTA")
# api_key_samanta = os.getenv("API_KEY_SAMANTA")
# default_key = config("DEF_KEY")
default_key = os.getenv("DEF_KEY")


def home(request):
    return HttpResponse("App successfulll")


class CustomError(Exception):
    pass


class GetNearbyPlacesLocallyV3(APIView):
    def get(self, request, format=None):

        return JsonResponse({"info": f"Kindly use a POST request instead of GET"})

    def post(self, request, format=None):
        gmaps = googlemaps.Client(key=api_key)
        myDict = request.data
        try:
            # Retrieve and validate input parameters
            type_error_message = "Kindly check if the parameter"
            radius1 = float(myDict['radius1'])
            radius2 = float(myDict['radius2'])
            if radius2 <= 0:
                return Response({"place_id_list": []}, status=status.HTTP_200_OK)

            center_latt = float(myDict['center_lat'])
            center_lonn = float(myDict['center_lon'])
            search_string = myDict['query_string']
            if not isinstance(search_string, str):
                raise ValueError("Search string must be of type string.")

            limit = int(myDict['limit'])
            if limit not in [20, 40, 60]:
                raise ValueError(
                    "Limit should be one of the following: 20, 40, 60.")

            wanted_api_key = myDict['api_key']
            # if wanted_api_key != default_key:
            #     res = dh.processApikey(wanted_api_key)
            #     if res.status_code == 400:
            #         raise ValueError("Invalid API key.")

            # Initialize parameters
            center_loc_str = f"{center_latt}, {center_lonn}"
            check = True
            t = 0
            page_tok = None
            wanted_list = []
            place_id_list = []
            count_res = limit

            while check:
                t += 1
                print("Request iteration:", t)

                params = {
                    'query': search_string,
                    'location': (center_latt, center_lonn),
                    'radius': radius2
                }
                if page_tok:
                    params['page_token'] = page_tok

                try:
                    r_json = gmaps.places(**params)
                except googlemaps.exceptions.ApiError as e:
                    return Response({"error": f"API Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
                except googlemaps.exceptions.Timeout as e:
                    return Response({"error": "Timeout occurred while accessing Google Maps API."}, status=status.HTTP_408_REQUEST_TIMEOUT)
                except googlemaps.exceptions.TransportError as e:
                    return Response({"error": "Network error while accessing Google Maps API."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
                except Exception as e:
                    return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                count_res -= 20
                wanted_list.extend(r_json.get('results', []))
                if count_res <= 0 or 'next_page_token' not in r_json:
                    check = False
                else:
                    page_tok = r_json['next_page_token']
                    time.sleep(2)  # Ensure token becomes active

            for place in wanted_list:
                place_id_list.append(place.get('place_id', ''))

            payload_2 = {
                "place_id_list": place_id_list,
                "center_loc": center_loc_str
            }
            return Response(payload_2, status=status.HTTP_200_OK)

        except ValueError as ve:
            return Response({"error": f"ValueError: {str(ve)}"}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as ke:
            return Response({"error": f"Missing parameter: {str(ke)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print("Unexpected Error:", message)
            return Response({"error": f"Unexpected Error: {message}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetPlaceDetailsListStage1(APIView):
    """
    List all countries, or create a new country.
    """

    def get(self, request, format=None):
        # ll2 = {'html_attributions': [], 'result': {'address_components': [{'long_name': 'Nairobi', 'short_name': 'Nairobi', 'types': ['locality', 'political']}, {'long_name': 'Maziwa', 'short_name': 'Maziwa', 'types': ['sublocality_level_1', 'sublocality', 'political']}, {'long_name': 'Nairobi County', 'short_name': 'Nairobi County', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'Kenya', 'short_name': 'KE', 'types': ['country', 'political']}, {'long_name': '00600', 'short_name': '00600', 'types': ['postal_code']}], 'adr_address': 'kingara Road, <span class="street-address">opp kingara close behind Junction Mall</span>, <span class="postal-code">00600</span>, <span class="locality">Nairobi</span>, <span class="country-name">Kenya</span>', 'business_status': 'OPERATIONAL', 'current_opening_hours': {'open_now': True, 'periods': [{'close': {'date': '2023-04-23', 'day': 0, 'time': '2100'}, 'open': {'date': '2023-04-23', 'day': 0, 'time': '1100'}}, {'close': {'date': '2023-04-24', 'day': 1, 'time': '2100'}, 'open': {'date': '2023-04-24', 'day': 1, 'time': '1100'}}, {'close': {'date': '2023-04-25', 'day': 2, 'time': '2100'}, 'open': {'date': '2023-04-25', 'day': 2, 'time': '1100'}}, {'close': {'date': '2023-04-26', 'day': 3, 'time': '2100'}, 'open': {'date': '2023-04-26', 'day': 3, 'time': '1100'}}, {'close': {'date': '2023-04-27', 'day': 4, 'time': '2100'}, 'open': {'date': '2023-04-27', 'day': 4, 'time': '1100'}}, {'close': {'date': '2023-04-21', 'day': 5, 'time': '2100'}, 'open': {'date': '2023-04-21', 'day': 5, 'time': '1100'}}, {'close': {'date': '2023-04-22', 'day': 6, 'time': '2100'}, 'open': {'date': '2023-04-22', 'day': 6, 'time': '1100'}}], 'weekday_text': ['Monday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Tuesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Wednesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Thursday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Friday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Saturday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Sunday: 11:00\u202fAM\u2009–\u20099:00\u202fPM']}, 'delivery': True, 'dine_in': True, 'formatted_address': 'kingara Road, opp kingara close behind Junction Mall, Nairobi, Kenya', 'formatted_phone_number': '0742 894700', 'geometry': {'location': {'lat': -1.2960063, 'lng': 36.7616708}, 'viewport': {'northeast': {'lat': -1.294604919708498, 'lng': 36.7631173802915}, 'southwest': {'lat': -1.297302880291502, 'lng': 36.76041941970851}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png', 'icon_background_color': '#FF9E67', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet', 'international_phone_number': '+254 742 894700', 'name': 'Whitefield Restaurant', 'opening_hours': {'open_now': True, 'periods': [{'close': {'day': 0, 'time': '2100'}, 'open': {'day': 0, 'time': '1100'}}, {'close': {'day': 1, 'time': '2100'}, 'open': {'day': 1, 'time': '1100'}}, {'close': {'day': 2, 'time': '2100'}, 'open': {'day': 2, 'time': '1100'}}, {'close': {'day': 3, 'time': '2100'}, 'open': {'day': 3, 'time': '1100'}}, {'close': {'day': 4, 'time': '2100'}, 'open': {'day': 4, 'time': '1100'}}, {'close': {'day': 5, 'time': '2100'}, 'open': {'day': 5, 'time': '1100'}}, {'close': {'day': 6, 'time': '2100'}, 'open': {'day': 6, 'time': '1100'}}], 'weekday_text': ['Monday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Tuesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Wednesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Thursday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Friday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Saturday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Sunday: 11:00\u202fAM\u2009–\u20099:00\u202fPM']}, 'photos': [{'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jkATuC0T8GjDwd36b2qFmdvX05LoynTd7UYt21ecQeWWbhro-dFZ1X5fmPWgnYx3St6-5ceQoznAl9kiFDzRBivsyP_rNHc0jA9vHJ0SZ2wwzamP4FcP2Pu_36nSZObngCkWOcLN3UeLo5meFYAGLaWsxhhiJjlX2QcM64ZL9CP1_bP', 'width': 960}, {'height': 2448, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jnZFX2-uMZTgVBBo52uE6iWjdNFAemLYStnV1LOKq5vrrkdfvLF8UR0VPrYgo9ZzNFPkZusndaGms8EGKdgWpU02jL59Hr-HZy0tgpD13AV1ikVuKAWuxury0aLX5H845y_JoKhcbRhknrAT1tKEpUvnqth6heS34IZvjxEf3YDiXUB', 'width': 3264}, {'height': 4032, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/117873843766263809334">Evans Sigei</a>'], 'photo_reference': 'AUjq9jmoR1PWZKV0rA8iYwS2LqOJJRtntAmFwurFxPNWpm8hQft8wZnDk_RcC-RwLdDv7AxsLTeLrFUNB554gZ2sR1xKR1DJ7DzbjNyGF-aOQh43DMSKMqeCOA4k9Ql99LCTTFzU-fnf6wyCAKq0g1i5QxFgNNBrZGMbIbFFt96A4WGQBO1J', 'width': 3024}, {'height': 1650, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jmJff323BYeFMIzMLzJmxYwD-2g0EDLrOpGks_FbmyrcYfqnstiZ5U5TUNDGNuC0hN0qN0lw8qjnTZCcPmfJvJH5Rw6AnSuVcWACS45D3o9SVDEFFMg1tfSF1uudbSLT54w63lh0QXj4SqOtYxISaUusPahxCXSHqxa-v8-yhVo_t6B', 'width': 1275}, {'height': 3264, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/117685926906985511601">Mahim Hegde</a>'], 'photo_reference': 'AUjq9jnWZfCKYMFcUXoOBWghItru6bc8lwZF7QSaAECOUu-JJ684azbtplyQcjnLdsr_ZA6ocM-G-JaXsjMVKPjen_KKAWKCj2-OfYIRc_rlm0o4sEePGf2NDpwitGMxnQ8itKHweK3L4CeiJx-Mn71j1gbGiVnXPpRHiYfk_4UQYPwJ9o3i', 'width': 2448}, {'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jngXTtuMCD-Pt2OmZcwEKS40hC5rpC9fKJxnx0-ZVLv4RWNt38JRWcaz6xGPXBUKf9sdhH51EhciXmYfM2hWvgi3qNAJvQ6LALvAuP6y3bChqLSefLhlAwQuq395cuhTCoviwWZAjFCO6lsKjDo0mekdGlc4TpxXx2nJUytXq3d1IgS', 'width': 960}, {'height': 1280, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jlNsDNyP6iGDW5G0IEJRTUasz4LkHXbw6YEIly95wgh6fzUSYaAKTL2csQ8n3toTuhUQIsVy6ekD2ZjUXQIk4FHLLkjI_-mIsQWQWmefjh867qtQprVjyC7Cn38OMdbiHq0M1GlEbZNmACByoLF_cr3jgOMZ0bbqSq8P3ySlE15A9J5', 'width': 1280}, {'height': 1280, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jkPG8gKWMtee3Ct8KGUDlber9BW4PqCySq8LhSOYJmAYltKg4hnV-n0UejRM91RHEiW1CCDph049QiJ_wNNowXEX0Ozj0nMjyu0PhF6o01k52bO8BvoViUlSdfOUCom_ZGTw48oMKMvkrCPSGzQuJadfA-DOWbPuiubtO6ur9t-XeYG', 'width': 1280}, {'height': 500, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jn9GgvLFriqvar95wBBO9C44wSkVPpD7BMd6ArKwebr9Lyjq-93XbVEPvkP-pWWnYBfJ6XkLiM21a_W7mNqzv_JlzGnGCUs-YFJ4ugFzmUVWupb-aSM8EdntR7RjNg_hKyGOeXqu_HUOBdTCT7aVgawoy4P9H_i7UN_lps_fmqAJ8ub', 'width': 500}, {'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jlkN2f5c9x01-8wd6hVFQZRITX0Rar1RgnKeViKewap2DNzMoY_5QFqchKpWyqyJrSNd7X2elYUGhA-G-qNoH3cCrNDeexeHV3lMragck_96Kfj4crDmjVqDQNvl-jaE79PhkzmESSV6iOySH8s9lgIyr8o-T27LlqL5z0taUxPvbRq', 'width': 960}], 'place_id': 'ChIJj3S0t1IbLxgRYgL-7uH0NIo', 'plus_code': {'compound_code': 'PQ36+HM Nairobi, Kenya', 'global_code': '6GCRPQ36+HM'}, 'price_level': 2, 'rating': 4.3, 'reference': 'ChIJj3S0t1IbLxgRYgL-7uH0NIo', 'reservable': True, 'reviews': [{'author_name': 'David Kanagaretnam', 'author_url': 'https://www.google.com/maps/contrib/109567623568041706461/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5R7RaF1ueYKm_U0ye8jTBBG7K5T3fjTBWQ1MO4BiQ=s128-c0x00000000-cc-rp-mo-ba5', 'rating': 5, 'relative_time_description': 'a year ago', 'text': 'This is a great restaurant for Indian foods mainly however, you will get Kenyan and others too. A calm place to dine with your family and its has a big parking space.  Staff are welcoming and serving the food fast. The place is clean. Prices for food is affordable.', 'time': 1649416437, 'translated': False}, {'author_name': 'Julliet Esta', 'author_url': 'https://www.google.com/maps/contrib/109510066687005858247/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5TQOlQJn_hcLNSJJbB7omg4O-RCyfpbt-4t3unXQls=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 5, 'relative_time_description': '11 months ago', 'text': "We received a warm welcome, service was fast, the food was great and the portions are definitely enough. I would recommend this restaurant for Indian, Chinese and African cuisine, there's a large parking area, kids play area and also a kids menu. The food was also affordable", 'time': 1651396718, 'translated': False}, {'author_name': 'Aoko Gathoni', 'author_url': 'https://www.google.com/maps/contrib/110036374557197962895/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5RHO3ZIMXY_WihCLk7C2xcQcTKdoc5-QhSNkoWh=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 4, 'relative_time_description': '4 months ago', 'text': "When I arrived, the place looked like it wasn't open. But upon asking someone there, he said it was open.\nI ordered for the half koroga chicken with Naan, and to drink, I had tea masala. I liked that their portions were good size.\nI would definitely go back there.", 'time': 1670771464, 'translated': False}, {'author_name': 'Duncanah Gwat', 'author_url': 'https://www.google.com/maps/contrib/116990714119709426524/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5QXiXwls4KibppDfJxM5IHebKyTFfNr5J2j_LoEmw=s128-c0x00000000-cc-rp-mo-ba2', 'rating': 5, 'relative_time_description': '2 months ago',
        # 'text': 'Beutiful place to be, went for a late lunch, nicely ushered in, the waiter was very polite, super helpful. The serve was quick too. The meal was tasty as well', 'time': 1675536564, 'translated': False}, {'author_name': 'B -', 'author_url': 'https://www.google.com/maps/contrib/111323236689199522335/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5Rp3yfS6xwFBSbA9ZvQjd0F50zh5RkWTANNhk44IeI=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 1, 'relative_time_description': '2 weeks ago', 'text': 'Lovely place. Quiet and clean. Polite and friendly staff and they make really good Indian food. The parking is a bit cramped but overall a good intimate experience. The prices are also very agreeable.\n\nI went back recently and standards have plummeted. Its now a really horrible, depressing restaurant that has no identity. It wants to be an Indian restaurant but cant, also Chinese but not happening. Poor service and food that was definitely not fresh.', 'time': 1680543330, 'translated': False}], 'serves_beer': True, 'serves_brunch': True, 'serves_dinner': True, 'serves_lunch': True, 'serves_vegetarian_food': True, 'serves_wine': True, 'takeout': True, 'types': ['restaurant', 'food', 'point_of_interest', 'establishment'], 'url': 'https://maps.google.com/?cid=9958853927237452386', 'user_ratings_total': 171, 'utc_offset': 180, 'vicinity': 'kingara Road, opp kingara close behind Junction Mall, Nairobi', 'website': 'https://whitefieldrestaurant.reserveport.com/', 'wheelchair_accessible_entrance': True}, 'status': 'OK'}
        return JsonResponse({"data": "Kindly use a POST request instead of GET"})

    def post(self, request, format=None):
        # place_id_list = request.POST.getlist('place_id_list')
        # place_id_list2 = request.POST.get('place_id_list')
        myDict = request.data
        place_id_list = myDict['place_id_list']
        center_loc = 'None'
        # if "center_loc" in myDict:
        # center_loc = myDict["center_loc"]
        total_succ_queried = list()
        total_failed_queried = list()
        total_succ_saved = list()
        place_id = ''
        result_list = list()
        result_error = list()
        # print("raw POSY============")
        # print(list(request.POST.items()))
        # print("raw rquest============")
        # print(place_id_list)
        # print(type(place_id_list))
        # print("raw rquest2============")
        # print(place_id_list2)
        # print(type(place_id_list2))
        # print("raw simplejspn============")
        # print(myDict)
        # print(type(myDict))

        try:
            wanted_api_key = myDict['api_key']
            change_to_utf_8 = False
            if 'change_to_utf_8' in myDict:
                change_to_utf_8 = (bool(myDict['change_to_utf_8']))
            print("wanted_api_key ------>>> ", wanted_api_key)
            type_error_message = "Invalid key."
            # if wanted_api_key != default_key:
            #     res = dh.processApikey(wanted_api_key)
            #     if res.status_code == 400:
            #         result = json.loads(res.text)
            #         type_error_message = type_error_message + \
            #             " "+result["message"]
            #         # raise CustomError(type_error_message)
            #         return Response(type_error_message, status=status.HTTP_400_BAD_REQUEST)
            for plc_id in place_id_list:
                place_id = plc_id
                url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=' + \
                    place_id+'&key='+api_key

                r = requests.get(url)
                results = json.loads(r.text)
                # print("raw results new stage 1============")
                # print(results)
                # if center_loc != 'None':
                if r.status_code == 400:
                    # result = json.loads(res.text)
                    type_error_message = type_error_message + \
                        " "+results["message"]
                    # raise CustomError(type_error_message)
                    return Response(type_error_message, status=status.HTTP_400_BAD_REQUEST)
                if change_to_utf_8:
                    resp = dh.retrieve_details(
                        results, plc_id, True, center_loc, True)
                else:
                    resp = dh.retrieve_details(
                        results, plc_id, True, center_loc)
                if not resp['error']:
                    result_list.append(resp)
                    total_succ_queried.append(plc_id)
                else:
                    result_error.append(resp)
                    total_failed_queried.append(plc_id)

            result_dict = {
                "succesful_results": result_list,
                "failed_results": result_error
            }
            return Response(result_dict, status=status.HTTP_200_OK)
        except CustomError:
            return Response("No results for the place id: "+place_id, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("No results for the place id: "+place_id, status=status.HTTP_400_BAD_REQUEST)
