from django.shortcuts import redirect, render
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

# Create your views here.
@login_required

def home(request):
    if request.method=="POST":
        utilisateur_obj=Utilisateur.objects.get(user=request.user)
        link = Link.objects.create(nbr_vu=0,utilisateur=utilisateur_obj)
        link.save()
        link_obj = Link.objects.filter(utilisateur=utilisateur_obj)
        context = {'link':link_obj}
    else:
        utilisateur_obj = Utilisateur.objects.get(user=request.user)
        link=Link.objects.filter(utilisateur=utilisateur_obj)
        link_obj = Link.objects.filter(utilisateur=utilisateur_obj)
        context={'list_lik':link,'link':link_obj}
    return render(request,'home.html',context)

def link (request,id=0):
    link =Link.objects.get(pk=id)
    link.nbr_vu=link.nbr_vu+1
    link.save()
    context={'link':link}
    return render(request,'link.html',context)






def loginn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/loginn')

        utilisateur_obj = Utilisateur.objects.filter(user=user_obj).first()

        if not utilisateur_obj.is_verified:
            messages.success(request, 'User is not verified check your mail.')
            return redirect('/loginn')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/login')

        login(request, user)
        return redirect('/')

    return render(request, 'loginn.html')




def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).first():
            messages.success(request, 'Username is taken.')
            return redirect('/register')

        if User.objects.filter(email=email).first():
            messages.success(request, 'Email is taken.')
            return redirect('/register')

        user_obj = User(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()
        auth_token = str(uuid.uuid4())
        utilisateur_obj = Utilisateur.objects.create(user=user_obj, auth_token=auth_token)
        utilisateur_obj.save()
        send_mail_after_registration(email,auth_token)
        return redirect('/token')

    return render(request,'register.html')




def success(request):
    return render(request,'success.html')




def token_send(request):
    return render(request,'token_send.html')




def verify(request, auth_token):
    try:
        utilisateur_obj= Utilisateur.objects.filter(auth_token=auth_token).first()

        if utilisateur_obj:
            if utilisateur_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/loginn')
            utilisateur_obj.is_verified = True
            utilisateur_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/loginn')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return render(request,'error.html')

def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )


