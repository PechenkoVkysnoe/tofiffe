import calendar
import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView

from transaction.models import Transaction, TransactionStatus, TransactionType


from credit.forms import CreateCreditForm

from credit.models import CreditStatus

from credit.models import CreditTransaction, CreditType

from credit.models import UserCredit


def make_credit_transactions(credit):
    if credit.credit.type == CreditType.objects.get(type='Аннуитетный'):
        # константы из формулы 3/4 лабы
        i = credit.credit.percent
        n = credit.credit.period_in_month
        k = (i / 1200 * ((1 + i / 1200) ** n)) / ((1 + i / 1200) ** n - 1)
        current_date = datetime.datetime.now()
        first = current_date.replace(day=1, month=current_date.month)
        for j in range(credit.credit.period_in_month):
            # я хз как прибавлять ровно месяц по другому
            sum_mont = 0
            for h in range(first.month, first.month + j + 1):
                _, month_days = calendar.monthrange(first.year, i)
                sum_mont += month_days
            CreditTransaction.objects.create(
                dt=first + datetime.timedelta(days=sum_mont),
                amount=float(credit.amount) * k,
                credit=credit
            )


class MyCreditView(View):
    def get(self, request, *args, **kwargs):
        credits = UserCredit.objects.filter(bank_account__user=request.user)
        context = {
            'credits': credits
        }
        return render(request, 'bank_account/my_credit.html', context)


class CreateCreditView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = CreateCreditForm
    template_name = 'credit/make_credit.html'
    success_url = reverse_lazy('bank-account')

    def form_valid(self, form):
        form.instance.credit = form.cleaned_data['credit']
        form.instance.bank_account = form.cleaned_data['bank_account']
        form.instance.status = CreditStatus.objects.get(name='В ожидании')
        form.instance.amount = form.cleaned_data['amount']

        credit = form.save()
        make_credit_transactions(credit)
        messages.success(self.request, "Ваша заявка на кредит принята, ожидайте!")
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
