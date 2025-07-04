#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Qruplarda UNO oynamaq üçün Telegram botu
# Müəllif hüquqları © 2016 Jannes Höke <uno@jhoeke.de>
#
# Bu proqram azad proqramdır: Siz onu GNU Affero General Public License şərtlərinə əsasən
# dəyişdirə və ya paylaya bilərsiniz — üçüncü versiya və ya (istədiyiniz halda) daha sonrakı versiyalar.
#
# Bu proqram faydalı olacağı ümidi ilə paylaşılır, lakin HİÇ BİR ZƏMANƏT VERİLMİR;
# hətta DƏQİQLİK və ya İSTƏNİLƏN MƏQSƏDƏ UYĞUNLUQ zəmanəti də daxil deyil.
#
# GNU Affero General Public License nüsxəsini əldə etməlisiniz.
# Əldə etməmisinizsə, baxın: <http://www.gnu.org/licenses/>.


from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackContext

from utils import send_async
from user_setting import UserSetting
from shared_vars import dispatcher
from locales import available_locales
from internationalization import _, user_locale


@user_locale
def show_settings(update: Update, context: CallbackContext):
    chat = update.message.chat

    if update.message.chat.type != 'private':
        send_async(context.bot, chat.id,
                   text=_("Zəhmət olmasa ayarları botla şəxsi çatda dəyişin."))
        return

    us = UserSetting.get(id=update.message.from_user.id)

    if not us:
        us = UserSetting(id=update.message.from_user.id)

    if not us.stats:
        stats = '📊' + ' ' + _("Statistikanı aktiv et")
    else:
        stats = '❌' + ' ' + _("Bütün statistikanı sil")

    kb = [[stats], ['🌍' + ' ' + _("Dili dəyiş")]]
    send_async(context.bot, chat.id, text='🔧' + ' ' + _("Ayarlar"),
               reply_markup=ReplyKeyboardMarkup(keyboard=kb,
                                                one_time_keyboard=True))


@user_locale
def kb_select(update: Update, context: CallbackContext):
    chat = update.message.chat
    user = update.message.from_user
    option = context.match[1]

    if option == '📊':
        us = UserSetting.get(id=user.id)
        us.stats = True
        send_async(context.bot, chat.id, text=_("Statistika aktiv edildi!"))

    elif option == '🌍':
        kb = [[locale + ' - ' + descr]
              for locale, descr
              in sorted(available_locales.items())]
        send_async(context.bot, chat.id, text=_("Dil seçin:"),
                   reply_markup=ReplyKeyboardMarkup(keyboard=kb,
                                                    one_time_keyboard=True))

    elif option == '❌':
        us = UserSetting.get(id=user.id)
        us.stats = False
        us.first_places = 0
        us.games_played = 0
        us.cards_played = 0
        send_async(context.bot, chat.id, text=_("Statistika deaktiv edildi və silindi!"))


@user_locale
def locale_select(update: Update, context: CallbackContext):
    chat = update.message.chat
    user = update.message.from_user
    option = context.match[1]

    if option in available_locales:
        us = UserSetting.get(id=user.id)
        us.lang = option
        _.push(option)
        send_async(context.bot, chat.id, text=_("Dil uğurla dəyişdirildi!"))
        _.pop()


def register():
    dispatcher.add_handler(CommandHandler('settings', show_settings))
    dispatcher.add_handler(MessageHandler(Filters.regex('^([' + '📊' +
                                                        '🌍' +
                                                        '❌' + ']) .+$'),
                                        kb_select))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'^(\w\w_\w\w) - .*'),
                                        locale_select))
