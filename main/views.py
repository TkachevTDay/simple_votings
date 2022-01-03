import datetime

from django.shortcuts import render, get_object_or_404
from .models import Voting, VoteFact, VoteVariant, User
from django.contrib.auth import get_user_model
from .forms import UserForm


def get_menu_context():
    return [
        {'url_name': 'index', 'name': 'Главная'},
        {'url_name': 'time', 'name': 'Текущее время'},
        {'url_name': 'votings', 'name': 'Голосования'},
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

    context = {
        'pagename': 'Vote page',
        'menu': get_menu_context(),
        'author': voting.author,
        "vote": voting,
        "vote_variants": vote_variants,
        "vote_fact": vote_facts.first(),
    }

    # todo: make vote fact
    return render(request, 'pages/vote.html', context)


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid() and not User.objects.filter(username=form.cleaned_data.get("username")).exists():
            user = User.objects.create_user(form.cleaned_data.get("username"),
                                            form.cleaned_data.get("email"),
                                            form.cleaned_data.get("password"))
            user.first_name, user.last_name = form.cleaned_data.get("first_name"), form.cleaned_data.get("last_name")
            user.save()
        else:
            form = UserForm()
    else:
        form = UserForm()
    return render(request, 'registration/registration.html', {'form': form})
