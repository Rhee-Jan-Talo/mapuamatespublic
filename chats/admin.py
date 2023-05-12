from django.contrib import admin
from .models import *
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

admin.site.register(ChatMessage)

class ChatMessage(admin.TabularInline):
    model = ChatMessage


class ThreadForm(forms.ModelForm):
    def clean(self):
        super(ThreadForm, self).clean()
        first_person = self.cleaned_data.get('first_person')
        second_person = self.cleaned_data.get('second_person')

        lookup1 = Q(first_person=first_person) & Q(second_person=second_person)
        lookup2 = Q(first_person=second_person) & Q(second_person=first_person)
        lookup = Q(lookup1 | lookup2)
        qs = Thread.objects.filter(lookup)
        if qs.exists():
            raise ValidationError(f'Thread between {first_person} and {second_person} already exists')
        

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    form = ThreadForm 
    class Meta:
        model = Thread


admin.site.register(Thread, ThreadAdmin)

