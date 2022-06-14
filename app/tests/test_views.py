from django import urls
import pytest
from app.models import Guess
# from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from app.tests.utils import type_word
from app.views import check_word


HOMEPAGE = 'http://127.0.0.1:8000'


@pytest.mark.parametrize('view_name', ['home'])
@pytest.mark.django_db
def test_render_views(client, view_name):
    temp_url = urls.reverse(view_name)
    resp = client.get(temp_url)
    assert resp.status_code == 200


@pytest.mark.parametrize('guess_data_label', ['wrong', 'unknown', 'correct'])
@pytest.mark.django_db
def test_guess_view_post(client, guess_data, guess_data_label):
    nb_guesses_before = Guess.objects.count()
    temp_url = urls.reverse('home')
    resp = client.post(temp_url, data=guess_data[guess_data_label])
    assert resp.status_code == 200
    nb_guesses_after = Guess.objects.count()
    if guess_data_label in ['correct', 'wrong']:
        assert nb_guesses_after == nb_guesses_before + 1
    elif guess_data_label in ['unknown']:
        assert nb_guesses_after == nb_guesses_before
    else:
        raise ValueError("Unknown guess_data_label")    


@pytest.mark.django_db
def test_keyboard_helper(client, live_server, browser, guess_data):
    assert client.get(live_server.url).status_code == 200
    browser.get(live_server.url)
    keys = browser.find_elements(By.CLASS_NAME, 'keyboard-key')
    for key in keys:
        assert 'wrong' not in key.get_attribute('class')
    
    word = guess_data.get('wrong').get('word').lower()
    type_word(browser, word)
    browser.find_element(By.ID, f'keyboard-letter-!').click()
    check = check_word(word, guess_data.get('correct').get('word'))
    for item in filter(lambda x: x['result'] == 'wrong', check):
        if item['result'] == 'wrong':
            assert 'wrong' in browser.find_element(By.ID, f'keyboard-letter-{item["character"]}').get_attribute('class').split(' ')
        else:
            assert 'wrong' not in browser.find_element(By.ID, f'keyboard-letter-{item["character"]}').get_attribute('class').split(' ')
    
    
