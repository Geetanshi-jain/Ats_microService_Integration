import os
from dotenv import load_dotenv

# Load local .env file if it exists
load_dotenv()

class Settings:
    ATS_PROVIDER = os.getenv("ATS_PROVIDER", "zoho") # Default to zoho
    
    # Zoho Configuration
    ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID", "")
    ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET", "")
    ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN", "")
    ZOHO_BASE_URL = os.getenv("ZOHO_BASE_URL", "https://recruit.zoho.in/recruit/v2")
    
    # Auth URL for Zoho (can vary by region .com, .in, etc.)
    ZOHO_AUTH_URL = os.getenv("ZOHO_AUTH_URL", "https://accounts.zoho.in/oauth/v2/token")

settings = Settings()
