# Generated by Django 4.2.7 on 2024-09-24 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0028_contact_theme'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('broke_up_at', models.DateTimeField(blank=True, null=True)),
                ('experience', models.PositiveBigIntegerField(default=0)),
                ('first_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first_user_set', to='users.user')),
                ('second_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second_user_set', to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='RelationshipStarsTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('description', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('relationship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='relationships.relationship')),
            ],
        ),
        migrations.AddConstraint(
            model_name='relationshipstarstransaction',
            constraint=models.CheckConstraint(check=models.Q(('amount__exact', 0), _negated=True), name='amount_must_not_be_zero', violation_error_message='Amount must not be zero.'),
        ),
    ]
