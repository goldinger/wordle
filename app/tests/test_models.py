from datetime import datetime, timezone
from app.models import Guess, Round

def test_round_methods():
    rounds = Round.objects.all().order_by('-datetime')
    assert Round.get_current_round() == rounds[0]
    assert Round.get_round_before() == rounds[1]


def test_create_guess():
    round = Round.get_current_round()
    Guess.objects.create(round=round, word='words', ip_address='127.0.0.1')
    assert Guess.objects.count() == 1


def test_model_str():
    round = Round.objects.create(word='words', datetime=datetime.now(timezone.utc))
    assert round.word in str(round)
    guess = Guess.objects.create(round=round, word='words', ip_address='127.0.0.1')
    assert guess.word in str(guess)