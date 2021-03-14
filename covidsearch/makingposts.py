import re, ast, sys, os, django, facebook, datetime

def updateposts():   
    token = 'EAADnXNlY9sMBANcTV7F9ZBh4byJ2FPjyxaz4YasOLbn6HrR3vzvetBn3QMNDrYNq2SkdyP5XlvRkQM8V1wZBgt8OLRAWxhXLBI96c0aAv7huFKrc4KnZA2THIZChbK2hP9CxUleEZCzWoCiOz8rHZA1wHq86bmDpdvZALaJU6pNGwZDZD'
    graph = facebook.GraphAPI(token, version=3.1)
    grabpost = graph.get_all_connections(id='103082354713531', connection_name='posts')
    f = open('/Users/simonbosslet/Desktop/searchcovidpage/covidsearch/static/covidsearch/posts.txt', 'w')
    for i in grabpost:
        attachments = []
        date = datetime.datetime.strptime(i['created_time'], '%Y-%m-%dT%H:%M:%S+0000').strftime('%A, %B %m, %Y')
        i['date_fomatted'] = date
        f.write(str(i))        
    f.close()

    sys.path.append("/Users/simonbosslet/Desktop/searchcovidpage/")
    os.environ["DJANGO_SETTINGS_MODULE"] = "searchcovidpage.settings"
    django.setup()

    from covidsearch.models import post

    f = open('/Users/simonbosslet/Desktop/searchcovidpage/covidsearch/static/covidsearch/posts.txt', 'r')
    posts = re.split(r'(})', f.read())
    new_posts = []
    all_posts = []
    for i in posts[::2]:
        try:
            add = i
            orig = posts[posts.index(add)+1]
            new = str(add) + str(orig)
            new_posts.append(new)
        except: pass
        

    for i in new_posts:
        new = ast.literal_eval(i)
        all_posts.append(new)
        
    for i in all_posts:
        try:
            thepost = post(created_date=i['created_time'], message=i['message'], formatted_date=i['date_formatted'])
            post.save(thepost)
        except: pass
    print('\nPosts updated.')
