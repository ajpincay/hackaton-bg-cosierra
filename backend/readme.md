# Banco de Guayaquil Trusted Network Backend

A Python-based backend ecosystem built using FastAPI. This service is designed for Banco de Guayaquil’s Trusted Network, a platform aimed at facilitating B2B collaboration among SMEs and entrepreneurs. The backend supports user authentication (mocked for the MVP), user profile management, an opt-in mechanism, and user categorization with a simulated AI (bedrock model) integration.

## Features

- **Mock Authentication**  
  Uses a simple UUID-based login to simulate authentication. In production, integrate with Banco de Guayaquil’s SSO/OAuth.
  
- **User Profile Management**  
  Create and retrieve user profiles. Profiles include company name, opt-in status, categorization tier, and a badge URL.
  
- **Opt-In Mechanism**  
  Endpoints to allow users to opt-in or opt-out of the trusted network.
  
- **User Categorization**  
  Recalculates user categorization based on simulated data from financial health, business reputation, digital presence, legal status, and web/SEO metrics.  
  Integrates with a simulated bedrock model for advanced scoring adjustments.
  
- **Health Check Endpoint**  
  A root endpoint for verifying that the service is running, including a startup timestamp.
  
- **Background Task Processing**  
  Uses FastAPI’s `BackgroundTasks` for asynchronous category recalculation.

- **Poetry Managed & Custom Start Script**  
  Uses Poetry for dependency management and includes a custom script entry point (`poetry run start`) to run the application.

## Prerequisites

- **Python 3.11 or later**
- **Poetry** (installation guide: [Poetry Installation](https://python-poetry.org/docs/#installation))

## Installation

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd backend

2. **Install Dependencies**

   ```bash
   poetry install

3. **Run the Application**

   ```bash
    poetry run start

This command will start the FastAPI server at http://127.0.0.1:8000 with automatic reloading enabled.
Alternatively, you can activate the Poetry shell and run Uvicorn directly:

    ```bash
    poetry shell
    uvicorn app.main:app --reload


API Endpoints
GET /
Health check endpoint returning a welcome message and the service startup time.

POST /login
Mock login endpoint. Accepts a username and password, returns a user profile and a mock token.

GET /profile/{user_id}
Retrieve a user profile by ID.

POST /opt-in
Opt-in or opt-out endpoint for users to join the trusted network.

POST /recalculate_category/{user_id}
Triggers a background task to recalculate a user’s category based on simulated data and an AI-based adjustment.