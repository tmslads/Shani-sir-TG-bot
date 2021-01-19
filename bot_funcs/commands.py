import itertools
import random as r

from telegram import error, InlineKeyboardButton, InlineKeyboardMarkup, Poll, Update
from telegram.ext import CallbackContext

from constants import class_12b
from helpers.logger import logger
from helpers.namer import get_chat_name
from online import util, quiz_scraper

with open(r"files/lad_words.txt", "r") as f:
    prohibited = set(f.read().lower().split('\n'))

swear_advice = ["Don't use such words. Okay, fine?", "Such language fails to hit the tarjit.",

                "Vocabulary like this really presses my jokey.",

                "It's embarrassing vocabulary like basically.",

                "Such language is not expected from 12th class students", "There's no meaning of soo sowry, okay?",

                "You say shit like this then you go 'oh i'm so sowry sir it slipped' and expect me to forgive your"
                " sorry ass. Pathetic. Get a grip, loser.",

                "Some of you dumbasses talk as if your teachers are all deaf. Trust me; we hear a lot more than you'd"
                " like us to."]

r.shuffle(swear_advice)
swear_advice = itertools.cycle(swear_advice)


def ladcased(normal: str) -> str:
    """Convert a string to 'ladcase' (Alternating uppercase and lowercase)"""

    ladified = ''
    for i, c in enumerate(normal):
        ladified += c.lower() if (i % 2 == 0) else c.upper()

    return ladified


def del_command(update: Update) -> None:
    """Deletes the command message sent by the user."""

    try:
        update.message.delete()

    except error.BadRequest as e:
        logger(message=f"The command {update.message.text} could not be deleted due to {e}.")


class BotCommands:
    @staticmethod
    def start(update: Update, context: CallbackContext) -> None:
        """Starts the bot. Sends a short message detailing what the bot does."""

        name = update.effective_user.first_name

        msg = "You can use me anywhere, @ me in the chatbox and type to get an audio clip." \
              " Or just talk to me here and get help from me directly. Type /help to know more."

        if context.args:
            msg = "See if you want to tell your nickname and birthday click this --> /tell"
            logger(message=f"{name} just clicked the button to use /tell in private from {get_chat_name(update)}.")
        else:
            logger(update=update, message=f"/start", command=True)

        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        del name, msg

    @staticmethod
    def helper(update: Update, context: CallbackContext) -> None:
        """Sends a message to the user which explains how to use the bot."""

        buttons = [[InlineKeyboardButton(text="Try out inline mode", switch_inline_query_current_chat="")],
                   [InlineKeyboardButton(text="Use inline mode in another chat", switch_inline_query="")]]
        markup = InlineKeyboardMarkup(buttons)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=r"This bot sends you audio clips straight from the Shani Sir Module\. "
                                      "He's savage when he's cranky\."
                                      "\n\nHow to get clips \(Inline mode\):"
                                      "\n@ me in the chatbox \(don't press send yet\!\), press space and then type"
                                      r" to get a clip\."
                                      "\n\nCommands available:"
                                      "\n/help \- This will literally just send this message again\."
                                      "\n/start \- Starts the bot in private chat\."
                                      "\n/swear \- Teaches you not to swear\."
                                      "\n/snake \- Sends you a roast\."
                                      "\n/facts \- Blesses you with an incredibly useful fact\."
                                      "\n/8ball \- Answers yes/no questions in Shani Sir style\!"
                                      "\n/settings \- Modify my behaviour with granular precision\."
                                      "\n/quizizz \- Sends you a physics question\."
                                      "\n\nHow to use /8ball:\nReply to a message with /8ball\nor send /8ball in"
                                      " chat and reply to the message the bot sends\.\n\n"
                                      r"Inspired by the [Shani Sir Module](https://github.com/tmslads/Shanisirmodule)"
                                      r" and Telegram\!", parse_mode="MarkdownV2", disable_web_page_preview=True,
                                 reply_markup=markup)
        logger(update=update, message=f"/help", command=True)

    @staticmethod
    def secret(update: Update, context: CallbackContext) -> None:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="stop finding secret commands :P")  # Secret command for later use

    @staticmethod
    def swear(update: Update, context: CallbackContext) -> None:
        """Sends 4 swear words to the user along with a message saying not to use them."""

        del_command(update)

        while True:
            swears = r.choices(tuple(prohibited), k=4)  # Returns a list of 4 elements
            if len(set(swears)) == len(swears):  # i.e. if there is a duplicate element
                break

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=ladcased(f"'{swears[0]}',\n'{swears[1]}',\n'{swears[2]}',\n'{swears[3]}'\n\n"
                                               f"{next(swear_advice)}"))
        logger(update=update, message=f"/swear", command=True)

    @staticmethod
    def snake(update: Update, context: CallbackContext) -> None:
        """Sends a roast to the user."""

        del_command(update)

        with open(r"files/snake.txt", "r") as f1:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f1.read())

        logger(update=update, message=f"/snake", command=True)

    @staticmethod
    def facts(update: Update, context: CallbackContext) -> None:
        """Sends one random fact to the user."""

        del_command(update)
        context.bot.send_message(chat_id=update.effective_chat.id, text=r.choice(util.facts()))
        logger(update=update, message=f"/facts", command=True)

    @staticmethod
    def quizizz(update: Update, context: CallbackContext) -> None:
        """This is called when user calls /quizizz. This sends one physics quiz for the user from the internet."""

        logger(update=update, message=f"/quizizz", command=True)

        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')

        question, options, answer = quiz_scraper.quiz_maker_v2(number=1)

        logger(message=f"The question was: {question[0]}\n\n" + '\n'.join(options[0]) + f"\n\nAnswer:{answer[0]}")

        context.bot.send_poll(chat_id=update.effective_chat.id, question=question[0], options=options[0],
                              is_anonymous=False, type=Poll.QUIZ, correct_option_id=answer[0])

    @staticmethod
    def mention_all(update: Update, context: CallbackContext) -> None:
        """Bot mentions all 12B users"""

        del_command(update)
        msg = ''
        for lad, _id in class_12b.items():
            msg += f"[{lad}](tg://user?id={_id})\t"

        context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode="MarkdownV2")

        logger(message=f"{update.message.from_user.first_name} used mention_all. Group: {update.effective_chat.title}")

    # @staticmethod
    # def broadcast(update: Update, context: CallbackContext) -> None:
    #     """Allows unclesam79 or harshil21 to broadcast a message via the bot"""
    #
    #     if update.effective_chat.id in [samir, harshil]:
    #         context.bot.send_message(chat_id=update.effective_chat.id, text="Who do I broadcast to, master?")
    #         logger(message=f"Broadcast initiated.")
    #         return 0
    #
    #     return -1

    @staticmethod
    def unknown(update: Update, context: CallbackContext) -> None:
        """When user uses an invalid command."""

        context.bot.send_message(chat_id=update.effective_chat.id, text="I didn't say wrong I don't know.")
        logger(message=f"{update.effective_user.first_name} just used something weird in {get_chat_name(update)}.")