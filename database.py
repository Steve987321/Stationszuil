import psycopg2
import psycopg2.extras # DictCursor
import psycopg2.errors # Logging errors

class StationsZuilDB():
    def __init__(self):
        self.con = None
        self.cursor = None

        self.error_str = None
        
    def connect(self):
        if self.con != None:
            self.error_str = "Er is al een connectie gemaakt."
            return True
        
        try:
            self.con = psycopg2.connect(
                        database="StationZuil", 
                        user="postgres",
                        password="pass",
                        host="localhost",
                        port="5433",
                        connect_timeout=5 
                        )
            
            self.cursor = self.con.cursor()
        except Exception as e:
            self.error_str = f"Error bij het verbinden van de database: {e}"
            return False
        
        return True
    
    def disconnect(self):
        if self.con.closed:
            self.error_str("De connectie is al afgesloten.")
            return
        
        print("connectie sluiten")
        self.con.close()

    def get_rows(self, query, args = None):
        self.cursor.execute(query, args)
        return self.cursor.fetchall()
    
    def update_rows(self, query, args = None):
        self.cursor.execute(query, args)
        self.con.commit()
    
    def get_row(self, query, args = None):
        self.cursor.execute(query, args)
        return self.cursor.fetchone()
    