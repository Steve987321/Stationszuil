"""
Module 1: Zuil
Op een zuil op een willekeurig NS-station kunnen reizigers hun bericht van maximaal 140 karakters invoeren. Het bericht moet worden opgeslagen in een tekstbestand met een logische structuur. Sla de onderstaande gegevens op in een gestructureerd tekstbestand:

het bericht;
de datum en tijd van het bericht;
de naam van de reiziger – als de reiziger geen naam invult, gebruik dan als naam ‘anoniem’;
het station – deze locatie van de zuil mag in de module zelf worden vastgelegd op basis van een random choice van drie stations. De computer (jouw python computer programma) kiest dan één station uit een lijst Download lijstvan minimaal drie stations en dat station wordt dan gekoppeld aan de berichten.
Deze module werkt met een Command Line Interface (CLI).
"""

import random
from datetime import datetime


def get_time(frmt: str):
    return datetime.now().strftime(frmt)


def get_random_station():
    with open("stations.txt", 'r') as f:
        return random.choice(f.readlines())


def main():
    bericht = input("je bericht: (max 140 letters) ")

    # Bericht mag niet meer dan 140 letters hebben
    while len(bericht) > 140:
        bericht = input("je bericht: (max 140 letters) ")

    naam = input("wat is je naam: (niks invullen is 'anoniem') ")

    if not naam:
        naam = "anoniem"

    # Pak een willekeurig station uit de lijst
    station = get_random_station()

    # De tijd als string
    timeStr = get_time("%d-%m-%y %H:%M")

    # Sla het bericht op
    with open("berichten.txt", "a+") as f:
        f.write(f"'{bericht}'\n")
        f.write(f"-{naam} op {timeStr} van {station}")


if __name__ == "__main__":
    main()
