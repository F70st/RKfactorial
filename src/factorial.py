import functools
from threading import Thread

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes


@functools.cache  # Сразу возвращаем значение, если значение, если такой кусок факториала уже считался
def calc_fact(low: int, n: int):
    if low == n:
        return n
    else:
        return n * calc_fact(low, n - 1)


class FactorialThread(Thread):
    def __init__(self, low: int, high: int):
        Thread.__init__(self)
        self.low = low
        self.high = high
        self.counter = 1

    def run(self):
        self.counter = calc_fact(self.low, self.high)


@functools.cache  # Сразу возвращаем значение, если такой факториал уже считался
def factorial(n: int):
    if n < 0:
        raise ValueError
    elif n < 2:
        return 1
    else:
        thread_1 = FactorialThread(1, n // 2)
        thread_2 = FactorialThread(n // 2 + 1, n)

        thread_1.start()
        thread_2.start()

        thread_1.join()
        thread_2.join()
        return thread_1.counter * thread_2.counter


async def tele_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        input_value = int(update.message.text)
        result = factorial(input_value)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=result)
    except ValueError:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Введите неотрицательное целое число')


if __name__ == '__main__':
    application = ApplicationBuilder().token('6403743185:AAGXLt-Wv3w770pdxqja9kZ4Xnb5t4CEH5U').build()

    fact_handler = MessageHandler(filters.TEXT, tele_fact)

    application.add_handler(fact_handler)

    application.run_polling()

