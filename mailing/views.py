import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from mailing.forms import ClientForm, MailingForm, MessageForm
from mailing.models import Client, Message
from mailing.tasks import *


class HomeView(TemplateView):

    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        mailing = Mailing.objects
        context_data['mailing_all'] = mailing.all().count()
        context_data['mailing_active'] = mailing.filter(status='CREATED').count()
        context_data['unique_clients'] = Client.objects.distinct().count()
        return context_data


@login_required
def display_clients_menu(request):
    return render(request, 'mailing/client_menu.html')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def test_func(self):
        client = self.get_object()
        user = self.request.user
        return client.user == user or user.is_staff


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')

    def test_func(self):
        client = self.get_object()
        user = self.request.user
        return client.user == user or user.is_staff


@login_required
def display_mailings_menu(request):
    return render(request, 'mailing/mailing_menu.html')


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset

        return queryset.filter(user=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        if form.is_valid():
            # создание рассылки
            mailings = Mailing.objects.create(
                time_start=form.cleaned_data['time_start'],
                time_end=form.cleaned_data['time_end'],
                frequency=form.cleaned_data['frequency'],
                message=form.cleaned_data['message'],
                user=self.request.user
            )
            # создание клиентов
            mailings.clients.set(form.cleaned_data['clients'])

            # парсим дату
            date_start = parser.parse(str(form.cleaned_data['time_start']))

            # если время старта в будущем, отправляем рассылку по времени старта
            if date_start > timezone.now():
                create_mailing.s(
                    form.cleaned_data['time_start'],
                    form.cleaned_data['time_end'],
                    mailings.id,
                    form.cleaned_data['message'].subject,
                    form.cleaned_data['message'].body,
                ).apply_async(eta=date_start)
            # в ином случае отправляем сразу
            else:
                create_mailing.s(
                    form.cleaned_data['time_start'],
                    form.cleaned_data['time_end'],
                    mailings.id,
                    form.cleaned_data['message'].subject,
                    form.cleaned_data['message'].body,
                ).apply_async()

            mailings.status = 'STARTED'
            mailings.save()
        return redirect('mailing:mailing_menu')


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def test_func(self):
        client = self.get_object()
        user = self.request.user
        return client.user == user or user.is_superuser


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def test_func(self):
        client = self.get_object()
        user = self.request.user
        return client.user == user or user.is_superuser


def change_status_mailing(request, pk):
    """Отключает рассылку"""
    obj = get_object_or_404(Mailing, pk=pk)
    if obj.status == 'CREATED' or 'STARTED':
        obj.status = 'FINISHED'
    obj.save()
    return redirect(reverse('mailing:mailing_list'))


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset

        return queryset.filter(user=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()

        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:mailing_list')

    def test_func(self):
        client = self.get_object()
        user = self.request.user
        return client.user == user or user.is_superuser


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:mailing_list')

    def test_func(self):
        client = self.get_object()
        user = self.request.user
        return client.user == user or user.is_superuser


