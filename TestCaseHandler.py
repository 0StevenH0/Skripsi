import yaml
import requests

# Utility Function to populate answer data based on text_cases
def process_yaml_questions(yaml_file_path, api_url):
	with open(yaml_file_path, 'r', encoding='utf-8') as file:
		data = yaml.safe_load(file)

	for category in data:
		print(f"Processing category: {category}")

		for entry_number, entry_data in data[category].items():
			indonesian_question = entry_data['Indonesian']

			print(f"  Question {entry_number}: {indonesian_question}")

			response = call_api(api_url, indonesian_question)

			print(f"  API Response: {response}\n")


def call_api(url, question):

	try:
		response = requests.post(url, json={'search': question})
		response.raise_for_status()
		return response.json()
	except requests.RequestException as e:
		return f"API call failed: {str(e)}"


# Usage
yaml_file_path = 'test_cases.yaml'
api_url = 'http://127.0.0.1:8000/response'

process_yaml_questions(yaml_file_path, api_url)