import datetime

from bank_account.models import BankPartner
from django.test import TestCase, RequestFactory
from bank_account.models import CreditCard, CreditCardType, BankAccount
from bank_account.views import MakeCreditCard, MakeCreditCardForm
from bank_account.models import BankAccountType, Currency
from django.urls import reverse

from bank_account.forms import MakeBankAccountForm

from django.contrib.auth import get_user_model

from bank_account.forms import PayCreditForm, PayDepositForm

User = get_user_model()


class MyTest1(TestCase):
    @classmethod
    def setUpTestData(cls):
        BankPartner.objects.create(name='1', description='2')

    def test_partner(self):
        partner = BankPartner.objects.get(id=1)
        field_label = partner._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_partner_str(self):
        partner = BankPartner.objects.get(id=1)
        self.assertEquals(str(partner), '1')


class MyTest2(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='user', telegram_id='123', confirmed=True)
        self.credit_card_type = CreditCardType.objects.create(name='Visa', description='-')
        self.currency = Currency.objects.create(name='USD', description='-')
        self.account_type = BankAccountType.objects.create(type='Обычная', description='-')
        self.bank_account_1 = BankAccount.objects.create(
            user=self.user,
            name='1234567890',
            balance=1233,
            currency=self.currency,
            account_type=self.account_type
        )
        self.bank_account_2 = BankAccount.objects.create(
            user=self.user,
            name='123456789',
            balance=1235,
            currency=self.currency,
            account_type=self.account_type
        )

    def test_form(self):
        form_data = {
            'owner_name': 'date',
            'card_type': self.credit_card_type,
            'bank_account': self.bank_account_1
        }
        form = MakeCreditCardForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

        form_data = {
            'currency': self.currency,
            'account_type': self.account_type,
        }
        form = MakeBankAccountForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {
            'amount': 228,
            'bank_account': self.bank_account_1,
        }
        form = PayCreditForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

        form_data = {
            'amount': 228,
            'bank_account': self.bank_account_1,
        }
        form = PayDepositForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_logic(self):
        form_data = {
            'value': 1,
            'bank_account_from': self.bank_account_1,
            'bank_account_to': self.bank_account_2
        }
        resp = self.client.post(reverse('make-bank-account-transaction'), form_data)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.bank_account_1.balance, 1233)
        self.assertEqual(self.bank_account_2.balance, 1235)

        form_data = {
            'owner_name': 'date',
            'card_type': self.credit_card_type,
            'bank_account': self.bank_account_1
        }
        resp = self.client.post(reverse('make-credit-card'), form_data)
        self.assertEqual(resp.status_code, 302)
        self.assertIsNotNone(CreditCard.objects.all())

        form_data = {
            'currency': self.currency,
            'account_type': self.account_type,
        }
        resp = self.client.post(reverse('make-bank-account'), form_data)
        self.assertEqual(resp.status_code, 302)
        self.assertIsNotNone(BankAccount.objects.all())
