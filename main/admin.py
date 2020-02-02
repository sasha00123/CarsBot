from django.contrib import admin
from mapwidgets.widgets import GooglePointFieldWidget
from main.models import Car, Image, Search, TelegramUser
from django.contrib.gis.db import models


class ImageInline(admin.TabularInline):
    model = Image
    verbose_name = 'Изображения'
    verbose_name_plural = 'Изображения'
    extra = 0


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
    list_display = ['brand', 'model', 'number', 'year', 'mileage', 'vin', 'address', 'status', 'comments', 'created_date', 'updated_date']
    search_fields = ['brand', 'model', 'address', 'year']


    def save_model(self, request, obj, form, change):
        obj.save()

        for afile in request.FILES.getlist('photos_multiple'):
            obj.images.create(file=afile)


@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ['user', 'search_value', 'is_success', 'created_date']
    search_fields = ['user', 'search_value']


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'full_name', 'username']
    search_fields = ['full_name', 'username']