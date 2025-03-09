# Banco de Guayaquil Trusted Network Backend

A Python-based backend ecosystem built using FastAPI. This service is designed for Banco de Guayaquil’s Trusted Network, a platform aimed at facilitating B2B collaboration among SMEs and entrepreneurs. The backend supports user authentication (mocked for the MVP), user profile management, an opt-in mechanism, and user categorization with a simulated AI (bedrock model) integration.

## Features

- **Mock Authentication**  
  Utilizes a simple UUID-based login to simulate user authentication. In production, this can be replaced or extended to integrate with Banco de Guayaquil’s SSO/OAuth.

- **User Profile Management**  
  Create and retrieve user profiles. Each profile can include a company name, opt-in status, categorization tier, and a badge URL.

- **Opt-In Mechanism**  
  Allows users to opt in or out of the trusted network through dedicated endpoints.

- **User Categorization**  
  Recalculates user trust scores based on simulated data sources (financial health, business reputation, digital presence, legal status, and web/SEO metrics).  
  Includes an additional AI-based adjustment from a simulated Bedrock model for more accurate scoring.

- **Health Check Endpoint**  
  A root endpoint to verify that the service is running, including a startup timestamp for reference.

- **Background Task Processing**  
  Employs FastAPI’s BackgroundTasks for asynchronous user categorization recalculations.

- **Poetry Managed & Custom Start Script**  
  Manages dependencies with Poetry and provides a custom script entry point (poetry run start) for starting the application.

## Prerequisites

- Python 3.11 or later
- Poetry (installation guide: [Poetry Installation](https://python-poetry.org/docs/#installation))

## Installation

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd backend
   ```

2. **Install Dependencies**

   ```bash
   poetry install
   ```

3. **Run the Application**

   ```bash
   poetry run start
   ```
   This command starts the FastAPI server at http://127.0.0.1:8000 with automatic reloading enabled.

   Alternatively, you can activate the Poetry shell and run Uvicorn directly:
   ```bash
   poetry shell
   uvicorn app.main:app --reload
   ```

## API Endpoints

Below is a brief overview of the primary endpoints in this application. Adjust these paths as needed based on your specific project structure:

1. GET /  
   » A health check endpoint returning a welcome message and the service startup time.

2. POST /auth/login  
   » Mock login endpoint. Accepts a username and password, then returns a user profile and a mock token.

3. GET /auth/profile/{user_id}  
   » Retrieves a user profile by ID. (Path may vary if you have different routing logic.)

4. POST /category/recalculate/{ruc}  
   » Triggers a background task to recalculate a user's trust score and tier based on simulated data and an AI-based adjustment (Bedrock integration).
