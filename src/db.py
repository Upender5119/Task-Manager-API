import psycopg2
import psycopg2.extras

DB_CONFIG = {
    'host': 'localhost',
    'database': 'task_manager',
    'user': 'postgres',
    'password': 'upender',
    'port': 5432
}


def get_connection():
    """
    Establishes and returns a connection to the PostgreSQL database.

    The connection is created using the configuration specified in the 
    `DB_CONFIG` dictionary and uses a RealDictCursor for the cursor factory, 
    which allows query results to be returned as dictionaries.

    Returns:
        psycopg2.extensions.connection: A connection object to interact with the database.

    Raises:
        psycopg2.OperationalError: If the connection to the database fails.
        psycopg2.DatabaseError: For other database-related errors.
    """
    return psycopg2.connect(**DB_CONFIG, cursor_factory=psycopg2.extras.RealDictCursor)
