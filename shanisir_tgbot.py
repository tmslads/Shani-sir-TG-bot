import getpass
import logging
import random as r
from datetime import time
from difflib import get_close_matches
from time import sleep
from uuid import uuid4
import getpass
import itertools

import chatterbot
from telegram import InlineQueryResultAudio

from telegram.ext import CommandHandler
from telegram.ext import InlineQueryHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
from textblob import TextBlob

import chatbot
import util

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

chatbot.shanisirbot.initialize()  # Does any work that needs to be done before the chatbot can process responses.

user = getpass.getuser()  # To determine which location to provide for clips
if user == 'Uncle Sam':
    clip_loc = r'C:/Users/Uncle Sam/Desktop/sthyaVERAT/4 FUN ya Practice/Shanisirmodule/Assets/clips/'
elif user == 'aarti':
    clip_loc = r'C:/Users/aarti/Documents/Python stuff/Bored/Shanisirmodule/Assets/clips/'

with open("token.txt", 'r') as file:
    bot_token = file.read()
updater = Updater(token=f'{bot_token}', use_context=True)
dispatcher = updater.dispatcher

with open("lad_words.txt", "r") as f:
    prohibited = f.read().lower().split('\n')

with open("snake.txt", "r") as f:
    snake_roast = f.read()

latest_response = None
results = []
rebukes = ["this is not the expected behaviour", "i don't want you to talk like that",
           "this language is embarassing to me like basically", "this is not a fruitful conversation"]
r.shuffle(rebukes)
rebukes = itertools.cycle(rebukes)
swear_advice = ["Don't use such words. Okay, fine?", "Such language fails to hit the tarjit.",
                "Vocabulary like this really presses my jokey.", "It's embarrassing vocabulary like basically.", "Such language is not expected from 12th class students",
                "You say shit like this then you go 'oh i'm so sowry sir it slipped' and expect me to forgive your sorry ass. Pathetic. Get a grip, loser.",
                "Some of you dumbasses talk as if your teachers are all deaf. Trust me; we hear a lot more than you'd like us to."]
r.shuffle(swear_advice)
swear_advice = itertools.cycle(swear_advice)
frequency = 0

user = getpass.getuser()  # To determine which location to provide for clips
if user == 'Uncle Sam':
    clip_loc = r'C:/Users/Uncle Sam/Desktop/sthyaVERAT/4 FUN ya Practice/Shanisirmodule/Assets/clips/'
elif user == 'aarti':
    clip_loc = r'C:/Users/aarti/Documents/Python stuff/Bored/Shanisirmodule/Assets/clips/'

with open("token.txt", 'r') as file:
    bot_token = file.read()

with open("lad_words.txt", "r") as f:
    prohibited = f.read().lower().split('\n')

with open("snake.txt", "r") as f:
    snake_roast = f.read()

links, names = util.clips()
for clip in zip(links, names):
    results.append(InlineQueryResultAudio(id=uuid4(),
                                          audio_url=clip[0], title=clip[1], performer="Shani Sir"))


class Commands:
    def delete_command(updt):
        """Delete the command message sent by the user"""
        dispatcher.bot.delete_message(chat_id=updt.message.chat_id,
                                      message_id=updt.message.message_id,)

    @staticmethod
    def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="You can use me anywhere, @ me in the chatbox and type to get an audio clip."
                                      " Or just talk to me here and get help from me directly.")

    @staticmethod
    def helper(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="This bot sends you actual shani sir clips straight from Shanisirmodule! "
                                      "He is savage in groups too! More commands will be added in the future."
                                      " @ me in the chatbox and type to get an audio clip."
                                      " P.S: Download Shanisirmodule from:"
                                      " https://github.com/tmslads/Shanisirmodule/releases")

    @staticmethod
    def secret(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="stop finding secret commands :P")

    @staticmethod
    def swear(update, context):
        Commands.delete_command(update)
        while True:
            swears = r.choices(prohibited, k=4)
            if len(set(swears)) == len(swears):  # i.e. if there is a duplicate element
                break
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"'{swears[0]}',\n'{swears[1]}',\n'{swears[2]}',\n'{swears[3]}'\n\n"
                                      f"{r.choice(swear_advice)}")

    @staticmethod
    def snake(update, context):
        Commands.delete_command(update)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=snake_roast)

    @staticmethod
    def facts(update, context):
        Commands.delete_command(update)
        factoid = util.facts()
        facts = [factoid[0].getText()[:-6], factoid[1].getText()[:-6],
                 factoid[2].getText()[:-6]]  # List of three random facts
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=r.choice(facts))

    @staticmethod
    def unknown(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="I didn't say wrong I don't know.")


