from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from app.models import MyUser
from app.models import Question
from app.models import Tag
from app.models import Answer
from app.forms import LoginForm
from app.forms import RegistrationForm

# Create your views here.

best_tags = {}
best_tags_list = []

best_members = {}
best_members_list = []

###Если делаешь чето с БД, то это всё нужно закомментить###


for tag in Tag.objects.all():
    if tag.name_tag in best_tags:
        best_tags[tag.name_tag] += 1
    else:
        best_tags[tag.name_tag] = 1

for answer in Answer.objects.all():
    if answer.id_author_answer.id_user in best_members:
        best_members[answer.id_author_answer.id_user] += 1
    else:
        best_members[answer.id_author_answer.id_user] = 1

##############################################################

best_members = dict(sorted(best_members.items(), key=lambda item: item[1], reverse=True))
best_tags = dict(sorted(best_tags.items(), key=lambda item: item[1], reverse=True))

max_best_members = 3
counter = 0

for user in best_members:
    if counter == max_best_members:
        break
    best_members_list.append(MyUser.objects.get(id_user=user))
    counter += 1

for tag_name in best_tags:
    best_tags_list.append(tag_name)


def index(request):
    objects_list = Question.objects.all()

    paginator = Paginator(objects_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'best_members': best_members_list,
                                          'best_tags': best_tags_list,
                                          'tags': Tag.objects.all(),
                                          'page_obj': page_obj,
                                          'paginator': paginator})


# @login_required()
# def ask(request):
#     if request.method == 'POST':
#         q_form = QuestionForm(data=request.POST)
#         if q_form.is_valid():
#             Question(**q_form.cleaned_data) # или вручную заполнить поля
#             Question.save()

@login_required(login_url='/login/')
def question(request, i: int):
    return render(request, 'page_question.html', {'best_members': best_members_list,
                                                  'best_tags': best_tags_list,
                                                  'question': Question.objects.get(id_question=i),
                                                  'tags': Tag.objects.all()})


@login_required(login_url='/login/')
def answers(request, i: int):
    question = Question.objects.get(id_question=i)
    objects_list = []

    for answer in Answer.objects.all():
        if answer.id_question.id_question == i:
            objects_list.append(answer)

    paginator = Paginator(objects_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'page_answers.html', {'best_members': best_members_list,
                                                 'best_tags': best_tags_list,
                                                 'answers': Answer.objects.all(),
                                                 'question': question,
                                                 'tags': Tag.objects.all(),
                                                 'questions': Question.objects.all(),
                                                 'page_obj': page_obj,
                                                 'paginator': paginator})


@login_required(login_url='/login/')
def tag(request, tag_name: str):
    objects_list = []

    for tag in Tag.objects.all():
        if tag.name_tag == tag_name:
            objects_list.append(Question.objects.get(id_question=tag.id_question.id_question))

    paginator = Paginator(objects_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listing_po_tegu.html', {'best_members': best_members_list,
                                                    'best_tags': best_tags_list,
                                                    'find_tag': tag_name,
                                                    'tags': Tag.objects.all(),
                                                    'page_obj': page_obj,
                                                    'paginator': paginator})


@login_required(login_url='/login/')
def settings(request):
    return render(request, "settings.html")


def login(request):
    if request.method == "GET":
        form = LoginForm()
    elif request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(**form.cleaned_data)
            if not user:
                form.add_error(None, "User not found")
            else:
                auth.login(request, user)
                return redirect('/')
    return render(request, "login.html", {'form': form})


def registration(request):
    print(request.POST)
    if request.method == 'GET':
        form = RegistrationForm()
    elif request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            User.objects.create_user(username=form.cleaned_data['login'],
                                     email=form.cleaned_data['email'],
                                     password=form.cleaned_data['password'])
            MyUser.objects.create(id_user=MyUser.objects.all().count() + 1,
                                  login=form.cleaned_data['login'],
                                  email=form.cleaned_data['email'],
                                  nickname=form.cleaned_data['nickname'],
                                  password=form.cleaned_data['password'],
                                  avatar=form.cleaned_data['avatar'])
            return redirect('/login/')





            # user = form.save()
            # user.profile.nickname = form.cleaned_data.get('nickname')
            # user.profile.avatar = request.FILES.get('avatar', None)
            # user.save()
            # user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            # if user is not None:
            #     auth.login(request, user)
            #     return redirect('index')

        # data = request.POST
        # form = RegistrationForm(request.POST)
        # if form.is_valid():
        #     MyUser.objects.create(id_user=MyUser.objects.all().count() + 1,
        #                           login=data['login'],
        #                           email=data['email'],
        #                           nickname=data['nickname'],
        #                           password=data['password'],
        #                           avatar=request.FILES)  # почему-то на этом поле крашится...
        #     User.objects.create_user(username=data['login'],
        #                              email=data['email'],
        #                              password=data['password'])
        #     return redirect('/login/')
    return render(request, "registration.html", {'form': form})


@login_required(login_url='/login/')
def new_ask(request):
    return render(request, "new_ask.html")
