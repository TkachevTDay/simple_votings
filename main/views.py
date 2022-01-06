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
        'pagename': 'Голосования',
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
    vote_facts_variants = []
    current_user = request.user

    if request.method == 'POST':
        if not current_user.is_anonymous:
            vote = request.POST.get("VOTE")
            if (vote):
                variant = VoteVariant.objects.get(id = vote)

                isexist = VoteFact.objects.filter(user=current_user, variant__voting=voting)# голосовал ли ранее
                if(not isexist) or voting.type == 2:
                    if not VoteFact.objects.filter(user=current_user, variant = variant).exists():
                        VoteFact(user=current_user, variant=variant).save()
                    else:
                        print("Голос уже засчитан")
                else:
                    print("Голос уже засчитан")

    if not current_user.is_anonymous:
        vote_facts = VoteFact.objects.filter(user=current_user, variant__voting=voting)
        for i in vote_facts:
            vote_facts_variants.append(i.variant)
    context = {
        'pagename': 'Vote page',
        'menu': get_menu_context(),
        'author': voting.author,
        "vote": voting,
        "vote_variants": vote_variants,
        "vote_fact": vote_facts_variants,
    }

    # todo: make vote fact
    return render(request, 'pages/vote.html', context)
