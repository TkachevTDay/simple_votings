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

def new_update_message(le,header,body):
    return{
        "heading": "heading"+str(le),
        "collapse": "collapse"+str(le),
        "header": header,
        "body": body,
    }

def index_page(request):

    last_updates = [
        [
            "Голосования",
            "Теперь можно выбирать какой-нибудь ответ. В зависимости от типа выборы: один из многих, несколько из многих и один из двух. + добавлена надпись о типе голосования"
        ],
        [
            "Дискретное голосование",
            "Теперь дискретное голосование состоит из выбора из двух сторон. (Короче два варианта в горизонтальной плоскости, удобно будет фото добавить)"
        ],
        [
            "Регистрация",
            "Рабочая регистрация пользователей с Именем, Фамилией, Никнэймом для сайта, почтой и паролем"
        ],
        [
            "Результаты",
            "Сбор результатов и их показ в процентном соотношении под голосовании (условие показа еще не сделано)"
        ],
        [
            "Добавление голосования",
            "Добавление голосования: название, описание, автор, без вариантов ответа"
        ],
        [
            "Устранение багов",
            "Пофикшен баг при просмотре голосования анонимусом, теперь они могут только смотреть голосование (возможно в будущем и результат, если голование закрыто), но не голосовать + предупреждение о невозможности голосовать"
        ],
        [
            "Лента новостей на главной странице",
            "Лента новостей для описания новых функций"
        ],
    ] # Пишите сюда свои обновления

    for i in range(len(last_updates)):
        last_updates[i] = new_update_message(i,last_updates[i][0],last_updates[i][1])


    context = {
        'menu': get_menu_context(),
        'last_updates': last_updates,
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
