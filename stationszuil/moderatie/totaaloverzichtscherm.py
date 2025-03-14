from tkinter import *
from tkinter import messagebox
from stationszuil import database

# voor Tkinter widgets
GREEN = "#0F0"
RED = "#F00"
BLUE = "#00F"
WHITE = "#FFF"
GRAY = "#999"


def clamp(n, a, b):
    """klem n tussen a en b

    Returns:
        n dat is beperkt tussen a en b
    """
    if n > b:
        return b
    elif n < a:
        return a
    else:
        return n


class BerichtPreviewWidget(LabelFrame):
    """Bericht widget frame

    Laat belangrijke info zien van het bericht, kan ook alles tonen door op inspecteer te drukken
    """

    # geeft aan of er een bericht wordt geïnspecteerd
    is_inspecteren = False

    def __init__(self, root: Misc, group, bericht, naam, station, datum, tijd, goedgekeurd, email):
        super().__init__(group, text="", width=150, height=100)

        self.root = root

        # verkort het bericht als nodig is zodat het past in de widget (max. 1 lijn van 20 letters)
        posnline = bericht.find('\n')

        if posnline != -1 and posnline <= 20:
            # verkort tot \n bij < 20
            bericht_verkort = bericht[0:clamp(posnline, 0, 15)] + ".."
            self.bericht_label = Label(self, text=bericht_verkort)
        elif len(bericht) > 20:
            # geen \n maar bericht is langer dan 20
            bericht_verkort = bericht[0:15] + ".."
            self.bericht_label = Label(self, text=bericht_verkort)
        else:
            # bericht is al klein genoeg
            self.bericht_label = Label(self, text=bericht)

        # gekleurde beoordeling status tekst
        if goedgekeurd:
            self.goedgekeurd_label = Label(self, text="Goedgekeurd", fg=GREEN)
        else:
            self.goedgekeurd_label = Label(self, text="Afgekeurd", fg=RED)

        self.naam_label = Label(self, text=naam)
        self.btn_inspecteer = Button(self, text="inspecteer", command=self.on_inspecteer)

        self.naam_label.pack()
        self.bericht_label.pack()
        self.goedgekeurd_label.pack()
        self.btn_inspecteer.pack()

        # inspecteer bericht frame
        self.full_preview_frame = LabelFrame(root, text="inspecteer bericht", width=300, height=300)
        self.full_preview_frame.pack_propagate(False)

        self.btn_sluit = Button(self.full_preview_frame, text="X", command=self.on_sluit_inspecteer)
        self.naam_label_full = Label(self.full_preview_frame, text=f"naam: {naam}")
        self.station_label_full = Label(self.full_preview_frame, text=f"station: {station}")
        self.tijd_label_full = Label(self.full_preview_frame, text=f"datum: {datum}")
        self.datum_label_full = Label(self.full_preview_frame, text=f"tijd: {tijd}")
        self.datum_label_full = Label(self.full_preview_frame, text=f"beoordeeld door: {email}")
        self.bericht_full = Text(self.full_preview_frame)
        self.bericht_full.insert(END, bericht)
        self.bericht_full["state"] = DISABLED

        self.btn_sluit.pack()
        self.naam_label_full.pack()
        self.station_label_full.pack()
        self.tijd_label_full.pack()
        self.datum_label_full.pack()
        self.bericht_full.pack()

    def on_inspecteer(self):
        """Laat de inspecteer frame zien, bovenop andere alle preview frames"""
        if BerichtPreviewWidget.is_inspecteren:
            return

        for widget in self.root.winfo_children():
            try:
                widget["state"] = DISABLED
            except:  # kan niet worden disabled, dit kan worden negeert
                pass

        BerichtPreviewWidget.is_inspecteren = True

        self.full_preview_frame.place(anchor=CENTER, relx=0.5, rely=0.5)

    def on_sluit_inspecteer(self):
        """Sluit inspecteer frame"""
        BerichtPreviewWidget.is_inspecteren = False
        self.full_preview_frame.place_forget()


