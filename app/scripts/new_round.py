from datetime import datetime
import json
import random

from app.models import Round


def run():
    with open('static/data/words.json', 'r') as f:
        possible_words = json.load(f)
    possible_words = {x.lower() for x in possible_words}
    new_word = random.choice(tuple(possible_words))
    # print(new_word)
    Round.objects.create(word=new_word, datetime=datetime.now())