# Generated by Django 4.2.4 on 2023-08-23 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_contact_is_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_premium',
        ),
        migrations.AddField(
            model_name='user',
            name='subscription_started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
