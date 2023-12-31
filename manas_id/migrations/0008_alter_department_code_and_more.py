# Generated by Django 4.2.7 on 2024-01-03 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manas_id', '0007_remove_manasid_personality_type_department_emoji_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='code',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='manasid',
            name='personality_type_prefix',
            field=models.CharField(blank=True, choices=[('INTJ', 'Стратег (INTJ)'), ('INTP', 'Ученый (INTP)'), ('ENTJ', 'Командир (ENTJ)'), ('ENTP', 'Полемист (ENTP)'), ('INFJ', 'Активист (INFJ)'), ('INFP', 'Посредник (INFP)'), ('ENFJ', 'Тренер (ENFJ)'), ('ENFP', 'Борец (ENFP)'), ('ISTJ', 'Администратор (ISTJ)'), ('ISFJ', 'Защитник (ISFJ)'), ('ESTJ', 'Менеджер (ESTJ)'), ('ESFJ', 'Консул (ESFJ)'), ('ISTP', 'Виртуоз (ISTP)'), ('ISFP', 'Артист (ISFP)'), ('ESTP', 'Делец (ESTP)'), ('ESFP', 'Развлекатель (ESFP)')], max_length=4, null=True),
        ),
    ]
