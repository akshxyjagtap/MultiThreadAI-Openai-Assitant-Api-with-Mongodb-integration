import pymongo
from flask_restful import Resource, reqparse
from time import sleep
from .assistant_db_manager import AssistantDBManager
from openai import OpenAI
import json
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

client = OpenAI(api_key="your openai api key")
mongo_connection_string = "your mongo connection string"
manager = AssistantDBManager(mongo_connection_string)


def parse_json_garbage(s):
    # function to truncate garbage part from the response
    s = s[next(idx for idx, c in enumerate(s) if c in "{[") :]
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        return json.loads(s[: e.pos])


def check_and_add_user_data(user_id):
    # Check if user data exists for the given user_id
    if not manager.check_user_exists(user_id):
        # If user data doesn't exist, insert data for the user
        assistantID = "your assistant id"  # insert your assistant id that you got from create_assistant.py file
        thread = client.beta.threads.create()
        manager.insert_data(user_id, thread.id, assistantID)
        print(f"User data for UserID '{user_id}' added successfully.")
        user_data = manager.get_user_data(user_id)
        return user_data
    else:
        print(f"User data for UserID '{user_id}' already exists.")
        user_data = manager.get_user_data(user_id)
        print(user_data)
        return user_data


# Example user ID to check and create if not present
# user_id_to_check = "akshay vijay jagtap"
# check_or_create_user_data(user_id_to_check)


class AssistantApi(Resource):
    def post(self):
        try:
            # Define Request body schema
            parser = reqparse.RequestParser()
            parser.add_argument(
                "user_response",
                type=str,
                required=False,
                help="user input",
            )
            parser.add_argument(
                "user_id",
                type=str,
                required=True,
                help="id is required to save the thread in DB",
            )

            # Parse the request to extract the  arguments
            args = parser.parse_args()
            user_id = args["user_id"]
            user_input = args["user_response"]

            all_ids = check_and_add_user_data(user_id)
            print("info", all_ids)
            # Accessing thread id  and assistant id within the document
            thread_id = all_ids["threadID"]
            assistant_id = all_ids["assistantID"]

            # add user input to thread
            client.beta.threads.messages.create(
                thread_id=thread_id, role="user", content=user_input
            )
            # appending user response in the database
            manager.append_message(user_id, user_input, "user")

            # Run the Assistant
            run = client.beta.threads.runs.create(
                thread_id=thread_id, assistant_id=assistant_id
            )

            # Check if the Run requires action (function call)
            while True:
                run_status = client.beta.threads.runs.retrieve(
                    thread_id=thread_id, run_id=run.id
                )
                print(f"Run status: {run_status.status}")
                if run_status.status == "completed":
                    break
                sleep(1)  # Wait for a second before checking again

            # Retrieve and return the latest message from the assistant
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            response = messages.data[0].content[0].text.value
            # json_response = parse_json_garbage(response)
            print(f"Assistant response: {response}")

            json_response = parse_json_garbage(response)
            # appending assistant response in the database
            manager.append_message(user_id, json_response, "assistant_response")
            return {"message": "Success", "data": json_response}, 200

        # error handling
        except Exception as a:
            a = str(a)
            #  Handle exception
            print(a)
            return {
                "success": False,
                "error": {
                    "statusCode": 500,
                    "message": "Something went wrong!",
                    "errorMessage": a,
                },
            }


api.add_resource(AssistantApi, "/v1")

if __name__ == "__main__":
    app.run(debug=True)
