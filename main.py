import openai
import json
from dotenv import load_dotenv
from datetime import datetime
import os

# Load OpenAI API key from .env file using dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

context = []
# Create log directory if it doesn't exist
if not os.path.exists('log'):
	os.makedirs('log')
# Create message history file name current timestamp.json
context_file = f'log/{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.json'
# Create message history file named by current timestamp.json
with open(context_file, 'w') as f:
	json.dump(context, f)

# Function for sending a message to OpenAI API
def send_message(context):
	completion = openai.ChatCompletion.create(
		model="gpt-4",
		messages=context,
		max_tokens=2000,
		temperature=0.7,
		)
	return completion.choices[0].message.content

# Loop through new messages
while True:
	# Get new message from user
	new_message = input("User: ")
	# Add new message to message history as an array of json objects like {"role": "user", "content": message}
	context.append({"role": "user", "content": new_message})
	# Save updated message history to file
	with open(context_file, 'w') as f:
		json.dump(context, f)

	# Get response from OpenAI API
	bot_response = send_message(context)
	print(f"Bot: {bot_response}/n")

	# Add bot response to message history
	context.append({"role": "assistant", "content": bot_response})
