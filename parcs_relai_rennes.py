import datetime
import json
import folium
import requests


def get_color(fill_rate):
    if fill_rate > .9:
        return "#FF0000"
    elif fill_rate > .6:
        return "#FF7F00"
    else:
        return "#00FF00"


def get_date_elements(date_string):
    # A way to calculate the time zone
    delta = datetime.datetime.now() - datetime.datetime.utcnow()
    update_time = datetime.datetime.fromisoformat(date_string) + delta
    return {
        "year": update_time.year,
        "month": update_time.month,
        "day": update_time.day,
        "hour": update_time.hour,
        "minute": update_time.minute,
    }


def get_data():
    return requests.get(
        'https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-parcs-relais-du-reseau-star-en-temps-reel&q=&sort=idparc&facet=nom&facet=etat'
    )


def get_park_information(api_string):
    json_string = json.loads(api_string.text)
    parking_lots = {}
    for i in range(json_string["nhits"]):
        parking_lots[json_string["records"][i]["fields"]["nom"]] = {
            "etat": json_string["records"][i]["fields"]["etat"],
            "lastupdate": get_date_elements(json_string["records"][i]["fields"]["lastupdate"]),
            "latitude": json_string["records"][i]["fields"]["coordonnees"][0],
            "longitude": json_string["records"][i]["fields"]["coordonnees"][1],
            "capaciteactuelle": json_string["records"][i]["fields"]["capaciteactuelle"],
            "capaciteactuellepmr": json_string["records"][i]["fields"]["capaciteactuellepmr"],
            "nombreplacesdisponibles": json_string["records"][i]["fields"]["nombreplacesdisponibles"],
            "nombreplacesdisponiblespmr": json_string["records"][i]["fields"]["nombreplacesdisponiblespmr"],
            "nombreplacesoccupees": json_string["records"][i]["fields"]["nombreplacesoccupees"],
            "nombreplacesoccupeespmr": json_string["records"][i]["fields"]["nombreplacesoccupeespmr"]
        }
    return parking_lots


def generate_map():
    # file = open("jsonParkingsRennes.json", "r")
    # data = eval(file.readline())
    # parkings = get_park_information(data)
    parkings = get_park_information(get_data())
    print("API data parsed")

    m = folium.Map(location=[48.114722, -1.679444], zoom_start=13)
    print("Map opened")
    for name in parkings:
        last_update = str(parkings[name]["lastupdate"]["day"]) + "/" + \
                      str(parkings[name]["lastupdate"]["month"]) + "/" + \
                      str(parkings[name]["lastupdate"]["year"]) + " " + \
                      str(parkings[name]["lastupdate"]["hour"]) + ":" + \
                      str(parkings[name]["lastupdate"]["minute"])

        state = parkings[name]["etat"]

        if state == 'Ouvert':
            occupation = parkings[name]["nombreplacesoccupees"] / parkings[name]["capaciteactuelle"]
            color = get_color(occupation)
            weight = 2 + int(20 * occupation)
            radius = 21 - int(10 * occupation)
            card = "<div style='width:25rem;position:relative;display:flex;flex-direction:column;min-width:0;word-wrap:break-word;'> \
                      <div style='padding:.5rem 1rem;margin-bottom:0;'><h3>" + name + "</h3></div> \
                      <div style='flex:1 1 auto;padding:1rem 1rem;'> \
                        <h4 style='margin-bottom:3rem!important;margin-top:0;'><span class='label label-success'>Ouvert</span></h4> \
                        <h4 style='margin-bottom:.5rem;'>Disponibilité</h4> \
                        <div style='width:200px;margin:auto;display:grid;grid-template:repeat(4,1fr)/1fr 30px'> \
                          <p style='margin-bottom:1rem;grid-row:1;grid-column:1;'>Places disponibles :</p><p style='margin-bottom:1rem;grid-row:1;grid-column:2;text-align:right;'>" + str(parkings[name]["nombreplacesdisponibles"]) + "</p> \
                          <p style='margin-bottom:1rem;margin-top:1rem;grid-row:2;grid-column:1;'>Places occupées :</p><p style='margin-bottom:1rem;margin-top:1rem;grid-row:2;grid-column:2;text-align:right;'>" + str(parkings[name]["nombreplacesoccupees"]) + "</p> \
                          <p style='margin-bottom:1rem;grid-row:3;grid-column:1;'>Places disponibles (PMR) :</p><p style='margin-bottom:1rem;grid-row:3;grid-column:2;text-align:right;'>" + str(parkings[name]["nombreplacesdisponiblespmr"]) + "</p> \
                          <p style='margin-bottom:1rem;margin-top:1rem;grid-row:4;grid-column:1;'>Places occupées (PMR) :</p><p style='margin-bottom:1rem;margin-top:1rem;grid-row:4;grid-column:2;text-align:right;'>" + str(parkings[name]["nombreplacesoccupeespmr"]) + "</p> \
                        </div> \
                        <p style='color:#777;margin-bottom:0;text-align:center;'> Mise à jour : " + last_update + "</p> \
                      </div> \
                    </div>"

        else:
            color = '#FF0000'
            weight = 22
            radius = 11
            card = "<div style='width:25rem;position:relative;display:flex;flex-direction:column;min-width:0;word-wrap:break-word;'> \
                      <div style='padding:0.5rem 1rem;margin-bottom:0;'><h3>" + name + "</h3></div> \
                      <div style='flex:1 1 auto;padding:1rem 1rem;'> \
                        <h4 style='margin-bottom:3rem!important;margin-top:0;'><span class='label label-danger'>Fermé</span></h4> \
                        <p style='color:#777;margin-bottom:0;text-align:center;'> Mise à jour : " + last_update + "</p> \
                      </div> \
                    </div>"

        folium.CircleMarker(
            location=(parkings[name]["latitude"], parkings[name]["longitude"]),
            radius=radius,
            tooltip=name,
            popup=folium.Popup(html=card, max_width=300),
            color=color,
            weight=weight,
            fill=True,
            fill_color="#000000",
        ).add_to(m)
        print("Marker added for " + name + " parking lot")
    m.save("parcs.html")


if __name__ == "__main__":

    generate_map()
