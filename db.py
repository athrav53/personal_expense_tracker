import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="Wealth-tracker",
        user="postgres",
        password="yogita17",
        port="5432"
    )
    return conn