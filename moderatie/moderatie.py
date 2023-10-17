import psycopg2
import csv
from tkinter import * 

GREEN = "#0F0"
RED = "#F00"
BLUE = "#00F"
WHITE = "#FFF"
GRAY = "#999"


class Modereer():
    def __init__(self, berichten_bestand_naam):
        self.bestand = berichten_bestand_naam
        self.index = 0 # hoe ver we zijn met beoordelen

        with open(self.bestand) as f:
            self.berichten = list(csv.DictReader(f))
        
    def geef_bericht(self):
        """Geeft berichten terug die nog niet zijn beoordeeld"""
        if self.index >= len(self.berichten):
            return "Geen berichten om te beoordelen."
        return self.berichten[self.index]
    
    def beoordeel_bericht(self, goedgekeurd):
        """Beoordeel bericht op index"""
        if goedgekeurd:
            # stuur naar database
            pass

        self.index += 1
        
    def update_bestand(self):
        """Verwijderd beoordeelde berichten"""
        with open(self.bestand, "r+") as f:
            lines = f.readlines()

            f.seek(0)
            f.truncate()

            f.write(lines[0])
            if self.index != len(self.berichten):
                f.writelines(lines[self.index + 1:])
                print(self.index, len(self.berichten))

            self.index = 0
        with open(self.bestand, 'r') as f:
            self.berichten = list(csv.DictReader(f))

# TODO: update csv bij aflsuiten
class ModeratieGUI():
    def __init__(self, naam_window: str = "moderatie"):
        self.moderatie = Modereer("berichten.csv")

        self.root = Tk()
        self.root.title(naam_window)
        self.root.resizable(False, False)
        self.root.geometry("500x500")

        self.info_frame = LabelFrame(self.root, height=300, width=450, text="bericht")
        self.info_frame.pack_propagate(False)
        self.info_frame.pack(padx=20, pady=10)

        # self.info_bericht_frame = Frame(self.info_frame, height=100, width=200)
        # self.info_bericht_frame.pack(padx=20, pady=10, side=BOTTOM)

        # laat voorgang van beoordelen zien
        # self.info_label_counter = Label(self.info_frame, text="")
        # self.info_label_counter.pack()

        # bericht
        self.naam = Label(self.info_frame)
        self.station = Label(self.info_frame)
        self.tijd = Label(self.info_frame)
        self.bericht = Text(self.info_frame, height=10)

        self.update_bericht_labels()

        self.bericht["state"] = DISABLED
        self.bericht.pack(padx=20, pady=10, side=BOTTOM, anchor=CENTER)
        self.naam.pack(padx=50, pady=2, side=TOP, anchor=CENTER)
        self.station.pack(padx=50, pady=2, side=TOP, anchor=CENTER)
        self.tijd.pack(padx=50, pady=2, side=TOP, anchor=CENTER)

        # moderatie 
        self.optie_frame = LabelFrame(self.root, height=200, width=450, text="moderatie")
        self.optie_frame.pack_propagate(False)
        self.optie_frame.pack(pady=10)
    
        self.btn_goedkeuren = Button(self.optie_frame, text="goedkeuren", command=self.on_goedkeuring)
        self.btn_goedkeuren.pack(padx=10, anchor=CENTER)

        self.btn_afkeuren = Button(self.optie_frame, text="afkeuren", command=self.on_afkeuring)
        self.btn_afkeuren.pack(padx=10, anchor=CENTER)

        self.btn_update = Button(self.optie_frame, text="update csv", command=self.update_csv)
        self.btn_update.pack(padx=10, anchor=CENTER)
        
    def on_goedkeuring(self):
        self.moderatie.beoordeel_bericht(True)
        self.update_bericht_labels()
        pass

    def on_afkeuring(self):
        self.moderatie.beoordeel_bericht(False)
        self.update_bericht_labels()
        pass

    def update_bericht_labels(self):
        bericht_info = self.moderatie.geef_bericht()
        
        self.bericht["state"] = NORMAL

        if isinstance(bericht_info, str):
            self.naam["text"] = "naam: -"
            self.station["text"] = "station: -"
            self.tijd["text"] = "tijd: -"
            self.bericht.delete("1.0", END)
            self.bericht.insert(END, bericht_info)
            self.bericht["state"] = DISABLED
            return
        
        naam = bericht_info["naam"]
        tijd = bericht_info["tijd"]
        station = bericht_info["station"]
        bericht = bericht_info["bericht"]

        self.bericht.delete("1.0", END)
        self.bericht.insert(END, bericht)
        self.bericht["state"] = DISABLED

        self.naam["text"] = f"naam: {naam}" 
        self.station["text"] = f"station: {station}" 
        self.tijd["text"] = f"tijd: {tijd}" 

    def update_csv(self):
        self.moderatie.update_bestand()

    def show(self):
        self.root.mainloop()


def main():
    GUI = ModeratieGUI()
    GUI.show()
    # con = psycopg2.connect(
    #                 database="StationZuil", 
    #                 user="postgres",
    #                 password="pass",
    #                 host="localhost",
    #                 port="5433"
    #                 )

    # cursor = con.cursor()

    # cursor.execute("select * from station_service;")
    # print(cursor.fetchall())

    # if not con.closed:
    #     con.close()


if __name__ == "__main__":
    main()
