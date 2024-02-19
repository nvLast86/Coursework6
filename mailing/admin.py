from django.contrib import admin

from mailing.models import Client, MailingLogs, Mailing


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'comment',)
    search_fields = ('name', 'email',)
    list_filter = ('name',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_start', 'time_end', 'frequency', 'status')


@admin.register(MailingLogs)
class MailingLogsAdmin(admin.ModelAdmin):
    list_display = ('server_response', 'mailing', 'status', 'time')
