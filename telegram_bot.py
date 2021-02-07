from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from dotenv import load_dotenv
from google.cloud import dialogflow
import os
import logging
import time
from logger_bot import BotLogsHandler


bot_logger_telegram = logging.getLogger("bot_logger_telegram")

class SupportBot():
    def __init__(self):


        updater = Updater(os.environ['TELEGRAM_BOT_TOKEN'])

        dispacher = updater.dispatcher
        dispacher.add_handler(CommandHandler("start", self.greet_user))
        dispacher.add_handler(MessageHandler(Filters.text, self.answer_to_user))

        updater.start_polling()
        updater.idle()

    def greet_user(self, update, context):
        update.message.reply_text('Здравствуйте!')

    def answer_to_user(self, update, context):
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(os.environ['GOOGLE_PROJECT_NAME'],
                                                        f'tg-{update.message.chat_id}')
        text_input = dialogflow.TextInput(text=update.message.text, language_code='ru')
        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(request={'session': session, 'query_input': query_input})
        update.message.reply_text(response.query_result.fulfillment_text)


if __name__ == '__main__':
    load_dotenv(dotenv_path='.env')
    logging.basicConfig(format="%(levelname)s %(message)s")
    bot_logger_telegram.setLevel(logging.INFO)
    bot_logger_telegram.addHandler(BotLogsHandler())
    bot_logger_telegram.info('Запущен телеграм бот!')
    while True:
        try:
            bot = SupportBot()
        except ConnectionError:
            bot_logger_telegram.error(f'В работе бота возникла ошибка:\n{error}', exc_info=True)
            time.sleep(60)
        except Exception as error:
            bot_logger_telegram.error(f'В работе бота возникла ошибка:\n{error}', exc_info=True)
            time.sleep(60)