from tkinter import *
from stationinfo import *
from datetime import datetime

def scale_img_down(img: PhotoImage, factorx, factory):
    """Geeft een verkleinde PhotoImage terug met de gegeven factoren
    
    Args:
        img: image die wordt verkleint
        factorx: de breedte factor van de nieuwe image, moet kleiner zijn dan 1
        factory: de hoogte factor van de nieuwe image, moet kleiner zijn dan 1
    """
    assert factorx < 1 and factory < 1

    w = img.width()
    h = img.height()

    # nieuwe width en height
    scaledw = int(w * factorx)
    scaledh = int(h * factory)

    # de grootte van de stappen van de pixel iteraties (x,y) door de originele image
    stepx = int(w / scaledw)
    stepy = int(h / scaledh)

    # nog een lege verkleinde versie van de image
    new_img = PhotoImage(width=scaledw, height=scaledh)

    # vul de new_img met de dichtsbijzeinde pixels via de stepx en stepy
    for x in range(0, w, stepx):
        for y in range(0, h, stepy):
            rgb = img.get(x, y)

            # TODO: verander dit zodat dit niet naar hex color string hoeft, 
            # new_img.put rgb can't parse color "255"

            rgbstr = "#"
            for i in rgb:
                hexstr = hex(i)[2:]
                if len(hexstr) == 1:
                    hexstr = "0" + hexstr
                rgbstr += hexstr

            # vul de pixel met de kleur van de originele image
            new_img.put(rgbstr, (int(x * factorx), int(y * factory)))

    return new_img


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

    def update(self, bericht: StationBericht = None, dictstr=None, maak_leeg=False):
        """Update bericht inhoud
        
        Args:
            bericht: Het nieuwe bericht
            dictstr: Het nieuwe bericht maar dan via een dictionary
            maak_leeg: Leeg de widget inhoud
        """
        if maak_leeg:
            self.info["text"] = ""
            self.bericht["text"] = ""
            return

        if bericht == None:
            if dictstr == None:
                raise Exception("Bericht en dict argumenten kunnen niet leeg zijn")

            bericht = StationBericht(dictstr)

        self.info["text"] = f"{bericht.naam} op {bericht.datum} om {bericht.tijd}"
        self.bericht["text"] = f"“{bericht.text}”"


