from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm
from .forms import SignUpForm
from .models import MyUser
from django.utils import timezone
from django.core.mail import send_mail
from django.http import JsonResponse
import random


def log_in(request):
    if request.method == "POST":
        usernm = request.POST.get("username")
        passwd = request.POST.get("password")

        user = authenticate(request, username=usernm, password=passwd)

        if user is not None:
            login(request, user)
            return redirect("/myapp") #aaa
        else:
            messages.error(request, "Invalid username or email, or incorrect password. Please try again.")
            return redirect("/myapp/login?state=loginfail") #aaa
    else:
        form = LoginForm()

    return render(request, "myapp/login.html", {"form": form})
        #aaa

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            stored_code = request.session.get('verification_code')
            code_sent_at = request.session.get('code_sent_at')

            if stored_code and code_sent_at:
                elapsed_time = timezone.now().timestamp() - code_sent_at
                if elapsed_time > 600:
                    form.add_error('verification_code', 'Verification code has expired.')
                elif stored_code != form.cleaned_data['verification_code']:
                    form.add_error('verification_code', 'Invalid verification code.')
                else:
                    username = form.cleaned_data['username']
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password']
                    user = MyUser.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    messages.success(request, 'Sign up successful!')
                    return redirect('home') #aaa
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'signup.html', {'form': form})

    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

def send_verification_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            code = random.randint(100000, 999999) 

            send_mail(
                'Your verification code',
                f'Your verification code is {code}',
                'zhang0129pia@gmail.com',
                [email],
                fail_silently=False,
            )

            request.session['verification_code'] = code
            request.session['code_sent_at'] = timezone.now().timestamp()

            return JsonResponse({'status': 'ok', 'message': 'Verification code sent'})
        return JsonResponse({'status': 'error', 'message': 'Invalid email'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})