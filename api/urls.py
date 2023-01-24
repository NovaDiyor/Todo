from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view),
    path('register/', register),
    path('logout/', logout_view),
    path('edit/profile/', edit_profile),
    path('create/task/', create_task),
    path('all/task/', get_task),
    path('get/task/<int:pk>/', get_one),
    path('edit/task/<int:pk>/', edit_task),
    path('delete/task/<int:pk>/', delete_task)
]
