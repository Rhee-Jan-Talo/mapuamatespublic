from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Thread
from accounts.models import User
from django.db.models import Q

@login_required
def MessagesInbox(request):
    users = User.objects.all()
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by("-id")
    try:
        chatthread = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').last()
    except:
        chatthread = 0
    chatted_users = []
    for thread in threads:
        if thread.second_person.id == request.user.id:
            chatted_users.append(thread.first_person.id)
        else:
            chatted_users.append(thread.second_person.id)
    context = {
        'users':users,
        'threads':threads,
        'threadss':chatthread,
        'chatted_users':chatted_users
    }
    return render(request, 'chats/inbox.html', context)

@login_required
def MessagesInboxSingle(request, thread_id):
    users = User.objects.all()
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by("-id")
    chatthread = Thread.objects.get(id=thread_id)
    chatted_users = []
    for thread in threads:
        if thread.second_person.id == request.user.id:
            chatted_users.append(thread.first_person.id)
        else:
            chatted_users.append(thread.second_person.id)
    context = {
        'users':users,
        'threads':threads,
        'thread':chatthread,
        'thread_id': chatthread.id,
        'chatted_users':chatted_users
    }
    return render(request, 'chats/inbox.html', context)

@login_required
def StartChat(request, user_id):
    Thread.objects.create(
        first_person = User.objects.get(id=user_id),
        second_person = User.objects.get(id=request.user.id)
    )
    return redirect('messages-inbox')