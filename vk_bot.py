from vk_api import VkApi
import random
import os
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from google.cloud import dialogflow
import logging
import time
from logger_bot import BotLogsHandler
from google.api_core.exceptions import InvalidArgument

bot_logger_vk = logging.getLogger("bot_logger_vk")

class VK_Bot():
    def __init__(self):
        self.vk_session = VkApi(token=os.environ['VK_GROUP_TOKEN'])
        self.vk_api = self.vk_session.get_api()
        self.longpoll = VkLongPoll(self.vk_session)


    def answer_to_user(self, event):
        try:
            session_client = dialogflow.SessionsClient()
            session = session_client.session_path(os.environ['GOOGLE_PROJECT_NAME'],
                                                            f'vk-{event.user_id}')
            text_input = dialogflow.TextInput(text=event.text, language_code='ru')
            query_input = dialogflow.QueryInput(text=text_input)

            response = session_client.detect_intent(request={'session': session, 'query_input': query_input})
            if not response.query_result.intent.is_fallback:
                self.vk_api.messages.send(
                    user_id=event.user_id,
                    message=response.query_result.fulfillment_text,
                    random_id=random.randint(1, 1000)
                )
        except InvalidArgument:
            self.vk_api.messages.send(
                user_id=event.user_id,
                message= 'Введена слишком длинная строка. Длинна строки не должна превышать 256 символов.',
                random_id=random.randint(1, 1000)
            )


if __name__ == "__main__":
    load_dotenv(dotenv_path='.env')
    logging.basicConfig(format="%(levelname)s %(message)s")
    bot_logger_vk.setLevel(logging.INFO)
    bot_logger_vk.addHandler(BotLogsHandler())
    bot_logger_vk.info('Запущен VK бот!')
    while True:
        try:
            vk_bot = VK_Bot()
            for event in vk_bot.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    vk_bot.answer_to_user(event)
        except ConnectionError:
            bot_logger_vk.error(f'В работе бота возникла ошибка:\n{error}', exc_info=True)
            time.sleep(60)

        except Exception as error:
            bot_logger_vk.error(f'В работе бота возникла ошибка:\n{error}', exc_info=True)
            time.sleep(60)