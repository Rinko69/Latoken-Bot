import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Установите ключ API
openai.api_key = 'sk-proj-njxY0yWiNpCAYBhEHHo6T3BlbkFJaWrGN35X9gIDNI33pjvq'

latoken_info = """
Латокен - это платформа для торговли криптовалютами, предоставляющая пользователям возможность торговать различными цифровыми активами. Дополнительную информацию можно найти по ссылке: https://coda.io/@latoken/latoken-talent/latoken-161.
"""

hackathon_info = """
Хакатон - это мероприятие, где разработчики, дизайнеры и другие специалисты собираются вместе, чтобы создать новые проекты и идеи. Хакатоны могут быть отличной возможностью для обучения, сетевого общения и создания новых проектов. Дополнительную информацию можно найти по ссылке: https://deliver.latoken.com/hackathon.
"""

faq = {
    "что такое латокен": latoken_info,
    "что такое хакатон": hackathon_info,
}

# Функция для запроса к API ChatGPT
def ask_chatgpt(question: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}],
            max_tokens=150
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.InvalidRequestError as e:
        return f"Неверный запрос: {e}"
    except openai.error.AuthenticationError as e:
        return f"Ошибка аутентификации: {e}"
    except openai.error.APIConnectionError as e:
        return f"Ошибка соединения с API: {e}"
    except openai.error.RateLimitError as e:
        return f"Превышен лимит запросов: {e}"
    except Exception as e:
        return f"Произошла ошибка при обращении к API ChatGPT: {e}"

# Асинхронная функция, которая будет вызвана при получении команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        'Привет! Я телеграм-бот, и я могу помочь тебе с информацией о Латокен и Хакатоне. '
        'Просто задай свой вопрос! Для начала посмотри: /help'
    )

# Асинхронная функция, которая будет вызвана при получении команды /help
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        'Вот, чем я могу помочь:\n'
        '- Вопросы о Латокен\n'
        '- Вопросы о Хакатоне\n'
        'Просто напиши свой вопрос!'
    )

# Асинхронная функция, которая будет вызвана при получении любого текстового сообщения
async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text.lower()

    for question, answer in faq.items():
        if question in text:
            await update.message.reply_text(answer)
            return

    response = ask_chatgpt(update.message.text)
    await update.message.reply_text(response)

def main() -> None:
    # Вставь сюда свой токен
    telegram_token = '7325030603:AAGRI5bHCSZdJE_DdbPXUPUf9jy5tJBrul0'

    # Создаем Application и передаем ему токен
    application = Application.builder().token(telegram_token).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Регистрируем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
