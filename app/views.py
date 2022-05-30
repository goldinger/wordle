from django.shortcuts import render

# Create your views here.


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
    
    return render(request, 'home.html', context={"words": [hello, world]})