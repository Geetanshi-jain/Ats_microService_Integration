import requests
import sys
import json

def get_refresh_token(client_id, client_secret, grant_code, redirect_uri):
    """
    Exchanges a Zoho Grant Code for a Refresh Token.
    """
    url = "https://accounts.zoho.in/oauth/v2/token"
    
    payload = {
        'code': grant_code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        data = response.json()
        
        if 'error' in data:
            print(f"Error from Zoho: {data['error']}")
            return
            
        print("\nSuccess! Here are your tokens:\n")
        print(f"Refresh Token: {data.get('refresh_token')}")
        print(f"Access Token:  {data.get('access_token')}")
        print(f"Expires In:    {data.get('expires_in')} seconds")
        print("\nAdd the Refresh Token to your .env file.")
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
    except json.JSONDecodeError:
        print("Error decoding response from Zoho.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python get_zoho_token.py <CLIENT_ID> <CLIENT_SECRET> <GRANT_CODE> <REDIRECT_URI>")
        sys.exit(1)
        
    client_id = sys.argv[1]
    client_secret = sys.argv[2]
    grant_code = sys.argv[3]
    redirect_uri = sys.argv[4]
    
    get_refresh_token(client_id, client_secret, grant_code, redirect_uri)
