# Generated by Django 5.1.7 on 2025-03-19 19:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, verbose_name='Название услуги')),
                ('price', models.CharField(max_length=10, verbose_name='Цена услуги')),
                ('status', models.CharField(help_text='Выберите либо Основной, либо Дополнительный (писать строго так, как здесь указано)', max_length=30, verbose_name='Статус услуги')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='access_time_end',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 19, 22, 7, 17, 281276), verbose_name='Время конца доступа'),
        ),
    ]
