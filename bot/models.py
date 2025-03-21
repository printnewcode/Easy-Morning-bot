from datetime import datetime
from django.db import models
from django.utils import timezone

class User(models.Model):
    is_paid = models.BooleanField(
        default = False,
        verbose_name = "Оплата"
    )
    is_monthly = models.BooleanField(
        default = False,
        verbose_name = "Продление по месяцу(со скидкой)"
    )
    is_vip = models.BooleanField(
        default = False,
        verbose_name = "ВИП-доступ"
    )
    is_admin = models.BooleanField(
        default = False,
        null = True,
        blank = True,
        verbose_name = "Админ"
    )
    telegram_id = models.CharField(
        max_length = 50,
        verbose_name = "Телеграм-айди пользователя"
    )
    access_time_end = models.DateTimeField(
        auto_now = False,
        auto_now_add = False,
        verbose_name = "Время конца доступа",
        default = timezone.now,
    )
    def __str__(self):
        return str(self.telegram_id)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Goods(models.Model):
    name = models.CharField(
        max_length=1000,
        verbose_name = "Название услуги"
    )
    price = models.CharField(
        max_length=10,
        verbose_name = "Цена услуги"
    )
    status = models.CharField(
        max_length = 30,
        verbose_name = "Статус услуги",
        help_text = "Выберите либо Основной, либо Дополнительный (писать строго так, как здесь указано)"
    )
    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
