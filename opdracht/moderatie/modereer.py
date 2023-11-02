import psycopg2
import psycopg2.extras  # DictCursor
import csv
import sys
import os
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from database import *

class Modereer():
    """Handelt de moderatie voor berichten"""
    def __init__(self, berichten_bestand_naam):
        self.bestand = berichten_bestand_naam
        self.index = 0  # hoe ver we zijn met beoordelen
        self.moderator_email = None
        
        self.error_str = None

        try: 
            with open(self.bestand) as f:
                self.berichten = list(csv.DictReader(f))
        except Exception as e: 
            print(f"Error tijdens het openen van {berichten_bestand_naam}: {e}")
        
        self.db = StationsZuilDB()

    def connect(self):
        """Maak connectie met de stationzuil database"""
        return self.db.connect()

    def disconnect(self):
        """Sluit de connectie met de database"""
        return self.db.disconnect()

    def login(self, email, wachtwoord):
        """Login als een moderator
        
        Returns:
            Als de login succesvol is gegaan
        """
        row = self.db.get_row("""
                            select count(*) from moderator 
                            where email = %s and wachtwoord = %s
                            """,
                            (email, wachtwoord))
        
        self.moderator_email = email
        
        return row[0] == 1
        
    def geef_bericht(self):
        """Geeft berichten terug die nog niet zijn beoordeeld"""
        if self.index >= len(self.berichten):
            return "Geen berichten om te beoordelen."
        return self.berichten[self.index]
    
    def beoordeel_bericht(self, goedgekeurd: bool):
        """Beoordeel bericht en stuur naar de database"""
        tijd = datetime.now().time()
        datum = datetime.now().date()

        # voeg nieuwe beoordeling
        self.db.update_rows("""
                            insert into beoordeling (is_goedgekeurd, datum, tijd, moderator_email)
                            values (%s, %s, %s, %s)

                            returning beoordelingnr
                            """,
                            (goedgekeurd, datum, tijd, self.moderator_email))
        
        # de net gemaakte beoordelings' serial
        beoordeling_nr = self.db.cursor.fetchone()[0]
        
        # voeg nieuwe bericht
        bericht = self.berichten[self.index]
        self.db.update_rows("""
                            insert into bericht (tekst, datum, tijd, naam, station, beoordelingnr)
                            values (%s, %s, %s, %s, %s, %s)
                            """,
                            (bericht["bericht"], bericht["datum"], bericht["tijd"], bericht["naam"], bericht["station"], beoordeling_nr)
                            )      
          
        self.index += 1
        
    def update_bestand(self):
        """Verwijderd beoordeelde berichten van het csv bestand"""
        with open(self.bestand, "r+") as f:
            lines = f.readlines()

            # leeg het bestand
            f.seek(0)
            f.truncate()

            # schrijf de header
            f.write(lines[0])

            # schrijf onbeoordeelde berichten
            if self.index != len(self.berichten):
                f.writelines(lines[self.index + 1:])

            self.index = 0

        # update berichten via het nieuwe bestand zelf
        with open(self.bestand, 'r') as f:
            self.berichten = list(csv.DictReader(f))
