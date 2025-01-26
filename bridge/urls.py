from django.urls import path

from . import views

app_name = 'bridge'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('transactions-history', views.transactions_history, name='transactions-history'),
    path('transaction/<int:transaction_id>', views.transaction_view, name='transaction'),
    path('deposit', views.deposit, name='deposit'),
    path('withdraw', views.withdraw, name='withdraw'),
]