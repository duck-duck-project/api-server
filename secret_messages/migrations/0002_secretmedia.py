# Generated by Django 4.2.3 on 2023-08-02 10:56

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('secret_messages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecretMedia',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('file_id', models.CharField(max_length=255, unique=True)),
                ('media_type', models.PositiveSmallIntegerField(choices=[(1, 'Photo'), (2, 'Voice')])),
                ('contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='secret_messages.contact')),
            ],
        ),
    ]
