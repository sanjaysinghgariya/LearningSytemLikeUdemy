from django.contrib import admin
from my_app import models
# Register your models here.

# class what_you_learn_TabularInLine(admin.TabularInline):
#     model = models.what_you_learn

# class Requirements_TabularInline(admin.TabularInline):
#     model = models.Requirements

# class Video_TabularInline(admin.TabularInline):
#     model = models.Video


# class course_admin(admin.ModelAdmin):
#     inlines = (what_you_learn_TabularInLine,Requirements_TabularInline, Video_TabularInline)


# admin.site.register(models.Course, course_admin)
admin.site.register([models.Course, models.Categories, models.Author,  models.Level
                     ,models.what_you_learn, models.Requirements, models.Lesson, models.Video, models.Language
                     ,models.CustomModelName, models.User_Course, models.Contactus, models.Comment])

# clpy