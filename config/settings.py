import os

class Settings:
    ATS_PROVIDER = os.getenv("ATS_PROVIDER", "zoho") # Default to zoho
    
    # Zoho Configuration
    ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID", "")
    ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET", "")
    ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN", "")
    ZOHO_BASE_URL = os.getenv("ZOHO_BASE_URL", "https://recruit.zoho.com/recruit/v2")
    
    # Auth URL for Zoho (can vary by region .com, .in, etc.)
    ZOHO_AUTH_URL = os.getenv("ZOHO_AUTH_URL", "https://accounts.zoho.com/oauth/v2/token")

settings = Settings()
