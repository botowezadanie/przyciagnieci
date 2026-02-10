import random
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
TOKEN = os.getenv ("BOT_TOKEN")

PORTAL_1_URL = "https://direct-promo.pro/a/6RXMfGjyzHpzB1"
PORTAL_2_URL = "https://safeoffers.pro/a/gLZyiYRXWH2wxq"

# ===================== LISTY =====================

MALE_USERS = [
    "Marcin K","Tomek_W","Paweł89","Adam_N","Michał K.","Krzysiek_PL",
    "Łukasz M","Daniel_91","KubaR","Piotr_S","Bartek77","Rafał_Z",
    "WojtekK","Sebastian_PL","Mateusz M.","MaciekX","Arek_Online",
    "Kamil_B","Norbert88","DamianK","Patryk_86","Olek_W","GrzesiekL",
    "Szymon_PL","Adrian_K","Michał_T","Jacek_90","Tomek_naLuzie",
    "KrystianM","Kuba_Real","FilipK","Maro_PL","Janek_W","ArturK",
    "Lukasz_Active","MateuszPL","Robert_S","DawidM","IgorK","Kacper_7",
    "Paweł_Nowy","Alex_PL","Michał_Classic","Bartek_naStart","WiktorK",
    "TomekSimple","Radek_84","Jarek_W","Daniel_PL","Marcin_naCzasie"
]

FEMALE_USERS = [
    "Anna K","Kasia_M","Ola_W","Magda89","Natalia K.","Ewa_PL",
    "Monika_S","PaulinaM","Karolina_91","Asia_W","Agnieszka K",
    "Zosia_PL","KlaudiaM","Marta_Online","BasiaK","Julia_W",
    "Weronika_PL","Ania_88","PatrycjaK","Lena_M","Dominika_W",
    "Iza_PL","AlicjaK","Kinga_90","MilenaM","Natalia_S","SylwiaK",
    "Paula_PL","Ula_W","DariaK","KarinaM","Kasia_naLuzie","Ola_Real",
    "AnetaK","Justyna_PL","EmiliaM","Gosia_W","Julia_Classic",
    "PatkaK","Lena_Smile","Asia_Active","Natalia_naStart","Magda_PL",
    "LauraK","Monia_W","Sara_PL","WiktoriaM","Klaudia_Online",
    "AniaSimple","PolaK"
]

# ===================== TEKSTY =====================

START_TEXT = (
    "Przyciągnięci to przestrzeń do poznawania nowych ludzi w naturalny sposób.\n"
    "Bez presji, bez ocen i bez zobowiązań.\n\n"
    "Możesz sprawdzić aktywnych użytkowników lub przejść "
    "do zewnętrznych portali randkowych.\n\n"
    "Na początek podaj swój wiek."
)

MENU_TEXT = (
    "Panel użytkownika\n\n"
    "Dostępne opcje:\n"
    "• Aktywni użytkownicy – zobacz kto jest online\n"
    "• Przeglądaj profile – rekomendowane portale randkowe\n"
    "• Regulamin – zasady korzystania\n"
    "• Pomoc – jak działa bot"
)

REGULAMIN_TEXT = (
    "Regulamin korzystania z bota Przyciągnięci\n\n"
    "1. Bot przeznaczony jest wyłącznie dla osób pełnoletnich.\n"
    "2. Bot nie przechowuje trwałych danych osobowych.\n"
    "3. Listy użytkowników mają charakter informacyjny.\n"
    "4. Bot przekierowuje do zewnętrznych serwisów randkowych.\n"
    "5. Administrator nie odpowiada za treści i relacje "
    "powstałe poza botem.\n"
    "6. Korzystanie z bota oznacza akceptację regulaminu."
)

HELP_TEXT = (
    "Pomoc\n\n"
    "Aktywni użytkownicy:\n"
    "Wyświetla listę osób aktualnie online z podziałem na płeć.\n\n"
    "Przeglądaj profile:\n"
    "Prezentuje zewnętrzne portale randkowe wraz ze statystykami.\n\n"
    "Cofnij:\n"
    "Pozwala wrócić do menu bez restartu bota."
)

# ===================== KLAWIATURY =====================

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Aktywni użytkownicy", callback_data="active")],
        [InlineKeyboardButton("Przeglądaj profile", callback_data="browse")],
        [InlineKeyboardButton("Regulamin", callback_data="rules")],
        [InlineKeyboardButton("Pomoc", callback_data="help")]
    ])

def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Cofnij", callback_data="back")]
    ])

def gender_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Mężczyźni", callback_data="men")],
        [InlineKeyboardButton("Kobiety", callback_data="women")],
        [InlineKeyboardButton("Cofnij", callback_data="back")]
    ])

def browse_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Kobiety 18–20", url=PORTAL_1_URL)],
        [InlineKeyboardButton("Kobiety 25–40", url=PORTAL_2_URL)],
        [InlineKeyboardButton("Cofnij", callback_data="back")]
    ])

# ===================== FUNKCJE =====================

def render_users(users):
    count = random.randint(10, min(100, len(users)))
    selected = random.sample(users, count)
    line = ", ".join(f"{u} ({random.randint(18,50)})" for u in selected)
    return f"Aktywni online: {count}\n\n{line}"

def render_browse_text():
    stats_1 = random.randint(1800, 5400)
    stats_2 = random.randint(1600, 4800)

    return (
        "Poniżej znajdują się rekomendowane portale randkowe. "
        "Każdy z nich działa niezależnie i wymaga osobnej rejestracji.\n\n"
        "Statystyki aktywności:\n"
        f"• Portal dla kobiet 18–20 lat: {stats_1} wejść\n"
        f"• Portal dla kobiet 25–40 lat: {stats_2} wejść"
    )

# ===================== HANDLERY =====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["step"] = "age"
    with open("przyciagnieci.png", "rb") as photo:
        await update.message.reply_photo(photo=photo, caption=START_TEXT)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("step") == "age":
        if not update.message.text.isdigit():
            await update.message.reply_text("Podaj wiek jako liczbę.")
            return
        if int(update.message.text) < 18:
            await update.message.reply_text("Bot dostępny jest tylko dla osób pełnoletnich.")
            return
        context.user_data["step"] = "done"
        await update.message.reply_text(MENU_TEXT, reply_markup=main_menu())

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "back":
        await q.edit_message_text(MENU_TEXT, reply_markup=main_menu())
    elif q.data == "active":
        await q.edit_message_text("Wybierz płeć:", reply_markup=gender_menu())
    elif q.data == "men":
        await q.edit_message_text(render_users(MALE_USERS), reply_markup=back_keyboard())
    elif q.data == "women":
        await q.edit_message_text(render_users(FEMALE_USERS), reply_markup=back_keyboard())
    elif q.data == "browse":
        await q.edit_message_text(render_browse_text(), reply_markup=browse_menu())
    elif q.data == "rules":
        await q.edit_message_text(REGULAMIN_TEXT, reply_markup=back_keyboard())
    elif q.data == "help":
        await q.edit_message_text(HELP_TEXT, reply_markup=back_keyboard())

# ===================== MAIN =====================

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    print("Bot działa")
    app.run_polling()

if __name__ == "__main__":
    main()

