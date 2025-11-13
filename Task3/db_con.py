import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import logging as lgn

load_dotenv()

# Supabase PostgreSQL Configuration
PG_HOST = "aws-1-eu-west-2.pooler.supabase.com"
PG_PORT = 6543
PG_USER = "postgres.tykuknkebjhzenngzujf" 
PG_PASSWORD = "cowjacketdec"
PG_DATABASE = "postgres"
PG_TABLE = "phonerequest"

PG_QUERY = """SELECT newusername, samplename, phonenumber, departmentname, job, 
            emailaddress, costcenter, telephonelinesandinstallations,handsetsandheadsets,
            timeframe, dateneededby, "Comments" FROM public.phonerequest WHERE approximateendingdate IS NULL"""

def fetch_incident_data():
    """Connects to Supabase PostgreSQL and fetches the next incident record."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=PG_HOST,
            database=PG_DATABASE,
            user=PG_USER,
            password=PG_PASSWORD,
            port=PG_PORT
        )
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(PG_QUERY)
        
        record = cur.fetchone()
        cur.close()
        
        if record is None:
            print("No new incident data found in PostgreSQL.")
            return None
        
        # Convert the DictRow object to a standard Python dict for easier use
        return dict(record) 

    except Exception as e:
        print(f"Error connecting to or querying PostgreSQL: {e}")
        return None
    finally:
        if conn is not None:
            conn.close()

fetch_incident_data()