# === Begin File: backend/config.py ===
import os
from dotenv import load_dotenv


def load_config(app):
    load_dotenv()
    app.config["GPT_API_KEY"] = os.getenv("GPT_API_KEY")
    app.config["SHOPIFY_SECRET"] = os.getenv("SHOPIFY_SECRET")
    app.config["ENV"] = os.getenv("FLASK_ENV", "development")

# === End File: backend/config.py ===