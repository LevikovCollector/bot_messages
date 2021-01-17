# Боты консультанты в VK и Телегерам
## Описание
Созданы боты которые созданы для того чтобы разгрузить техподдержку от типичных вопросов пользователя

## Как установить
Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей
```
pip install -r requirements.txt
```

## Пример запуска скрипта
Для запуска скрипта требуется сделать следующее:

1. Созадать бота и получить его токен(Telegram)
2. Создать группу в ВК и добавить к ней ключ (дать доступы к отправке сообщений)
3. Получить свой id (использовать бота @userinfobot) - чат id для телеграмм бота
4. Создать проект DialogFlow
Создать ключ для google project
5. В папке со скаченным скриптом создать файл .env
6. Открыть файл в текстом редакторе и добавить строки
```
GOOGLE_PROJECT_NAME=<указать название проекта DialogFlow>
VK_GROUP_TOKEN=<указать токен группы VK>
TELEGRAM_BOT_TOKEN=<токен от телеграмма>
TELEGRAM_CHAT_ID=<ваш id полученный от @userinfobot>
TELEGRAMM_LOGGER_BOT=<токен от телеграмма> - бот который сообщает об ошибках в приложении
GOOGLE_APPLICATION_CREDENTIALS=<указать путь к ключу с проектом>
```
7. Сформировать файлы json с вопросами и ответами (questions.json)
8. Выполнить команду (в папке со скаченным скриптом)
```
python create_new_intents.py - создает вопросы и ответы в проекте DialogFlow и обучает агента
```
9. Выполнить команду (в папке со скаченным скриптом)
```
python telegram_bot.py - запускает телеграм бота 
python vk_bot.py - запускает вк бота 
```

## Деплой на сервера heroku
1. Зарегистрироваться на сайте https://id.heroku.com/login
2. Создать прилолжение
3. В корне папки создать файл Procfile (без расширения)
4. Указать в нем параметры запуска приложения
 ```
bot-tg: python3 telegram_bot.py
bot-vk: python3 vk_bot.py
```
5. Подключить github к heroku
6. Запустить deploy из бранча

Комментарии:
1. Если используются переменные окружения(токены, id и т.п.) то их нужно добавить на вкладке Settings приложения в блок Config Vars
2. Для анализа логов требуется скачать и установить Heroku CLI