def private(update, context):
    global frequency, latest_response
    cleaned = []
    JJ_RB = ["like you say", "like you speak"]  # For Adjectives or Adverbs

    initial = update.message.text
    initialStatement = chatterbot.conversation.Statement(update.message.text, in_response_to=latest_response)
    chatbot.shanisirbot.learn_response(initialStatement,
                                       latest_response)  # Learn user's latest message as response to bot's message
    latest_response = chatbot.shanisirbot.get_response(initial)
    try:
        msg = latest_response.text
    except AttributeError:
        msg = 'Hello'

    punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    msg = ''.join(c for c in msg if c not in punctuation)
    blob = TextBlob(msg)
    cleaned = blob.words  # Returns list with no punctuation marks
    
    flag = 0  # To check if a modal is present in the sentence
    lydcount = 0  # Counts the number of times "like you do" has been added
    JJ_RBcount = 0  # Counts the number of times a phrase from JJ_RB has been added

    if len(cleaned) < 20:
        lydlim = 1  # to limit the number of times we add
        JJ_RBlim = 1  # lyd and JJ_RB
    else:
        lydlim = len(cleaned) // 20
        JJ_RBlim = len(cleaned) // 20

    temp = 0

    for word, tag in blob.tags:  # returns list of tuples which tells the POS
        index = cleaned.index(word)
        if index - temp < 7:  # Do not add lad things too close to each other
            continue

        if tag == 'MD' and not flag:  # Modal
            cleaned.insert(index + 1, "(if the laws of physics allow it)")
            flag = 1

        if tag in ['JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS'] and JJ_RBcount < JJ_RBlim:  # Adjective or Adverb
            cleaned.insert(index + 1, r.choice(JJ_RB))
            JJ_RBcount += 1
            temp = index

        elif tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'] and lydcount < lydlim:  # Verb
            cleaned.insert(index + 1, "like you do")
            lydcount += 1
            temp = index

    if r.choice([0, 1]):
        if r.choice([0, 1]):
            cleaned.append(r.choice(["I am so sowry", "i don't want to talk like that",
                                     "it is embarrassing to me like basically", "it's not to trouble you like you say",
                                     "go for the worksheet", "it's not that hard"]))
        else:
            cleaned.append(r.choice(["it will be fruitful", "you will benefit", "that is the expected behaviour",
                                     "now you are on the track like", "now class is in the flow like",
                                     "aim to hit the tarjit", "don't press the jockey"]))
        cleaned.insert(0, update.message.from_user.first_name)
    else:
        cleaned.append(update.message.from_user.first_name)

    if len(cleaned) < 5:  # Will run if input is too short
        cleaned.append(r.choice(["*draws perfect circle*", "*scratches nose*"]))

    if 'when' in cleaned or 'When' in cleaned or 'time' in cleaned or 'Time' in cleaned:  # If question is present
        cleaned.insert(-1, 'decide a date')

    shanitext = ' '.join(cleaned).capitalize()

    with open("interactions.txt", "a") as f:
        inp = f"UTC+0 {update.message.date} {update.message.from_user.full_name} ({update.message.from_user.username}) says: {update.message.text}\n"
        if update.message.reply_to_message:  # If user is replying to bot directly
            out = 'I don\'t want to talk to you.'
            the_id = update.message.message_id  # Gets id of the message replied
            frequency += 1
            if frequency == 2:
                out = '*ignored*'
                frequency = 0
                context.bot.send_chat_action(chat_id=update.effective_chat.id, action='upload_audio')
                sleep(1)
                context.bot.send_audio(chat_id=update.effective_chat.id,
                                       audio=open(f"{clip_loc}that's it.mp3", 'rb'),
                                       title="That's it")
                context.bot.send_sticker(chat_id=update.effective_chat.id,
                                         sticker="CAADBQADHAADkupnJzeKCruy2yr2FgQ",  # Sahel offensive sticker
                                         reply_to_message_id=the_id)
        else:
            out = shanitext
            the_id = None
        print(inp)
        print(out)
        f.write(inp)
        f.write(f"Output: {out}\n\n")
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')  # Sends 'typing...' status
        # Assuming 25 WPM typing speed on a phone
        time_taken = (25 / 60) * len(out.split())
        sleep(time_taken) if time_taken < 6 else sleep(6)
        context.bot.send_message(chat_id=update.effective_chat.id, text=out,
                                 reply_to_message_id=the_id)  # Sends message


