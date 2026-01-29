# Zoho Recruit Setup Guide

To integrate this service with Zoho Recruit, follow these steps:

## 1. Create a Zoho Self-Client
1. Go to [Zoho API Console](https://api-console.zoho.com/).
2. Click **Add Client** and choose **Self Client**.
3. Note down the **Client ID** and **Client Secret**.

## 2. Generate Refresh Token
1. In the Zoho API Console, go to the **Generate Code** tab.
2. Enter the scope: `ZohoRecruit.modules.ALL,ZohoRecruit.settings.ALL`.
3. Set the Time Duration and Scope Description.
4. Click **Generate**. Note down the **Grant Token**.
5. Use a tool like Postman to exchange the Grant Token for a **Refresh Token**:
   - **URL**: `https://accounts.zoho.com/oauth/v2/token`
   - **Method**: `POST`
   - **Parameters**: `grant_type=authorization_code`, `client_id`, `client_secret`, `code={GRANT_TOKEN}`, `redirect_uri={YOUR_REDIRECT_URI}`.

## 3. Configure Environment
Add the following to your environment variables or `serverless.yml`:
- `ZOHO_CLIENT_ID`
- `ZOHO_CLIENT_SECRET`
- `ZOHO_REFRESH_TOKEN`
- `ZOHO_BASE_URL` (e.g., `https://recruit.zoho.com/recruit/v2`)
