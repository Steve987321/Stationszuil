import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import database


station = "Groningen" # station waar dit scherm op staat
API_KEY = "70dc2324e9a7f4f81b9d37f2a1489ef6"
db = database.StationsZuilDB()

class StationBericht: 
    """Structuur voor een station bericht"""
    def __init__(self, dict = None, naam = None, bericht = None, station = None, tijd = None, datum = None):
        if dict != None: 
            self.naam = dict["naam"]
            self.text = dict["bericht"]
            self.station = dict["station"]
            self.tijd = dict["tijd"]
            self.datum = dict["datum"]
            return

        self.naam = naam
        self.text = bericht
        self.station = station
        self.datum = datum
        self.tijd = tijd


def get_station_coords(station):
    """Geeft de coordinaten van de gegeven station locatie"""
    r = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={station},31&limit=5&appid={API_KEY}")

    if not r.ok:
        print(f"Er is iets fout gegaan met het ophalen van het weer info: {r.status_code}")

    info = r.json()[0]

    return (info["lat"], info["lon"])

def get_station_weer_info():
    """"Geeft weer info via een json formaat van de station"""
    coords = get_station_coords(station)

    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={coords[0]}&lon={coords[1]}&units=metric&lang=nl&exclude=hourly,daily&appid={API_KEY}")

    if not r.ok:   
        print(f"Er is iets fout gegaan met het ophalen van het weer info: {r.status_code}")      
        
    return dict(r.json())

def get_station_faciliteiten():
    """Geeft beschikbare faciliteiten van de station via een dictionary"""
    rows = db.get_row("""
                select ov_bike, elevator, toilet, park_and_ride from station_service
                where station_city = %s    
                """,
                (station,)) # tuple 

    return {"fiets": rows[0], "lift": rows[1], "toilet": rows[2], "pr": rows[3]}

def get_stations():
    """Geef alle beschikbare stations in een lijst"""
    with open("stations.txt", 'r') as f:
        return f.readlines()
