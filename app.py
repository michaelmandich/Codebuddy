import openai
import sys
import os
import time
import json

def write_code_to_file(messages_response, filename):
    # Find the last message from the assistant
    assistant_message_content = get_last_assistant_message(messages_response)

    # Define the path where the file will be saved
    file_path = f".{filename}"

    # Write the code to a file
    print(assistant_message_content)
    with open(file_path, 'w') as file:
        file.write(assistant_message_content)

    return file_path

def get_last_assistant_message(messages_response):
    # Convert the cursor to a list if necessary
    if not isinstance(messages_response.data, list):
        messages = list(messages_response.data)
    else:
        messages = messages_response.data

    # Iterate through messages to find the last assistant message
    for message in reversed(messages):
        if message.role == 'assistant':
            # Get the content of the last assistant message
            for content in message.content:
                if hasattr(content, 'text'):
                    assistant_message_content = content.text.value
                    # Remove the Markdown code block delimiters and the 'python' keyword
                    cleaned_content = assistant_message_content.replace('```python\n', '').replace('\n```', '').strip()
                    return cleaned_content

    return ""  # Return an empty string if there is no assistant message

# ... rest of your existing code ...

# Call the write_code_to_file function with the messages response

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run
def show_json(obj):
    # Using print to display the JSON data in the console
    print(json.dumps(json.loads(obj.model_dump_json()), indent=4))
# Ensure a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python app.py \"<message>\"")
    sys.exit(1)

# The message is taken from the command-line argument
content = sys.argv[1]
print(content)

# Initialize the OpenAI client with your API key
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=openai.api_key)

# Define the Assistant ID (replace with your actual Assistant ID)
assistant_id = 'asst_JY0cdRArr6t156XEFwHXbsHj'

thread = client.beta.threads.create()
# Step 2: Create a Thread with the initial message
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content = " " + str(content)
)
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id,
)
run = wait_on_run(run, thread)
messages_response = client.beta.threads.messages.list(thread_id=thread.id)
write_code_to_file(messages_response, "jawn.py")
# Polling the run status (simplified for example purposes, implement with sleep for actual use)
