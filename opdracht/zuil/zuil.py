"""Module 1: Zuil
Op een zuil op een willekeurig NS-station kunnen reizigers hun bericht van maximaal 140 karakters invoeren.
Het bericht moet worden opgeslagen in een tekstbestand met een logische structuur.
Sla de onderstaande gegevens op in een gestructureerd tekstbestand:

het bericht;
de datum en tijd van het bericht;
de naam van de reiziger – als de reiziger geen naam invult, gebruik dan als naam ‘anoniem’;
het station – deze locatie van de zuil mag in de module zelf worden vastgelegd op basis van een random choice van drie stations.
De computer (jouw python computer programma) kiest dan één station uit een lijst Download lijstvan minimaal drie stations en dat station wordt dan gekoppeld aan de berichten.
"""

import random
import csv

# constanten
MAX_BERICHT_LENGTE = 140        # de maximale lengte van een bericht
BESTAND_NAAM = "berichten.csv"  # waar de berichten worden opgeslagen

CSV_BESTAND_VELDEN = ["naam", "bericht", "station", "tijd", "datum"] 


def get_random_station():
    """Pakt een willekeurige station uit stations.txt

    Returns:
        De station naam als string.
    """
    with open("stations.txt", 'r') as f:
        return random.choice(f.readlines()).strip()
    

def sla_bericht_op(bericht: dict):
    """"Slaat het bericht op in het bestand via append."""
    with open(BESTAND_NAAM, newline='', mode="a+") as f:
        writer = csv.DictWriter(f, CSV_BESTAND_VELDEN)

        # check of het nog geen csv header heeft en dus leeg is
        if f.tell() == 0:
            writer.writeheader()

        writer.writerow(bericht)
        