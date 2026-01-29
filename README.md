# ATS Integration Microservice
 serverless Python microservice that provides a unified REST API for integrating with multiple Applicant Tracking Systems (ATS) like Zoho, Greenhouse, and Workable.


## Features
- **Unified API**: Abstraction layer over ATS.
- **Serverless**: Built with Serverless Framework and AWS Lambda.
- **Mock ATS**: Includes a mock implementation for testing and development.

## Setup

### Prerequisites
- Node.js & npm (for Serverless Framework)
- Python 3.9+
- AWS Credentials (if deploying to AWS)


## 🛠️ Folder Structure
```text
ats-microservice/
├── src/
│   ├── handlers/          # Lambda Entry Points (REST API)
│   │   ├── jobs.py         # GET /jobs
│   │   ├── candidates.py   # POST /candidates
│   │   └── applications.py # GET /applications
│   ├── services/          # Core Business Logic
│   │   └── ats/           # ATS Integration Layer
│   │       ├── base.py    # Interface Definition
│   │       ├── factory.py # Provider Selector
│   │       ├── mock.py    # Mock Provider
│   │       └── zoho.py    # Zoho Recruit Stub
├── serverless.yml         # INFRA-as-Code (AWS Lambda Config)
├── package.json           # Plugin Management
└── requirements.txt       # Python Dependencies

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

```bash
npx serverless offline
```

The API will be available at `http://localhost:3000`.

## API Endpoints

### 1. Get Jobs
Return list of open jobs.

- **URL**: `/dev/jobs`
- **Method**: `GET`
- **Response**:
  ```json
  [
    {
      "id": "job-101",
      "title": "Software Engineer",
      "location": "Remote",
      "status": "OPEN",
      "external_url": "https://ats.mock/jobs/101"
    }
  ]
  ```

### 2. Create Candidate & Apply
Create a candidate and apply them to a job.

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

### Pagination Implementation
The service uses a recursive fetching strategy to ensure all data is retrieved, even if the ATS paginates its responses.

*   **How it works**: The `utils/pagination.py` utility handles the loop. It calls the provider's fetch method repeatedly, incrementing the `page` number each time until no more results are found.
*   **Concurrency & Speed**: Pages are currently fetched **sequentially** (one at a time) to respect ATS rate limits and avoid overwhelming the external API.
*   **Safety Break**: To prevent infinite loops with mock data or misbehaving APIs, there is a hard safety limit of **100 pages** per request.
*   **Data Source**: All pages are aggregated into a single list before being returned to the user, providing a seamless "fetch all" experience.

##Developed by Geetanshi jain 29 jan 2026