class TotaalOverzichtScherm:
    """Laat een totaal overzicht zien van alle beoordeelde berichten"""
    def __init__(self, db: database.StationsZuilDB = None):
        # houd de pagina's en daarvan de pagina inhoud
        self.paginas = []

        # layout is in rijen met elk 3 berichten (Frame met 3 Frames)
        # max 5 rijen in 600 hoogte
        self.db_bericht_group_frame = []

        # geselecteerde pagina
        self.pagina = 0

        # database connectie

        if db == None:
            self.db = database.StationsZuilDB()
            connectie_resultaat = self.db.connect()

            while connectie_resultaat == False:
                # geef een messagebox scherm als er iets fout gaat met het verbinden

                try_again = messagebox.askretrycancel(
                    "Database",
                    f"Er kon geen verbinding worden gemaakt met de database: {self.db.error_str}")
                if try_again:
                    connectie_resultaat = self.db.connect()
                else:
                    self.root = None
                    return
        else:
            self.db = db

        db_berichten = self.db.get_rows("""
        select bericht.tekst, bericht.naam, bericht.station, bericht.datum, bericht.tijd, beoordeling.is_goedgekeurd, beoordeling.moderator_email from bericht
        inner join beoordeling on bericht.beoordelingnr = beoordeling.beoordelingnr
        """)

        # groepeer de berichten in groepen van 15
        if len(db_berichten) > 15:
            for _ in range(0, len(db_berichten), 15):
                self.paginas.append(db_berichten[:15])
                db_berichten = db_berichten[15:]

        # als het niet precies uit komt vul een laatste pagina met de overige berichten
        if len(db_berichten) > 0:
            self.paginas.append([])
            laatste_index = len(self.paginas) - 1
            for bericht in db_berichten:
                self.paginas[laatste_index].append(bericht)

        self.root = Toplevel()
        self.root.title("Totaal Overzicht")
        self.root.resizable(False, False)
        self.root.geometry("500x600")

        navigatie_frame = Frame(self.root)

        self.pagina_label = Label(navigatie_frame, text=f"{self.pagina + 1}/{len(self.paginas)}")
        self.btn_pagina_rechts = Button(navigatie_frame, text=">", command=self.pagina_rechts)
        self.btn_pagina_links = Button(navigatie_frame, text="<", command=self.pagina_links)
        self.db_berichten_frame = Frame(self.root)

        self.toon_pagina(0)

        # layout
        self.db_berichten_frame.pack()

        navigatie_frame.pack(side=BOTTOM)
        self.btn_pagina_links.pack(side=LEFT)
        self.btn_pagina_links["state"] = DISABLED
        self.pagina_label.pack(side=LEFT)
        self.btn_pagina_rechts.pack(side=LEFT)

    def is_open(self):
        """Geeft aan of scherm bestaat"""
        return self.root.winfo_exists()

    def pagina_rechts(self):
        """Ga naar volgende pagina"""
        self.btn_pagina_links["state"] = NORMAL
        self.btn_pagina_rechts["state"] = NORMAL

        self.pagina += 1
        self.toon_pagina(self.pagina)
        self.pagina_label["text"] = f"{self.pagina + 1}/{len(self.paginas)}"

        if self.pagina == len(self.paginas) - 1:
            self.btn_pagina_rechts["state"] = DISABLED

    def pagina_links(self):
        """Ga naar vorige pagina"""
        self.btn_pagina_rechts["state"] = NORMAL
        self.btn_pagina_links["state"] = NORMAL

        self.pagina -= 1
        self.toon_pagina(self.pagina)
        self.pagina_label["text"] = f"{self.pagina + 1}/{len(self.paginas)}"

        if self.pagina == 0:
            self.btn_pagina_links["state"] = DISABLED

    def toon_pagina(self, pagina_index):
        """Toont de pagina met berichten

        Args:
            pagina_index: index van pagina vanaf 0, wordt geklemt
        """
        if len(self.paginas) == 0:
            messagebox.showinfo("Totaal Overzicht",
                                "Er zijn geen beoordelingen om te tonen")
            return

        pagina_index = clamp(pagina_index, 0, len(self.paginas) - 1)

        cur_frame = None

        # verwijder vorige
        for frame in self.db_bericht_group_frame:
            for child_frame in frame.winfo_children():
                child_frame.pack_forget()
                child_frame.destroy()
            frame.pack_forget()
            frame.destroy()

        self.db_bericht_group_frame.clear()

        for frame in self.db_berichten_frame.winfo_children():
            frame.pack_forget()
            frame.destroy()

        for i, bericht in enumerate(self.paginas[pagina_index]):
            if i % 3 == 0:
                cur_frame = Frame(self.db_berichten_frame)
                self.db_bericht_group_frame.append(cur_frame)

            bericht_frame = BerichtPreviewWidget(self.root,
                                                 cur_frame,
                                                 bericht=bericht[0],
                                                 naam=bericht[1],
                                                 station=bericht[2],
                                                 datum=bericht[3],
                                                 tijd=bericht[4],
                                                 goedgekeurd=bericht[5],
                                                 email=bericht[6])

            bericht_frame.pack_propagate(False)
            bericht_frame.pack(side=LEFT, padx=2, pady=5)

        for frame in self.db_bericht_group_frame:
            frame.pack(side=TOP)
