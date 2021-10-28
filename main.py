############################################################
# Project : Real-time public transport network data        #
# File name : api_bus_v5.py                                #
# Version : 5.0                                            #
# Last release : 27/10/2021                                #
# Author : Group B - CIPA 5 - ISEN Yncréa Ouest BREST      #
# Program that makes requests on the API of 4 cities to    #
# get bus stop schedule in real time defined by the user   #
############################################################


# -*- coding: utf-8 -*-


import requests, json, urllib, time, pytz, datetime
from time import sleep
from datetime import datetime, timedelta, date
from moduleEcran import ModuleEcran


def get_parameters():
    """
    Function that read parameters from an external JSON file, to know in which city, and in which bus stop the program
    have to make the search for the API request.
    Return "city" <str> and "bus_stop" <str>.
    """
    json_file = open("parameters.json")
    parameters = json.load(json_file)
    json_file.close()
    city = str(parameters["city"]).encode("latin1").decode("utf-8").upper()  # prevent special characters errors
    bus_stop = str(parameters["bus_stop"]).encode("latin1").decode("utf-8")  # prevent special characters errors
    return city, bus_stop


def get_url(city, bus_stop):
    """
    Function that build an URL to make a request on the API, in accordance to API URL syntax.
    This function takes as input the bus stop specified by the user and return a URL according to the bus stop.
    Takes "city" <str>, "bus_stop" <str> and return "url" <str>.
    """
    url = ""  # URLs of cities to get results of the 10 last bus in chronological order by bus stop name at UTC Paris
    if city == "RENNES":
        url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-bus-circulation-passages-tr" \
              "&q=&rows=10&sort=-depart&facet=nomarret&refine.nomarret=" + bus_stop + "&timezone=Europe%2FParis"
    elif city == "NANTES":
        url = "http://open.tan.fr/ewp/tempsattente.json/" + bus_stop
    elif city == "CAEN":
        bus_stop = urllib.parse.quote(bus_stop, safe='')
        url = "https://data.twisto.fr/api/records/1.0/search/?dataset=horaires-tr" \
              "&q=&rows=10&sort=horaire_de_depart_reel&facet=nom_de_l_arret_stop_name" \
              "&refine.nom_de_l_arret_stop_name=" + bus_stop + "&timezone=Europe%2FParis"
    return url


def get_json(url):
    """
    Function that calls the API to get a response and convert it into a JSON file in dictionary type.
    Takes "url" <str> and return "json_file" <dict>.
    """
    json_file = json.loads(requests.get(url).text)  # convert response from API into a JSON file
    return json_file


def get_data(city, data):
    """
    Function that extract and treat data of each bus from JSON file to convert them into multiple dictionaries.
    Then, each dictionary are put into a general list that will be send to a led display matrix.
    Takes "city" <str>, "data" <dict> and return "bus_list" <list>.
    """
    bus_list = []  # initialisation of the list containing all bus results
    keys = {  # dictionary of data keys to set for each city treatment
        "RENNES": ["nomcourtligne", "destination", "depart", ""],
        "NANTES": ["ligne", "terminus", "temps"],
        "CAEN": ["ligne", "destination_stop_headsign", "horaire_de_depart_reel", "date_du_jour"]
    }
    if city == "RENNES":
        for bus in data["records"]:  # for each recorded bus recover in the json file
            field = bus["fields"]  # json key to access to data
            line = field[keys[city][0]]  # name of the bus line
            destination = field[keys[city][1]]  # destination of the bus line
            departure = field[keys[city][2]]  # time of bus departure
            time = get_time(city, line, destination, departure, "")  # call function to time treatment
            bus_dictionary = {  # create a dictionary with previous data for each bus
                "ligne": line,
                "terminus": destination,
                "temps": time
            }
            bus_list.append(bus_dictionary)  # add each dictionary in the general list
    elif city == "CAEN":
        for bus in data["records"]:  # for each recorded bus recover in the json file
            field = bus["fields"]  # json key to access to data
            line = field[keys[city][0]]  # name of the bus line
            destination = field[keys[city][1]]  # destination of the bus line
            departure = field[keys[city][2]]  # time of bus departure
            date = field[keys[city][3]]  # date of bus departure
            time = get_time(city, line, destination, departure, date)  # call function to time treatment
            bus_dictionary = {  # create a dictionary with previous data for each bus
                "ligne": line,
                "terminus": destination,
                "temps": time
            }
            bus_list.append(bus_dictionary)  # add each dictionary in the general list
    elif city == "NANTES":
        for bus in range(len(data)):  # for each recorded bus recover in the json file
            line = data[bus]["ligne"]["numLigne"]  # name of the bus line
            destination = data[bus]["terminus"]  # destination of the bus line
            departure = data[bus]["temps"]  # time of bus departure
            time = get_time(city, line, destination, departure, "")  # call function to time treatment
            bus_dictionary = {  # create a dictionary with previous data for each bus
                "ligne": line,
                "terminus": destination,
                "temps": time
            }
            bus_list.append(bus_dictionary)  # add each dictionary in the general list
        bus_list = sorted(bus_list, key=lambda j: float(j["temps"]))  # sort by chronological order
    return bus_list


