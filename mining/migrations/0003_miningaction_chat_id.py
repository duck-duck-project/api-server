# Generated by Django 4.2.7 on 2024-08-27 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mining', '0002_rename_wealth_miningaction_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='miningaction',
            name='chat_id',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]
