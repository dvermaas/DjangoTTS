from django.contrib import admin

from .models import Sequence, Question, Choice, Vote


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 0

class SequenceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['sequence_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [QuestionInline]
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text', 'sequence']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]



admin.site.register(Sequence, SequenceAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Vote)
