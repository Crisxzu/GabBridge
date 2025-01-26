from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ClientLoginForm, TransactionForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from .models import Transaction, BankAccount, Client


@login_required()
def index(request):
    user = request.user
    try:
        client = Client.objects.get(pk=user.pk)
        bank_account = client.bank_account
        transactions = bank_account.transactions.all().order_by('-creation_date')[:5] if bank_account else []
        context = {
            'client': client,
            "bank_account": bank_account,
            'transactions': transactions,
        }
        return render(request, 'bridge/index.html', context)
    except BankAccount.DoesNotExist:
        client = Client.objects.get(pk=user.pk)
        context = {
            'client': client,
            'bank_account': None,
            'transactions': [],
        }
        return render(request, 'bridge/index.html', context)
    except Transaction.DoesNotExist:
        client = Client.objects.get(pk=user.pk)
        bank_account = client.bank_account
        context = {
            'client': client,
            'bank_account': bank_account,
            'transactions': [],
        }
        return render(request, 'bridge/index.html', context)
    except Client.DoesNotExist:
        return redirect(reverse('bridge:login'))

def login_view(request):
    if request.method == "POST":
        form = ClientLoginForm(request.POST)
        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            pin = form.cleaned_data['pin']
            client = authenticate(card_number=card_number, pin=pin)
            if client:
                login(request, client)
                return redirect(reverse('bridge:index'))
            else:
                message = {'incorrect_credentials': "Identifiants invalides"}
                context = {
                    'message': message,
                }
                return render(request, 'bridge/login.html', context)
        else:
            context = {
                'message': form.errors,
            }
            return render(request, 'bridge/login.html', context)

    else:
        context = {
            'message': None
        }
        return render(request, "bridge/login.html", context)


def logout_view(request):
    logout(request)
    return redirect(reverse('bridge:login'))
@login_required()
def transactions_history(request):
    user = request.user
    try:
        client = Client.objects.get(pk=user.pk)
        bank_account = client.bank_account

        transactions = bank_account.transactions.all()

        search = request.GET.get('search')
        date_start = request.GET.get('date_start')
        date_end = request.GET.get('date_end')
        amount = request.GET.get('amount')
        order_by = request.GET.get('order_by', '-creation_date')

        if search:
            transactions = transactions.filter(label__icontains=search)
        if date_start:
            transactions = transactions.filter(creation_date__gte=date_start)
        if date_end:
            transactions = transactions.filter(creation_date__lte=date_end)
        if amount:
            transactions = transactions.filter(amount=amount)

        order_mapping = {
            'date': '-creation_date',
            'amount': '-amount',
            'status': 'status'
        }
        transactions = transactions.order_by(order_mapping.get(order_by, '-creation_date'))

        paginator = Paginator(transactions, 10)
        page = request.GET.get('page')
        transactions = paginator.get_page(page)

        return render(request, 'bridge/transactions-history.html', {
            'transactions': transactions,
            'bank_account': bank_account,
        })
    except Client.DoesNotExist:
        return redirect(reverse('bridge:login'))
    except BankAccount.DoesNotExist:
        return redirect(reverse('bridge:index'))
    except Transaction.DoesNotExist:
        return redirect(reverse('bridge:index'))


@login_required()
def transaction_view(request, transaction_id : int):
    user = request.user
    try:
        client = Client.objects.get(pk=user.pk)
        bank_account = client.bank_account

        transaction = get_object_or_404(Transaction, pk=transaction_id, account=bank_account)
        context = {
            'transaction': transaction,
        }
        return render(request, 'bridge/transaction.html', context)
    except Client.DoesNotExist:
        return redirect(reverse('bridge:login'))
    except BankAccount.DoesNotExist:
        return redirect(reverse('bridge:index'))
    except Transaction.DoesNotExist:
        return redirect(reverse('bridge:index'))


@login_required()
def deposit(request):
    user = request.user
    try:
        client = Client.objects.get(pk=user.pk)
        bank_account = client.bank_account

        if request.method == "POST":
            form = TransactionForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                label = form.cleaned_data['label']

                if not label:
                    label = "Non précisé"

                new_transaction = Transaction.objects.create(amount=amount, label=label, account=bank_account, type="CREDIT")
                return redirect(reverse('bridge:transaction', args=[new_transaction.pk]))
            else:
                context = {
                    'message': form.errors,
                }
                return render(request, 'bridge/deposit.html', context)

        context = {
            'bank_account': bank_account,
        }
        return render(request, 'bridge/deposit.html', context)

    except Client.DoesNotExist:
        return redirect(reverse('bridge:login'))
    except BankAccount.DoesNotExist:
        return redirect(reverse('bridge:index'))


@login_required()
def withdraw(request):
    user = request.user
    try:
        client = Client.objects.get(pk=user.pk)
        bank_account = client.bank_account

        if request.method == "POST":
            form = TransactionForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                label = form.cleaned_data['label']

                if not label:
                    label = "Non précisé"

                new_transaction = Transaction.objects.create(amount=amount, label=label, account=bank_account,
                                                             type="DEBIT")
                return redirect(reverse('bridge:transaction', args=[new_transaction.pk]))
            else:
                context = {
                    'message': form.errors,
                }
                return render(request, 'bridge/withdraw.html', context)

        context = {
            'bank_account': bank_account,
        }
        return render(request, 'bridge/withdraw.html', context)

    except Client.DoesNotExist:
        return redirect(reverse('bridge:login'))
    except BankAccount.DoesNotExist:
        return redirect(reverse('bridge:index'))
