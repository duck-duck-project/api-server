# Generated by Django 4.2.7 on 2024-06-19 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_user_health'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='did_sports_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
