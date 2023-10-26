import psycopg2
import psycopg2.extras # DictCursor
import csv
from datetime import datetime

class Modereer():
    def __init__(self, berichten_bestand_naam):
        self.bestand = berichten_bestand_naam
        self.index = 0 # hoe ver we zijn met beoordelen
        self.con = None
        self.cursor = None
        self.moderator_email = None
        
        self.error_str = None

        with open(self.bestand) as f:
            self.berichten = list(csv.DictReader(f))

    def connect(self):
        if self.con != None:
            self.error_str = "Er is al een connectie gemaakt."
            return True
        
        try:
            self.con = psycopg2.connect(
                        database="StationZuil", 
                        user="postgres",
                        password="pass",
                        host="51.132.140.12",
                        port="5432",
                        connect_timeout=5
                        )
            
            self.cursor = self.con.cursor()
        except Exception as e:
            self.error_str = f"Error bij het verbinden van de database: {e}"
            return False
        
        return True

    def disconnect(self):
        if self.con.closed:
            return
        
        print("connectie sluiten")
        self.con.close()

    def login(self, email, wachtwoord):
        self.cursor.execute("""
                            select count(*) from moderator 
                            where email = %s and wachtwoord = %s
                            """,
                            (email, wachtwoord))
        
        self.moderator_email = email
        
        return self.cursor.fetchone()[0] == 1
        
    def geef_bericht(self):
        """Geeft berichten terug die nog niet zijn beoordeeld"""
        if self.index >= len(self.berichten):
            return "Geen berichten om te beoordelen."
        return self.berichten[self.index]
    
    def beoordeel_bericht(self, goedgekeurd: bool):
        """Beoordeel bericht en stuur naar de database"""
        self.cursor.execute("select count(*) from beoordeling")
        beoordeling_nr = int(self.cursor.fetchone()[0])
        tijd = datetime.now().time()
        datum = datetime.now().date()

        self.cursor.execute("""
                            insert into beoordeling (beoordelingnr, is_goedgekeurd, datum, tijd, moderator_email)
                            values (%s, %s, %s, %s, %s)
                            """,
                            (beoordeling_nr, goedgekeurd, datum, tijd, self.moderator_email))
        self.con.commit()
        
        self.cursor.execute("select count(*) from bericht")
        berichtnr = int(self.cursor.fetchone()[0])
        bericht = self.berichten[self.index]
        self.cursor.execute("""
                            insert into bericht (berichtnr, tekst, datum, tijd, naam, station, beoordelingnr)
                            values (%s, %s, %s, %s, %s, %s, %s)
                            """,
                            (berichtnr, bericht["bericht"], bericht["datum"], bericht["tijd"], bericht["naam"], bericht["station"], beoordeling_nr))
        self.con.commit()
        
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
