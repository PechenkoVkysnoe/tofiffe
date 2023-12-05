# Generated by Django 4.2.7 on 2023-12-04 20:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='BankAccountType',
            fields=[
                ('type', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='BankPartner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CreditCardType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PrivilegeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Privileges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('bank_partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank_account.bankpartner')),
                ('privilege_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank_account.privilegetype')),
            ],
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('number', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('owner_name', models.CharField(max_length=19)),
                ('date_to', models.DateField()),
                ('cvv', models.IntegerField()),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank_account.bankaccount')),
                ('card_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank_account.creditcardtype')),
            ],
        ),
        migrations.CreateModel(
            name='CardTypePrivileges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_card_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank_account.creditcardtype')),
                ('privileges', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank_account.privileges')),
            ],
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank_account.currency'),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CurrencyRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coefficient_buy', models.DecimalField(decimal_places=2, max_digits=12)),
                ('coefficient_sell', models.DecimalField(decimal_places=2, max_digits=12)),
                ('currency_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relations_from', to='bank_account.currency')),
                ('currency_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relations_to', to='bank_account.currency')),
            ],
            options={
                'unique_together': {('currency_from', 'currency_to')},
            },
        ),
    ]
