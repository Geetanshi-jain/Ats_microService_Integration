# ATS Integration Microservice
 serverless Python microservice that provides a unified REST API for integrating with multiple Applicant Tracking Systems (ATS) like Zoho, Greenhouse, and Workable.

---

## 1. ATS Setup & Access

This service abstracts the complexity of different ATS providers. To use it, you need to set up accounts and generate credentials.

### How to Create a Sandbox / Free Trial
*   **Zoho Recruit**: Visit the [Zoho Recruit Free Trial](https://www.zoho.com/recruit/signup.html) page. They offer a 15-day free trial of their enterprise features.
*   **Greenhouse**: Standard sandboxes are usually reserved for customers or partners. You can explore their APIs using their [Developer Portal](https://developers.greenhouse.io/).
*   **Workable**: Sign up for a 15-day free trial on the [Workable website](https://www.workable.com/free-trial/). No credit card is required.

### How to Generate API Keys / Tokens
*   **Zoho Recruit (OAuth 2.0)**:
    1.  Go to the [Zoho API Console](https://api-console.zoho.in/).
    2.  Click **Add Client** and choose **Self Client**.
    3.  In the **Generate Code** tab, enter these scopes: `ZohoRecruit.modules.all,ZohoRecruit.settings.modules.all`.
    4.  Set the duration and click **Generate**. Copy the Code.
    5.  Run the helper script: `python scripts/get_zoho_token.py` and provide your Client ID, Secret, and the generated Code.
    6.  Copy the resulting **Refresh Token** to your `.env` file.
*   **Greenhouse**: Go to `Configure (Gear Icon) -> Dev Center -> API Credential Management` and click "Create New API Key".
*   **Workable**: Navigate to `Settings -> Integrations -> Access Tokens` and generate a new token.

---

## 2. Local Development

### Prerequisites
- Python 3.9+
<<<<<<< HEAD
- Node.js & NPM (for Serverless Framework)
- Active ATS credentials (API Key or Refresh Token)

### Local Setup
1.  **Clone the repository and enter the directory**:
    ```bash
    cd Ats_microService_integration
    ```
2.  **Set up a Virtual Environment**:
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Install Dependencies**:
    ```powershell
    pip install -r requirements.txt
    npm install
    ```
4.  **Configure Environment**: Create a `.env` file from the [.env.example](file:///c:/Users/jaing/OneDrive/Desktop/Ats_microService_integration/.env.example) template.
=======
- AWS Credentials (if deploying to AWS)
### folder Structure
Ats_microService_Integration/
```│
├── serverless.yml          # Serverless framework configuration (routes, functions)
├── handler.py              # Main Lambda handlers (API logic)
├── requirements.txt        # Python dependencies
├── package.json            # Node.js dependencies (serverless, plugins)
├── package-lock.json
│
├── services/               # ATS integration business logic
│   └── ats_service.py
│
├── providers/              # External ATS API clients / adapters
│
├── utils/                  # Common utility functions (response, errors, helpers)
│
├── config/                 # Configuration files
│
├── scripts/                # Helper / setup scripts
│
├── tests/                  # Unit & integration tests
│
├── mock_db.json             # Mock ATS data (for local testing)
│
├── response1.jpg.jpeg      # Screenshot: GET /jobs API response
├── response2.jpg.jpeg      # Screenshot: POST /candidates API response
│
├── README.md               # Project documentation
└── SETUP.md                # Setup & environment configuration guide

```

##Installation

1. **Install Serverless Framework and Plugins**:
   ```bash
   npm install
   ```
   (This will install `serverless` and `serverless-offline` defined in `package.json` if it existed, but we rely on global or just generic install. Better: `npm install -D serverless-offline serverless-python-requirements`)

2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running Locally

Use `serverless-offline` to run the API locally.
>>>>>>> 8e65e979a293622e71b37cc14297c82a155f3bdb

### Running the Service
```bash
npx serverless offline start
```
The service will be available at `http://localhost:3000/dev`.

---

## 3. API Documentation & Examples

### [GET] `/jobs`
Fetches a normalized list of all available job openings.

**Curl Command:**
```bash
curl http://localhost:3000/dev/jobs
```

**Response Screenshot:**
![Jobs Output](file:///c:/Users/jaing/OneDrive/Desktop/Ats_microService_integration/screenshots/jobs_output.png)

---

### [POST] `/candidates`
Submits a candidate application for a specific job.

**Curl Command:**
```bash
curl.exe -X POST http://localhost:3000/dev/candidates -H "Content-Type: application/json" -d "{\`"name\`": \`"Jane Doe\`", \`"email\`": \`"jane.doe453@example.com\`", \`"phone\`": \`"555-0199998\`", \`"job_id\`": \`"210908000000354790\`"}"
```

**Response Screenshot:**
![Candidate Output](file:///c:/Users/jaing/OneDrive/Desktop/Ats_microService_integration/screenshots/candidate_output.png)

---

### [GET] `/applications?job_id=ID`
Retrieves all applications associated with a specific job ID.

**Curl Command:**
```bash
curl "http://localhost:3000/dev/applications?job_id=210908000000354790"
```

**Response Screenshot:**
![Applications Output](file:///c:/Users/jaing/OneDrive/Desktop/Ats_microService_integration/screenshots/applications_output.png)

---

## 4. Error Handling & Pagination Implementation

For a technical deep dive, see [doc.md](file:///c:/Users/jaing/OneDrive/Desktop/Ats_microService_integration/doc.md).

### Error Handling Flow
When an ATS returns an error (e.g., 401 Unauthorized or 404 Not Found), the microservice catches the exception in the Provider layer and wraps it into a **Clean JSON Error**.

**Internal Logic:**
1.  Provider raises `ATSError(message, status_code)`.
2.  `handler.py` catches the error in a `try/except` block.
3.  Client receives:
    ```json
    {
      "error": "Friendly error message"
    }
    ```

### Pagination Implementation
The service uses a recursive fetching strategy to ensure all data is retrieved, even if the ATS paginates its responses.

<<<<<<< HEAD
*   **How it works**: The `utils/pagination.py` utility handles the loop. It calls the provider's fetch method repeatedly, incrementing the `page` number each time until no more results are found.
*   **Concurrency & Speed**: Pages are currently fetched **sequentially** (one at a time) to respect ATS rate limits and avoid overwhelming the external API.
*   **Data Source**: All pages are aggregated into a single list before being returned to the user, providing a seamless "fetch all" experience.

---
**Maintained by:** Geetanshi Jain / ATS Integration Team
=======
- **URL**: `/dev/candidates`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "555-0199",
    "resume_url": "https://resume.link/jane",
    "job_id": "job-101"
  }
  ```
- **Response**: `201 Created`
**Response Screenshot:**
*(Place screenshot here)*

### 3. Get Applications
List applications for a given job.

- **URL**: `/dev/applications?job_id=job-101`
- **Method**: `GET`
- **Response**:
  ```json
  [
    {
      "id": "app-1234abcd",
      "candidate_name": "Jane Doe",
      "email": "jane@example.com",
      "status": "APPLIED"
    }
  ]
  ```
### 📸 GET /jobs API – Sample Response

![GET /jobs API Screenshot](https://raw.githubusercontent.com/Geetanshi-jain/Ats_microService_Integration/main/response1.jpg.jpeg)

### 📸 POST /candidates API – Sample Response

![POST /candidates API Screenshot](https://raw.githubusercontent.com/Geetanshi-jain/Ats_microService_Integration/main/response2.jpg.jpeg)

### Pagination Implementation
The service uses a recursive fetching strategy to ensure all data is retrieved, even if the ATS paginates its responses.

*   **How it works**: The `utils/pagination.py` utility handles the loop. It calls the provider's fetch method repeatedly, incrementing the `page` number each time until no more results are found.
*   **Concurrency & Speed**: Pages are currently fetched **sequentially** (one at a time) to respect ATS rate limits and avoid overwhelming the external API.
*   **Safety Break**: To prevent infinite loops with mock data or misbehaving APIs, there is a hard safety limit of **100 pages** per request.
*   **Data Source**: All pages are aggregated into a single list before being returned to the user, providing a seamless "fetch all" experience.

##Developed by Geetanshi jain 29 jan 2026
>>>>>>> 8e65e979a293622e71b37cc14297c82a155f3bdb
