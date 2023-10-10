"""Module 1: Zuil
Op een zuil op een willekeurig NS-station kunnen reizigers hun bericht van maximaal 140 karakters invoeren.
Het bericht moet worden opgeslagen in een tekstbestand met een logische structuur.
Sla de onderstaande gegevens op in een gestructureerd tekstbestand:

het bericht;
de datum en tijd van het bericht;
de naam van de reiziger – als de reiziger geen naam invult, gebruik dan als naam ‘anoniem’;
het station – deze locatie van de zuil mag in de module zelf worden vastgelegd op basis van een random choice van drie stations. De computer (jouw python computer programma) kiest dan één station uit een lijst Download lijstvan minimaal drie stations en dat station wordt dan gekoppeld aan de berichten.
"""

import random
import csv
from datetime import datetime
from tkinter import *

# constanten
MAX_BERICHT_LENGTE = 140        # de maximale lengte van een bericht
BESTAND_NAAM = "berichten.csv"  # waar de berichten worden opgeslagen

CSV_BESTAND_VELDEN = ["naam", "bericht", "station", "tijd"] 

GREEN = "#0F0"
RED = "#F00"
BLUE = "#00F"
WHITE = "#FFF"
GRAY = "#999"

class ZuilGUI():
    def __init__(self, naam_window: str = "zuil"):
        self.root = Tk()
        self.root.title(naam_window)
        self.root.resizable(False, False)
        
        self.invoer_frame = Frame(self.root, height=300, width=450)
        self.invoer_frame.grid_propagate(False)
        self.invoer_frame.pack()

        self.invoer_naam_label = Label(self.invoer_frame, text="naam")
        self.invoer_naam_label.place(relx=0.2, rely=0.12, width=350, anchor=CENTER)

        self.invoer_naam = Entry(self.invoer_frame)
        self.invoer_naam.place(relx=0.5, rely=0.2, width=350, anchor=CENTER)

        self.invoer_bericht_label = Label(self.invoer_frame, text="bericht")
        self.invoer_bericht_label.place(relx=0.2, rely=0.31, width=350, anchor=CENTER)

        self.invoer_bericht = Text(self.invoer_frame, highlightthickness=1, borderwidth=1)
        self.invoer_bericht.place(relx=0.5, rely=0.6, height=150, width=350, anchor=CENTER)
        self.invoer_bericht.bind("<KeyRelease>", self.check_bericht_limiet)
        
        self.invoer_limiet_label = Label(self.invoer_frame, wraplength=350, fg=GRAY,text=f"0/{MAX_BERICHT_LENGTE}")
        self.invoer_limiet_label.place(relx=0.8, rely=0.9, anchor=CENTER)

        self.btn_verstuur = Button(self.invoer_frame, text="verstuur", command=self.on_button_press)
        self.btn_verstuur.place(relx=0.5, rely=0.9, height=20, width=80, anchor=CENTER)

    def check_bericht_limiet(self, event):
        """"""
        invoer_len = len(self.invoer_bericht.get("1.0", "end-1c"))
        self.invoer_limiet_label.configure(text=f"{invoer_len}/{MAX_BERICHT_LENGTE}")
        if invoer_len > MAX_BERICHT_LENGTE:
            self.invoer_limiet_label.configure(text=f"limiet bereikt {invoer_len}/{MAX_BERICHT_LENGTE}")
            self.invoer_limiet_label.configure(fg=RED)
            self.invoer_bericht.configure(highlightcolor=RED)
            self.btn_verstuur["state"] = DISABLED
        else:
            self.invoer_limiet_label.configure(fg=GRAY)
            self.invoer_bericht.configure(highlightcolor=WHITE)
            self.btn_verstuur["state"] = NORMAL


    def on_button_press(self):
        naam = self.invoer_naam.get()
        bericht = self.invoer_bericht.get("1.0", "end-1c")
        station = get_random_station()
        tijd = get_time_str("%d-%m-%y %H:%M")

        if len(naam) == 0:
            naam = "anoniem"

        opgeslagen_bericht =  {"naam": naam, "bericht": bericht, "tijd": tijd, "station": station}

        sla_bericht_op(opgeslagen_bericht)

        # laat bericht zien dat het bericht is opgeslagen

    def show(self):
        self.root.mainloop()


def get_random_station():
    """Pakt een willekeurige station uit stations.txt

    Returns:
        De station naam als string.
    """
    with open("stations.txt", 'r') as f:
        return random.choice(f.readlines()).strip()


def vraag_bericht():
    """Vraagt de gebruiker om een bericht en naam via de CLI.

    Returns:
        Een string met het bericht, naam en datum in een mooi formaat.
    """
    bericht = input(f"je bericht: (max {MAX_BERICHT_LENGTE} letters) ")

    # Bericht mag de lengte limiet niet overschrijden
    while len(bericht) > MAX_BERICHT_LENGTE:
        bericht = input("je bericht: (max 140 letters) ")

    naam = input("wat is je naam: (niks invullen is 'anoniem') ")

    # Er was niks ingevuld
    if not naam:
        naam = "anoniem"

    # Pak een willekeurig station uit de lijst
    station = get_random_station()

    # De tijd als string
    time_str = get_time_str("%d-%m-%y %H:%M")

    # return {"naam": naam, "bericht": bericht, "tijd": time_str, "station": station}
    return (
        f"'{bericht}'\n" 
        f"-{naam} op {time_str} van {station}"
    )


def sla_bericht_op(bericht: dict):
    """"Slaat het bericht op in het bestand via append.
    
    """
    with open(BESTAND_NAAM, newline='', mode="a+") as f:
        writer = csv.DictWriter(f, CSV_BESTAND_VELDEN)
        writer.writerow(bericht)
    # with open(BESTAND_NAAM, "a+") as f:
        # f.write(bericht)


def get_time_str(frmt: str):
    """ Geeft de tijd als string terug met de gegeven tijd formaat. """
    return datetime.now().strftime(frmt)


def main():
    GUI = ZuilGUI()
    GUI.show()

if __name__ == "__main__":
    main()