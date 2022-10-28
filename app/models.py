from django.db import models
# from django.contrib.auth.models import User, AbstractUser


class MyUser(models.Model):
    id_user = models.IntegerField()
    login = models.CharField(max_length=256)
    email = models.EmailField()
    nickname = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    avatar = models.ImageField(upload_to='media/')

class Question(models.Model):
    id_author_question = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    id_question = models.IntegerField()
    title_question = models.CharField(max_length=256)
    text_question = models.TextField()
    counting_likes = models.IntegerField()
    counting_answers = models.IntegerField()

class Tag(models.Model):
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    name_tag = models.CharField(max_length=256)

class Answer(models.Model):
    id_author_answer = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text_answer = models.TextField()
    correct = models.BooleanField()