def get_time(city, line, destination, departure, date):
    """
    Function that makes time treatment in function of each city, to convert input time, to a universal string.
    Takes "city" <str>, "line" <str>, "destination" <str>, "departure" <str> and "date" <str> (for CAEN only)
    to return "departure" <str> in timestamp format.
    """
    if city == "RENNES":
        departure = str(datetime.timestamp(datetime.strptime(departure, "%Y-%m-%dT%H:%M:%S%z")))  # time conversion
    elif city == "NANTES":
        current_time = int(time.time())  # get actual time now
        if departure == "Proche":  # prevent values error when remaining time is < 1 minute
            departure = str(60 + current_time)
        elif "h" in departure:
            if ">" in departure:  # Prevent values error when remaining time is > 1 hour
                offset = 3600 / 2
            else:
                offset = 0
            departure = "".join([c * c.isnumeric() for c in departure])
            departure = str(int(departure) * 3600 + current_time + offset)
        elif "m" in departure:
            departure = departure[0:departure.index("m") + 1]
            departure = "".join([c * c.isnumeric() for c in departure])
            departure = str(int(departure) * 60 + current_time)
        else:
            # We should not be here
            print("Error on data")
    elif city == "CAEN":
        departure_hour_tens = departure[0]  # tens digit of the hour value of departure string
        departure_hour_units = departure[1]  # units digit of the hour value of departure string
        if int(str(departure_hour_tens + departure_hour_units)) >= 24:  # prevent values error when hour >= 24
            departure = list(departure)
            departure[1] = str(int(departure_hour_tens + departure_hour_units) - 24)  # transform hour in 24hour format
            departure[0] = "0"  # makes tens digits of hour to zero when midnight passed
            departure = "".join(departure)
            departure = datetime.strptime(departure, "%H:%M:%S").time()
            date = datetime.strptime(date, "%Y-%m-%d").date()
            date = date + timedelta(days=1)  # increments the day of the date when midnight passed
        departure = str(datetime.timestamp(datetime.strptime(str(date) + str(departure), "%Y-%m-%d%H:%M:%S")))
    else:
        print("Error, not cities specified")
    # *** START : Console print to compare validity of data with reality ***
    bus_time_left_timestamp = float(departure) - datetime.timestamp(datetime.now())
    bus_departure_fromtimestamp = datetime.fromtimestamp(float(departure))
    bus_departure_hour = bus_departure_fromtimestamp.hour
    bus_departure_minute = bus_departure_fromtimestamp.minute
    if bus_time_left_timestamp >= 0.0:  # prevent calcul error of negative values
        bus_time_left = str(int(bus_time_left_timestamp//60)) + " min" if bus_time_left_timestamp//60<60 else ">1h"  # calculate time minute in <datetime>
        if bus_time_left_timestamp//60 >= 0:  # double prevention : only if time left is superior or equal than 0 minutes
            print("")
            print("Ligne : ", line)
            print("Destination : ", destination)
            print("Départ à : " + str(bus_departure_hour).zfill(2) + "h" + str(bus_departure_minute).zfill(2))
            print("Temps restant : ", bus_time_left)
            print("")
            print("*"*30)
    # *** END : Console print to compare validity of data with reality ***
    return departure


def get_brest_data(stop_name):
    # Calculate timezone time difference
    tz = pytz.timezone('Europe/Paris')
    dt = datetime.fromtimestamp(time.time(), tz)
    timezone_time_difference = (int(dt.strftime('%z')) / 100) * 3600

    # Get all route for this stop
    routes_stop = eval(requests.get('https://applications002.brest-metropole.fr/WIPOD01/Transport/REST/getRoutes_Stop?format=json&stop_name=' + stop_name).text)
    sleep(1.5)

    routes = []
    for i in range(len(routes_stop)):
        routes.append(routes_stop[i]['Route_id'])

    # Get terminus for each line
    routes_params = []
    for i in range(len(routes)):
        terminus = eval(requests.get('https://applications002.brest-metropole.fr/WIPOD01/Transport/REST/getDestinations?format=json&route_id=' + routes[i]).text)
        sleep(1.5)
        for j in range(len(terminus)):
            routes_params.append({
                'route': routes[i],
                'terminus': terminus[j]['Trip_headsign']
            })

    # for each line and terminus, get next bus remaining time
    bus = []
    for i in range(len(routes_params)):
        url = 'https://applications002.brest-metropole.fr/WIPOD01/Transport/REST/getRemainingTimes?format=json&route_id=' + routes_params[i]['route'] + '&trip_headsign=' + routes_params[i]['terminus'].replace(' ', '+') + '&stop_name=' + stop_name
        next_bus = eval(requests.get(url).text)
        sleep(1.5)
        for k in range(min(len(next_bus), 1)):
            bus.append({
                'ligne': routes_params[i]['route'],
                'terminus': routes_params[i]['terminus'],
                'temps': str(time.mktime(datetime.strptime(str(date.today()) + next_bus[k]['Arrival_time'], "%Y-%m-%d%H:%M:%S").timetuple()) + timezone_time_difference)
            })

    bus = sorted(bus, key=lambda x: (x['temps']))
    return bus


def process(city, bus_stop):
    city, bus_stop = city, bus_stop
    print("")
    string = "--- Réseau de bus de la ville de " + city + " ---"
    print(string.center(30))
    print("\n Liste de tout les bus passant à l'arrêt : ", bus_stop, "\n")
    print("*" * 30)
    # Currently Brest is treated separatly because his API do not work like the others
    if city == "BREST":
        data = get_brest_data(bus_stop)
    else:
        url = get_url(city, bus_stop)
        json_file = get_json(url)
        data = get_data(city, json_file)
    print("\nData to send to the led display matrix :")
    print(type(data), data)
    return data


if __name__ == '__main__':
    scr = ModuleEcran(1)
    scr.start()
    while 1:
        wait_time = 60.0
        city = get_parameters()[0]
        bus_stop = get_parameters()[1]
        scr.conf(city + " " + bus_stop)
        time.sleep(2.0)
        try:
            data = process(city, bus_stop)
            if len(data)>0:
                scr.update(data)
            else:
                wait_time = 8.0
        except:
            wait_time = 8.0
        time.sleep(wait_time)
    scr.stop()
