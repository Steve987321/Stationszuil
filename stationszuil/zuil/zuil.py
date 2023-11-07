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
    with open("../../stations.txt", 'r') as f:
        return random.choice(f.readlines()).strip()


def sla_bericht_op(bericht: dict):
    """"Slaat het bericht op in het bestand via append."""
    with open("../../" + BESTAND_NAAM, newline='', mode="a+") as f:
        writer = csv.DictWriter(f, CSV_BESTAND_VELDEN)

        # check of het nog geen csv header heeft en dus leeg is
        if f.tell() == 0:
            writer.writeheader()

        writer.writerow(bericht)
        