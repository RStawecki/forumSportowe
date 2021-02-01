from django.shortcuts import render, redirect
from accounts.forms import SignUpForm
from accounts.models import User
from django.db import IntegrityError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from verify_email.email_handler import send_verification_email
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

def signupuser(request):
    if request.method == "GET":
        return render(request, 'accounts/signupuser.html', {'form': SignUpForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['email'], request.POST['password1'])
            except IntegrityError:
                error = "Email already exists in our system. Log in or use different email."
                return render(request, 'accounts/signupuser.html', {'form': SignUpForm(), 'error': error})
            else:
                try:
                    validate_password(request.POST['password1'], user)
                except ValidationError as e:
                    return render(request, 'accounts/signupuser.html', {'form': SignUpForm(), 'passwordError': e, 'email': request.POST['email']})
                else:
                    #msg = EmailMessage('Witaj na naszym forum', 'Mamy nadzieje, że forum bedzie pomocne.', 'Forum Sportowe<rafiks28@gmail.com>', [request.POST['email']])
                    #msg.send()
                    #user.save()
                    try:
                        inactive_user = send_verification_email(request, form=SignUpForm(request.POST)) #zapis do bazy danych
                    except ValueError:
                        emailTaken = "This email already exists in our system. Log in or use different email."
                        return render(request, 'accounts/signupuser.html', {'emailTaken': emailTaken})
                    else:
                        #informacja aby zweryfikować maila
                        return redirect('home')
        else:
            error = "Passwords did not match."
            return render(request, 'accounts/signupuser.html', {'form': SignUpForm(), 'error': error})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'accounts/loginuser.html', {'form': AuthenticationForm()})
    else:
        #pobieram mail z formularza (tworzę zmienną)
        #sprawdzam czy user o podanym emailu istnieje
        #sprawdzam czy user o podanym mailu i statusie is_active=True istnieje
        #jeżeli wszystko jest ok logujemy
        email = request.POST['username']
        user = User.objects.filter(email=email)
        if not user.exists():
            wrongEmail = "Email not found. Try again or register."
            return render(request, 'accounts/loginuser.html', {'form': AuthenticationForm(), 'wrongEmail': wrongEmail})
        else:
            userActive = User.objects.filter(email=email, is_active=True)
            if not userActive.exists():
                notActive = "Your account is not active. Check your inbox for verification email."
                return render(request, 'accounts/loginuser.html', {'form': AuthenticationForm(), 'notActive': notActive})
            else:
                user = authenticate(email=request.POST['username'], password=request.POST['password'])
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    error = "Password is incorrect."
                    return render(request, 'accounts/loginuser.html', {'form': AuthenticationForm(), 'passwordError': error})

def logoutuser(request):
    if request.method =="POST":
        logout(request)
        return redirect('home')
