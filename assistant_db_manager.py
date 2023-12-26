import pymongo
from datetime import datetime


class AssistantDBManager:
    def __init__(self, connection_string):
        # Establishing connections and initializing collections
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client["assistantDB"]
        self.assistants_collection = self.db["data"]

    def check_user_exists(self, user_id):
        # Check if user exists in the assistants collection
        user = self.assistants_collection.find_one({"userID": user_id})
        return user is not None

    def insert_data(self, user_id, thread_id, assistant_id):
        # Insert new data into the assistants collection
        new_data = {
            "userID": user_id,
            "threadID": thread_id,
            "assistantID": assistant_id,
        }
        self.assistants_collection.insert_one(new_data)
        return new_data

    def get_user_data(self, user_id):
        # Retrieve user data based on user ID from the assistants collection
        user_data = self.assistants_collection.find_one({"userID": user_id})
        return user_data

    def append_message(self, user_id, message, message_type):
        # Find the document for the user
        user_doc = self.assistants_collection.find_one({"userID": user_id})
        timestamp = datetime.utcnow()

        if user_doc:
            # Depending on the message type, append the message to the unified list
            if message_type == "user":
                self.assistants_collection.update_one(
                    {"_id": user_doc["_id"]},
                    {
                        "$push": {
                            "messages": {
                                "type": "user",
                                "content": message,
                                "timestamp": timestamp,
                            }
                        }
                    },
                )
            elif message_type == "assistant_response":
                self.assistants_collection.update_one(
                    {"_id": user_doc["_id"]},
                    {
                        "$push": {
                            "messages": {
                                "type": "assistant",
                                "content": message,
                                "timestamp": timestamp,
                            }
                        }
                    },
                )
            return True
        else:
            # If the user document is not found, return False
            return False


