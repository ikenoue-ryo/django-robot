from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import Schedule
from .models import User_Question

class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class EditForm(forms.ModelForm):
    class Meta:
        model = User_Question
        fields = '__all__'


class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = ('date', 'summary', 'description', 'start_time', 'end_time')
        widgets = {
            'date': forms.TextInput(attrs={
                'autocomplete': 'off',
                'class': 'form-control',
            }),
            'summary': forms.TextInput(attrs={
                'autocomplete': 'off',
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'autocomplete': 'off',
                'class': 'form-control',
            }),
            'start_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'end_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean_end_time(self):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        if end_time <= start_time:
            raise forms.ValidationError(
                '終了時間は、開始時間よりも後にしてください'
            )
        return end_time