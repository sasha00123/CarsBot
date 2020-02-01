from django.contrib.gis.db import models


class Status(models.TextChoices):
    ACTIVE = ('ACTIVE', 'Активно')
    HIDDEN = ('HIDDEN', 'Скрыто')
    DELETED = ('DELETED', 'Удалено')


class Car(models.Model):
    # Legal info
    number = models.CharField(max_length=10, verbose_name='Номер')
    vin = models.CharField(max_length=17, verbose_name='VIN')

    # Parameters
    brand = models.CharField(max_length=255, verbose_name='Марка')
    model = models.CharField(max_length=255, verbose_name='Модель')
    year = models.IntegerField(verbose_name='Год')
    mileage = models.IntegerField(verbose_name='Пробег')

    # Address + Geoposition
    address = models.CharField(max_length=512, verbose_name='Адрес')

    # Extra fields
    status = models.TextField(choices=Status.choices, default=Status.ACTIVE, verbose_name='Статус')
    comments = models.TextField(blank=True, verbose_name='Комментарии')

    # Timestamps
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Обновлено')


    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'


class TelegramUser(models.Model):
    chat_id = models.BigIntegerField(verbose_name='ID чата', db_index=True)
    full_name = models.CharField(max_length=255, verbose_name='Полное имя')
    username = models.CharField(max_length=255, blank=True, verbose_name='Username')
    email = models.EmailField(max_length=255, blank=True, default="")

    class Meta:
        verbose_name = 'Пользователь Telegram'
        verbose_name_plural = 'Пользователи Telegram'

    def __str__(self):
        return f"{self.full_name}"


class Search(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    matches = models.ManyToManyField(Car, related_name='searches', related_query_name='search')
    search_value = models.CharField(max_length=32, verbose_name='Строка поиска')
    is_success = models.BooleanField(verbose_name='Удачно?')

    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')

    class Meta:
        verbose_name = 'Поиск'
        verbose_name_plural = 'Поиски'


class Image(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images', related_query_name='image')
    file = models.ImageField(verbose_name='Файл')


