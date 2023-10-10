import zuil
from tkinter import *

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
        
        self.invoer_limiet_label = Label(self.invoer_frame, wraplength=350, fg=GRAY,text=f"0/{zuil.MAX_BERICHT_LENGTE}")
        self.invoer_limiet_label.place(relx=0.8, rely=0.9, anchor=CENTER)

        self.btn_verstuur = Button(self.invoer_frame, text="verstuur", command=self.on_button_press)
        self.btn_verstuur.place(relx=0.5, rely=0.9, height=20, width=80, anchor=CENTER)

    def check_bericht_limiet(self, event):
        """"""
        invoer_len = len(self.invoer_bericht.get("1.0", "end-1c"))
        self.invoer_limiet_label.configure(text=f"{invoer_len}/{zuil.MAX_BERICHT_LENGTE}")
        if invoer_len > zuil.MAX_BERICHT_LENGTE:
            self.invoer_limiet_label.configure(text=f"limiet bereikt {invoer_len}/{zuil.MAX_BERICHT_LENGTE}")
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
        station = zuil.get_random_station()
        tijd = zuil.get_time_str("%d-%m-%y %H:%M")

        if len(naam) == 0:
            naam = "anoniem"

        opgeslagen_bericht =  {"naam": naam, "bericht": bericht, "tijd": tijd, "station": station}

        zuil.sla_bericht_op(opgeslagen_bericht)

        # laat bericht zien dat het bericht is opgeslagen

    def show(self):
        self.root.mainloop()

def main():
    GUI = ZuilGUI()
    GUI.show()

if __name__ == "__main__":
    main()