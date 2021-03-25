from typing import Iterator
from django.shortcuts import render
from .models import post

posts = post.objects.all()
tracker = 2
q = None
loadedpostnum = 5
qs = []
searchResults = []
result_count = 0
page = 0
pages = None
allsearchs = []

# Create your views here.
def index(request):
    if request.method == "POST":
        return render(request, 'covidsearch/index.html', {
            'posts': posts,
            'reverse': True,
            'empty': 'onlylinks'
        })
    return render(request, 'covidsearch/index.html', {
        'posts': posts,
        'reverse': False,
        'empty': 'onlylinks'
    })

def post(request, pk):
    post = posts.filter(pk=pk)
    post = post.values('formatted_date', 'message', 'pk')
    return render(request, 'covidsearch/post.html', {
        'post': post[0]
    })

def search(request):
    global q, tracker, qs, searchResults, result_count, page, pages, allsearchs
    page = 0
    if request.method == "POST":
        if request.POST.get('search-query') == 'a' or 'http' in request.POST.get('search-query'):
            return render(request, 'covidsearch/index.html', {
            'posts': posts,
            'reverse': False
        })
        elif request.POST.get('search-query') is not None:
            q = request.POST.get('search-query')
            qs.append(q)
            searched = False
        elif request.POST.get('search-query') is None:
            searched = True
            page = request.POST.get('page')
            searchResults = allsearchs[-1]
            activepage = searchResults.index(searchResults[int(page)])
            results = searchResults[int(page)]
            noResults = False
        if not searched:
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
            if len(searchResults) < 25:
                searchResults = [searchResults[x:x+25] for x in range(0, len(searchResults), 25)]
            else:
                searchResults = [searchResults[x:x+10] for x in range(0, len(searchResults), 10)]
            allsearchs.append(searchResults)
            pages = [searchResults.index(i)+1 for i in searchResults]
            try:
                pages.pop()
            except:
                pass
            if not searchResults:
                noResults = True
                activepage = None
                results = None
            else:
                activepage = searchResults.index(searchResults[int(page)])+1
                results = searchResults[int(page)]
                noResults = False
        if (tracker % 2) == 0:
            tracker += 1
            return render(request, 'covidsearch/search.html', {
            'results': results,
            'pages': pages,
            'q': q,
            'resultCount': result_count,
            'reverse': True,
            'noResults': noResults,
            'activepage': activepage
            })
        else:
            tracker += 1
            return render(request, 'covidsearch/search.html', {
            'results': results,
            'pages': pages,
            'q': q,
            'resultCount': result_count,
            'reverse': False,
            'noResults': noResults,
            'activepage': activepage
            })