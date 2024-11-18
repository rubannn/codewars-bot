import os
import botogram
from dotenv import load_dotenv
from codewars_info import user_codewars_tasks


load_dotenv()
bot = botogram.create(os.getenv('TELEGRAM_CW_API_KEY'))


@bot.command("survey")
def survey_command(chat, message, args):
    """Reply to a simple survey!"""
    btns = botogram.Buttons()
    btns[0].callback("Great", "notify", "Happy to hear that!")
    btns[1].callback("Not so great", "notify", "I'm sorry! What happened?")

    chat.send("How are you feeling?", attach=btns)


@bot.callback("notify")
def notify_callback(query, data, chat, message):
    # query.notify(data)
    print(data)
    chat.send('qqqqqqq')


if __name__ == "__main__":
    bot.run()