def group(update, context):
    if any(bad_word in update.message.text.lower().split() for bad_word in prohibited):
        if r.choices([0, 1],  # Only rebuke when this evaluates to True. Probabilities are 0.8 for False, 0.2 for True.
                     weights=[0.8, 0.2])[0]:  # Note that choices() returns a list.
            out = f"{next(rebukes)} {update.message.from_user.first_name}"
            context.bot.send_message(chat_id=update.effective_chat.id, text=out,
                                     reply_to_message_id=update.message.message_id)  # Sends message
            print("Rebuke: ", out)


def morning_goodness(context):
    context.bot.send_message(chat_id=-1001396726510, text="Good morning everyone")
    context.bot.send_chat_action(chat_id=-1001396726510, action='upload_audio')
    sleep(1)
    context.bot.send_audio(chat_id=-1001396726510, audio=open(f"{clip_loc}good mourning.mp3", 'rb'),
                           title="Good morning")
    context.bot.send_chat_action(chat_id=-1001396726510, action='typing')
    sleep((25 / 60) * 22)
    context.bot.send_message(chat_id=-1001396726510,
                             text="Hope you all know physics is first exam. January 6. Don't forget like you say.")


def inline_clips(update, context):
    query = update.inline_query.query
    if not query:
        context.bot.answer_inline_query(update.inline_query.id, results[:50])
    else:
        matches = get_close_matches(query, names, n=15, cutoff=0.4)
        index = 0
        while index <= len(matches) - 1:
            for pos, result in enumerate(results):
                if index == len(matches):
                    break
                if matches[index] == result['title']:
                    results[index], results[pos] = results[pos], results[index]
                    index += 1

        context.bot.answer_inline_query(update.inline_query.id, results[:16])


inline_clips_handler = InlineQueryHandler(inline_clips)
dispatcher.add_handler(inline_clips_handler)

help_handler = CommandHandler('help', Commands.helper)
dispatcher.add_handler(help_handler)

clip_handler = CommandHandler('secret', Commands.secret)
dispatcher.add_handler(clip_handler)

start_handler = CommandHandler('start', Commands.start)
dispatcher.add_handler(start_handler)

swear_handler = CommandHandler('swear', Commands.swear)
dispatcher.add_handler(swear_handler)

snake_handler = CommandHandler('snake', Commands.snake)
dispatcher.add_handler(snake_handler)

facts_handler = CommandHandler('facts', Commands.facts)
dispatcher.add_handler(facts_handler)

group_handler = MessageHandler(Filters.group, group)
dispatcher.add_handler(group_handler)

private_handler = MessageHandler(Filters.text, private)
dispatcher.add_handler(private_handler)

unknown_handler = MessageHandler(Filters.command, Commands.unknown)
dispatcher.add_handler(unknown_handler)

updater.job_queue.run_daily(morning_goodness, time(8, 00, 00))  # sends message everyday at 8am on the group
updater.start_polling()
updater.idle()
