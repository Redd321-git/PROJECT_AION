import psycopg2
from . import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from database import Base, engine

def create_database():
	con=psycopg2.connect(
		dbname="postgres",
		user=DB_USER,
		password=DB_PASSWORD,
		host=DB_HOST,
		port=DB_PORT
	)
	con.autocommit=True
	cur=con.cursor()
	con.execute(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'")
	exists=cur.fetchone()
	if not exists:
		cur.execute(f"CREATE DATABASE {DB_NAME};")
		cur.execute(f"CREATE EXTENSION IF NOT EXISTS vector;")
		print("{DB_NAME} created")
	else:
		print("{DB_NAME} already exists")
	cur.close()
	con.close()
	
def create_tables():
	Base.metadata.create_all(bind=engine)
	print("Tables created")
	
	