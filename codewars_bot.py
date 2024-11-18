import os
import botogram
from dotenv import load_dotenv
from codewars_info import user_codewars_tasks

load_dotenv()
bot = botogram.create(os.getenv('TELEGRAM_CW_API_KEY'))


@bot.command("Surkiss")
def codewarsinfo(chat, message, args):
    """Info by Surkiss"""
    res = user_codewars_tasks('Surkiss')
    chat.send(res)


@bot.command("Nrj_eX")
def codewarsinfo2(chat, message, args):
    """Info by Nrj_eX"""
    res = user_codewars_tasks('Nrj_eX')
    chat.send(res)


@bot.command("start")
def start_command(chat, message, args):
    buttons = botogram.Buttons()
    # buttons[0].callback("Surkiss", "/Surkiss")
    # buttons[1].callback("Nrj_eX", "/Nrj_eX")
    buttons[0].callback("button1", "button1")
    chat.send('qqq', attach=buttons)


@bot.command("survey")
def survey_command(chat, message, args):
    """Reply to a simple survey!"""
    btns = botogram.Buttons()
    btns[0].callback("Great", "notify", "Happy to hear that!")
    btns[1].callback("Not so great", "notify", "I'm sorry! What happened?")

    chat.send("How are you feeling?", attach=btns)


@bot.callback("notify")
def notify_callback(query, data, chat, message):
    query.notify(data)


# @bot.command("start")
# def start_command(chat, message, args):
#     buttons = botogram.Buttons()
#     buttons[0].add("Button 1", callback_data="button1")
#     buttons[1].add("Button 2", callback_data="button2")
#     chat.send("Choose a button:", attach=buttons)



@bot.command("hello")
def hello_command(chat, message, args):
    """Say hello to the world!"""
    chat.send("Hello world")


@bot.message_matches(r'.*')
def send_echo(chat, message: botogram.Message):
    """Echo"""
    chat.send(message.text)


if __name__ == "__main__":
    bot.run()
