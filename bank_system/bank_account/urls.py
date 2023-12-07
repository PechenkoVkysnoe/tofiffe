from django.urls import path
from transaction.views import MoneyTransferView
from bank_account.views import (
    MakeBankAccount,
    MakeCreditCard,
    BankAccountView,
    MyBankAccountView,
    MyCreditCardView,
    MyTransactionView,
    CartTransactionView,
    PayCreditView,
    CreditHistoryView
)
from credit.views import CreateCreditView, MyCreditView

urlpatterns = [
    path('', BankAccountView.as_view(), name='bank-account'),
    path('my-bank-account/', MyBankAccountView.as_view(), name='my-bank-account'),
    path('my-account/make-bank-account/', MakeBankAccount.as_view(), name='make-bank-account'),
    path('my-credit-card/', MyCreditCardView.as_view(), name='my-credit-card'),
    path('my-credit-card/make-credit-card/', MakeCreditCard.as_view(), name='make-credit-card'),
    path('my-transaction/', MyTransactionView.as_view(), name='my-transaction'),
    path('my-transaction/make-transaction/', MoneyTransferView.as_view(), name='make-transaction'),
    path('my-credit/', MyCreditView.as_view(), name='my-credit'),
    path('my-credit/make-credit/', CreateCreditView.as_view(), name='make-credit'),
    path('my-credit/pay-credit/<int:id>/', PayCreditView.as_view(), name='pay-credit'),
    path('my-credit/history/<int:id>/', CreditHistoryView.as_view(), name='credit-history'),
    path('my-credit/cart-transaction/<str:number>/', CartTransactionView.as_view(), name='cart-transaction'),
]
