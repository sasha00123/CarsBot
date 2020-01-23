from django.contrib import admin
from mapwidgets.widgets import GooglePointFieldWidget
from main.models import Car, Image, Search, TelegramUser
from django.contrib.gis.db import models


class ImageInline(admin.TabularInline):
    model = Image
    verbose_name = 'Изображения'
    verbose_name_plural = 'Изображения'


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
    list_display = ['brand', 'model', 'number', 'year', 'vin', 'address', 'status', 'comments', 'created_date', 'updated_date']
    search_fields = ['brand', 'model', 'address', 'year']

    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }


@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ['user', 'search_value', 'is_success', 'created_date']
    search_fields = ['user', 'search_value']


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'full_name', 'username']
    search_fields = ['full_name', 'username']