from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import * 
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str 
from django.core.mail import EmailMessage
from django.contrib import messages
from .tokens import account_activation_token

# Create your views here.

@login_required
def dashboard(request):
    return render(request, 'registration/dashboard.html', {'section': 'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
            user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
        
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html',{'user_form': user_form})

def activate(request, uidb64, token):
    return redirect('base.html')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account"
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid':  urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
        })
    email = EmailMessage(mail_subject,message,to=[to_email])
    if email.send():
        messages.success(request, 'sent')
    else:
        messages.error(request, 'ERROR')