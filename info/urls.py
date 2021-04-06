from django.urls import path

from . import views

urlpatterns =[
    path('',views.register,name = 'register'),
    path('signin', views.signin, name="signin"),
    path('login_db', views.login_db, name="login_db"),
    path('book_data', views.book_data, name="book_data"),
    path('search', views.search, name="search"),
]