import datetime

from django.shortcuts import render, get_object_or_404
from .models import Voting
from .models import VoteVariant
from .models import VoteFact
from django.contrib.auth import get_user_model


def get_menu_context():
    return [
        {'url_name': 'index', 'name': 'Главная'},
        {'url_name': 'time', 'name': 'Текущее время'},
        {'url_name': 'votings', 'name': 'Голосования'}
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
    context = {
        'menu': get_menu_context(),
        'votings': Voting.objects.all(),
    }
    return render(request, 'pages/votings.html', context)


def time_page(request):
    context = {
        'pagename': 'Текущее время',
        'time': datetime.datetime.now().time(),
        'menu': get_menu_context()
    }
    return render(request, 'pages/time.html', context)


def vote_page(request, vote_id):
    voting = get_object_or_404(Voting, id=vote_id)
    vote_variants = VoteVariant.objects.filter(voting=vote_id)
    current_user = request.user
    vote_facts = VoteFact.objects.filter(user=current_user, variant__voting=voting)

    view_result = True
    results = VoteFact.objects.filter(variant__voting=voting)
    len_results = len(results)
    result_percents = []
    for i in vote_variants:
        result_percents.append([i.description,int(len(VoteFact.objects.filter(variant=i)) / len_results * 100)]) # процент голосования с 1 знаком после запятой

    print(result_percents)

    #for i,j in zip([1,2,3],[4,5,6]):
        #print(i,j)
    context = {
        'pagename': 'Vote page',
        'menu': get_menu_context(),
        'author': voting.author,
        "vote": voting,
        "vote_variants": vote_variants,
        "vote_fact": vote_facts.first(),
        "view_result": view_result,
        "result_percents": result_percents,
    }
    # todo: make vote fact
    return render(request, 'pages/vote.html', context)
