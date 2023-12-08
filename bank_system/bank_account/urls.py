from django.urls import path
from transaction.views import CardTransactionView, BankAccountTransactionView
from bank_account.views import (
    MakeBankAccount,
    MakeCreditCard,
    BankAccountView,
    MyBankAccountView,
    MyCreditCardView,
    MyTransactionView,
    CartTransactionView,
    PayCreditView,
    CreditHistoryView,
    BankAccoundTransactionView,
    PayDepositView,
)
from credit.views import CreateCreditView, MyCreditView
from deposit.views import CreateDepositView, MyDepositView

urlpatterns = [
    path('', BankAccountView.as_view(), name='bank-account'),
    path('my-bank-account/', MyBankAccountView.as_view(), name='my-bank-account'),
    path('my-account/make-bank-account/', MakeBankAccount.as_view(), name='make-bank-account'),
    path('my-credit-card/', MyCreditCardView.as_view(), name='my-credit-card'),
    path('my-credit-card/make-credit-card/', MakeCreditCard.as_view(), name='make-credit-card'),
    path('my-transaction/', MyTransactionView.as_view(), name='my-transaction'),
    path('my-transaction/make-bank-account-transaction/', BankAccountTransactionView.as_view(), name='make-bank-account-transaction'),
    path('my-transaction/make-card-transaction/', CardTransactionView.as_view(), name='make-card-transaction'),
    path('my-transaction/cart-transaction/<str:number>/', CartTransactionView.as_view(), name='cart-transaction'),
    path('my-transaction/bank-account-transaction/<str:number>/', BankAccoundTransactionView.as_view(), name='bank-account-transaction'),

    path('my-credit/', MyCreditView.as_view(), name='my-credit'),
    path('my-credit/make-credit/', CreateCreditView.as_view(), name='make-credit'),
    path('my-credit/<slug:pk>/pay-credit/', PayCreditView.as_view(), name='pay-credit'),

    path('my-credit/history/<int:id>/', CreditHistoryView.as_view(), name='credit-history'),

    path('my-deposit/', MyDepositView.as_view(), name='my-deposit'),
    path('my-deposit/make-deposit/', CreateDepositView.as_view(), name='make-deposit'),
    path('my-deposit/<slug:pk>/pay-deposit/', PayDepositView.as_view(), name='pay-deposit'),
    # path('my-deposit/history/<int:id>/', DepositHistoryView.as_view(), name='deposit-history'),
]
