#from django.db import models

from djongo import models

class User(models.Model):
    id = models.ObjectIdField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
   # gender = 
    contact = models.CharField(max_length=30) 
    email = models.CharField(max_length = 50)
    city = models.CharField(max_length = 30)
    username = models.CharField(max_length = 30)
    password = models.CharField(max_length = 30)

class Books(models.Model):
    title = models.CharField(max_length = 30)
    book_genre = models.CharField(max_length = 30)
    book_url = models.CharField(max_length = 30)
    book_description = models.CharField(max_length = 30)
    author_name = models.CharField(max_length = 30)
    rating = models.CharField(max_length = 30)
