from datetime import datetime, timedelta, timezone
import json
import os
from django.test import override_settings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pytest
import shutil
from app.models import Guess


@pytest.fixture
def example_words():
    return ['COMME', 'PLAGE', 'THEME']

@pytest.fixture(autouse=True)
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


@override_settings(DEBUG=True)
@pytest.fixture(scope="session")
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    chrome_driver = webdriver.Chrome(options=options)
    yield chrome_driver
    chrome_driver.quit()


@pytest.fixture
def init_static_folder():
    os.mkdir('app/tests/static')
    os.mkdir('app/tests/static/data')
    yield 'app/tests/static/data'
    shutil.rmtree('app/tests/static')

@pytest.fixture
def words_json_file(example_words, init_static_folder):
    file = os.path.join(init_static_folder, 'words.json')
    with open(file, 'w') as f:
        json.dump(example_words, f) 
    yield file
    os.remove(file)