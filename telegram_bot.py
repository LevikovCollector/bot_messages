from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import telegram
from dotenv import load_dotenv
from google.cloud import dialogflow
import os
import logging
import time

bot_logger_telegram = logging.getLogger("bot_logger_telegram")

class BotLogsHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)
        self.bot =  telegram.Bot(token=os.environ['TELEGRAMM_LOGGER_BOT'])
        self.chat_id = os.environ["TELEGRAM_CHAT_ID"]

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)

class SupportBot():
    def __init__(self):
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(os.environ['GOOGLE_PROJECT_NAME'], os.environ['TELEGRAM_CHAT_ID'])

        updater = Updater(os.environ['TELEGRAM_BOT_TOKEN'])

        dispacher = updater.dispatcher
        dispacher.add_handler(CommandHandler("start", self.greet_user))
        dispacher.add_handler(MessageHandler(Filters.text, self.echo))

        updater.start_polling()
        updater.idle()

    def greet_user(self, update, context):
        update.message.reply_text('Здравствуйте!')

    def echo(self, update, context):
        text_input = dialogflow.TextInput(text=update.message.text, language_code='ru')
        query_input = dialogflow.QueryInput(text=text_input)

        response = self.session_client.detect_intent(request={'session': self.session, 'query_input': query_input})
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