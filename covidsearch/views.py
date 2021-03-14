from typing import Iterator
from django.shortcuts import render
from .models import post

posts = post.objects.all()
tracker = 2
q = None

# Create your views here.
def index(request):
    if request.method == "POST":
        return render(request, 'covidsearch/index.html', {
            'posts': posts,
            'reverse': True
        })
    return render(request, 'covidsearch/index.html', {
        'posts': posts,
        'reverse': False
    })

def post(request, pk):
    post = posts.filter(pk=pk)
    post = post.values('formatted_date', 'message', 'pk')
    return render(request, 'covidsearch/post.html', {
        'post': post[0]
    })

def search(request):
    global q
    global tracker
    if request.method == "POST":
        if request.POST.get('search-query') != None:
            q = request.POST.get('search-query')
        searchResults = []
        result_count = 0
        for post in posts.filter(message__contains=q):
            searchResults.append(post)
            result_count += 1
        for post in posts.filter(formatted_date__contains=q):
            if post not in searchResults:
                searchResults.append(post)
                result_count += 1
        for post in posts.filter(created_date__contains=q):
            if post not in searchResults:
                searchResults.append(post)
                result_count += 1
        if (tracker % 2) == 0:
            tracker += 1
            return render(request, 'covidsearch/search.html', {
            'results': searchResults,
            'q': q,
            'resultCount': result_count,
            'reverse': True
            })
        else:
            tracker += 1
            return render(request, 'covidsearch/search.html', {
            'results': searchResults,
            'q': q,
            'resultCount': result_count,
            'reverse': False
            })