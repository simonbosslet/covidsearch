from django.urls import path
from . import views

urlpatterns = [
path('', views.index, name='index'),
path('<int:pk>', views.post, name='post'),
path('search', views.search, name='search')
]