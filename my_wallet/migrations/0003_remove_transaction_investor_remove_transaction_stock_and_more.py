# Generated by Django 4.2 on 2023-05-03 04:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_wallet', '0002_alter_investor_investor_transaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='investor',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='stock',
        ),
        migrations.DeleteModel(
            name='Investor',
        ),
        migrations.DeleteModel(
            name='Stock',
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]