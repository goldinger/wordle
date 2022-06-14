from datetime import datetime, timezone
import json
import os
import random
from typing import Iterable, List, Optional, Tuple, Union
from app.models import Round
from wordle.settings import STATIC_ROOT


def pick_random_word(words: Union[Tuple, List]) -> str:
    return random.choice(words)
    

def create_round_from_words(words: Union[Tuple, List]) -> None:
    new_word = pick_random_word(words)
    Round.objects.create(word=new_word, datetime=datetime.now(timezone.utc))    


def new_round(words_file: str) -> None:
    with open(words_file, 'r') as f:
        possible_words = json.load(f)
    possible_words = tuple({x.lower() for x in possible_words})
    create_round_from_words(possible_words)


def run():
    new_round(os.path.join(STATIC_ROOT, 'data/words.json'))
