# Generated by Django 4.2.7 on 2023-12-31 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('economics', '0002_remove_transaction_source_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='transaction',
            name='either_sender_or_recipient',
        ),
        migrations.AddConstraint(
            model_name='transaction',
            constraint=models.CheckConstraint(check=models.Q(('sender__isnull', False), ('recipient__isnull', False), _connector='OR'), name='either_sender_or_recipient', violation_error_message=('Transaction must have at least either sender or recipient',)),
        ),
    ]
