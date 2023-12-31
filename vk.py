import os
import random
import traceback

import telegram
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api as vk

from contact_dialogflow import detect_intent_texts
from logging_handler import TelegramLogsHandler


def handle_messages(event, vk_api):
    is_fallback, response_text = detect_intent_texts(
        project_id, event.user_id, event.text, 'RU'
    )
    if not is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response_text,
            random_id=random.randint(1, 1000),
        )


if __name__ == '__main__':
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    project_id = os.getenv('PROJECT_ID')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    telegram_token = os.getenv('TELEGRAM_TOKEN')
    tg_chat_id = os.getenv('TG_CHAT_ID')
    bot = telegram.Bot(token=telegram_token)
    bot.logger.addHandler(TelegramLogsHandler(bot, tg_chat_id))
    bot.logger.warning('Dialogflow bot via vk has been started')

    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    handle_messages(event, vk_api)
        except Exception:
            exception_data = traceback.format_exc().splitlines()
            bot.logger.warning(exception_data[-1])
