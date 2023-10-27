import requests 
import json 
from tkinter import *

# laat de laatste 5 berichten zien (de meest recente) op chronologische volgorde nieuw naar oud 
# voor elk bericht pak het station en daarvan de faciliteiten (station_service table)
# voor het station zelf waar het scherm staat, laat de weersvoorspelling zien https://openweathermap.org/
# doc: https://openweathermap.org/current


station = "Groningen"

def get_stations():
    with open("stations.txt", 'r') as f:
        return f.readlines()

class stationshalUI():
    def __init__(self):
        # root 
        self.root = Tk()
        self.root.title("stationshalscherm")
        self.root.resizable(False, False)
        self.root.geometry("700x600")

        self.weer_info_frame = LabelFrame(self.root)
        self.station_frame = LabelFrame(self.root)
        self.station_label = Label(self.root, text=station, font="Courier 20 normal")

        # weer label vars
        self.temperatuur = StringVar()
        self.bewolktheid = StringVar()
        self.regenmm = StringVar()
        self.temperatuur.set("12°C")
        self.bewolktheid.set("Bewolkt")
        self.regenmm.set("3.2 mm")

        # props 
        self.station_label.pack(anchor=CENTER, side=TOP)
        self.weer_info_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)
        self.station_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=20, pady=20)

        # weer info frame
        self.temp_label = Label(self.weer_info_frame, textvariable=self.temperatuur, font="Courier 30 normal")
        self.bewolktheid_label = Label(self.weer_info_frame, textvariable=self.bewolktheid, font="Courier 20 normal")
        self.regen_label = Label(self.weer_info_frame, textvariable=self.regenmm, font="Courier 20 normal")

        # layout 
        self.bewolktheid_label.pack()
        self.temp_label.pack()
        self.regen_label.pack()

        # station frame
        
    def update_weer_labels():
        pass

    def update_bericht_labels():
        pass

    def show(self): 
        self.root.mainloop()


r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat=52.0&lon=5.19&units=metric&lang=nl&exclude=hourly,daily&appid=70dc2324e9a7f4f81b9d37f2a1489ef6")

def main():
    stationshal =  stationshalUI()
    stationshal.show()

if __name__ == "__main__":
    main()