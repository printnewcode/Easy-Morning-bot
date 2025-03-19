from django.contrib import admin
from .models import User, Goods  # Добавлено Goods

class UserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'is_paid', 'access_time_end', 'is_admin')
    search_fields = ('telegram_id', 'access_time_end')
    list_filter = ('is_admin','is_paid', 'access_time_end')

class GoodsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')  # Поля для отображения в админке
    
    search_fields = ('name', 'price')  # Поля для поиска


admin.site.register(User, UserAdmin)
admin.site.register(Goods, GoodsAdmin)  # Регистрация модели Goods с админкой