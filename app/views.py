from django.shortcuts import render

# Create your views here.

def check_word(word, reference) -> list:
    for i in range(len(word)):
        if word[i] == reference[i]:
            yield { "character": word[i], "result": "correct" }
        elif word[i] in reference:
            yield { "character": word[i], "result": "close" }
        else:
            yield { "character": word[i], "result": "wrong" }
        
def home(request):
    hello = [
        { "character": "h", "result": "correct" },
        { "character": "e", "result": "wrong" },
        { "character": "l", "result": "close" },
        { "character": "l", "result": "wrong" },
        { "character": "o", "result": "close" },
    ]
    
    world = [
        { "character": "w", "result": "wrong" },
        { "character": "o", "result": "wrong" },
        { "character": "r", "result": "wrong" },
        { "character": "l", "result": "close" },
        { "character": "d", "result": "correct" },
    ]
    words = [hello, world]
    if request.method == "POST":
        words.append(check_word(request.POST.get("word"), "hello"))
    return render(request, 'home.html', context={"words": words})