# Generated by Django 4.2.7 on 2024-04-04 06:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_user_born_at_user_personality_type_prefix_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='born_at',
            new_name='born_on',
        ),
    ]
