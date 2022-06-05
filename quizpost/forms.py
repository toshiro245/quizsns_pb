from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import QuizPost


class QuizCreateForm(forms.ModelForm):
    title = forms.CharField(label='タイトル')
    problem = forms.CharField(
        label='問題', 
        widget=SummernoteWidget(attrs={
            'summernote': {
                'toolbar': [['insert', ['picture']]],
                'width': '100%',
                'height': '300px',
                }
            
        })
    )
    hint = forms.CharField(label='ヒント', widget=forms.Textarea(attrs={'rows':5, 'cols':100}), required=False)
    answer = forms.CharField(
        label='答え',
        widget=SummernoteWidget(attrs={
            'summernote': {
                'toolbar': [['insert', ['picture']]],
                'width': '100%',
                'height': '300px',
            }
        })
    )

    class Meta:
        model = QuizPost
        fields = ('title', 'problem', 'hint', 'answer')
        widgets = {
            'problem': SummernoteWidget(),
            'answer': SummernoteWidget(),
        }


    def __init__(self, *args, **kwargs):
        super(QuizCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form'
        self.fields['problem'].widget.attrs['class'] = 'form'
        self.fields['hint'].widget.attrs['class'] = 'form'
        self.fields['answer'].widget.attrs['class'] = 'form'

    
    def save(self, commit=False):
        quiz = super().save(commit=False)
        quiz.user = self.user
        quiz.save()
        return quiz