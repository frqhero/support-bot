# Support bot

## Required env vars
In order the script to work please create `.env` file and specify these env vars:  
`TELEGRAM_TOKEN`  
`PROJECT_ID`  
`VK_TOKEN`  
`CREDENTIALS_PATH`  
`TG_CHAT_ID_SEND_ERRORS_TO`  

## Installation
1. Clone `git clone ...`
2. Install venv `python3 -m venv venv`
3. Activate venv `source venv/bin/python`
4. Install dependencies `pip install -r requirements.txt`
5. Create `.env` file in the project root directory and enter the env vars
6. Run the script 
   * `python3 main.py`

## Demo
![Demo](demo.gif)

## Bot learning
It is possible to programmatically extend the bot's capabilities by teaching it using a JSON file with a specific structure. The create_intent.py script expects to receive the JSON structure file as input. The repository contains an appropriate example file named 'questions.json.' This script parses the data, prepares it, and sends it to Google's Dialogflow API in the expected format, ultimately creating new intents in the agent.