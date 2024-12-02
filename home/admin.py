from django.contrib import admin
from .models import MyFormModel, Lesson, Curriculum, Resource, Material


# Register your models here.
admin.site.register(MyFormModel)
admin.site.register(Lesson)
admin.site.register(Curriculum)
admin.site.register(Resource)
admin.site.register(Material)

