from django.shortcuts import render, get_object_or_404, redirect

from Home.models import rating, Comment

from django.core.paginator import Paginator
from .forms import CommentForm
import sqlite3

# def add_feedback(request):
#     if request.method == 'POST':
#         form = FeedBack(request.POST)
#         if form.is_valid():
#             form.save()
#         messages.success(request, ('Ваше сообщение отправлено'))
#         return redirect('feedback')
#     else:
#         form = FeedBack()
#     return render(request, 'feedback/feedback.html', {'form': form})


def show_chanel(request, chanel_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                username = request.user.username
            chanelss = request.GET.get('pk')
            temp = form.save(commit=False)
            temp.name = username
            rates = ''
            rates2 = ''
            for i in range(int(temp.rate)):
                rates += 'a'
            for i in range(5-int(temp.rate)):
                rates2 += 'a'
            temp.rate1 = rates
            temp.rate2= rates2
            temp.chanel_id = chanelss
            temp.save()
        return redirect('page', chanel_id)
    else:
        # форма
        form = CommentForm()
        # пагинатор 1
        rat = Paginator(rating.objects.all().order_by('-id'), 8)
        page = request.GET.get('page')
        chanels = rat.get_page(page)
        chanel = rating.objects.get(pk=chanel_id)
        # paginator 2
        comentslist = Comment.objects.filter(chanel_id = chanel_id).order_by('-id')
        comments = Paginator(comentslist, 3)
        page1 = request.GET.get('page')
        coments = comments.get_page(page1)
        alla = Paginator(rating.objects.filter(passed = False).order_by('-id'), 8)
        stra = request.GET.get('page')
        alla = alla.get_page(stra)
        rate = ''
        rate2 = ''
        rate1 = ''
        rate21 = ''
        for i in range(chanel.rating):
            rate = rate + 'a'
        for i in range(5-chanel.rating):
            rate2 = rate2 + 'a'
        return render(request, 'Home/show_chanel.html', {
            'chanel': chanel,
            'form': form,
            'comments': coments,
            'rating_list': chanels,
            'rate': rate,
            'rate2': rate2,
            'rate1': rate1,
            'rate2': rate21,
            'chanels': alla,
        })


def all_events(request):
    alla = Paginator(rating.objects.filter(passed = False).order_by('-id'), 8)
    stra = request.GET.get('page')
    alla = alla.get_page(stra)
    rat = Paginator(rating.objects.all().order_by('-id'), 8)
    page = request.GET.get('page')
    chanels = rat.get_page(page)
    rating_list = rating.objects.filter(passed = True).order_by('-id')
    rating_list = Paginator(rating_list, 8)
    page2 = request.GET.get('page')
    rating_list = rating_list.get_page(page2)
    return render(request, 'Home/home.html',
                  {'chanels': chanels,
                   'chanel': alla,
                   'rating_list': rating_list
                   })


def search_chanel(request):
    if request.method == 'POST':
        search = request.POST['search']
        searched = rating.objects.filter(name__contains=search)
        p = Paginator(rating.objects.filter(name__contains=search), 8)
        page = request.GET.get('page')
        chanels = p.get_page(page)
        return render(request, 'Home/search_chanel.html',
                      {'search': search,
                       'results': searched,
                       'chanels': chanels})
    else:
        pk = request.GET.get('pk')
        searched = rating.objects.filter(name__contains=pk)
        p = Paginator(rating.objects.filter(name__contains=pk), 8)
        page = request.GET.get('page')
        chanels = p.get_page(page)
        return render(request, 'Home/search_chanel.html',
               {'search': pk,
                'results': searched,
                'chanels': chanels})


def delete_comment(request, comment_id):
    coment = Comment.objects.get(pk = comment_id)
    if request.user.username == coment.name or request.user.is_staff:
        chanel_id = coment.chanel_id
        coment.delete()
        return redirect('page', chanel_id)
    else:
        return redirect('home')
