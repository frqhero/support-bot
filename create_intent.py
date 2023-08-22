import argparse
import json
import os

from dotenv import load_dotenv
from google.cloud import dialogflow


def is_file(filename):
    if os.path.isfile(filename):
        return filename
    else:
        raise argparse.ArgumentTypeError(f'{filename} is not a valid filename')


def create_intent(
    project_id, display_name, training_phrases_parts, message_texts
):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
        )
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message],
    )

    response = intents_client.create_intent(
        request={'parent': parent, 'intent': intent}
    )

    print('Intent created: {}'.format(response))


if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser(description='Add dialogflow intents')
    parser.add_argument(
        '-p',
        '--path',
        help='Specify path to json file',
        type=is_file,
        default='questions.json',
    )
    json_file_path = parser.parse_args().path
    with open(json_file_path, 'r') as json_file:
        questions_json = json_file.read()

    questions = json.loads(questions_json)

    project_id = os.getenv('PROJECT_ID')

    for display_name, questions_and_answer in questions.items():
        create_intent(
            project_id,
            display_name,
            questions_and_answer['questions'],
            [questions_and_answer['answer']],
        )
