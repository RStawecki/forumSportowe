from django.shortcuts import render, redirect
from accounts.forms import SignUpForm
from accounts.models import User
from django.db import IntegrityError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from verify_email.email_handler import send_verification_email

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
