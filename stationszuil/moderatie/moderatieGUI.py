from modereer import *
from tkinter import *
from tkinter import messagebox
from totaaloverzichtscherm import TotaalOverzichtScherm

# voor Tkinter widgets
GREEN = "#0F0"
RED = "#F00"
BLUE = "#00F"
WHITE = "#FFF"
GRAY = "#999"


class ModeratieGUI:
    """Moderatie window en UI voor beoordelen van berichten"""

    def __init__(self, naam_window: str = "moderatie"):
        self.moderatie = Modereer("../../berichten.csv")
        self.overzicht_scherm = None

        connectie_resultaat = self.moderatie.connect()

        while connectie_resultaat == False:
            try_again = messagebox.askretrycancel(
                "Database",
                f"Er kon geen connectie worden gemaakt met de database: {self.moderatie.error_str}")
            if try_again:
                connectie_resultaat = self.moderatie.connect()
            else:
                self.root = None
                return

        # window
        self.root = Tk()
        self.root.title(naam_window)
        self.root.resizable(False, False)
        self.root.geometry("500x500")

        # moderatie scherm
        self.info_frame = LabelFrame(self.root, height=300, width=450, text="bericht")
        self.naam = Label(self.info_frame)
        self.station = Label(self.info_frame)
        self.tijd = Label(self.info_frame)
        self.bericht = Text(self.info_frame, height=10)
        self.bericht["state"] = DISABLED

        # moderatie 
        self.moderatie_frame = LabelFrame(self.root, height=200, width=450, text="moderatie")
        self.btn_goedkeuren = Button(self.moderatie_frame, text="goedkeuren", command=self.on_goedkeuring)
        self.btn_afkeuren = Button(self.moderatie_frame, text="afkeuren", command=self.on_afkeuring)
        self.btn_update = Button(self.moderatie_frame, text="update csv", command=self.on_update_csv)
        self.btn_overzicht = Button(self.moderatie_frame, text="toon overzicht", command=self.on_toon_overzicht)

        # login scherm 
        self.login_frame = LabelFrame(self.root, text="login", height=400, width=300)
        self.login_email_label = Label(self.login_frame, text="email")
        self.login_wachtwoord_label = Label(self.login_frame, text="wachtwoord")
        self.login_email = Entry(self.login_frame)
        self.login_wachtwoord = Entry(self.login_frame, show='*')
        self.btn_login = Button(self.login_frame, text="login", command=self.on_login)
        self.foutmelding_label = Label(self.login_frame, foreground=RED)

        self.toon_login()

    def toon_login(self):
        """Laat de login widgets zien"""
        # verberg moderatie scherm
        self.info_frame.pack_forget()

        self.login_frame.pack_propagate(False)
        self.login_frame.pack()

        # widgets
        self.login_email_label.pack()
        self.login_email.pack()
        self.login_wachtwoord_label.pack()
        self.login_wachtwoord.pack()
        Label(self.login_frame, text="").pack()  # spacing
        self.btn_login.pack()
        self.foutmelding_label.pack()

    def toon_moderatie(self):
        """Laat de moderatie widgets zien"""
        # verberg login scherm 
        self.login_frame.pack_forget()

        self.info_frame.pack_propagate(False)
        self.info_frame.pack(padx=20, pady=10)
        self.bericht.pack(padx=20, pady=10, side=BOTTOM, anchor=CENTER)
        self.naam.pack(padx=50, pady=2, side=TOP, anchor=CENTER)
        self.station.pack(padx=50, pady=2, side=TOP, anchor=CENTER)
        self.tijd.pack(padx=50, pady=2, side=TOP, anchor=CENTER)

        self.moderatie_frame.pack_propagate(False)
        self.moderatie_frame.pack(pady=10)
        self.btn_goedkeuren.pack(padx=10, anchor=CENTER)
        self.btn_afkeuren.pack(padx=10, anchor=CENTER)
        self.btn_update.pack(padx=10, anchor=CENTER)
        self.btn_overzicht.pack()

    def on_login(self):
        """Login knop press, probeer in te loggen"""
        if self.moderatie.login(self.login_email.get(), self.login_wachtwoord.get()):
            self.toon_moderatie()
            self.update_bericht_labels()
        else:
            self.foutmelding_label["text"] = "Fout wachtwoord of email adress."

    def on_goedkeuring(self):
        """Goedgekeeurd bericht knop press"""
        self.moderatie.beoordeel_bericht(True)
        self.update_bericht_labels()
        pass

    def on_afkeuring(self):
        """Afgekeurd bericht knop press"""
        self.moderatie.beoordeel_bericht(False)
        self.update_bericht_labels()
        pass

    def on_toon_overzicht(self):
        """Laat het overzicht scherm zien in een aparte window"""
        if self.overzicht_scherm != None:
            if self.overzicht_scherm.is_open():
                return

        self.overzicht_scherm = TotaalOverzichtScherm(self.moderatie.db)

    def update_bericht_labels(self):
        """Update csv bestand knop press"""
        bericht_info = self.moderatie.geef_bericht()

        # zodat we de widget kunnen aanpassen
        self.bericht["state"] = NORMAL

        # geeft een string als er geen berichten meer zijn om te beoordelen
        if isinstance(bericht_info, str):
            self.naam["text"] = "naam: -"
            self.station["text"] = "station: -"
            self.tijd["text"] = "tijd: -"
            self.bericht.delete("1.0", END)
            self.bericht.insert(END, bericht_info)
            self.bericht["state"] = DISABLED

            # zet beoordeel knoppen uit als er geen berichten zijn om te beoordelen
            self.btn_afkeuren["state"] = DISABLED
            self.btn_goedkeuren["state"] = DISABLED

            return

        # update widgets met het nieuwe bericht
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

        # zet beoordeel knoppen uit als er geen berichten zijn om te beoordelen
        self.btn_afkeuren["state"] = NORMAL
        self.btn_goedkeuren["state"] = NORMAL

    def on_update_csv(self):
        self.moderatie.update_bestand()

    def show(self):
        # check of de database connectie fout ging
        if self.root == None:
            return

        self.root.mainloop()


def main():
    gui = ModeratieGUI()
    gui.show()

    # bij afsluiten update en disconnect van database
    gui.on_update_csv()
    gui.moderatie.disconnect()


if __name__ == "__main__":
    main()
