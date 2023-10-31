import requests 
import json 
from tkinter import *


# laat de laatste 5 berichten zien (de meest recente) op chronologische volgorde nieuw naar oud 
# voor elk bericht pak het station en daarvan de faciliteiten (station_service table)
# voor het station zelf waar het scherm staat, laat de weersvoorspelling zien https://openweathermap.org/
# doc: https://openweathermap.org/current

station = "Groningen"

# CSV_BESTAND_VELDEN = ["naam", "bericht", "station", "tijd", "datum"] 
test_berichten = [
    {"naam": "anoniem1", "bericht": "bericht test bericht test1 .","station": "Groningen", "tijd": "12:13:31", "datum": "30-10-2023"},
    {"naam": "anoniem2", "bericht": "bericht test bericht test 2.","station": "Groningen", "tijd": "12:13:31", "datum": "30-10-2023"},
    {"naam": "anoniem3", "bericht": "bericht test bericht test .3","station": "Groningen", "tijd": "12:13:31", "datum": "30-10-2023"},
    {"naam": "anoniem4", "bericht": "bericht test bericht test4 .","station": "Groningen", "tijd": "12:14:31", "datum": "30-10-2023"},
    {"naam": "anoniem5", "bericht": "bericht test bericht test 5.","station": "Groningen", "tijd": "12:15:31", "datum": "30-10-2023"},
]

API_KEY = "70dc2324e9a7f4f81b9d37f2a1489ef6"

def get_station_coords(station):
    r = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={station},31&limit=5&appid={API_KEY}")

    if not r.ok:
        print(f"Er is iets fout gegaan met het ophalen van het weer info: {r.status_code}")

    info = r.json()[0]

    return (info["lat"], info["lon"])

def get_station_weer_info():
    coords = get_station_coords(station)

    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={coords[0]}&lon={coords[1]}&units=metric&lang=nl&exclude=hourly,daily&appid={API_KEY}")

    if not r.ok:   
        print(f"Er is iets fout gegaan met het ophalen van het weer info: {r.status_code}")      
        
    return dict(r.json())

def get_stations():
    with open("stations.txt", 'r') as f:
        return f.readlines()
    

class StationBericht: 
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
        

class StationBerichtWidget: 
    """Label en Text widget voor stationsinhoud"""
    def __init__(self, root: Misc):
        self.root = root
        self.bericht = Label(root)
        self.info = Label(root)
        self.bericht.pack()
        self.info.pack()

        # spacing 
        Label(self.root, text="").pack()

    def update(self, bericht: StationBericht = None, dict = None):
        if bericht == None: 
            if dict == None: 
                raise Exception("bericht en dict argumenten kunnen niet leeg zijn")

            bericht = StationBericht(dict)

        self.info["text"] = f"{bericht.naam} op {bericht.datum} om {bericht.tijd}"
        self.bericht["text"] = f"“{bericht.text}”"

class StationshalUI:
    def __init__(self):
        # root 
        self.root = Tk()
        self.root.title("stationshalscherm")
        self.root.resizable(False, False)
        self.root.geometry("700x600")

        self.weer_info_frame = Frame(self.root)
        self.station_frame = Frame(self.root)
        self.station_label = Label(self.root, text=station, font="Courier 20 normal")

        # weer label vars
        self.temperatuur = StringVar()
        self.weer_beschrijving = StringVar()
        self.regenmm = StringVar()

        # props 
        self.station_label.pack(anchor=CENTER, side=TOP)
        self.weer_info_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)
        self.station_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=20, pady=20)

        # weer info frame
        self.temp_label = Label(self.weer_info_frame, textvariable=self.temperatuur, font="Courier 30 normal")
        self.bewolktheid_label = Label(self.weer_info_frame, textvariable=self.weer_beschrijving, font="Courier 20 normal")
        self.regen_label = Label(self.weer_info_frame, textvariable=self.regenmm, font="Courier 20 normal")

        # layout 
        self.bewolktheid_label.pack()
        self.temp_label.pack()
        self.regen_label.pack()

        # station frame
        self.bericht_labels = (
            StationBerichtWidget(self.station_frame),
            StationBerichtWidget(self.station_frame),
            StationBerichtWidget(self.station_frame),
            StationBerichtWidget(self.station_frame),
            StationBerichtWidget(self.station_frame),
        )

        self.update_weer_labels()
        self.update_bericht_labels()
        
    def update_weer_labels(self):
        weer = get_station_weer_info()
        try:
            self.temperatuur.set(f"{round(weer['main']['temp'])}°C")
            self.weer_beschrijving.set(weer["weather"][0]["description"])
            # self.regenmm.set(f"{round(weer['main']['temp'])}")
        except KeyError as e:
            print(f"Error bij lezen van weer info: {e}")
            return 
        
    def update_bericht_labels(self):
        for i, bericht in enumerate(test_berichten):
            self.bericht_labels[i].update(dict=bericht)

    def show(self): 
        self.root.mainloop()


def main():
    stationshal = StationshalUI()
    stationshal.show()

if __name__ == "__main__":
    main()