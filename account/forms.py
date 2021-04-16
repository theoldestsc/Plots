from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label = 'Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = str(self[field].name)

    def as_input(self):
        return self._html_output(
            normal_row=u'%(field)s %(help_text)s %(errors)s',
            error_row=u'<div class="error">%s</div>',
            row_ender='</div>',
            help_text_html=u'',
            errors_on_separate_row=False)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    class Meta:
        model = User
        fields = ('email', 'username', 'password')