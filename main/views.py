import datetime

from django.shortcuts import render
from .models import Voting
from .models import VoteVariant
from django.contrib.auth import get_user_model


def get_menu_context():
    return [
        {'url_name': 'index', 'name': 'Главная'},
        {'url_name': 'time', 'name': 'Текущее время'},
        {'url_name': 'votings', 'name': 'Голосования'},
        {'url_name': 'vote', 'name': 'Hard-coded Vote'},
    ]


def index_page(request):
    context = {
        'pagename': 'Главная',
        'author': 'Andrew',
        'pages': 4,
        'menu': get_menu_context()
    }
    return render(request, 'pages/index.html', context)

def votings(request):
    votings = []
    users = get_user_model()
    for i in Voting.objects.all():
        votings.append({'author': users.objects.get(id = i.author), 'voting': i.name, 'id': i.id})
    context = {
        'menu': get_menu_context(),
        'votings': votings,
    }
    return render(request, 'pages/votings.html', context)


def time_page(request):
    context = {
        'pagename': 'Текущее время',
        'time': datetime.datetime.now().time(),
        'menu': get_menu_context()
    }
    return render(request, 'pages/time.html', context)

def vote_page(request):
    vote_id = request.GET.get("vote_id", None)

    if not vote_id:
        return render(request, 'pages/404.html')

    vote_content = Voting.objects.get(id = vote_id)

    vote_variants = []
    for i in VoteVariant.objects.filter(voting=vote_id):
        vote_variants.append({"voting": i.voting,"description": i.description})

    users = get_user_model()

    context = {
        'pagename': 'Vote',
        'menu': get_menu_context(),
        'author': users.objects.get(id=vote_content.author),
        "vote_name": vote_content.name,
        "vote_description": vote_content.description,
        "vote_variants": vote_variants,
    }
    #todo add voting_variants (working)

    return render(request, 'pages/vote.html', context)
