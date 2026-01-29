# Project Documentation

## Architecture
This project follows a provider-service pattern to abstract different ATS systems.

- **`handler.py`**: Entry point for AWS Lambda events.
- **`services/`**: High-level business logic that coordinates data flow.
- **`providers/`**: Low-level implementations that talk to specific ATS APIs (Zoho Recruit).
- **`config/`**: Centralized configuration and environment variable management.

## API Specification
Same as the root README.md.
