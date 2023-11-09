from django.urls import path

from chat.views import MessageList

urlpatterns = [
    path('messages/<str:username>', MessageList.as_view()),
]
