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

import logging
from telegram import Update
from telegram.ext import CallbackContext

from internationalization import _, __
from mwt import MWT
from shared_vars import gm, dispatcher

logger = logging.getLogger(__name__)

TIMEOUT = 2.5

def list_subtract(list1, list2):
    """ İki siyahını bir-birindən çıxan və nəticəni sıralayan köməkçi funksiya """
    list1 = list1.copy()

    for x in list2:
        list1.remove(x)

    return list(sorted(list1))


def display_name(user):
    """ İstifadəçinin adını və varsa, istifadəçi adını qaytarır """
    user_name = user.first_name
    if user.username:
        user_name += ' (@' + user.username + ')'
    return user_name


def display_color(color):
    """ Rəng kodunu rəng adı ilə əvəz edir """
    if color == "r":
        return _("{emoji} Qırmızı").format(emoji='❤️')
    if color == "b":
        return _("{emoji} Mavi").format(emoji='💙')
    if color == "g":
        return _("{emoji} Yaşıl").format(emoji='💚')
    if color == "y":
        return _("{emoji} Sarı").format(emoji='💛')


def display_color_group(color, game):
    """ Rəng kodunu oyunun dilinə uyğun rəng adı ilə əvəz edir """
    if color == "r":
        return __("{emoji} Qırmızı", game.translate).format(emoji='❤️')
    if color == "b":
        return __("{emoji} Mavi", game.translate).format(emoji='💙')
    if color == "g":
        return __("{emoji} Yaşıl", game.translate).format(emoji='💚')
    if color == "y":
        return __("{emoji} Sarı", game.translate).format(emoji='💛')


def error(update: Update, context: CallbackContext):
    """Sadə xəta işləyici"""
    logger.exception(context.error)


def send_async(bot, *args, **kwargs):
    """Mesajı asinxron şəkildə göndər"""
    if 'timeout' not in kwargs:
        kwargs['timeout'] = TIMEOUT

    try:
        dispatcher.run_async(bot.sendMessage, *args, **kwargs)
    except Exception as e:
        error(None, None, e)


def answer_async(bot, *args, **kwargs):
    """Inline sorğunu asinxron cavablandır"""
    if 'timeout' not in kwargs:
        kwargs['timeout'] = TIMEOUT

    try:
        dispatcher.run_async(bot.answerInlineQuery, *args, **kwargs)
    except Exception as e:
        error(None, None, e)


def game_is_running(game):
    """Oyun hal-hazırda davam edirmi?"""
    return game in gm.chatid_games.get(game.chat.id, list())


def user_is_creator(user, game):
    """İstifadəçi oyunun yaradıcısıdırmı?"""
    return user.id in game.owner


def user_is_admin(user, bot, chat):
    """İstifadəçi qrup adminidir?"""
    return user.id in get_admin_ids(bot, chat.id)


def user_is_creator_or_admin(user, game, bot, chat):
    """İstifadəçi həm yaradıcısı, həm də admin ola bilər"""
    return user_is_creator(user, game) or user_is_admin(user, bot, chat)


@MWT(timeout=60*60)
def get_admin_ids(bot, chat_id):
    """Qrup üçün adminlərin ID-sini qaytarır. Nəticə 1 saat keşlənir."""
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]
