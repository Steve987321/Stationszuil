import psycopg2
import psycopg2.extras  # DictCursor
import psycopg2.errors  # Logging errors


class StationsZuilDB:
    """De stationzuil database via psycopg2 dat wordt gebruikt door bijna alle modules"""
    def __init__(self):
        self.con = None
        self.cursor = None
        self.error_str = None
        
    def connect(self):
        """Maakt een connectie met de database en handelt de errors
        
        Returns: 
            False als er geen connectie kon worden gemaakt
            True als er een connectie is gemaakt

            check error_str voor een kleine beschrijving
        """
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
        """Breekt de verbinding af met de database als die bestaat"""
        if self.con.closed:
            self.error_str("De connectie is al afgesloten.")
            return
        
        print("connectie sluiten")
        self.con.close()

    def get_rows(self, query, args=None):
        """Geeft de rijen van de gegeven query"""
        self.cursor.execute(query, args)
        return self.cursor.fetchall()
    
    def update_rows(self, query, args=None):
        """Update rijen met de gegeven query"""
        self.cursor.execute(query, args)
        self.con.commit()
    
    def get_row(self, query, args=None):
        """Geeft een rij van de gegeven query"""
        self.cursor.execute(query, args)
        return self.cursor.fetchone()
    