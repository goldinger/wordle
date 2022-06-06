from django import urls
import pytest
from app.models import Guess


@pytest.mark.parametrize('view_name', ['home'])
@pytest.mark.django_db
def test_render_views(client, view_name, init_rounds):
    temp_url = urls.reverse(view_name)
    resp = client.get(temp_url)
    assert resp.status_code == 200


@pytest.mark.parametrize('guess_data_label', ['correct', 'wrong', 'unknown'])
@pytest.mark.django_db
def test_guess_view_post(client, init_rounds, guess_data, guess_data_label):
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
