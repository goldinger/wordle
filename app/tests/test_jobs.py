from app.models import Guess, Round
from app.scripts import new_round


def test_new_round_job():
    count = Round.objects.count()
    new_round.run()
    new_count = Round.objects.count()
    assert new_count == count + 1

def test_new_round_generation(words_json_file):
    count = Round.objects.count()
    new_round.new_round(words_json_file)
    new_count = Round.objects.count()
    assert new_count == count + 1
    
def test_round_creation_from_words(example_words):
    new_round.create_round_from_words(['words'])
    assert Round.get_current_round().word == 'words'

def test_pick_random_word():
    words = ['word1', 'word2', 'word3']
    size = 100000
    # call new_round.pick_random_word 1000 times and verify that the words are picked evenly
    random_words = [new_round.pick_random_word(words) for _ in range(size)]
    # count the number of times each word is picked
    random_words_count = {word: random_words.count(word) for word in words}
    # verify that each word is picked equally
    min_count = size*0.95 / len(words)
    max_count = size*1.05 / len(words)
    for count in random_words_count.values():
        assert min_count <= count <= max_count