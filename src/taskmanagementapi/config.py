import os
from dotenv import load_dotenv

load_dotenv()

def _get_setting(name: str) -> str | None:
    file_path = os.getenv(f"{name}_FILE")
    if file_path:
        with open(file_path, encoding="utf-8") as secret_file:
            return secret_file.read().strip()
    return os.getenv(name)

# Exemplo: postgresql://[username]:[password]@[host]:[port]/[database_name]
DATABASE_URL = _get_setting("DATABASE_URL")

TEST_DATABASE_URL = _get_setting("TEST_DATABASE_URL")

TOKEN_SECRET_KEY = _get_setting("TOKEN_SECRET_KEY")
