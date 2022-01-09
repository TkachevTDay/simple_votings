import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import AddVotingForm
from .models import Voting
from .models import VoteVariant
from .models import VoteFact
from django.shortcuts import render, get_object_or_404
from .models import Voting, VoteFact, VoteVariant, User
from django.contrib.auth import get_user_model
from .forms import UserForm
from django.shortcuts import render, get_object_or_404
from .models import Voting, VoteFact, VoteVariant, User


def get_menu_context():
    return [
        {'url_name': 'index', 'name': 'Главная'},
        {'url_name': 'time', 'name': 'Текущее время'},
        {'url_name': 'votings', 'name': 'Голосования'},
        {'url_name': 'votings', 'name': 'Голосования'},
        {'url_name': 'vote_add', 'name': 'Создать'},
        {'url_name': 'votings', 'name': 'Голосования'},
        {'url_name': 'registration', 'name': 'Регистрация'}
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
    vote_facts = []
    vote_facts_variants = []
    is_anonymous = current_user.is_anonymous
    if not is_anonymous:
        vote_facts = VoteFact.objects.filter(user=current_user, variant__voting=voting)
        for i in vote_facts:
            vote_facts_variants.append(i.variant)
    is_anonymous = current_user.is_anonymous
    if request.method == 'POST':
        if not is_anonymous:
            vote = request.POST.get("VOTE")
            if (vote):
                variant = VoteVariant.objects.get(id = vote)

                isexist = VoteFact.objects.filter(user=current_user, variant__voting=voting)# голосовал ли ранее
                if(not isexist) or voting.type == 2:
                    if not VoteFact.objects.filter(user=current_user, variant = variant).exists():
                        VoteFact(user=current_user, variant=variant).save()

    if not is_anonymous:
        vote_facts = VoteFact.objects.filter(user=current_user, variant__voting=voting)
        for i in vote_facts:
            vote_facts_variants.append(i.variant)

    allow_vote = True

    if is_anonymous:
        allow_vote = False
    #todo: при закрытом голосовании также запрещать голосовать

    types = [
        "Выберите один из двух вариантов ответа",
        "Выберите один из вариантов ответа",
        "Выберите один или несколько вариантов ответа",
    ]

    str_type = types[voting.type]
    context = {
        'pagename': 'Vote page',
        'menu': get_menu_context(),
        'author': voting.author,
        "vote": voting,
        "vote_variants": vote_variants,
        "vote_fact": vote_facts_variants,
        "is_anonymous": is_anonymous,
        "allow_vote": allow_vote,
        "str_type": str_type,
        "type": voting.type,
    }

    # todo: make vote fact
    return render(request, 'pages/vote.html', context)

def profile(request):
    current_user = request.user
    current_user = User.objects.get(id=current_user.id)

    user_votings = Voting.objects.filter(author=current_user)

    context = {
        'pagename': 'Профиль',
        'menu': get_menu_context(),
        'author': current_user,
        'user_votings': user_votings,
    }
    return render(request, 'pages/profile.html', context)


def register(request):
    error_name_alredy_exsist = False
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid() and not User.objects.filter(username=form.cleaned_data.get("username")).exists():
            user = User.objects.create_user(form.cleaned_data.get("username"),
                                            form.cleaned_data.get("email"),
                                            form.cleaned_data.get("password"))
            user.first_name, user.last_name = form.cleaned_data.get("first_name"), form.cleaned_data.get("last_name")
            user.save()
            return render(request, 'registration/registration_done.html', {'new_user': user})
        else:
            if User.objects.filter(username=form.cleaned_data.get("username")).exists():
                error_name_alredy_exsist = True
            form = UserForm()
    else:
        form = UserForm()

    context = {
        'pagename': 'Регистрация',
        'menu': get_menu_context(),
        'form': form,
        'error_name_alredy_exsist': error_name_alredy_exsist
    }

    return render(request, 'registration/registration.html', context)

@login_required
def add_voting(request):
    context = {
        'menu': get_menu_context()
    }
    if request.method == 'GET':
        context['form'] = AddVotingForm()
    if request.method == 'POST':
        context['form'] = AddVotingForm(request.POST)
        if context['form'].is_valid():
            record = Voting(
                name=context['form'].cleaned_data['name'],
                description=context['form'].cleaned_data['description'],
                type=context['form'].cleaned_data['vote_type'],
                author=request.user
            )
            record.save()
            return redirect(reverse('vote', kwargs={'vote_id': record.id}))
    return render(request, 'pages/add_voting.html', context)
