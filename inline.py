from difflib import get_close_matches
from uuid import uuid4

from telegram import InlineQueryResultAudio, Update
from telegram.ext import CallbackContext

from online import util

results = []
names = []


def get_clips(_: CallbackContext) -> None:
    global results, names

    results.clear()
    names.clear()
    links, names = util.clips()

    # Adds all clips and names into one list
    for link, name in zip(links, names):
        results.append(InlineQueryResultAudio(id=uuid4(), audio_url=link, title=name, performer="Shani Sir"))


def inline_clips(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    if not query:
        # Show first 49 clips if nothing is typed-
        context.bot.answer_inline_query(update.inline_query.id, results[:50], cache_time=60)
    else:
        matches = get_close_matches(query, names, n=15, cutoff=0.3)  # Searches for close matches
        index = 0
        # Bubble sort (kinda) to sort the list according to close matches-
        while index <= len(matches) - 1:
            for pos, result in enumerate(results):
                if index == len(matches):  # Breaks if everything is sorted (to prevent exceptions)
                    break
                if matches[index] == result['title']:
                    results[index], results[pos] = results[pos], results[index]  # Swapping positions if matched
                    index += 1  # Increment by 1 to compare next element

        context.bot.answer_inline_query(inline_query_id=update.inline_query.id,
                                        results=results[:16])  # Show only 15 results
