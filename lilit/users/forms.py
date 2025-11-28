from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


class LoginUserForm(AuthenticationForm):
    class Meta:
        model=get_user_model()
        fields=['email','password']

class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username','email', 'password1', 'password2']

    # def cleaned_email(self):
    #     email = self.cleaned_data['email']
    #     if get_user_model().objects().filter(email=email).exist():
    #         raise forms.ValidationError('Email already exist')
    #     return email


class VerifyForm(forms.Form):
    code = forms.CharField(
        label='Введите 6-значный код',
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={'placeholder': '123456'})
    )


class PasswordRecoveryEmailForm(forms.Form):
    email = forms.CharField(
        label='Введите вашу почту',
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not get_user_model().objects.filter(email=email).exists():

            raise forms.ValidationError(
                "Пользователя с таким email не существует. Пожалуйста, проверьте ввод или зарегистрируйтесь.",
                code='user_not_found'
            )
        return email


class PasswordRecoveryCodeForm(forms.Form):
    code = forms.CharField(
        label='Введите 6-значный код',
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={'placeholder': '123456'})
    )
