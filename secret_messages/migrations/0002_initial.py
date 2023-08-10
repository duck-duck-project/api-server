# Generated by Django 4.2.3 on 2023-08-10 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('secret_messages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='of_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='of_user', to='users.user'),
        ),
        migrations.AddField(
            model_name='contact',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='users.user'),
        ),
        migrations.AlterUniqueTogether(
            name='contact',
            unique_together={('of_user', 'to_user')},
        ),
    ]
