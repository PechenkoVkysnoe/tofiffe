from bank_account.models import BankPartner
from django.test import TestCase, RequestFactory
from django.urls import reverse
from accounts.models import User
from bank_account.models import CreditCard, CreditCardType, BankAccount
from bank_account.views import MakeCreditCard, MakeCreditCardForm
#
from bank_account.models import BankAccountType, Currency
#
from django.test import Client
from django.urls import reverse

from bank_account.forms import MakeBankAccountForm


class YourTestClass(TestCase):
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


class MakeCreditCardViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='user', telegram_id='123', confirmed=True)
        self.credit_card_type = CreditCardType.objects.create(name='Visa', description='-')
        self.currency = Currency.objects.create(name='USD', description='-')
        self.account_type = BankAccountType.objects.create(type='Обычная', description='-')
        self.bank_account = BankAccount.objects.create(
            user=self.user,
            name='1234567890',
            balance=1234,
            currency=self.currency,
            account_type=self.account_type
        )
        self.url = reverse('make-credit-card')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    # def test_view_renders_correct_template(self):
    #     request = self.factory.get(self.url)
    #     request.user = type(self.user)
    #     response = MakeCreditCard.as_view()(request)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'bank_account/make_credit_card.html')

    def test_form_valid(self):
        request = self.factory.post(self.url, )
        # request.user = self.user
        data = {
            'owner_name': 'John Doe',
            'card_type': self.credit_card_type,
            'bank_account': self.bank_account,
        }
        form = MakeBankAccountForm(data=data)
        self.assertTrue(form.is_valid())
        response = MakeCreditCard.form_valid(form=request)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.assertEqual(CreditCard.objects.count(), 1)
        credit_card = CreditCard.objects.first()
        self.assertEqual(credit_card.owner_name, 'JOHN DOE')
        self.assertIsNotNone(credit_card.number)
        self.assertIsNotNone(credit_card.cvv)
        self.assertIsNotNone(credit_card.date_to)
    #
    # def test_get_form_kwargs(self):
    #     request = self.factory.get(self.url)
    #     request.user = self.user
    #     response = MakeCreditCard.as_view()(request)
    #     form = response.context_data['form']
    #     self.assertEqual(form.user, self.user)
    #
    # def test_bank_account_queryset(self):
    #     request = self.factory.get(self.url)
    #     request.user = self.user
    #     response = MakeCreditCard.as_view()(request)
    #     form = response.context_data['form']
    #     bank_account_queryset = form.fields['bank_account'].queryset
    #     self.assertQuerysetEqual(bank_account_queryset, BankAccount.objects.filter(user=self.user), transform=lambda x: x)