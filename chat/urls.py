from django.urls import path
from . import views

urlpatterns = [
    path('messages/<str:username>', views.MessageList.as_view()),
]
