from django.urls import path
from .views import *
urlpatterns = [
    path('',home,name="home"),
    path('add-todo',add_todo,name="add_todo"),
    path('delete-todo/<str:id>',delete_todo,name="delete_todo"),
]
