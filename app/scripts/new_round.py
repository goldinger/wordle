from datetime import datetime
import json
import os
import random
from app.models import Round
from wordle.settings import STATIC_ROOT


def run():
    with open(os.path.join(STATIC_ROOT, 'data/words.json'), 'r') as f:
        possible_words = json.load(f)
    possible_words = {x.lower() for x in possible_words}
    new_word = random.choice(tuple(possible_words))
    # print(new_word)
    Round.objects.create(word=new_word, datetime=datetime.now())