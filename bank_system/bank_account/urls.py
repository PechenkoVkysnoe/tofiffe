from django.urls import path
from bank_account import views

urlpatterns = [
    path('', views.BankAccountView.as_view(), name='bank-account'),
    path('make-bank-account/', views.MakeBankAccount.as_view(), name='make-bank-account'),
    path('make-credit-card/', views.MakeCreditCard.as_view(), name='make-credit-card')
]
