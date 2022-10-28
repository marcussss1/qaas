from django.contrib import admin
from app.models import MyUser
from app.models import Question
from app.models import Tag
from app.models import Answer

# Register your models here.
admin.site.register(MyUser)
admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Answer)
