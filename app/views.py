import json
from typing import Dict, Generator, List
from django.shortcuts import render
from app.models import Round, Guess

# Create your views here.

def check_word(word: str, reference: str) -> List[Dict[str, str]]:
    response = []
    for i in range(len(word)):
        if word[i] == reference[i]:
            response.append({ "character": word[i], "result": "correct" })
        elif word[i] in reference:
            response.append({ "character": word[i], "result": "close" })
        else:
            response.append({ "character": word[i], "result": "wrong" })
    # for every letter that is "close", check if the letter has already been guessed "correct" and don't appear a second time. If so, set to wrong
    for item in filter(lambda x: x["result"] == "close", response):
        c = item["character"]
        total_size = len([x for x in response if x["character"] == c and x["result"] == "correct"])
        correct_size = len([x for x in reference if x == c])    
        if total_size == correct_size:
            item["result"] = "wrong"
    
    return response
            


def home(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # print(x_forwarded_for)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        
    # print(ip)
    current_round = Round.get_current_round()
    goal = current_round.word
    round_before = Round.get_round_before()
    response_data = { "yesterday": round_before.word }
    response_data["goal"] = goal
    if request.method == 'GET':
        history = [x.word for x in Guess.objects.filter(ip_address=ip, round=current_round).order_by('created_at')[:5]]
        all_words = [check_word(x, goal) for x in history]
        response_data["words"] = all_words
        if goal in history:
            response_data["won"] = True
        elif len(history) >= 5:
            response_data["lost"] = True
        
        return render(request, 'home.html', response_data)
    
    elif request.method == 'POST':
        word = request.POST.get("word", '').lower()
        
        history = [x.word for x in Guess.objects.filter(ip_address=ip, round=current_round).order_by('created_at')]
        all_words = [check_word(x, goal) for x in history]
        response_data["words"] = all_words
                
        if goal in history:
            response_data["error"] = "Arrête de spam, t'as gagné..."
            response_data["won"] = True
            return render(request, 'home.html', response_data)
        elif len(word) != 5:
            response_data["error"] = 'Il faut 5 lettres abruti.e !'
            return render(request, 'home.html', response_data)
        elif word in history:
            response_data["error"] = 'Déjà essayé !'
            return render(request, 'home.html', response_data)
        elif len(history) >= 5:
            response_data["error"] = "Abandonne frérot.e, tu est nul.le !"
            response_data["lost"] = True
            return render(request, 'home.html', response_data)
        
        if word == goal:
            response_data["won"] = True
            #don't return request, we need to register the guess
        elif len(history) == 4:
            response_data["error"] = "Oh mais quel loser.e"
            response_data["lost"] = True
        
        with open('static/data/words.json', 'r') as f:
            possible_words = json.load(f)
        possible_words = [x.lower() for x in possible_words]
        # print(len(possible_words))
        if word not in possible_words:
            response_data["error"] = "Ca n'existe pas enculé.e !"
            return render(request, 'home.html', response_data)
        
        all_words.append(check_word(word, goal))
        Guess.objects.create(word=word, ip_address=ip, round=current_round)
        return render(request, 'home.html', response_data)
