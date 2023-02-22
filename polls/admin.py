from django.contrib import admin

from .models import Enquete, Question, Choice, Vote


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 0

class EnqueteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [QuestionInline]
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['text', 'enquete']}),
    ]
    inlines = [ChoiceInline]



admin.site.register(Enquete, EnqueteAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Vote)
