import uuid
from decimal import Decimal

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, AbstractUser, UserManager
from django.core.validators import RegexValidator

from django.db import models, transaction as db_transaction


def hash_pin(pin):
    return make_password(pin)

class BridgeUser(AbstractUser):
    objects = UserManager()


class ClientManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=False)

    def create_user(self, card_number, pin, **extra_fields):
        user = self.model(card_number=card_number, pin=hash_pin(pin), **extra_fields)
        user.set_password(None)
        user.is_staff = False
        user.save(using=self._db)
        return user


class StaffManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=True)


class Client(BridgeUser):
    card_number = models.CharField(max_length=10, unique=True, validators=[RegexValidator(regex=r'^\d{10}$')])
    pin = models.CharField()

    objects = ClientManager()

    USERNAME_FIELD = 'card_number'


    def save(self, *args, **kwargs):
        self.is_staff = False
        super().save(*args, **kwargs)

    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'


class StaffUser(BridgeUser):
    objects = StaffManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.is_staff = True
        super().save(*args, **kwargs)

class BankAccount(models.Model):
    name = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    owner = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='bank_account')
    balance = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return f'{self.owner.card_number} - {self.name}'


class Transaction(models.Model):
    TYPES = [
        ('CREDIT', 'Crédit'),
        ('DEBIT', 'Débit'),
    ]
    STATUS = [
        ('PENDING', 'En attente'),
        ('REJECTED', 'Rejecté'),
        ("COMPLETE", 'Traité')
    ]

    label = models.CharField(max_length=100)
    amount = models.IntegerField()
    type = models.CharField(choices=TYPES)
    status = models.CharField(choices=STATUS, editable=False)
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='transactions')
    balance_after = models.IntegerField( blank=True, null=True, editable=False)
    reference = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        if self.pk:
            original = Transaction.objects.get(pk=self.pk)
            if self.amount != original.amount:
                raise ValueError('Amount does not match')
        else:
            self.status = 'PENDING'
            try:
                if self.type == 'CREDIT':
                    self.account.balance += self.amount
                else:
                    self.account.balance -= self.amount
                self.account.save()
                self.balance_after = self.account.balance
                self.status = 'COMPLETE'
            except Exception as e:
                self.status = 'REJECTED'
        super().save(*args, **kwargs)