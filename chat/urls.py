from django.urls import path
from .views import (
    index,
    create_chat,
    ListChat,
    UpdateChat,
    chat_view,
    about_or_contact,
    delete_view
)


app_name = "chat"

urlpatterns = [
    path('', index, name='index'),
    path('create/', create_chat, name='create'),
    path('list/', ListChat.as_view(), name='list'),
    path('update/<uuid:uuid>/', UpdateChat.as_view(), name='update'),
    path('delete/<uuid:uuid>/', delete_view, name="delete"),
    path('chat/<uuid:uuid>/', chat_view, name='chat'),
    path('info/<str:about_or_contact>/', about_or_contact, name='about_or_contact'),
]
