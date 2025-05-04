from databases import Database
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

DB_URL = os.getenv('DB_URL')

database = Database(DB_URL)