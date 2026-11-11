import sqlite3
import csv
import uuid  

DB_NAME = "Nexus_Cargo.db"

def setup_db():
    """Connects to the local database and sets up the table for the Nexus Cargo Pipeline ."""
    try:
        connection = sqlite3.connect(DB_NAME)
        pointer = connection.cursor()
        
        pointer.execute('''
            CREATE TABLE IF NOT EXISTS dispatches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tracking_number TEXT UNIQUE NOT NULL,
                sender TEXT NOT NULL,
                receiver TEXT NOT NULL,
                receiver_phone TEXT,
                origin TEXT,
                destination TEXT,
                weight_kg REAL CHECK (weight_kg > 0),
                description TEXT,
                status TEXT DEFAULT 'Received',
                last_updated TEXT
            )
        ''')
        connection.commit()
        connection.close()
        print("Database setup successfully!")

    except sqlite3.Error as E:
        print(f"Oops! Something went wrong: {E}")

def get_connection():
    """Opens a clean connection link to my database file."""
    return sqlite3.connect(DB_NAME)


class CargoApp:
    """Container holding all database actions (CRUD) and spreadsheet exports."""

    def add_parcel(self, sender, receiver, phone, origin, destination, weight_kg, description):
        """Generates a UUID and saves a new parcel into the database (Create)."""
        try:
            generated_uuid = str(uuid.uuid4()).upper()[:8]
            tracking_number = f"TRK-{generated_uuid}"
            
            connect = get_connection()
            cursor = connect.cursor()
            
            cursor.execute('''
                INSERT INTO dispatches (tracking_number, sender, receiver, receiver_phone, origin, destination, weight_kg, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (tracking_number, sender, receiver, phone, origin, destination, weight_kg, description))
            
            connect.commit()
            connect.close()
            
            return tracking_number
            
        except sqlite3.Error as E:
            print(f"\nERROR: Could not log cargo to database: {E}")
            return None  

    def lookup_parcel(self, track_no):
        """Retrieves an existing dispatches record using tracking numbers (Read)."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dispatches WHERE tracking_number = ?", (track_no,)) 
            data = cursor.fetchone() 
            conn.close()
            return data
        except sqlite3.Error:
            return None

    def change_status(self, track_no, new_status):
        """Modifies the transit status state of a parcel and stamps the time (Update)."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE dispatches 
                SET status = ?, last_updated = datetime('now') 
                WHERE tracking_number = ? 
            ''', (new_status, track_no))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False

    def purge_parcel(self, track_no):
        """Removes a dispatch entirely from database storage (Delete)."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM dispatches WHERE tracking_number = ?", (track_no,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False

    def export_to_csv(self):
        """Fetches all rows and exports them into an Excel-readable CSV file."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dispatches")
            rows = cursor.fetchall()
            
            with open("cargo_export.csv", "w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["ID", "Tracking Number", "Sender", "Receiver", "Phone", "Origin", "Destination", "Weight", "Description", "Status", "Timestamp"])
                writer.writerows(rows)
                
            conn.close()
            return True
        except (sqlite3.Error, IOError):
            return False


