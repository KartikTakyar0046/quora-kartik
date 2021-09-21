from .models import *
from django.forms import ModelForm
class AskQuestionForm(ModelForm):
    class Meta:
        model=Question
        fields=['body','tags']

class AddAnswer(ModelForm):
    class Meta:
        model=Answer
        fields=['body']
