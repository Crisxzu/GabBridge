from django.contrib import admin
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.admin import UserAdmin
from .models import BankAccount, Transaction, Client, StaffUser, hash_pin


class ClientCreationForm(forms.ModelForm):
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput, validators=[RegexValidator(regex=r'^\d{4}$')])
    class Meta:
        model = Client
        fields = ('card_number', 'pin', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.pin = hash_pin(self.cleaned_data['pin'])
        user.is_staff = True
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

@admin.register(Client)
class ClientAdmin(UserAdmin):
    form = ClientCreationForm
    add_form = ClientCreationForm
    list_display = ('card_number', 'first_name', 'last_name', 'email', 'is_active')
    search_fields = ('card_number', 'first_name', 'last_name', 'email')
    ordering = ('card_number',)

    fieldsets = (
        (None, {'fields': ('card_number', 'pin')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Status', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('card_number', 'pin', 'first_name', 'last_name', 'email', 'is_active'),
        }),
    )


@admin.register(StaffUser)
class StaffAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'balance', 'creation_date')
    search_fields = ('name', 'owner__card_number')
    list_filter = ('creation_date',)
    readonly_fields = ('balance',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('label', 'account', 'amount', 'type', 'creation_date', 'status')
    search_fields = ('label', 'account__owner__card_number')
    list_filter = ('type', 'creation_date', 'status')
    readonly_fields = ('creation_date', 'balance_after', 'status')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('amount', 'account', 'type') + self.readonly_fields
        return self.readonly_fields
