import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB Credentials
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

# MySQL Credentials
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB_NAME = os.getenv("MYSQL_DB_NAME")
