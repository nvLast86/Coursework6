from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig

from mailing.views import (HomeView, display_clients_menu, ClientListView, ClientDetailView, ClientCreateView,
                            ClientUpdateView, ClientDeleteView, display_mailings_menu, MailingListView,
                            MailingCreateView, MailingDetailView, MailingUpdateView, MailingDeleteView, MessageListView,
                            MessageCreateView, MessageUpdateView, MessageDeleteView, change_status_mailing)

app_name = MailingConfig.name


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('clients/menu', cache_page(60)(display_clients_menu), name='client_menu'),
    path('clients/all', ClientListView.as_view(), name='client_list'),
    path('clients/detail/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('clients/create', ClientCreateView.as_view(), name='client_create'),
    path('clients/update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
    path('clients/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),

    path('mailing/menu', cache_page(60)(display_mailings_menu), name='mailing_menu'),
    path('mailing/all', MailingListView.as_view(), name='mailing_list'),
    path('mailing/detail/<int:pk>', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/update/<int:pk>', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/delete/<int:pk>', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing/change-status/<int:pk>/', change_status_mailing, name='change_status_mailing'),

    path('message/all', MessageListView.as_view(), name='message_list'),
    path('message/create', MessageCreateView.as_view(), name='message_create'),
    path('message/update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),

]