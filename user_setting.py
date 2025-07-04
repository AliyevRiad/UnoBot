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


from pony.orm import Optional, PrimaryKey
from database import db


class UserSetting(db.Entity):

    id = PrimaryKey(int, auto=False, size=64)  # Telegram istifadəçi ID-si
    lang = Optional(str, default='')  # İstifadəçinin dil ayarı
    stats = Optional(bool, default=False)  # Statistika toplamağa razılıq verib (opt-in)
    first_places = Optional(int, default=0)  # Birinci yerdə bitirilən oyun sayı
    games_played = Optional(int, default=0)  # Oynanılmış ümumi oyun sayı
    cards_played = Optional(int, default=0)  # Oynanılmış ümumi kart sayı
    use_keyboards = Optional(bool, default=False)  # Klaviatura istifadə et (hazırda istifadə olunmur)
