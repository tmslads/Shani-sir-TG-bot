# The Shani Sir chatbot
import chatterbot
from chatterbot import response_selection

shanisirbot = chatterbot.ChatBot('The Shani Sir Bot',
                                 storage_adapter='chatterbot.storage.SQLStorageAdapter',
                                 logic_adapters=['chatterbot.logic.BestMatch'],
                                 response_selection_method=response_selection.get_first_response,
                                 preprocessors=['chatterbot.preprocessors.clean_whitespace'],
                                 read_only=False)  # Set to True to disable further learning from conversations the bot

shanisirbot.initialize()  # Does any work that needs to be done before the chatbot can process responses.
get_tags = shanisirbot.storage.tagger.get_bigram_pair_string


def train_with(corpus: str) -> None:
    """
    Trains the bot using the specified corpus
    eng ---> chatterbot.corpus.english (standard English corpus from chatterbot_corpora)
    woz ---> ./MULTIWOZ2.1 (Multi-Domain Wizard-of-Oz dataset from http://dialogue.mi.eng.cam.ac.uk/index.php/corpus/)
    ubu ---> Will download and extract the Ubuntu dialog corpus if that has not already been done.
    """

    from chatterbot.trainers import ChatterBotCorpusTrainer, UbuntuCorpusTrainer
    import time

    if corpus == 'ubu':  # WARNING: TAKES A REALLY LONG TIME
        start = time.time()  # (TOOK 114000 SECONDS = 31 HOURS TO EXTRACT & TRAIN FOR UNCLE SAM, NOT INCLUDING DL TIME)
        corpus_trainer = UbuntuCorpusTrainer(shanisirbot)
        corpus_trainer.train()
    else:
        start = time.time()
        corpus_trainer = ChatterBotCorpusTrainer(shanisirbot)
        if corpus == 'eng':
            corpus_trainer.train("chatterbot.corpus.english")
        elif corpus == 'woz':
            corpus_trainer.train('./data/MULTIWOZ2.1/attraction_db.json',
                                 './data/MULTIWOZ2.1/data.json',
                                 './data/MULTIWOZ2.1/dialogue_acts.json',
                                 './data/MULTIWOZ2.1/hospital_db.json',
                                 './data/MULTIWOZ2.1/hotel_db.json',
                                 './data/MULTIWOZ2.1/ontology.json',
                                 './data/MULTIWOZ2.1/police_db.json'
                                 './data/MULTIWOZ2.1/restaurant_db.json',
                                 './data/MULTIWOZ2.1/taxi_db.json',
                                 './data/MULTIWOZ2.1/testListFile.json',
                                 './data/MULTIWOZ2.1/train_db.json',
                                 './data/MULTIWOZ2.1/valListFile.json')
        else:
            print("Invalid corpus.")
            return
    end = time.time()
    time_taken = end - start
    print(f"\n\nThe Shani Sir chatbot has been trained using the corpus {corpus}. Time taken: {time_taken}s")
