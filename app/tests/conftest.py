from datetime import datetime, timedelta, timezone
import json
import pytest

from app.models import Guess


@pytest.fixture
def example_words():
    return ['COMME', 'PLAGE', 'THEME']

@pytest.fixture(autouse=False)
def init_rounds(django_db_setup, django_db_blocker, example_words):
    with django_db_blocker.unblock():
        from app.models import Round
        d = datetime.now(timezone.utc)
        yesterday = Round.objects.create(word=example_words[1], datetime=d - timedelta(days=1))
        today = Round.objects.create(word=example_words[0], datetime=d)
        yield yesterday, today
        Guess.objects.filter(round=yesterday).delete()
        yesterday.delete()
        Guess.objects.filter(round=today).delete()
        today.delete()
        


@pytest.fixture
def guess_data(example_words):
    return {
        "correct": {"word": example_words[0]},
        "wrong": {"word": example_words[2]},
        "unknown": {"word": 'unkno'},
    }
