from django.urls import path
import uuid
from chatbot import views

urlpatterns = [
    path('',views.home,name='home'),
    path('chat/<uuid:id>',views.chat_room,name='chat'),

    path('delete/<uuid:id>',views.delete_room,name='delete')
]