class StationshalUI:
    """Stationshalscherm UI en window"""

    def __init__(self):
        # root 
        self.root = Tk()
        self.root.title("Stationshalscherm")
        self.root.resizable(False, False)
        self.root.geometry("700x600")

        # root frames
        self.weer_info_frame = Frame(self.root)
        self.station_frame = Frame(self.root)
        self.station_label = Label(self.root, text=stationshalscherm_plek, font="Courier 20 normal")
        self.faciliteiten_frame = Frame(self.root)

        # klok
        self.klok_label = Label(self.root, text=datetime.now().strftime("%H:%M:%S"), font="Courier 20 normal")

        # image faciliteiten
        self.img_bike = PhotoImage(file="img_faciliteiten/img_ovfiets.png")
        self.img_lift = PhotoImage(file="img_faciliteiten/img_lift.png")
        self.img_toilet = PhotoImage(file="img_faciliteiten/img_toilet.png")
        self.img_pr = PhotoImage(file="img_faciliteiten/img_pr.png")

        # verklein 
        self.img_bike = scale_img_down(self.img_bike, 0.5, 0.5)
        self.img_lift = scale_img_down(self.img_lift, 0.5, 0.5)
        self.img_toilet = scale_img_down(self.img_toilet, 0.5, 0.5)
        self.img_pr = scale_img_down(self.img_pr, 0.5, 0.5)

        # sla de images op in widgets via Labels
        self.bike_widget = Label(self.faciliteiten_frame, image=self.img_bike)
        self.lift_widget = Label(self.faciliteiten_frame, image=self.img_lift)
        self.pr_widget = Label(self.faciliteiten_frame, image=self.img_pr)
        self.toilet_widget = Label(self.faciliteiten_frame, image=self.img_toilet)

        # weer label vars
        self.temperatuur = StringVar()
        self.weer_beschrijving = StringVar()
        self.regenmm = StringVar()
        self.windms = StringVar()

        # root layout
        self.station_label.pack(side=TOP)
        self.klok_label.pack(side=TOP)
        self.faciliteiten_frame.pack(anchor=CENTER, side=TOP, pady=10)
        self.weer_info_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)
        self.station_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=20, pady=20)

        # weer info frame
        self.temp_label = Label(self.weer_info_frame, textvariable=self.temperatuur, font="Courier 30 normal")
        self.bewolktheid_label = Label(self.weer_info_frame, textvariable=self.weer_beschrijving, font="Courier 20 normal")
        self.regen_label = Label(self.weer_info_frame, textvariable=self.regenmm, font="Courier 20 normal")
        self.wind_label = Label(self.weer_info_frame, textvariable=self.windms, font="Courier 20 normal")

        # layout
        self.temp_label.pack()
        self.bewolktheid_label.pack()
        self.regen_label.pack()
        self.wind_label.pack()

        # station frame
        self.bericht_labels = (
            StationBerichtWidget(self.station_frame),
            StationBerichtWidget(self.station_frame),
            StationBerichtWidget(self.station_frame),
            StationBerichtWidget(self.station_frame),
            StationBerichtWidget(self.station_frame),
        )

        # database connectie
        db.connect()

        # update inhoud van alle info widgets
        self.update_weer_labels()
        self.update_bericht_labels()
        self.update_faciliteiten()
        self.update_klok()

    def update_klok(self):
        self.klok_label["text"] = datetime.now().strftime("%H:%M:%S")
        self.klok_label.after(1000, self.update_klok)

    def update_weer_labels(self):
        """Update weer info van de station"""
        weer = get_station_weer_info()
        try:
            self.temperatuur.set(f"{round(weer['main']['temp'])}°C")
            self.weer_beschrijving.set(weer["weather"][0]["description"])
            if "rain" in weer.keys():
                self.regenmm.set(f"{round(weer['rain']['1h'], 1)}mm")
            if "wind" in weer.keys():
                self.windms.set(f"wind {round(weer['wind']['speed'], 1)}m/s")

        except KeyError as e:
            print(f"Error bij lezen van weer info: {e}")
            return

        # update elke minuut
        self.weer_info_frame.after(60000, self.update_weer_labels)

    def update_bericht_labels(self):
        """Update de labels met de nieuwste 5 berichten van de station"""
        rows = db.get_rows(""" 
                    select bericht.tekst, bericht.naam, bericht.datum, bericht.tijd, bericht.station from bericht
                    inner join beoordeling on bericht.beoordelingnr = beoordeling.beoordelingnr
                    where beoordeling.is_goedgekeurd = True
                    order by bericht.datum desc, bericht.tijd desc
                    limit 5
                    """
                           )

        for i, bericht in enumerate(self.bericht_labels):
            # check bij minder dan 5 berichten op station
            if i > len(rows) - 1:
                # heeft geen bericht
                bericht.update(maak_leeg=True)
                continue

            # vul de inhoud met het bericht
            row = rows[i]
            bericht = StationBericht(bericht=row[0], naam=row[1], datum=row[2], tijd=row[3].strftime("%H:%M"),
                                     station=row[4])
            self.bericht_labels[i].update(bericht)

    def update_faciliteiten(self):
        """Laat de beschikbare faciliteiten op het station zien, roep deze functie maar 1 keer in het begin op"""
        faciliteiten = get_station_faciliteiten()

        if faciliteiten["fiets"]:
            self.bike_widget.pack(side=TOP)
        if faciliteiten["lift"]:
            self.lift_widget.pack(side=LEFT)
        if faciliteiten["toilet"]:
            self.toilet_widget.pack(side=LEFT)
        if faciliteiten["pr"]:
            self.pr_widget.pack(side=LEFT)

    def show(self):
        self.root.mainloop()


def main():
    stationshal = StationshalUI()
    stationshal.show()


if __name__ == "__main__":
    main()
