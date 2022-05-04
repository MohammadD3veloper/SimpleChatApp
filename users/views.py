from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as dj_login, logout as lg_out
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from .tasks import send_verification_mail
from .forms import UserForm, MainUserForm
from .models import Users
import random
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from .backends import EmailBackend
from django.views import generic
from django.urls import reverse_lazy



authenticate = EmailBackend().authenticate


# Create your views here.
def login(request):
    if not request.user.is_authenticated:
        if request.method == "GET":
            form = UserForm()
            return render(request, 'users/login.html', {'form': form})
        elif request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get("email")
                code = form.cleaned_data.get("code")
                username = form.cleaned_data.get('username')
                try:
                    user, created = Users.objects.get_or_create(
                        username=username,
                        email=email,
                    )
                except IntegrityError:
                    return render(request, 'users/login.html', {'form': form, 'error': 'You are login with wrong username/email.'})
                user.code = code
                user.set_unusable_password()
                user.save()
                auth = authenticate(request, email=email, code=code)
                if isinstance(auth, get_user_model()):
                    print("There")
                    dj_login(request, auth)
                    return redirect('user:dashboard')
                else:
                    print(auth)
                    return render(request, 'users/login.html', {'form': form, 'error': auth})
            else:
                return render(request, 'users/login.html', {'form': form})
    else:
        return redirect("user:dashboard")


@login_required
def logout(request):
    lg_out(request)
    return render(request, 'chat/index.html', {})

@login_required
def dashboard(request):
    user = request.user
    return render(request, 'users/dashboard.html', {'user': user})


def send_code(request):
    if request.method == "POST":
        email = request.POST.get("email")
        code = random.randrange(10001, 99999)
        cache.set(email, code, 12000)
        send_verification_mail.delay(code, email)
        return JsonResponse({
            "success": "Code has been sent."
        })



class UserUpdateView(generic.UpdateView):
    model = Users
    form_class = MainUserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('user:dashboard')
