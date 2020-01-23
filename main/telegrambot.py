# Example code for telegrambot.py module
import logging

import telegram
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django_telegrambot.apps import DjangoTelegramBot
from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler

from main.models import Car, Search, TelegramUser

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    TelegramUser.objects.update_or_create(chat_id=update.effective_chat.id,
                                          defaults= {
                                              'full_name':update.effective_user.full_name,
                                              'username':update.effective_user.username
                                          })
    update.message.reply_text("Добро пожаловать!")


def send_info(update: Update, context: CallbackContext, car: Car):
    if settings.SEND_TYPE == "FILE":
        update.message.reply_media_group([InputMediaPhoto(open(image.file.path, 'rb')) for image in car.images.all()])
    else:
        update.message.reply_media_group([InputMediaPhoto(image.file.url) for image in car.images.all()])

    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Отправить на почту", callback_data=car.id)],])
    update.message.reply_text(settings.MESSAGE_TEMPLATE.format(car.brand, car.model, car.year, car.number, car.vin, car.address, car.comments), parse_mode=telegram.ParseMode.HTML, reply_markup = keyboard)
    update.message.reply_location(*list(car.geo)[::-1])


def search(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        update.message.reply_text("Неверное число аргументов! Синтаксис: /search <ID>")
        return

    pk = context.args[0]

    user = TelegramUser.objects.get(chat_id=update.effective_chat.id)
    search_log = Search.objects.create(user=user, search_value=pk, is_success=False)

    cars = Car.objects.filter(Q(vin=pk) | Q(number__contains=pk))

    if cars.count():
        update.message.reply_text(f"По вашему запросу найдено вхождений: {cars.count()}")
        for car in cars.all():
            search_log.matches.add(car)
            send_info(update, context, car)
        search_log.is_success = True
        search_log.save()
    else:
        update.message.reply_text("Машин с таким номером или VIN не найдено!")


def set_email(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        update.message.reply_text("Неверное число аргументов! Синтаксис: /email <EMAIL>")
        return

    user = TelegramUser.objects.get(chat_id=update.effective_chat.id)
    user.email = context.args[0]
    user.save()

    update.message.reply_text("Email успешно изменен!")


def send_email(update: Update, context: CallbackContext):
    user = TelegramUser.objects.get(chat_id=update.effective_chat.id)
    car = Car.objects.get(pk=update.callback_query.data)

    if not user.email:
        update.message.reply_text("Чтобы отправить сообщение на почту, нужно сначала указать email.\n" +
                                  "Это можно сделать при помощи команды /email <EMAIL>.")
        return

    send_mail(settings.MAIL_SUBJECT,
              settings.MESSAGE_TEMPLATE.format(car.brand, car.model, car.year,
                                               car.number, car.vin, car.address, car.comments),
              settings.EMAIL,
              [user.email])

    text = update.callback_query.message.text
    update.callback_query.message.edit_text(text + '\n\n Отправлено на почту!')
    update.callback_query.answer()


def main():
    logger.info("Loading handlers for telegram bot")

    dp = DjangoTelegramBot.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("search", search))
    dp.add_handler(CommandHandler("email", set_email))

    dp.add_handler(CallbackQueryHandler(send_email))

