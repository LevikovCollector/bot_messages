from vk_api import VkApi
import random
import os
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from google.cloud import dialogflow
import logging
import time
import telegram

bot_logger_vk = logging.getLogger("bot_logger_vk")

class BotLogsHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)
        self.bot =  telegram.Bot(token=os.environ['TELEGRAMM_LOGGER_BOT'])
        self.chat_id = os.environ["TELEGRAM_CHAT_ID"]

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


class VK_Bot():
    def __init__(self):
        self.vk_session = VkApi(token=os.environ['VK_GROUP_TOKEN'])
        self.vk_api = self.vk_session.get_api()
        self.longpoll = VkLongPoll(self.vk_session)
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(os.environ['GOOGLE_PROJECT_NAME'],
                                                        os.environ['TELEGRAM_CHAT_ID'])

    def echo(self, event):
        text_input = dialogflow.TextInput(text=event.text, language_code='ru')
        query_input = dialogflow.QueryInput(text=text_input)

        response = self.session_client.detect_intent(request={'session': self.session, 'query_input': query_input})
        if not response.query_result.intent.is_fallback:
            self.vk_api.messages.send(
                user_id=event.user_id,
                message=response.query_result.fulfillment_text,
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
                    vk_bot.echo(event)
        except ConnectionError:
            bot_logger_vk.error(f'В работе бота возникла ошибка:\n{error}', exc_info=True)
            time.sleep(60)
        except Exception as error:
            bot_logger_vk.error(f'В работе бота возникла ошибка:\n{error}', exc_info=True)
            time.sleep(60)