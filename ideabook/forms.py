from django.forms import ModelForm, Textarea

from .models import Idea, Suggestion

class PostForm(ModelForm):
  class Meta:
    model = Idea
    fields = ['idea_text']
    widgets = {
      'idea_text': Textarea(attrs={'class' : 'input', 'placeholder' : 'Write your idea here...','rows':'3','cols':'70'}),
    }

class SuggForm(ModelForm):
  class Meta:
    model = Suggestion
    fields = ['sugg_text']
    widgets = {
      'sugg_text': Textarea(attrs={'class' : 'input', 'placeholder' : 'Write your idea here...','rows':'3','cols':'70'}),
    }