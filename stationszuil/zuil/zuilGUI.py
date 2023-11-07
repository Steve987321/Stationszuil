import zuil
from datetime import datetime
from tkinter import *
from tkinter import messagebox

# voor Tkinter widgets
GREEN = "#0F0"
RED = "#F00"
BLUE = "#00F"
WHITE = "#FFF"
GRAY = "#999"
BLACK = "#000"


class ZuilGUI:
    """Zuil window en UI om berichten te plaatsen op een random station"""
    def __init__(self, naam_window: str = "zuil"):
        # Window
        self.root = Tk()
        self.root.title(naam_window)
        self.root.resizable(False, False)
        
        # Frame
        self.invoer_frame = Frame(self.root, height=300, width=450)

        # Invoer frame widgets
        self.invoer_naam_label = Label(self.invoer_frame, text="naam")
        self.invoer_naam = Entry(self.invoer_frame)
        self.invoer_bericht_label = Label(self.invoer_frame, text="bericht")
        self.invoer_bericht = Text(self.invoer_frame, highlightthickness=1, borderwidth=1)
        self.invoer_limiet_label = Label(self.invoer_frame, wraplength=350, fg=GRAY, text=f"0/{zuil.MAX_BERICHT_LENGTE}")
        self.btn_verstuur = Button(self.invoer_frame, text="verstuur", command=self.verstuur_bericht)

        # Widget props en layout
        self.invoer_naam_label.place(relx=0.2, rely=0.12, width=350, anchor=CENTER)
        self.invoer_naam.place(relx=0.5, rely=0.2, width=350, anchor=CENTER)
        self.invoer_bericht_label.place(relx=0.2, rely=0.31, width=350, anchor=CENTER)
        self.invoer_bericht.place(relx=0.5, rely=0.6, height=150, width=350, anchor=CENTER)
        self.btn_verstuur.place(relx=0.5, rely=0.9, height=20, width=80, anchor=CENTER)
        self.invoer_limiet_label.place(relx=0.8, rely=0.9, anchor=CENTER)

        self.invoer_naam.bind("<FocusIn>", self.on_naam_focus_in)
        self.invoer_naam.bind("<FocusOut>", self.on_naam_focus_out)
        self.invoer_naam.insert(0, "anoniem")
        self.invoer_naam.config(fg=GRAY)

        self.invoer_bericht.bind("<KeyRelease>", self.check_bericht_limiet)

        self.invoer_frame.grid_propagate(False)
        self.invoer_frame.pack()

    def on_naam_focus_in(self, _):
        """Naam input on focus event
        
        Verander de invoer naam naar anoniem bij geen gebruiker invoer.
        """
        if self.invoer_naam.get() == "anoniem" and self.invoer_naam.cget("fg") == GRAY:
            self.invoer_naam.delete(0, END)
            self.invoer_naam.config(fg=WHITE)

    def on_naam_focus_out(self, _):
        """Naam input out of focus event
        
        Verander de invoer naam naar anoniem bij geen gebruiker invoer.
        """
        if len(self.invoer_naam.get()) == 0:
            self.invoer_naam.insert(0, "anoniem")
            self.invoer_naam.config(fg=GRAY)

    def check_bericht_limiet(self, _):
        """Bericht input on key release event
        
        Laat weten dat de gebruiker dat er meer dan 140 karakters in het bericht zitten wat niet kan.
        Disable ook vestuur button. 
        """
        # update bericht lengte widget
        invoer_len = len(self.invoer_bericht.get("1.0", "end-1c"))
        self.invoer_limiet_label.configure(text=f"{invoer_len}/{zuil.MAX_BERICHT_LENGTE}")

        # check of het letter limiet is bereikt
        if invoer_len > zuil.MAX_BERICHT_LENGTE:
            self.invoer_limiet_label.configure(text=f"limiet bereikt {invoer_len}/{zuil.MAX_BERICHT_LENGTE}")
            self.invoer_limiet_label.configure(fg=RED)
            self.invoer_bericht.configure(highlightcolor=RED)
            self.btn_verstuur["state"] = DISABLED
        else:
            self.invoer_limiet_label.configure(fg=GRAY)
            self.invoer_bericht.configure(highlightcolor=WHITE)
            self.btn_verstuur["state"] = NORMAL

    def verstuur_bericht(self):
        """Verstuur button press event
        
        Verstuur het bericht naar het csv bestand en laat bericht zien
        """
        # pak info van de widgets
        naam = self.invoer_naam.get()
        bericht = self.invoer_bericht.get("1.0", "end-1c")

        if len(bericht.strip(naam)) <= 1:
            messagebox.showinfo("Bericht kon niet worden verstuurd", "Naam is te klein")
            return

        if len(bericht.strip()) <= 1:
            messagebox.showinfo("Bericht kon niet worden verstuurd", "Het bericht is te klein")
            return

        station = zuil.get_random_station()
        tijd = datetime.now().time()
        datum = datetime.now().date()

        opgeslagen_bericht = {"naam": naam, "bericht": bericht, "tijd": tijd, "station": station, "datum": datum}

        zuil.sla_bericht_op(opgeslagen_bericht)

        # leeg invulvelden
        self.invoer_naam.delete(0, END)
        self.invoer_naam.insert(0, "anoniem")
        self.invoer_naam.config(fg=GRAY)

        self.invoer_bericht.delete("1.0", END)

        self.invoer_limiet_label["text"] = f"0/{zuil.MAX_BERICHT_LENGTE}"

        messagebox.showinfo("Verstuurd", "Het bericht is verstuurd en in afwachting tot beoordeling.")

    def show(self):
        self.root.mainloop()


def main():
    gui = ZuilGUI()
    gui.show()


if __name__ == "__main__":
    main()