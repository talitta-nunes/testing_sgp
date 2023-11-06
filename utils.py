from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
load_dotenv()

engine = create_engine(f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_BASE')}")
