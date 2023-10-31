import psycopg2
import psycopg2.extras  # DictCursor
import csv
import sys
import os
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from database import *

class Modereer():
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
        return self.db.connect()

    def disconnect(self):
        return self.db.disconnect()

    def login(self, email, wachtwoord):
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

        self.db.update_rows("""
                            insert into beoordeling (is_goedgekeurd, datum, tijd, moderator_email)
                            values (%s, %s, %s, %s)

                            returning beoordelingnr
                            """,
                            (goedgekeurd, datum, tijd, self.moderator_email))
        
        beoordeling_nr = self.db.cursor.fetchone()[0]
        
        bericht = self.berichten[self.index]
        self.db.update_rows("""
                            insert into bericht (tekst, datum, tijd, naam, station, beoordelingnr)
                            values (%s, %s, %s, %s, %s, %s)
                            """,
                            (bericht["bericht"], bericht["datum"], bericht["tijd"], bericht["naam"], bericht["station"], beoordeling_nr)
                            )        
        self.index += 1
        
    def update_bestand(self):
        """Verwijderd beoordeelde berichten"""
        with open(self.bestand, "r+") as f:
            lines = f.readlines()

            f.seek(0)
            f.truncate()

            # header
            f.write(lines[0])

            if self.index != len(self.berichten):
                f.writelines(lines[self.index + 1:])

            self.index = 0

        with open(self.bestand, 'r') as f:
            self.berichten = list(csv.DictReader(f))
