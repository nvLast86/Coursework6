from django.core.exceptions import PermissionDenied
from django.views import generic
from django.urls import reverse_lazy
from django.conf import settings
from django.core.cache import cache

from blog.models import Blog
from mailing.models import Mailing, Contact, Message, MailingLog
from mailing.forms import MailingForm, ContactForm, MessageForm, MailingListForm, ContactListForm, MessageListForm
from django.contrib.auth.mixins import LoginRequiredMixin
from random import choices


# Домашняя страница ========================================================================================
class HomeView(generic.TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Главная страница'
        try:
            context_data['object_list'] = choices(Blog.objects.all(), k=3)
        except:
            context_data['object_list'] = []
        mailing_count_key = 'mailing_count'
        active_mailing_count_key = 'active_mailing_count'
        unique_client_count_key = 'unique_client_count'
        if settings.CACHE_ENABLED:
            mailing_count = cache.get(mailing_count_key)
            active_mailing_count = cache.get(active_mailing_count_key)
            unique_client_count = cache.get(unique_client_count_key)
            try:
                if mailing_count is None:
                    mailing_count = Mailing.objects.count()
                    cache.set(mailing_count_key, mailing_count)
                if active_mailing_count is None:
                    active_mailing_count = Mailing.objects.filter(status='запущена').count()
                    cache.set(active_mailing_count_key, active_mailing_count)
                if unique_client_count is None:
                    unique_client_count = len({contact.email for contact in Contact.objects.all()})
                    cache.set(unique_client_count_key, unique_client_count)
            except:
                mailing_count = 0
                active_mailing_count = 0
                unique_client_count = 0
        else:
            try:
                mailing_count = Mailing.objects.count()
                active_mailing_count = Mailing.objects.filter(status='запущена').count()
                unique_client_count = len({contact.email for contact in Contact.objects.all()})
            except:
                mailing_count = 0
                active_mailing_count = 0
                unique_client_count = 0
        context_data[mailing_count_key] = mailing_count
        context_data[active_mailing_count_key] = active_mailing_count
        context_data[unique_client_count_key] = unique_client_count

        return context_data


# Рассылка ===============================================================================================
class MailingCreateView(LoginRequiredMixin, generic.CreateView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')
    form_class = MailingForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        if self.request.user.groups.filter(name="managers"):
            kwargs['manager'] = True
        else:
            kwargs['manager'] = False
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        if self.request.user.groups.filter(name="managers"):
            kwargs['manager'] = True
        else:
            kwargs['manager'] = False
        return kwargs

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied()
        return self.object

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()

        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied()
        return self.object


class MailingDetailView(LoginRequiredMixin, generic.DetailView):
    model = Mailing

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied()
        return self.object


class MailingListView(LoginRequiredMixin, generic.ListView):
    model = Mailing
    form_class = MailingListForm
    template_name = 'mailing/mailing_list.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset().filter(owner=self.request.user)


# Контакты ==================================================================================================
class ContactListView(LoginRequiredMixin, generic.ListView):
    model = Contact
    form_class = ContactListForm
    template_name = 'mailing/contact_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class ContactDetailView(LoginRequiredMixin, generic.DetailView):
    model = Contact

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied()
        return self.object


class ContactCreateView(LoginRequiredMixin, generic.CreateView):
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('mailing:contact_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ContactUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Contact
    fields = ('first_name', 'last_name', 'email')
    success_url = reverse_lazy('mailing:contact_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied()
        return self.object


class ContactDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Contact
    success_url = reverse_lazy('mailing:contact_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied()
        return self.object


# Сообщения ===============================================================================================
class MessageListView(LoginRequiredMixin, generic.ListView):
    model = Message
    form_class = MessageListForm
    template_name = 'mailing/message_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, generic.DetailView):
    model = Message

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied()
        return self.object


class MessageCreateView(LoginRequiredMixin, generic.CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Message
    fields = ('header', 'contents')
    success_url = reverse_lazy('mailing:message_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied()
        return self.object


class MessageDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied()
        return self.object


# Логи рассылки =============================================================================================
class MailingLogDetailView(LoginRequiredMixin, generic.DetailView):
    model = MailingLog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied()
        return self.object


class MailingLogListView(LoginRequiredMixin, generic.ListView):
    model = MailingLog
    form_class = MailingListForm
    template_name = 'mailing/mailing_log_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
