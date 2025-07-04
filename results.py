"""Inline nəticə siyahısını yaratmaq üçün köməkçi funksiyalar"""

from uuid import uuid4
from telegram import InlineQueryResultArticle, InputTextMessageContent, \
    InlineQueryResultCachedSticker as Sticker

import card as c
from utils import display_color, display_color_group, display_name
from internationalization import _, __


def add_choose_color(results, game):
    """Rəng seçimi üçün variantları əlavə et"""
    for color in c.COLORS:
        results.append(
            InlineQueryResultArticle(
                id=color,
                title=_("Rəng seçin"),
                description=display_color(color),
                input_message_content=
                InputTextMessageContent(display_color_group(color, game))
            )
        )


def add_other_cards(player, results, game):
    """Rəng seçərkən əldeki kartları əlavə et"""
    results.append(
        InlineQueryResultArticle(
            "hand",
            title=_("Kart (oyun vəziyyəti üçün toxun):",
                    "Kartlar (oyun vəziyyəti üçün toxun):",
                    len(player.cards)),
            description=', '.join([repr(card) for card in player.cards]),
            input_message_content=game_info(game)
        )
    )


def player_list(game):
    """Oyunçular siyahısını qaytarır"""
    return [_("{name} ({number} kart)",
              "{name} ({number} kart)",
              len(player.cards))
            .format(name=player.user.first_name, number=len(player.cards))
            for player in game.players]


def add_no_game(results):
    """Oyun başlamayıbsa cavab ver"""
    results.append(
        InlineQueryResultArticle(
            "nogame",
            title=_("Siz oyunda deyilsiniz"),
            input_message_content=
            InputTextMessageContent(_('Hazırda oyunda deyilsiniz. Yeni oyun başlatmaq üçün /new, mövcud oyuna qoşulmaq üçün /join istifadə edin.'))
        )
    )


def add_not_started(results):
    """Oyun başlamayıbsa nəticə əlavə et"""
    results.append(
        InlineQueryResultArticle(
            "nogame",
            title=_("Oyun hələ başlamayıb"),
            input_message_content=
            InputTextMessageContent(_('Oyunu başlatmaq üçün /start yazın.'))
        )
    )


def add_mode_classic(results):
    """Klassik rejim əlavə et"""
    results.append(
        InlineQueryResultArticle(
            "mode_classic",
            title=_("🎻 Klassik rejim"),
            input_message_content=
            InputTextMessageContent(_('Klassik 🎻'))
        )
    )


def add_mode_fast(results):
    """Sanic rejimi əlavə et"""
    results.append(
        InlineQueryResultArticle(
            "mode_fast",
            title=_("🚀 Sanic rejimi"),
            input_message_content=
            InputTextMessageContent(_('Tez getmək lazımdır! 🚀'))
        )
    )


def add_mode_wild(results):
    """Vəhşi rejimi əlavə et"""
    results.append(
        InlineQueryResultArticle(
            "mode_wild",
            title=_("🐉 Vəhşi rejim"),
            input_message_content=
            InputTextMessageContent(_('Vəhşiliyə doğru~ 🐉'))
        )
    )


def add_mode_text(results):
    """Mətn rejimini əlavə et"""
    results.append(
        InlineQueryResultArticle(
            "mode_text",
            title=_("✍️ Mətn rejimi"),
            input_message_content=
            InputTextMessageContent(_('Mətn ✍️'))
        )
    )


def add_draw(player, results):
    """Kart çəkmə seçimi əlavə et"""
    n = player.game.draw_counter or 1

    results.append(
        Sticker(
            "draw", sticker_file_id=c.STICKERS['option_draw'],
            input_message_content=
            InputTextMessageContent(__('Kart çəkilir: {number}',
                                       'Kartlar çəkilir: {number}',
                                       n,
                                       multi=player.game.translate)
                                    .format(number=n))
        )
    )


def add_gameinfo(game, results):
    """Oyun məlumatı seçimi əlavə et"""
    results.append(
        Sticker(
            "gameinfo",
            sticker_file_id=c.STICKERS['option_info'],
            input_message_content=game_info(game)
        )
    )


def add_pass(results, game):
    """Ötür seçimi əlavə et"""
    results.append(
        Sticker(
            "pass", sticker_file_id=c.STICKERS['option_pass'],
            input_message_content=InputTextMessageContent(
                __('Ötür', multi=game.translate)
            )
        )
    )


def add_call_bluff(results, game):
    """Blöf çağır seçimi əlavə et"""
    results.append(
        Sticker(
            "call_bluff",
            sticker_file_id=c.STICKERS['option_bluff'],
            input_message_content=
            InputTextMessageContent(__("Sənin blöfünü çağırıram!",
                                       multi=game.translate))
        )
    )


def add_card(game, card, results, can_play):
    """Kart seçimi əlavə et"""
    if can_play:
        if game.mode != "text":
            results.append(
                Sticker(str(card), sticker_file_id=c.STICKERS[str(card)])
            )
        if game.mode == "text":
            results.append(
                Sticker(str(card), sticker_file_id=c.STICKERS[str(card)],
                        input_message_content=InputTextMessageContent(
                            "Oynanan Kart: {card}".format(
                                card=repr(card)
                                .replace('Draw Four', '+4')
                                .replace('Draw', '+2')
                                .replace('Colorchooser', 'Rəng seçici')
                            )
                        ))
            )
    else:
        results.append(
            Sticker(str(uuid4()), sticker_file_id=c.STICKERS_GREY[str(card)],
                    input_message_content=game_info(game))
        )


def game_info(game):
    players = player_list(game)
    return InputTextMessageContent(
        _("Cari oyunçu: {name}")
        .format(name=display_name(game.current_player.user)) +
        "\n" +
        _("Son kart: {card}").format(card=repr(game.last_card)) +
        "\n" +
        _("Oyunçu: {player_list}",
          "Oyunçular: {player_list}",
          len(players))
        .format(player_list=" -> ".join(players))
  )
