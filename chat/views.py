from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm
from .models import Message

def register_view(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('user_list')
    else:
        form = RegisterForm()
    return render(request,'chat/register.html',{'form':form})

def login_view(request):
    form=LoginForm(data=request.POST or None)
    if request.method=='POST' and form.is_valid():
        login(request,form.get_user())
        return redirect('user_list')
    return render(request,'chat/login.html',{'form':form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def user_list_view(request):
    users=User.objects.exclude(id=request.user.id)
    return render(request,'chat/user_list.html',{'users':users})

# @login_required
# def home(request):
#     users = User.objects.exclude(id=request.user.id)
#     return render(request, 'chat/home.html', {'users': users})

@login_required
def chat_room(request,username):
    other_user=get_object_or_404(User,username=username)
    messages=Message.objects.filter(
        sender__in=[request.user,other_user],
        receiver__in=[request.user,other_user]
    ).order_by("timestamp")
    return render(request, "chat/chat_room.html", {
        "other_user":other_user,
        "messages":messages
    })


def home(request):
    if request.user.is_authenticated:
        users=User.objects.exclude(id=request.user.id)
    else:
        users=User.objects.none()  # or some default queryset or message
    return render(request,'chat/home.html',{'users':users})
