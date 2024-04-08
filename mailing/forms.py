from django import forms

from mailing.models import Mailing, Contact, Message, MailingLog
from users.forms import FormStyleMixin


class MailingForm(FormStyleMixin, forms.ModelForm):

    def __init__(self, user=None, **kwargs):
        if 'manager' in kwargs:
            self.manager = kwargs.pop('manager')
        else:
            self.manager = None
        super().__init__(**kwargs)
        if self.manager:
            for field_name in self.fields:
                if field_name in ('status',):
                    continue
                self.fields[field_name].disabled = True
        if user:
            self.fields['contacts'] = forms.ModelMultipleChoiceField(queryset=Contact.objects.filter(owner=user))


    class Meta:
        model = Mailing
        exclude = ('owner', 'last_sent')


class ContactForm(FormStyleMixin, forms.ModelForm):

    class Meta:
        model = Contact
        exclude = ('owner',)


class MessageForm(FormStyleMixin, forms.ModelForm):

    class Meta:
        model = Message
        exclude = ('owner',)


class MailingListForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ('owner',)


class ContactListForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class MessageListForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class MailingLogForm(FormStyleMixin, forms.ModelForm):

    class Meta:
        model = MailingLog
        exclude = ('owner',)


class MailingLogListForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'