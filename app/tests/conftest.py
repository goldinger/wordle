from datetime import datetime, timedelta, timezone
import json
import pytest


@pytest.fixture(scope='session')
def example_words():
    with open('static/data/words.json', 'r') as f:
        words = json.load(f)
        
    return words[:3]

@pytest.fixture(scope='session')
def init_rounds(django_db_setup, django_db_blocker, example_words):
    with django_db_blocker.unblock():
        from app.models import Round
        today = datetime.now(timezone.utc)
        Round.objects.create(word=example_words[1], datetime=today - timedelta(days=1))
        today = Round.objects.create(word=example_words[0], datetime=today)
        


@pytest.fixture
def guess_data(example_words):
    return {
        "correct": {"word": example_words[0]},
        "wrong": {"word": example_words[2]},
        "unknown": {"word": 'unkno'},
    }
