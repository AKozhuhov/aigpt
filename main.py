import openai
import json
import tiktoken
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

gptmodel = "gpt-3.5-turbo-0301"
context_max = 2000
lean = False

def tokens_count(messages, model="gpt-3.5-turbo"):
	"""Returns the number of tokens used by a list of messages."""
	try:
		encoding = tiktoken.encoding_for_model(model)
	except KeyError:
		print("Warning: model not found. Using cl100k_base encoding.")
		encoding = tiktoken.get_encoding("cl100k_base")
	if model == "gpt-3.5-turbo":
		print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
		return tokens_count(messages, model="gpt-3.5-turbo-0301")
	elif model == "gpt-4":
		print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
		return tokens_count(messages, model="gpt-4-0314")
	elif model == "gpt-3.5-turbo-0301":
		tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
		tokens_per_name = -1  # if there's a name, the role is omitted
	elif model == "gpt-4-0314":
		tokens_per_message = 3
		tokens_per_name = 1
	else:
		raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
	num_tokens = 0
	for message in messages:
		num_tokens += tokens_per_message
		for key, value in message.items():
			num_tokens += len(encoding.encode(value))
			if key == "name":
				num_tokens += tokens_per_name
	num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
	return num_tokens

# Keep context array not more than 4000 tokens
def trim_context(context, tokens, model="gpt-3.5-turbo"):
	while tokens_count(context, model) > tokens:
		context.pop(0)
	return context

# Function for sending a message to OpenAI API
def send_message(context):
	completion = openai.ChatCompletion.create(
		model=gptmodel,
		messages=context,
		max_tokens=2000,
		temperature=0.7,
		)
	print(f'Usage: {completion["usage"]["prompt_tokens"]} + {completion["usage"]["completion_tokens"]} = {completion["usage"]["total_tokens"]} total tokens counted by the OpenAI API.')
	return completion.choices[0].message.content

if(lean):context.append({"role": "system", "content": "Provide a brief and concise answers to the following questions. Be lean and to the point."})

# Loop through new messages
while True:
	# Get new message from user
	new_message = input(f"User({gptmodel}): ")
	# Exit if user types "exit"
	if new_message == "exit":
		break
	# Change model if user types "model"
	if new_message == "gpt4":
		gptmodel = "gpt-4"
		continue
	if new_message == "gpt3.5":
		gptmodel = "gpt-3.5-turbo-0301"
		continue

	# Add new message to message history as an array of json objects like {"role": "user", "content": message}
	context.append({"role": "user", "content": new_message})
	# Save updated message history to file
	with open(context_file, 'w') as f:
		json.dump(context, f)

	context_length = tokens_count(context, gptmodel)
	if(context_length>context_max):
		trim_context(context, context_max, gptmodel)
		print("Context trimmed.")
	print(f"Context Tokens: {tokens_count(context, gptmodel)}")
	# Get response from OpenAI API
	bot_response = send_message(trim_context(context, context_max, gptmodel))
	print(f"Bot: {bot_response}\n")
	# Add bot response to message history
	context.append({"role": "assistant", "content": bot_response})
