import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# load environment variables
load_dotenv()

def get_engine():
    """
    Returns engine for PostgreSQL
    Password is securely loaded from environment variables
    """

    user = os.getenv("DB_USER")
    password = quote_plus(os.getenv("DB_PASSWORD")) 
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    engine = create_engine(
        f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    )

    return engine

print("Done")