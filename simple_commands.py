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

from telegram import ParseMode, Update
from telegram.ext import CommandHandler, CallbackContext

from user_setting import UserSetting
from utils import send_async
from shared_vars import dispatcher
from internationalization import _, user_locale


@user_locale
def help_handler(update: Update, context: CallbackContext):
    """ /help əmri üçün handler """
    help_text = _("Bu addımları izləyin:\n\n"
      "1. Botu bir qrupa əlavə edin\n"
      "2. Qrupda yeni oyun başlatmaq üçün /new yazın və ya hazırda davam edən oyuna qoşulmaq üçün /join yazın\n"
      "3. Ən azı iki oyunçu qoşulduqdan sonra /start komandasını yazın\n"
      "4. <code>@unobot</code> yazın və <b>boşluq</b> düyməsini basın və ya mesajların yanındakı <code>via @unobot</code> üzərinə klikləyin. Kartlarınızı (bəziləri boz rəngdə olacaq), əlavə seçimləri (məsələn, kart çəkmək) və cari oyun vəziyyətini göstərən <b>?</b> görəcəksiniz. <b>Boz olan kartlar</b> hal-hazırda oynana bilməyən kartlardır. Seçim üzərinə klikləyin ki, həmin əməli yerinə yetirilsin.\n"
      "Oyunçular istənilən vaxt oyuna qoşula bilər. Oyundan çıxmaq üçün /leave istifadə edin. Əgər oyunçu 90 saniyədən çox vaxt sərf edirsə, onu ötüb keçmək üçün /skip yazın. Yeni oyun başladıqda xəbər almaq üçün /notify_me yazın.\n\n"
      "<b>Dil</b> və digər ayarlar üçün: /settings\n"
      "Digər komandalar (yalnız oyun yaradıcısı üçün):\n"
      "/close - Lobini bağla\n"
      "/open - Lobini aç\n"
      "/kill - Oyunu sonlandır\n"
      "/kick - İstifadəçiyə cavab verərək onu oyundan çıxar\n"
      "/enable_translations - Oyun iştirakçılarının dilində tərcümələri aktiv et\n"
      "/disable_translations - Bütün mesajlar ingilis dilində olsun\n\n"
      "<b>Eksperimental xüsusiyyət:</b> Eyni anda bir neçə qrupda oynayın. <code>Current game: ...</code> düyməsinə klikləyin və kart oynamaq istədiyiniz qrupu seçin.\n"
      "Əgər bu bot xoşunuza gəldisə, <a href=\"https://telegram.me/storebot?start=mau_mau_bot\">qiymətləndirin</a>, "
      "<a href=\"https://telegram.me/unobotupdates\">yeniliklər kanalına</a> qoşulun və UNO kart oyununu alın.")

    send_async(context.bot, update.message.chat_id, text=help_text,
               parse_mode=ParseMode.HTML, disable_web_page_preview=True)


@user_locale
def modes(update: Update, context: CallbackContext):
    """ /modes əmri üçün handler """
    modes_explanation = _("Bu UNO botunun dörd oyun rejimi var: Klassik, Sanic, Vəhşi və Mətn.\n\n"
      " 🎻 Klassik rejimdə ənənəvi UNO kartları istifadə olunur və avtomatik ötürmə yoxdur.\n"
      " 🚀 Sanic rejimi də eyni kartlardan istifadə edir, amma oyunçu gecikərsə, bot onu avtomatik ötürür.\n"
      " 🐉 Vəhşi rejimdə daha çox xüsusi kart, daha az rəqəm çeşidi var və avtomatik ötürmə yoxdur.\n"
      " ✍️ Mətn rejimində ənənəvi kartlar istifadə olunur, lakin sticker əvəzinə mətn göstərilir.\n\n"
      "Oyun rejimini dəyişmək üçün, OYUN YARADICISI botun istifadəçi adını və bir boşluq yazmalıdır, sanki kart oynayırmış kimi. Bu zaman bütün rejimlər görünəcək.")
    
    send_async(context.bot, update.message.chat_id, text=modes_explanation,
               parse_mode=ParseMode.HTML, disable_web_page_preview=True)


@user_locale
def source(update: Update, context: CallbackContext):
    """ /source əmri üçün handler """
    source_text = _("Bu bot Azad Proqram təminatıdır və AGPL lisenziyası altındadır.\n"
      "Mənbə kodu burada mövcuddur: \n"
      "https://github.com/jh0ker/mau_mau_bot")
    
    attributions = _("Təşəkkürlər:\n"
      'Çəkmə ikonu: <a href="http://www.faithtoken.com/">Faithtoken</a>\n'
      'Keç ikonu: <a href="http://delapouite.com/">Delapouite</a>\n'
      "Orijinal ikonlar: http://game-icons.net\n"
      "İkonlar ɳick tərəfindən redaktə olunub")

    send_async(context.bot, update.message.chat_id,
               text=source_text + '\n' + attributions,
               parse_mode=ParseMode.HTML, disable_web_page_preview=True)


@user_locale
def news(update: Update, context: CallbackContext):
    """ /news əmri üçün handler """
    send_async(context.bot, update.message.chat_id,
               text=_("Bütün yeniliklər burada: https://telegram.me/unobotupdates"),
               disable_web_page_preview=True)


@user_locale
def stats(update: Update, context: CallbackContext):
    """ /stats əmri üçün handler — istifadəçi statistikası """
    user = update.message.from_user
    us = UserSetting.get(id=user.id)
    if not us or not us.stats:
        send_async(context.bot, update.message.chat_id,
                   text=_("Statistikanı aktiv etməmisiniz. Onu aktiv etmək üçün botla şəxsi söhbətdə /settings yazın."))
    else:
        stats_text = list()

        n = us.games_played
        stats_text.append(
            _("{number} oyun oynanılıb",
              "{number} oyun oynanılıb",
              n).format(number=n)
        )

        n = us.first_places
        m = round((us.first_places / us.games_played) * 100) if us.games_played else 0
        stats_text.append(
            _("{number} dəfə birinci yer ({percent}%)",
              "{number} dəfə birinci yer ({percent}%)",
              n).format(number=n, percent=m)
        )

        n = us.cards_played
        stats_text.append(
            _("{number} kart oynanılıb",
              "{number} kart oynanılıb",
              n).format(number=n)
        )

        send_async(context.bot, update.message.chat_id,
                   text='\n'.join(stats_text))


def register():
    dispatcher.add_handler(CommandHandler('help', help_handler))
    dispatcher.add_handler(CommandHandler('source', source))
    dispatcher.add_handler(CommandHandler('news', news))
    dispatcher.add_handler(CommandHandler('stats', stats))
    dispatcher.add_handler(CommandHandler('modes', modes))
