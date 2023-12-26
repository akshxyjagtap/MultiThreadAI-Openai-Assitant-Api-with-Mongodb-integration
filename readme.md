# Flask-based OpenAI Assistant Api with MongoDB Integration

This Flask-based RESTful API integrates OpenAI's assistant with MongoDB to manage multiple user sessions and threads. The assistant interacts with users, storing conversation threads in a MongoDB database.

## Features

- OpenAI assistant integration using Flask RESTful API
- MongoDB integration to manage multiple users, threads, and conversation history
- Thread management for each user interaction
-  The assistant provides responses in JSON format, following a predefined schema, making it easy to integrate with other systems and applications.
 ## Getting Started

To get started with this project, follow the steps below:
- **Clone the Repository:**
   ```bash
   git clone https://github.com/akshxyjagtap/MultiThreadAI-Openai-Assitant-Api-with-Mongodb-integration-.git
   
##  Files Included
#### 1. `app.py`

This file initializes the Flask application and sets up API endpoints for interaction with the OpenAI Assistant. It communicates with the OpenAI API, manages user input, runs the assistant, and stores conversation data in MongoDB.

#### 2. `create_assistant.py`

This script utilizes OpenAI's API to create an assistant by uploading a file (such as a knowledge base document) and setting up instructions for the assistant. It generates an assistant ID, which is utilized by the main application (`app.py`) to interact with the assistant.

#### 3. `assistant_db_manager.py`

This file contains the code for managing interactions with a MongoDB database. It includes functions to check user existence, insert user data, retrieve user data, and append messages to the database based on user and assistant interactions.

## Setup Instructions

1. **Install Dependencies:**
   - Ensure Python is installed.
   - Install required Python packages:
     ```bash
     pip install flask flask-restful pymongo openai

2. **Configuration:**
   - Obtain OpenAI API key and MongoDB connection string.
   - Update the respective placeholders (`"your openai api key"`, `"your mongo connection string"`, etc.) in the code files (`app.py`, `create_assistant.py`) with your actual credentials.

3. **Run the Application:**
   - Execute the Flask application by running `app.py`:
     ```bash
     python app.py
     ```
   - The API will start running locally on `http://localhost:5000/v1`.

### API Endpoints

- **POST `/v1`**
  - Accepts user input and interacts with the OpenAI Assistant.
  - Requires JSON payload with `user_response` and `user_id`.
  - Sends the user input to the assistant, retrieves the assistant's response, and returns it in JSON format adhering to a predefined schema.

### Usage Example

Assuming the application is running locally:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"user_response": "Hello", "user_id": "123"}' http://localhost:5000/v1