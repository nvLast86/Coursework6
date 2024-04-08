from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import HomeView, MailingCreateView, MailingUpdateView, MailingDeleteView, MailingDetailView, \
    MailingListView, ContactListView, ContactDetailView, ContactCreateView, ContactUpdateView, ContactDeleteView, \
    MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, MailingLogListView

app_name = MailingConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/update/<pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/delete/<pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing_detail/<pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('contact_list/', ContactListView.as_view(), name='contact_list'),
    path('contact_detail/<pk>/', ContactDetailView.as_view(), name='contact_detail'),
    path('contact/create/', ContactCreateView.as_view(), name='contact_create'),
    path('contact/update/<pk>/', ContactUpdateView.as_view(), name='contact_update'),
    path('contact/delete/<pk>/', ContactDeleteView.as_view(), name='contact_delete'),
    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('message_detail/<pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/update/<pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('mailing_log_detail/<pk>/', MailingDetailView.as_view(), name='mailing_log_detail'),
    path('mailing_log_list/', MailingLogListView.as_view(), name='mailing_log_list'),
]
