import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    "port": 4000,
    "user": "2LwupNhEckogWnm.root",
    "password": os.getenv("DB_PASSWORD"),
    "database": "chatbot_db",
    "ssl_ca": "ca.pem"
}