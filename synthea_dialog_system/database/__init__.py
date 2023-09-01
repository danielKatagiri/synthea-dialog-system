import os

from sqlalchemy import URL, create_engine

url = URL.create(
    "postgresql",
    username="root",
    password="root",
    host="localhost",
    port=5432,
    database="synthea",
)

ENGINE = create_engine(url=url)
SYNTHEA_FOLDER = os.environ["SYNTHEA_FOLDER"]
FILES = os.listdir(SYNTHEA_FOLDER)
