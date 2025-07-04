import logging
from datetime import datetime

import card as c
from errors import DeckEmptyError
from config import WAITING_TIME


class Player(object):
    """
    Bu sinif bir oyunçunu təmsil edir.
    Əsasən qoşa əlaqəli (doubly-linked) halqa siyahısı kimi işləyir
    və istiqaməti tərsinə çevirmək mümkündür.
    Başlanğıcda, özünü oyuna və digər oyunçulara bağlayır —
    mövcud oyunçunun arxasına yerləşir.
    """

    def __init__(self, game, user):
        self.cards = list()
        self.game = game
        self.user = user
        self.logger = logging.getLogger(__name__)

        # Əgər bu oyunçu oyundakı ilk oyunçudursa
        if game.current_player:
            self.next = game.current_player
            self.prev = game.current_player.prev
            game.current_player.prev.next = self
            game.current_player.prev = self
        else:
            self._next = self
            self._prev = self
            game.current_player = self

        self.bluffing = False
        self.drew = False
        self.anti_cheat = 0
        self.turn_started = datetime.now()
        self.waiting_time = WAITING_TIME

    def draw_first_hand(self):
        """Başlanğıcda 7 kart çəkir"""
        try:
            for _ in range(7):
                self.cards.append(self.game.deck.draw())
        except DeckEmptyError:
            for card in self.cards:
                self.game.deck.dismiss(card)

            raise

    def leave(self):
        """Oyunçunu oyundan çıxarır və siyahıdakı boşluğu bağlayır"""
        if self.next is self:
            return

        self.next.prev = self.prev
        self.prev.next = self.next
        self.next = None
        self.prev = None

        for card in self.cards:
            self.game.deck.dismiss(card)

        self.cards = list()

    def __repr__(self):
        return repr(self.user)

    def __str__(self):
        return str(self.user)

    @property
    def next(self):
        return self._next if not self.game.reversed else self._prev

    @next.setter
    def next(self, player):
        if not self.game.reversed:
            self._next = player
        else:
            self._prev = player

    @property
    def prev(self):
        return self._prev if not self.game.reversed else self._next

    @prev.setter
    def prev(self, player):
        if not self.game.reversed:
            self._prev = player
        else:
            self._next = player

    def draw(self):
        """Kart çəkir — say oyun qaydasına görə təyin olunur"""
        _amount = self.game.draw_counter or 1

        try:
            for _ in range(_amount):
                self.cards.append(self.game.deck.draw())

        except DeckEmptyError:
            raise

        finally:
            self.game.draw_counter = 0
            self.drew = True

    def play(self, card):
        """Kartı oynayır və əldən çıxarır"""
        self.cards.remove(card)
        self.game.play_card(card)

    def playable_cards(self):
        """Hal-hazırda oynana biləcək kartları qaytarır"""

        playable = list()
        last = self.game.last_card

        self.logger.debug("Son kart: " + str(last))

        cards = self.cards
        if self.drew:
            cards = self.cards[-1:]  # Əgər kart çəkibsə, yalnız son kart oynana bilər

        # +4 yalnız uyğun rəngli kart yoxdursa oynana bilər
        self.bluffing = False
        for card in cards:
            if self._card_playable(card):
                self.logger.debug("Uyğundur!")
                playable.append(card)

                # Bluff olub-olmadığını qeyd edir
                self.bluffing = (self.bluffing or card.color == last.color)

        # Əgər əlində son kart rəng seçici və ya +4-dürsə, onu oynamaq olmaz
        if len(self.cards) == 1 and self.cards[0].special:
            return list()

        return playable

    def _card_playable(self, card):
        """Bir kartın oynanıla biləcəyini yoxlayır"""

        is_playable = True
        last = self.game.last_card
        self.logger.debug("Kart yoxlanılır: " + str(card))

        if (card.color != last.color and card.value != last.value and
                not card.special):
            self.logger.debug("Rəng və ya dəyər uyğun gəlmir")
            is_playable = False
        elif last.value == c.DRAW_TWO and not \
                card.value == c.DRAW_TWO and self.game.draw_counter:
            self.logger.debug("Çəkmə zəncirini davam etdirmək lazım")
            is_playable = False
        elif last.special == c.DRAW_FOUR and self.game.draw_counter:
            self.logger.debug("Kart çəkilməli, qarşılıq verə bilməz")
            is_playable = False
        elif (last.special == c.CHOOSE or last.special == c.DRAW_FOUR) and \
                (card.special == c.CHOOSE or card.special == c.DRAW_FOUR):
            self.logger.debug("Rəng seçici kartın üstünə yenidən rəng seçici oynamaq olmaz")
            is_playable = False
        elif not last.color:
            self.logger.debug("Son kartın rəngi yoxdur")
            is_playable = False

        return is_playable
