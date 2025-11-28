import random
from django.contrib.auth import login, get_user_model, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, FormView
from .forms import RegisterForm, VerifyForm, LoginUserForm, PasswordRecoveryEmailForm, PasswordRecoveryCodeForm
from .models import VerificationCodes

# def send_code(email, is_recovery):


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': "Authorisation"}
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('reg')

class RegisterView(CreateView):
    template_name = 'users/registrate.html'
    form_class = RegisterForm

    def get_success_url(self):
        return reverse_lazy('verify')
    def form_valid(self, form):
        user = form.save(commit=False)
        user.password = make_password(user.password)
        code = str(random.randint(100000, 999999))
        verif_code = VerificationCodes.objects.create(email=user.email, code=code)
        send_mail('Подтвердите почту', f'{code}', '-t', [f'{user.email}'])
        responce = super().form_valid(form)
        login(self.request, self.object)

        return responce


class VerifyEmail(FormView):
    template_name = 'users/verify.html'
    form_class = VerifyForm

    def get_success_url(self):
        return reverse_lazy('reg')
    def form_valid(self, form):
        email = self.request.user.email
        data = form.cleaned_data
        verif = VerificationCodes.objects.filter(email=email).latest('time_create')
        if verif and not verif.is_expired:
            if str(verif.code) == str(data['code']):
                user_to_verify = get_user_model().objects.get(email = email)
                user_to_verify.is_verified = True
                user_to_verify.save()
                return super().form_valid(form)
            else:
                code = str(random.randint(100000, 999999))
                verif_code = VerificationCodes.objects.create(email=email, code=code)
                send_mail('Подтвердите почту', f'{code}', '-t', [f'{email}'])
                return super().form_invalid(form)
        else:
            code = str(random.randint(100000, 999999))
            verif_code = VerificationCodes.objects.create(email=email, code=code)
            send_mail('Подтвердите почту', f'{code}', '-t', [f'{email}'])



class PasswordRecoveryEmail(FormView):
    form_class = PasswordRecoveryEmailForm
    template_name = 'users/recoveryemail.html'

    def get_success_url(self):
        return reverse_lazy('confirmation')
    def form_valid(self, form):
        email = form.cleaned_data['email']
        code = str(random.randint(100000, 999999))
        verif_code = VerificationCodes.objects.create(email=email, code=code, is_recovery = True)
        send_mail('Подтвердите почту', f'{code}', '-t', [f'{email}'])
        self.request.session['email'] = email
        return super().form_valid(form)


class PasswordRecoveryCode(FormView):
    form_class = PasswordRecoveryCodeForm
    template_name = 'users/recoveryemail.html'

    def get_success_url(self):
        return reverse_lazy('reg')

    def form_valid(self, form):
        email = self.request.session['email']
        code = form.cleaned_data['code']
        recovery = VerificationCodes.objects.filter(email=email).latest('time_create')
        if recovery and not(recovery.expires_at<timezone.now()) and recovery.is_recovery:
            if str(recovery.code) == str(code):
                return super().form_valid(form)
            else:
                code = str(random.randint(100000, 999999))
                verif_code = VerificationCodes.objects.create(email=email, code=code, is_recovery = True)
                send_mail('Подтвердите почту', f'{code}', '-t', [f'{email}'])
                return super().form_invalid(form)
        else:
            code = str(random.randint(100000, 999999))
            verif_code = VerificationCodes.objects.create(email=email, code=code, is_recovery = True)
            send_mail(str('1') , f'{code}', '-t', [f'{email}'])
            return super().form_invalid(form)






def logout_user(request):
    logout(request)
    return(redirect('reg'))