from django import forms
from django.core.validators import RegexValidator


class ClientLoginForm(forms.Form):
    card_number = forms.CharField(
        min_length=10,
        max_length=10,
        required=True,
        validators=[RegexValidator(regex=r'^\d{10}$', message="Numéro de compte pas valide")],
        error_messages={
            'required': "Vous devez rentrer un numéro de compte",
            "min_length": "Numéro de compte pas valide",
            'max_length': "Numéro de compte pas valide",
        }
    )
    pin = forms.CharField(
        min_length=4,
        max_length=4,
        required=True,
        validators=[RegexValidator(regex=r'^\d{4}$', message="Code PIN invalide")],
        error_messages={
            'required': "Vous devez rentrer votre code PIN",
            'min_length': "Code PIN invalide",
            'max_length': "Code PIN invalide",
        }
    )


class TransactionForm(forms.Form):
    amount = forms.IntegerField(required=True, min_value=1000, max_value=1000000, error_messages={
        'required': "Vous devez préciser un montant",
        'min_value' : "Le montant doit être minimum de 1000 FCFA",
        'max_value': "Vous ne pouvez faire une transaction à la fois que maximum 1000000 FCFA"
    })
    label = forms.CharField(required=False)