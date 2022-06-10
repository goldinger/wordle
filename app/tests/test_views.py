from django import urls
import pytest
from app.models import Guess, Round
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone


@pytest.mark.parametrize('view_name', ['home'])
@pytest.mark.django_db
def test_render_views(client, view_name, init_rounds):
    temp_url = urls.reverse(view_name)
    resp = client.get(temp_url)
    assert resp.status_code == 200


@pytest.mark.parametrize('guess_data_label', ['wrong', 'unknown', 'correct'])
@pytest.mark.django_db
def test_guess_view_post(client, init_rounds, guess_data, guess_data_label):
    nb_guesses_before = Guess.objects.count()
    temp_url = urls.reverse('home')
    resp = client.post(temp_url, data=guess_data[guess_data_label])
    print(resp.content)
    assert resp.status_code == 200
    nb_guesses_after = Guess.objects.count()
    if guess_data_label in ['correct', 'wrong']:
        assert nb_guesses_after == nb_guesses_before + 1
    elif guess_data_label in ['unknown']:
        assert nb_guesses_after == nb_guesses_before
    else:
        raise ValueError("Unknown guess_data_label")    


@pytest.mark.django_db
def test_keyboard_helper(client, init_rounds):
    url = urls.reverse('home')
    home = client.get(url)
    assert home.status_code == 200
    soup = BeautifulSoup(home.content, 'html.parser')
    keys = soup.find_all('button', {'class': 'keyboard-key'})
    for key in keys:
        assert 'wrong' not in key.get('class')
    
    resp = client.post(url, data={'word': 'theme'})
    assert resp.status_code == 200
    soup = BeautifulSoup(resp.content, 'html.parser')
    t = soup.find('button', {'id': 'keyboard-letter-t'})
    print(t.get('class'))
    # h = soup.find('button', {'id': 'keyboard-letter-h'})
    # m = soup.find('button', {'id': 'keyboard-letter-m'})
    # e = soup.find('button', {'id': 'keyboard-letter-e'})
    # assert t and 'wrong' in t.get('class')
    # assert e and 'wrong' in h.get('class')
    # assert m and 'wrong' not in m.get('class')
    # assert e and 'wrong' not in e.get('class')
    
    
