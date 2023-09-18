""" Module 2 Moderatie
Voordat een bericht ook daadwerkelijk op het stationshalscherm wordt gezet, wordt er door een moderator van de NS naar de berichten gekeken. De moderator kan een bericht goed- of afkeuren. Alleen goedgekeurde berichten worden gepubliceerd op het stationshalscherm van het desbetreffende station.

Deze module leest de berichten uit het gestructureerde tekstbestand (zoals beschreven bij module 1) in,
beginnend bij het oudste bericht.

Na beoordeling door een moderator wordt het hele bericht (inclusief datum, tijd, naam en station) naar een database geschreven.
Daarnaast wordt de volgende data toegevoegd:
- of het bericht is goedgekeurd of afgekeurd;
- de datum en tijd van beoordeling;
- de naam van moderator die het bericht heeft beoordeeld;
- het email-adres van de moderator.

Deze module werkt met een Command Line Interface (CLI).
"""

from datetime import datetime
import utils


# TODO: naar bestand?
BANNED_WORDS = [
    "sukkel"
]


class ModBeoordeling:
    def __init__(self, beoordeling: bool, tijd: str, mod_naam: str, email: str):
        self.beoordeling = beoordeling
        self.tijd = tijd
        self.mod_naam = mod_naam
        self.email = email


def check_bericht(bericht: str, naam: str, email: str):
    beoordeling = ModBeoordeling(
        False,
        utils.get_time_str("%d-%m-%y %H:%M"),
        naam,
        email
    )

    # naar kleine letters
    bericht.lower()

    for banned_word in BANNED_WORDS:
        if banned_word in bericht:
            return beoordeling

    beoordeling.beoordeling = True

    return beoordeling
