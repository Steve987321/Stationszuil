"""Module 1: Zuil
Op een zuil op een willekeurig NS-station kunnen reizigers hun bericht van maximaal 140 karakters invoeren.
Het bericht moet worden opgeslagen in een tekstbestand met een logische structuur.
Sla de onderstaande gegevens op in een gestructureerd tekstbestand:

het bericht;
de datum en tijd van het bericht;
de naam van de reiziger – als de reiziger geen naam invult, gebruik dan als naam ‘anoniem’;
het station – deze locatie van de zuil mag in de module zelf worden vastgelegd op basis van een random choice van drie stations. De computer (jouw python computer programma) kiest dan één station uit een lijst Download lijstvan minimaal drie stations en dat station wordt dan gekoppeld aan de berichten.
Deze module werkt met een Command Line Interface (CLI).
"""

import utils
import random

# constanten
MAX_BERICHT_LENGTE = 140        # de maximale lengte van een bericht
BESTAND_NAAM = "berichten.txt"  # waar de berichten worden opgeslagen


def get_random_station():
    """Pakt een willekeurige station uit stations.txt

    Returns:
        De station naam als string.
    """
    with open("stations.txt", 'r') as f:
        return random.choice(f.readlines())


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
    time_str = utils.get_time_str("%d-%m-%y %H:%M")

    return (
        f"'{bericht}'\n" 
        f"-{naam} op {time_str} van {station}"
    )


def sla_bericht_op(bericht: str):
    """"Slaat het bericht op in het bestand via append."""
    with open(BESTAND_NAAM, "a+") as f:
        f.write(bericht)
