from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect
from participants.models import ParticipantGame, ParticipantResults
from questions.question_paper_models import QPForm
from questions.question_models import QForm
from .models import Game, GameForm


def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    
    return group in user.groups.all()



def format_time(seconds): 
    minutes, seconds = divmod(seconds, 60) 

    hours, minutes = divmod(minutes, 60) 

    minutes += hours * 60

    return f'{minutes:.2f}:{seconds:.2f}'


@login_required(login_url='units:login')
def view_games_creator(request):
    creator = request.user

    creator_user = User.objects.get(username=creator)

    permissions = has_group(creator, 'Creator') if creator else False

    if permissions:
        form = GameForm(creator_user)

        if request.method == 'POST' and permissions:

            form = GameForm(creator_user, request.POST)

            if form.is_valid():
                game = form.save(commit=False)
                game.creator = creator
                game.save()

                form.save_m2m()

                return redirect('questions:view_games')

        games = Game.objects.filter(creator=creator)

        context = {
            'games': games,
            'game_form': form,
            'creator': creator
        }

        return render(request, 'games/main-game.html', context)

    return redirect('questions:view_games_participant')


@login_required(login_url='units:login')
def add_question_paper(request):
    creator = request.user

    creator_user = User.objects.get(username=creator)

    permissions = has_group(creator, 'Creator') if creator else False

    if permissions:
        form = QPForm(creator_user)

        if request.method == 'POST' and permissions:
            form = QPForm(creator_user, request.POST)

            if form.is_valid():
                game = form.save(commit=False)
                game.creator = creator_user
                game.save()

                form.save_m2m()

                return redirect('questions:add_question_paper')

        games = Game.objects.filter(creator=creator)

        context = {
            'games': games,
            'game_form': form,
            'creator': creator
        }

        return render(request, 'games/add-question.html', context)

    return redirect('questions:view_games_participant')


@login_required(login_url='units:login')
def add_questions(request):
    creator = request.user

    creator_user = User.objects.get(username=creator)

    permissions = has_group(creator, 'Creator') if creator else False

    if permissions:
        form = QForm()

        if request.method == 'POST' and permissions:
            form = QForm(request.POST)

            if form.is_valid():
                game = form.save(commit=False)
                game.creator = creator_user
                game.save()

                form.save_m2m()

                return redirect('questions:add_questions')

        games = Game.objects.filter(creator=creator)

        context = {
            'games': games,
            'game_form': form,
            'creator': creator
        }

        return render(request, 'games/add-questions.html', context)

    return redirect('questions:view_games_participant')


@login_required(login_url='units:login')
def view_previous_games_creator(request):
    creator = request.user

    games = Game.objects.filter(creator=creator)

    context = {
        'games': games,
        'creator': creator
    }

    return render(request, 'games/previous-game.html', context)


@login_required
def participant_view_previous(request):
    games = Game.objects.all()

    uncompleted = []
    completed = []

    for game in games:
        if ParticipantGame.objects.filter(game_name=game.name, participant=request.user).exists() and ParticipantGame.objects.get(game_name=game.name,participant=request.user).completed:
            completed.append(game)

        else:
            uncompleted.append(game)

    context = {
        'games': uncompleted,
        'completed': completed
    }

    return render(request,'games/previous_participants.html', context)


@login_required(login_url='units:login')
def view_participants_creator(request):
    participants = User.objects.filter(groups__name='Participant')

    participant_name = []
    participant_completed = []
    count = 0
    dicts = {}

    gamen = Game.objects.filter(creator=request.user)

    for participant in participants:
        participant_name.append(participants.username)

        count = 0

        for game in gamen:
            count += ParticipantGame.objects.filter(participant=participant, game_name=game.name, completed=1).exists()

        participant_completed.append(count)

    for i, x in enumerate(participant_name):
        dicts[x] = participant_completed[i]

    context = {
        'participants': dicts
    }

    return render(request, 'games/participants.html', context)


