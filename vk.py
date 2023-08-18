import os
import random

from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api as vk

from run import detect_intent_texts

load_dotenv()


def echo(event, vk_api):
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
    vk_token = os.getenv('VK_TOKEN')
    project_id = os.getenv('PROJECT_ID')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
