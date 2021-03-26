from django.shortcuts import render
from .models import post

posts = post.objects.all()
tracker = 2
q = None
loadedpostnum = 5
qs = ['a']
searchResults = []
result_count = 0
page = 0
pages = None
allsearchs = []

# homepage
def index(request):
    #used method post in order to signal to sort by oldest
    if request.method == "POST":
        return render(request, 'covidsearch/index.html', {
            'posts': posts,
            'reverse': True,
        })
    return render(request, 'covidsearch/index.html', {
        'posts': posts,
        'reverse': False,
    })

#page for individual posts
def post(request, pk):
    #gets post's pk to find correct post
    post = posts.filter(pk=pk)
    post = post.values('formatted_date', 'message', 'pk')
    return render(request, 'covidsearch/post.html', {
        'post': post[0]
    })

#search page
def search(request):
    global q, tracker, qs, searchResults, result_count, page, pages, allsearchs
    page = 0
    q = qs[-1]
    if request.method == "POST":
        #some search queries such as 'a' and 'http' were causing bugs, decided to just redirect to homepage in those cases.
        if len(str(request.POST.get('search-query'))) == 1 or 'http' in str(request.POST.get('search-query')):
            return render(request, 'covidsearch/search.html', {
            'posts': posts,
            'reverse': False,
            'short': True
        })
        #if searching 
        elif request.POST.get('search-query') is not None:
            q = request.POST.get('search-query')
            qs.append(q)
            searched = False
        #if switching pages
        elif request.POST.get('search-query') is None:
            searched = True
            page = request.POST.get('page')
            searchResults = allsearchs[-1]
            activepage = searchResults.index(searchResults[int(page)])
            results = searchResults[int(page)]
            noResults = False
        #search method
        if not searched:
            searchResults = []
            result_count = 0
            print('searching')
            #if message/title contains query
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
            #if there aren't many searches it seemed better to just put all posts on 1 page.
            if len(searchResults) < 25:
                #splits search results into pages
                searchResults = [searchResults[x:x+25] for x in range(0, len(searchResults), 25)]
                print(searchResults)
            else:
                #splits search results into pages
                searchResults = [searchResults[x:x+10] for x in range(0, len(searchResults), 10)]
                print(len(searchResults))
                print(searchResults[-1])
            allsearchs.append(searchResults)
            pages = [searchResults.index(i)+1 for i in searchResults]
            try:
                pages.pop()
            except:
                pass
            #if no results:
            if not searchResults:
                noResults = True
                activepage = None
                results = None
            else:
                activepage = searchResults[0]
                results = searchResults[int(page)]
                noResults = False
        else:
            activepage = searchResults.index(searchResults[int(page)])
            results = searchResults[int(page)]
            noResults = False
        #used the tracker variable in order to keep track of whether to sort by new or by old
        #if tracker is divisible by 2, sort by oldest
        if (tracker % 2) == 0:
            tracker += 1
            return render(request, 'covidsearch/search.html', {
            'results': results,
            'pages': [i for i in pages],
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
            'pages': [i for i in pages],
            'q': q,
            'resultCount': result_count,
            'reverse': False,
            'noResults': noResults,
            'activepage': activepage
            })