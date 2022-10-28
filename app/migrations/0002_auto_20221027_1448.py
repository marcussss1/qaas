# Generated by Django 4.1.2 on 2022-10-25 09:41

from django.db import migrations
from random import randrange
import random
import string


def random_word(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def completion_user(apps, schema_editor):
    MyUser = apps.get_model('app', 'MyUser')
    for i in range(randrange(1, 101)):
        MyUser.objects.create(id_user=i + 1,
                              login=random_word(randrange(8, 12)),
                              email=random_word(randrange(8, 10)) + "@gmail.com",
                              nickname=random_word(randrange(10, 12)),
                              password=random_word(randrange(8, 12)),
                              avatar="static/img/abc.jpg")


def completion_question(apps, schema_editor):
    Question = apps.get_model('app', 'Question')
    MyUser = apps.get_model('app', 'MyUser')
    counting_users = MyUser.objects.all().count()
    for i in range(randrange(1, 101)):
        Question.objects.create(id_author_question=MyUser.objects.get(id_user=randrange(1, counting_users)),
                                id_question=100 + i,
                                title_question=random_word(randrange(15, 20)),
                                text_question=random_word(randrange(50, 100)),
                                counting_likes=randrange(0, 10),
                                counting_answers=randrange(0, 5))


def completion_tag(apps, schema_editor):
    Tag = apps.get_model('app', 'Tag')
    Question = apps.get_model('app', 'Question')
    counting_questions = Question.objects.all().count()
    tags = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5']
    for i in range(1, counting_questions):
        counting_tags = randrange(4)
        for j in range(counting_tags):
            Tag.objects.create(id_question=Question.objects.get(id_question=i + 100),
                               name_tag=tags[randrange(0, counting_tags)])


def completion_answer(apps, schema_editor):
    Answer = apps.get_model('app', 'Answer')
    Question = apps.get_model('app', 'Question')
    MyUser = apps.get_model('app', 'MyUser')

    counting_questions = Question.objects.all().count()
    counting_users = MyUser.objects.all().count()

    for i in range(0, counting_questions):
        for j in range(Question.objects.get(id_question=i + 100).counting_answers):
            Answer.objects.create(id_author_answer=MyUser.objects.get(id_user=randrange(1, counting_users + 1)),
                                  id_question=Question.objects.get(id_question=i + 100),
                                  text_answer=random_word(100),
                                  correct=False)


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [migrations.RunPython(completion_user),
                  migrations.RunPython(completion_question),
                  migrations.RunPython(completion_tag),
                  migrations.RunPython(completion_answer)]