@login_required(login_url='units:login')
def view_results_creator(request):
    participants = User.objects.filter(groups__name='Participant')

    dicts = {}

    creator = User.objects.get(username=request.user.username)

    gamen = Game.objects.filter(creator=creator)

    for game in gamen:
        if ParticipantGame.objects.filter(game_name=game.name, completed=1).exists():
            participants_filter = ParticipantGame.objects.filter(game_name=game.name, completed=1)

            for participant in participants_filter:
                key = str(participants.participant) + ' ' + str(participants.game_name) + ' ' + str(participants.question_paper.title)

                dicts[key] = participants.score

    context = {
        'participants': dicts
    }

    return render(request, 'games/participants-results.html', context)


@login_required
def view_games_participant(request):
    games = Game.objects.all()

    uncompleted = []
    completed = []

    for game in games:
        if ParticipantGame.objects.filter(game_name=game.name, participant=request.user).exists() and ParticipantGame.objects.get(game_name=game.name, participant=request.user).completed:
            completed.append(game)

        else:
            uncompleted.append(game)

    context = {
        'games': uncompleted,
        'completed': completed
    }

    return render(request, 'games/main-game-participants.html', context)


@login_required
def view_participant_attendance(request):
    games = Game.objects.all()

    uncompleted = []
    completed = []

    for game in games:
        if ParticipantGame.objects.filter(game_name=game.name, participant=request.user).exists() and ParticipantGame.objects.get(game_name=game.name, participant=request.user).completed:
                completed.append(game)

        else:
            uncompleted.append(game)

    context = {
        'games': uncompleted,
        'completed': completed
    }

    return render(request,'games/attendance.html', context)


@login_required
def appear_game(request,id):
    participant = request.user
    if request.method == 'GET':
        game = Game.objects.get(pk=id)

        time_delta = game.end_time - game.start_time

        time = format_time(time_delta.seconds)
        time = time.split(':')

        minutes = time[0]
        seconds = time[1]

        context = {
            'game': game,
            'question_list': game.QuestionPaper.questions.all(),
            'minutes': minutes,
            'seconds': seconds
        }

        return render(request, 'games/start-game.html', context)

    if request.method == 'POST' :
        participant = User.objects.get(username=request.user.username)

        paper = request.POST['paper']

        main_game = Game.objects.get(name = paper)

        participant_game = ParticipantGame.objects.get_or_create(
            game_name=paper,
            participant=participant,
            question_paper = main_game.QuestionPaper
        )[0]
        
        question_paper = main_game.QuestionPaper

        participant_game.question_paper = question_paper
         
        question_paper_list = main_game.QuestionPaper.questions.all()

        for question in question_paper_list:
            participant_question = ParticipantQuestion(
                participant=participant,
                question=question.question,
                optionA=question.optionA,
                answer=question.answer
            )
            participant_question.save()
            participant_game.questions.add(participant_question)
            participant_game.save()

        participant_game.completed = 1

        participant_game.save()

        game_questions_list = ParticipantGame.objects.filter(
            participant=request.user,
            game_name=paper,
            question_paper=main_game.QuestionPaper,
            questions__participant = request.user
        )[0]

        game_score = 0

        list_i = main_game.QuestionPaper.questions.all()

        questions_list = game_questions_list.questions.all()

        i = 0

        for j in range(list_i.count()):
            question = questions_list[j]

            max_marks = list_i[i].max_marks

            answer = request.POST.get(question.question, False)

            if not answer:
                answer = 'E'

            question.choice = answer

            question.save()

            if answer.lower() == question.answer.lower() or answer == question.answer:
                game_score = game_score + max_marks

            i += 1

        participant_game.score = game_score
        participant_game.save()

        participant = ParticipantGame.objects.filter(participant=request.user, game_name=main_game.name)  

        results = ParticipantResults.objects.get_or_create(participant=request.user)[0]
        results.games.add(participant[0])
        results.save()

        return redirect('questions:view_games_participant')


@login_required
def result(request,id):
    participant = request.user

    game = Game.objects.get(pk=id)

    score = ParticipantGame.objects.get(participant=participant,game_name=game.name,question_paper=game.QuestionPaper).score

    return render(request,'games/result.html',{'game':game,'score':score})
