from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator

from .models import DiscussionGroups, DiscussionReplies

# Create your views here.


def DiscussionBoard(request):
    if request.method == "POST":
        search_value = request.POST['search_value']
        disc_data = DiscussionGroups.objects.filter(disc_title__contains = search_value).order_by('-id')
    else:
        disc_data = DiscussionGroups.objects.all().order_by('-id')
    paginator = Paginator(disc_data, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'discussions/disc_board.html', {'disc_data':disc_data,'page_obj':page_obj})



def DiscussionDetails(request, discussion_id):
    myboards = DiscussionGroups.objects.filter(user_id = request.user.id).order_by("-id")
    board_data = DiscussionGroups.objects.get(id=discussion_id)
    board_comments = DiscussionReplies.objects.filter(discussion_id = discussion_id).order_by('-id')
    paginator_comments = Paginator(board_comments, 5)
    page_number = request.GET.get("page")
    page_obj_comments = paginator_comments.get_page(page_number)

    paginator_boards = Paginator(myboards, 5)
    page_number = request.GET.get("page")
    page_obj_boards = paginator_boards.get_page(page_number)

    context = {
        'myboards':myboards,
        'board_data':board_data,
        'board_comments':board_comments,
        'page_obj_comments':page_obj_comments,
        'page_obj_boards':page_obj_boards
    }
    return render(request, 'discussions/disc_details.html', context)


def CreateBoard(request):
    myboards = DiscussionGroups.objects.filter(user_id = request.user.id).order_by("-id")
    paginator_boards = Paginator(myboards, 5)
    page_number = request.GET.get("page")
    page_obj_boards = paginator_boards.get_page(page_number)

    if request.method == "POST":
        create_board(request)
        messages.success(request, 'A Discussion Board has been created')
        return redirect('discussion-board')
    return render(request, 'discussions/create_board.html', {'myboards':myboards,'page_obj_boards':page_obj_boards})


def SendComment(request, discussion_id):
    if request.method == "POST":
        send_comment(request, discussion_id)
        messages.success(request, 'Comment saved')
        return redirect('discussion-details', discussion_id)
    
def DeleteComment(request, discussion_id, discussion_comment_id):
    DiscussionReplies.objects.get(id=discussion_comment_id).delete()
    messages.success(request, 'Comment deleted')
    return redirect('discussion-details', discussion_id)

def DeletePost(request, discussion_id):
    DiscussionGroups.objects.get(id=discussion_id).delete()
    messages.success(request, 'Discussion Board has been deleted')
    return redirect('discussion-board')

def EditPost(request, discussion_id):
    myboards = DiscussionGroups.objects.filter(user_id = request.user.id).order_by("-id")
    paginator_boards = Paginator(myboards, 5)
    page_number = request.GET.get("page")
    page_obj_boards = paginator_boards.get_page(page_number)

    board_data = DiscussionGroups.objects.get(id=discussion_id)
    if request.method=="POST":
        board_data.disc_description = request.POST['disc_description']
        board_data.disc_title = request.POST['disc_title']
        board_data.save()
        messages.success(request, 'Board has been updated')
        return redirect('discussion-details', discussion_id)
    return render(request, 'discussions/edit_board.html', {'board_data': board_data,'page_obj_boards':page_obj_boards})

def create_board(request):
    DiscussionGroups.objects.create(
        user_id = request.user,
        disc_title = request.POST['disc_title'],
        disc_description = request.POST['disc_description']
    )

def send_comment(request, discussion_id):
    disc_data = DiscussionGroups.objects.get(id=discussion_id)
    DiscussionReplies.objects.create(
        user_id  = request.user,
        discussion_id  = disc_data,
        comment = request.POST['comment']
    )