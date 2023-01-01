from lib2to3.pgen2.tokenize import generate_tokens
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from site_1 import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import generate_token
from email.message import EmailMessage

from .forms import CreateNewUser, SignInForm

# Create your views here.
def home(request):
    return render(request,'main/index.html',{})

def signup(request):
    form = CreateNewUser()
    if request.method == 'POST':
        form = CreateNewUser(request.POST,request.FILES)

        if form.is_valid():
            username = form.cleaned_data['username']
            fname = form.cleaned_data['fname']
            lname = form.cleaned_data['lname']
            email = form.cleaned_data['email']
            pass1 = form.cleaned_data['pass1']
            pass2 = form.cleaned_data['pass2']

            if User.objects.filter(username=username):
                messages.error(request,"Username alrady exist! Please try some other username")
                return redirect('home')

            if User.objects.filter(email=email):
                messages.error(request,"Email alrady registered!")
                return redirect('home')

            if len(username) > 10:
                messages.error(request,"Username must be under 10 characters!")

            if pass1!=pass2:
                messages.error(request,"Passwords didn't match!")

            if not username.isalnum():
                messages.error(request,"Username must be Alpha-Numeric!")
                return redirect('home')


            myuser = User.objects.create_user(username,email,pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.isactive = False

            myuser.save()
            
            messages.success(request,'Your Account has been successfully created. We have sent you a confirmation email, please confirm your email in order to activate your account.')

            # Welcome Email
            subject = "Welcome to Site"
            message = "Hello " + myuser.first_name + "!! \nWelcome to our Site\nThank you for visiting our site\nPlease confirm your email address to activate your account. \n\n Thanking You"
            from_email = "noReply@gmail.com" #settings.EMAIL_HOST_USER
            to_list = [myuser.email]
            send_mail(subject, message, from_email, to_list,fail_silently=True)

            #Email address Configuration Email

            current_site = get_current_site(request)
            email_subject = "Confirm your email !"
            message2 = render_to_string('authentication/email_confirmation.html',{'name':myuser.first_name,
            'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
            })
            email = EmailMessage(email_subject,
            message2, 
            settings.EMAIL_HOST_USER,
            [myuser.email],
            )    
            email.fail_silently=True
            email.send() 


            from_email = "noReply@gmail.com" #settings.EMAIL_HOST_USER
            to_list = [myuser.email]
            send_mail(subject, message, from_email, to_list,fail_silently=True)



            return redirect('signin')        
        else: messages.error(request,'Form is not valid!')
    return render(request,'authentication/signup.html',{"form":form})

def signin(request):
    form = SignInForm()
    if request.method == 'POST':

        
        username = request.POST['username']
        pass1 = request.POST['pass1'] 

        user = authenticate(username=username,password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request,'main/index.html',{"form":form,'fname':fname})
        else:
            messages.error(request, 'Bad Credentials!')
            return redirect('home')
        
    return render(request,'authentication/signin.html',{"form":form})

def signout(request):
    logout(request)
    messages.success(request,'Logged Out Successfully')
    return redirect('home')

def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError,OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        myuser.save()

        login(request, myuser)
        return redirect('home')
    else:
        return render(request,'activation_failed.html')
