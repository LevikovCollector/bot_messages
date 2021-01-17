from dotenv import load_dotenv
import dialogflow_v2
import dialogflow_v2beta1
import os
import json
from google.api_core.exceptions import InvalidArgument
def train_clietn():
    client = dialogflow_v2beta1.AgentsClient()
    parent = client.project_path(os.environ['GOOGLE_PROJECT_NAME'])
    response = client.train_agent(parent)

def create_new_intents(intents_questions):
    intents = []
    for key in intents_questions.keys():
        intent = {}
        intent['display_name'] = key
        intent['messages'] = [{'text':{'text': [intents_questions[key]['answer']]}}]
        intent['training_phrases'] =  [{"parts":[{"text": question}]} for question in intents_questions[key]['questions']]
        intents.append(intent)
    return intents

if __name__ == '__main__':
    load_dotenv(dotenv_path='.env')
    client = dialogflow_v2.IntentsClient()
    parent = client.project_agent_path(os.environ['GOOGLE_PROJECT_NAME'])

    with open('questions.json', 'r', encoding='utf-8') as file_with_questions:
        intents_questions = json.load(file_with_questions)
        new_intents = create_new_intents(intents_questions)
    try:
        for intent in new_intents:
            response = client.create_intent(parent, intent)
    except InvalidArgument:
        pass
    train_clietn()
