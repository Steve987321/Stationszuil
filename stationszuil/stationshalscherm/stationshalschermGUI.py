from tkinter import *
from stationinfo import *
from datetime import datetime

# ns kleuren voor scherm
NS_GEEL = "#FEC917"
NS_BLAUW = "#03307b"


def verklein_image(img: PhotoImage, factorx, factory):
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
        self.berichten_frame = Frame(root, bg=NS_GEEL)
        self.naam = Label(self.berichten_frame, fg=NS_BLAUW, bg=NS_GEEL)
        self.bericht = Label(self.berichten_frame, font="Arial 15 italic",  fg=NS_BLAUW, bg=NS_GEEL)
        self.berichten_frame.pack(pady=10)

    def update(self, bericht: StationBericht = None, dictstr=None, maak_leeg=False):
        """Update bericht inhoud
        
        Args:
            bericht: Het nieuwe bericht
            dictstr: Het nieuwe bericht maar dan via een dictionary
            maak_leeg: Leeg de widget inhoud
        """
        if maak_leeg:
            self.bericht["text"] = ""
            return

        if bericht == None:
            if dictstr == None:
                raise Exception("Bericht en dict argumenten kunnen niet leeg zijn")

            bericht = StationBericht(dictstr)

        self.naam["text"] = f"{bericht.naam} op {bericht.station}"
        self.bericht["text"] = f"“{bericht.text}”"

        self.naam.pack()
        self.bericht.pack()

        # spacing
        Label(self.root, text="", bg=NS_GEEL).pack()


class StationshalUI:
    """Stationshalscherm UI en window"""

    def __init__(self):
        self.img_weer_icon = None

        # root 
        self.root = Tk()
        self.root.title("Stationshalscherm")
        self.root.resizable(False, False)
        self.root.geometry("700x600")
        self.root["background"] = NS_GEEL

        # root frames
        self.weer_info_frame = Frame(self.root, bg=NS_GEEL)
        self.bericht_frame = Frame(self.root, bg=NS_GEEL)
        self.faciliteiten_frame = Frame(self.root, bg=NS_GEEL)

        # klok
        self.klok_label = Label(self.root, text=datetime.now().strftime("%H:%M:%S"), font="Courier 25 normal",
                                fg=NS_BLAUW, bg=NS_GEEL)

        # image faciliteiten
        self.img_bike = PhotoImage(file="img_faciliteiten/img_ovfiets.png")
        self.img_lift = PhotoImage(file="img_faciliteiten/img_lift.png")
        self.img_toilet = PhotoImage(file="img_faciliteiten/img_toilet.png")
        self.img_pr = PhotoImage(file="img_faciliteiten/img_pr.png")

        # verklein 
        self.img_bike = verklein_image(self.img_bike, 0.7, 0.7)
        self.img_lift = verklein_image(self.img_lift, 0.7, 0.7)
        self.img_toilet = verklein_image(self.img_toilet, 0.7, 0.7)
        self.img_pr = verklein_image(self.img_pr, 0.7, 0.7)

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
        self.klok_label.pack(side=TOP)
        self.faciliteiten_frame.pack(anchor=CENTER, side=TOP, pady=25)
        self.weer_info_frame.pack(side=LEFT, fill=BOTH, padx=80, pady=20)
        self.bericht_frame.pack(side=RIGHT, fill=BOTH, padx=80, pady=20)

        # weer info frame
        self.weer_icon = Label(self.weer_info_frame, fg=NS_BLAUW, bg=NS_GEEL)
        self.station_label = Label(self.weer_info_frame, text=stationshalscherm_plek, font="Arial 25 normal",
                                   fg=NS_BLAUW, bg=NS_GEEL)
        self.temp_label = Label(self.weer_info_frame, textvariable=self.temperatuur, font="Arial 35 normal",
                                fg=NS_BLAUW, bg=NS_GEEL)
        self.weer_label = Label(self.weer_info_frame, text="", font="Arial 20 normal",
                                fg=NS_BLAUW, bg=NS_GEEL)

        # layout
        self.weer_icon.pack()
        self.station_label.pack()
        self.temp_label.pack()
        self.weer_label.pack()

        # station frame
        self.bericht_labels = (
            StationBerichtWidget(self.bericht_frame),
            StationBerichtWidget(self.bericht_frame),
            StationBerichtWidget(self.bericht_frame),
            StationBerichtWidget(self.bericht_frame),
            StationBerichtWidget(self.bericht_frame),
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

            rain1h = ""
            windms = ""

            if "rain" in weer.keys():
                rain1h = f"{round(weer['rain']['1h'], 1)}mm "
            if "wind" in weer.keys():
                windms = f"wind {round(weer['wind']['speed'], 1)}m/s \n"

            self.weer_label["text"] = (f"{weer['weather'][0]['description']} {rain1h}\n"
                                       f"{windms}")

            # update icoon
            r = requests.get(f"https://openweathermap.org/img/wn/{weer['weather'][0]['icon']}@2x.png")
            if not r.ok:
                print(f"Er is iets fout gegaan met het ophalen van het weer icoon: {r.status_code}")
                return

            self.img_weer_icon = PhotoImage(data=r.content)
            self.weer_icon["image"] = self.img_weer_icon

        except KeyError as e:
            print(f"Error bij lezen van weer info: {e}")
            return

        # update weer info elke 1 uur
        self.weer_label.after(60000, self.update_weer_labels)

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
        faciliteiten = get_station_faciliteiten(stationshalscherm_plek)

        if faciliteiten["fiets"]:
            self.bike_widget.pack(side=LEFT)
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
