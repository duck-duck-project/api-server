# Generated by Django 4.2.7 on 2024-08-23 08:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0027_user_premium_expires_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='theme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.theme'),
        ),
    ]