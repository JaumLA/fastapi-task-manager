import os
from dotenv import load_dotenv

load_dotenv()

# Exemplo: postgresql://[username]:[password]@[host]:[port]/[database_name]
DATABASE_URL = os.getenv("DATABASE_URL")

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")