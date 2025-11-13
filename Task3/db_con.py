import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

TABLE_NAME = os.getenv('TABLE_NAME', 'customer_requests')

def get_db_connection():
    """Create database connection"""
    return psycopg2.connect(**DB_CONFIG)