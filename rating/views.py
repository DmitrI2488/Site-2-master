from django.core.paginator import Paginator
from django.shortcuts import render
from Home.models import rating


def ratings(request):
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
    return render(request, 'rating/rating.html',
                  {'chanels': chanels,
                   'chanel': alla,
                   'rating_list': rating_list
                   })


def failed(request):
    rat = Paginator(rating.objects.filter(passed = False).order_by('-id'), 8)
    page = request.GET.get('page')
    chanels = rat.get_page(page)
    return render(request, 'rating/failed.html',
                  {'rating_list': chanels})
