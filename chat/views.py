from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Chat, Message, user, Members
from .forms import ChatForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.db import IntegrityError



# Create your views here.
def index(request):
    return render(request, 'chat/index.html', {})

@login_required
def create_chat(request):
    if request.method == "GET":
        form = ChatForm()
        return render(request, 'chat/create.html', {'form': form})
    elif request.method == "POST":
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.admin = request.user
            chat.save()
            return redirect("chat:chat", chat.address)
        return render(request, 'chat/create.html', {'form': form})


class ListChat(LoginRequiredMixin, generic.ListView):
    model = Chat
    context_object_name = 'chats'
    template_name = 'chat/list.html'
    queryset = Chat.objects.filter(private=False)

    def get_queryset(self):
        if self.request.GET.get('query'):
            queryset = Chat.objects.filter(address__iexact=self.request.GET.get('query')).first()
            if queryset:
                self.context_object_name = "chat_results"
                return queryset
        return self.queryset


class UpdateChat(LoginRequiredMixin, generic.UpdateView):
    model = Chat
    form_class = ChatForm
    template_name = 'chat/update.html'
    success_url = reverse_lazy('user:dashboard')

    def get_object(self):
        return get_object_or_404(Chat, address=self.kwargs['uuid'])

@login_required
def chat_view(request, uuid):
    chat = get_object_or_404(Chat, address=uuid)
    if request.user != chat.admin:
        try:
            Members.objects.get_or_create(
                user=request.user,
                chat=chat
            )
        except IntegrityError:
            pass
    return render(request, 'chat/chat.html', {'chat': chat})


def about_or_contact(request, about_or_contact):
    if "about" == about_or_contact:
        return render(request, 'chat/about.html', {})
    elif "contact" == about_or_contact:
        return render(request, 'chat/contact.html', {})


def delete_view(request, uuid):
    chat = get_object_or_404(Chat, address=uuid)
    chat.delete()
    return redirect('user:dashboard')