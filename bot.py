import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Привет! Я бот-диагностик. Я создан для того чтобы помочь и поддержать себя в трудную минуту.\n\n"
        "Важно помнить: я не человек и не искусственный интеллект. Я скрипт, я могу только поддержать тебя, не больше. "
        "Как бы это грустно не звучало, но это правда.\n\n"
        "Если после моего бота не помогло, то позвони по номеру ниже, тебе там должны помочь:\n\n"
        "Детская линия:\n8-800-2000-122\n\n"
        "Взрослая линия:\n8-800-100-49-94\n\n"
        "Не бойся кому-то рассказывать проблемы. Если ты будешь хранить всё в себе, так ты себя будешь медленно убивать."
    )
    await update.message.reply_text(welcome_text)

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    user_state = context.user_data.get('state', None)

    if user_text == 'мне плохо':
        await update.message.reply_text(
            "Тебе плохо как? Физически или морально? (Ответь одним словом: физически или морально)"
        )
        context.user_data['state'] = 'awaiting_type'
    
    elif user_text == 'морально' and user_state == 'awaiting_type':
        response = (
            "Слушай, у тебя походу выдался ОЧЕНЬ плохой и трудный день, раз ты пишешь сюда. Смотри, ты можешь терпеть, "
            "а терпеть = умирать, а у тебя точно кто-то есть близкий, который за тебя переживает. Поэтому, я дам тебе два варианта действий:\n\n"
            "Первый вариант:\n"
            "Если сидишь - встань.\n"
            "Если лежишь - встань.\n"
            "Пойди на кухню и поставь чайник.\n"
            "Сделай себе именно ЧАЙ, не кофе, ничего, чай и точка.\n"
            "Сделай его без ничего, если пьёшь только с сахаром — добавь немного.\n"
            "Сядь и пей его маленькими глоточками.\n"
            "Ты спросишь для чего? Чтобы себя для начала успокоить, а потом уже будешь давать себе силы с помощью чая.\n"
            "И запомни: чай как кровь, нужен для жизни."
        )
        await update.message.reply_text(response)
        context.user_data['state'] = 'already_helped'
    
    elif user_text == 'физически' and user_state == 'awaiting_type':
        response = (
            "Смотри, если это уже не впервые, то это первые признаки выгорания. "
            "Ты устал делать то, что тебе не нравится, и это АБСОЛЮТНО НОРМАЛЬНО. "
            "Дам тебе только один совет: отдохни. Нет, реально, поспи или просто полежи и отдохни. "
            "Это тебе ОЧЕНЬ ПОМОЖЕТ, проверено лично создателем бота."
        )
        await update.message.reply_text(response)
        context.user_data['state'] = 'already_helped'
    
    elif user_text == 'мне плохо' and user_state == 'already_helped':
        response = (
            "Хорошо. Понял. Ритуал с чаем не помог, значит подключаем другой способ.\n\n"
            "Смотри, если у тебя SoundCloud, то перейди по ссылке ниже и послушай музыку "
            "(она без слов и со спокойным битом):\n"
            "https://on.soundcloud.com/djTLnmrZtzQi7RB5RZ\n\n"
            "Если у тебя Яндекс Музыка, то нажми так же на ссылку ниже, там тоже музыка без слов и со спокойным битом:\n"
            "https://music.yandex.ru/users/nphne-7i2pwelo/playlists/1003?utm_medium=copy_link&ref_id=1af1d770-951a-46b1-92ed-62bf33d3d15e"
        )
        await update.message.reply_text(response)
        context.user_data['state'] = None
    
    else:
        # Сбрасываем состояние, если пользователь пишет что-то другое
        if user_state:
            context.user_data['state'] = None
        await update.message.reply_text(
            "Я понимаю только команду /start и фразу 'мне плохо'. Попробуй начать с /start."
        )

# Основная функция
def main():
    # Вставьте ваш API ключ здесь
    TOKEN = "8379922104:AAE2hfxie39YJkGJP3AVdP5RdCQzYh737yY"
    
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
