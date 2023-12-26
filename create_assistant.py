from openai import OpenAI
import json

client = OpenAI(api_key="your open api key")


def upload_file(file_path):
    """
    Uploads a file

    Args:
        file_path (str): The path to the file to be uploaded.

    Returns:
        file_to_upload (object): The uploaded file object.
    """
    file_to_upload = client.files.create(
        file=open(file_path, "rb"), purpose="assistants"
    )
    return file_to_upload


transformer_paper_path = "./sample_docs.pdf"
file_to_upload = upload_file(transformer_paper_path)
file_to_upload.id


def create_assistant(
    assistant_name, my_instruction, uploaded_file, model="gpt-4-1106-preview"
):
    """
    Creates an assistant using the OpenAI API.

    Args:
        assistant_name (str): The name of the assistant.
        my_instruction (str): The instruction for the assistant.
        uploaded_file (object): The uploaded file object.
        model (str): The model to be used for the assistant.

    Returns:
        my_assistant (object): The created assistant object.
    """
    my_assistant = client.beta.assistants.create(
        name=assistant_name,
        instructions=my_instruction,
        model="gpt-4-1106-preview",
        tools=[{"type": "retrieval"}],
        file_ids=[uploaded_file.id],
    )

    return my_assistant

# sample schema
json_schema = {
    "header": "header or title of response ",
    "explanation": "An detailed explanation of the topic.",
    "example": "An example  related to the topic. with syntax",
}

# sample instructions
inst = f"You are a helpfull  bot . consider the document as knowledge base and answer user querries . your output should be in json schema :{json_schema}"
assistant_name = "Akshay's Assistant"
uploaded_file = file_to_upload
my_assistant = create_assistant(assistant_name, inst, uploaded_file)
assistantID = my_assistant.id
print(assistantID)
