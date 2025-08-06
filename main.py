from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msgbox
import requests

# Цветовая схема
BG_COLOR = "#FFF0F5"  # Нежно-розовый (фон)
BUTTON_COLOR = "#E6E6FA"  # Фиалковый (кнопки)
TEXT_COLOR = "#4B0082"  # Индиго (текст)
COMBOBOX_COLOR = "#FFFFFF"  # Белый (выпадающие списки)

coins = {
    "bitcoin": "Bitcoin (BTC)",
    "ethereum": "Ethereum (ETH)",
    "ripple": "Ripple (XRP)",
    "litecoin": "Litecoin (LTC)",
    "cardano": "Cardano (ADA)"
}

fiat_currencies = {
    "usd": "USD (Американский доллар)",
    "eur": "EUR (Евро)",
    "jpy": "JPY (Японская йена)",
    "gbp": "GBR (Британский фунт стерлингов)",
    "aud": "AUD (Австралийский доллар)",
    "cad": "CAD (Канадский доллар)",
    "chf": "CHF (Швейцарский франк)",
    "cny": "CNY (Китайский юань)",
    "rub": "RUB (Российский рубль)"
}

def get_coin_id(name):
    for coin_id, coin_name in coins.items():
        if coin_name == name:
            return coin_id

def get_currency_code(name):
    for code, display_name in fiat_currencies.items():
        if display_name == name:
            return code

def fetch_rate():
    coin = get_coin_id(coin_choice.get())
    currency = get_currency_code(currency_choice.get())

    if coin and currency:
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={currency}"
            reply = requests.get(url)
            reply.raise_for_status()
            result = reply.json()
            if currency in result[coin]:
                rate = result[coin][currency]
                msgbox.showinfo("Текущий курс", f"1 {coins[coin]} = {rate:.0f} {fiat_currencies[currency]}")
            else:
                msgbox.showerror("Ошибка", f"Не удалось получить курс для {currency}")
        except Exception as e:
            msgbox.showerror("Ошибка", f"Произошла ошибка:\n{e}")
    else:
        msgbox.showwarning("Внимание", "Выберите и криптовалюту, и фиатную валюту")

app = Tk()
screen_w, screen_h = app.winfo_screenwidth(), app.winfo_screenheight()
app.geometry(f"400x350+{screen_w//2-200}+{screen_h//2-150}")
app.title("Конвертер криптовалют")
app.configure(bg=BG_COLOR)

# Стиль для кнопки
style = ttk.Style()
style.configure('TButton', background=BUTTON_COLOR, foreground=TEXT_COLOR)

# Виджеты с новой цветовой схемой
Label(app, text="Криптовалюта:", bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=5)
coin_choice = ttk.Combobox(app, values=list(coins.values()), background=COMBOBOX_COLOR)
coin_choice.pack(pady=5)

Label(app, text="Фиатная валюта:", bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=5)
currency_choice = ttk.Combobox(app, values=list(fiat_currencies.values()), background=COMBOBOX_COLOR)
currency_choice.pack(pady=5)

Button(app, text="Узнать курс", command=fetch_rate, bg=BUTTON_COLOR, fg=TEXT_COLOR,
       activebackground="#D8BFD8", activeforeground=TEXT_COLOR).pack(pady=20)

app.mainloop()