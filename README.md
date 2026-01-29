# ATS Integration Microservice

A serverless Python backend service that integrates with an Applicant Tracking System (ATS).

## Features
- **Unified API**: Abstraction layer over ATS.
- **Serverless**: Built with Serverless Framework and AWS Lambda.
- **Mock ATS**: Includes a mock implementation for testing and development.

## Setup

### Prerequisites
- Node.js & npm (for Serverless Framework)
- Python 3.9+
- AWS Credentials (if deploying to AWS)

### Installation

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

## Configuration

Environment variables in `serverless.yml`:
- `ATS_API_KEY`: API Key for the real ATS.
- `ATS_BASE_URL`: Base URL for the real ATS.
