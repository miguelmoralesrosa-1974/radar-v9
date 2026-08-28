import os
from datetime import datetime
import requests
import yfinance as yf

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

WATCHLIST = [('Diploma', 'DPLM.L', 'GBP', 57.6, 69.9, 102.8, 115.1, False, ''), ('Halma', 'HLMA.L', 'GBP', 30.8, 37.4, 54.9, 61.5, False, ''), ('Lifco', 'LIFCO-B.ST', 'SEK', None, 320, None, None, False, ''), ('Addtech', 'ADDT-B.ST', 'SEK', None, None, None, None, False, ''), ('Indutrade', 'INDT.ST', 'SEK', 196, 238, 350, 392, False, ''), ('Lagercrantz', 'LAGR-B.ST', 'SEK', 190, 231, 340, 381, False, ''), ('Games Workshop', 'GAW.L', 'GBP', 154.5, 187.6, 275.9, 309.1, False, ''), ('Belimo', 'BEAN.SW', 'CHF', None, None, None, None, False, ''), ('IMCD', 'IMCD.AS', 'EUR', 90, 105, 150, 170, False, ''), ('Geberit', 'GEBN.SW', 'CHF', 405, 492, 724, 811, False, ''), ('Schindler', 'SCHP.SW', 'CHF', None, None, None, None, False, ''), ('Beijer Ref', 'BEIJ-B.ST', 'SEK', None, None, None, None, False, ''), ('ABB', 'ABBN.SW', 'CHF', 60, 66, 85, 90, False, ''), ('Munich Re', 'MUV2.DE', 'EUR', None, None, None, None, False, ''), ('Hannover Re', 'HNR1.DE', 'EUR', None, None, None, None, False, ''), ('Allianz', 'ALV.DE', 'EUR', 303, 368, 541, 606, False, ''), ('Amadeus IT', 'AMS.MC', 'EUR', None, None, None, None, False, ''), ('Publicis', 'PUB.PA', 'EUR', None, None, None, None, False, ''), ('Ahold Delhaize', 'AD.AS', 'EUR', 27, 32.8, 48.2, 54, False, ''), ('Pandora', 'PNDORA.CO', 'DKK', 578, 702, 1033, 1157, False, ''), ('ASML', 'ASML.AS', 'EUR', 1100, 1250, 1650, 1900, False, ''), ('Intuitive Surgical', 'ISRG', 'USD', 335, 406, 598, 669, True, 'Cartera'), ('SAP', 'SAP.DE', 'EUR', 145, 176, 259, 290, True, 'Cartera'), ('Nemetschek', 'NEM.DE', 'EUR', 60, 70, 103, 115, True, 'Cartera'), ('LVMH', 'MC.PA', 'EUR', 435, 460, 625, 700, True, 'Cartera'), ('Sampo', 'SAMPO.HE', 'EUR', 8.5, 9.5, 13.2, 14.8, False, ''), ('BMW', 'BMW.DE', 'EUR', None, None, None, None, True, 'Cartera'), ('Nestlé', 'NESN.SW', 'CHF', None, None, None, None, False, ''), ('Sika', 'SIKA.SW', 'CHF', None, None, None, None, False, ''), ('Deutsche Börse', 'DB1.DE', 'EUR', None, None, None, None, False, ''), ('DNB', 'DNB.OL', 'NOK', None, None, None, None, True, 'Cartera'), ('Borregaard', 'BRG.OL', 'NOK', None, None, None, None, True, 'Cartera'), ('Qt Group', 'QTCOM.HE', 'EUR', None, None, None, None, True, 'Cartera'), ('Valmet', 'VALMT.HE', 'EUR', None, None, None, None, True, 'Cartera'), ('Tokmanni', 'TOKMAN.HE', 'EUR', None, None, None, None, True, 'Cartera'), ('Obayashi', '1802.T', 'JPY', None, None, None, None, False, ''), ('Shimano', '7309.T', 'JPY', None, None, None, None, True, 'Cartera'), ('Osaka Soda', '4046.T', 'JPY', None, None, None, None, False, ''), ('SIA Engineering', 'S59.SI', 'SGD', None, None, None, None, False, ''), ('Singapore Exchange', 'S68.SI', 'SGD', None, None, None, None, False, ''), ('Keppel', 'BN4.SI', 'SGD', None, None, None, None, True, 'Cartera'), ('Hongkong Land', 'H78.SI', 'USD', None, None, None, None, False, ''), ('Cellnex', 'CLNX.MC', 'EUR', None, None, None, None, True, 'Cartera'), ('Viscofan', 'VIS.MC', 'EUR', None, None, None, None, True, 'Cartera'), ('CIE Automotive', 'CIE.MC', 'EUR', None, None, None, None, True, 'Cartera'), ('Saint-Gobain', 'SGO.PA', 'EUR', None, None, None, None, True, 'Cartera'), ('Microsoft', 'MSFT', 'USD', None, None, None, None, True, 'Cartera'), ('Oracle', 'ORCL', 'USD', None, None, None, None, True, 'Cartera'), ('Danaher', 'DHR', 'USD', None, None, None, None, False, ''), ('Texas Instruments', 'TXN', 'USD', None, None, None, None, False, ''), ('Qualcomm', 'QCOM', 'USD', None, None, None, None, True, 'Cartera'), ('KLA', 'KLAC', 'USD', None, None, None, None, False, ''), ('TSMC', 'TSM', 'USD', None, None, None, None, False, ''), ('Berkshire Hathaway', 'BRK-B', 'USD', None, None, None, None, False, ''), ('Newmont', 'NEM', 'USD', None, None, None, None, False, 'Vendida; solo watchlist'), ('Cameco', 'CCJ', 'USD', None, None, None, None, False, ''), ('NexGen Energy', 'NXE', 'USD', None, None, None, None, False, ''), ('Repsol', 'REP.MC', 'EUR', None, None, None, None, False, ''), ('Occidental Petroleum', 'OXY', 'USD', None, None, None, None, False, ''), ('Rio Tinto', 'RIO.L', 'GBP', None, None, None, None, True, 'Cartera'), ('Vale', 'VALE', 'USD', None, None, None, None, False, ''), ('SQM', 'SQM', 'USD', None, None, None, None, False, ''), ('Croda', 'CRDA.L', 'GBP', None, None, None, None, False, ''), ('Sanoma', 'SANOMA.HE', 'EUR', None, None, None, None, False, ''), ('Tietoevry', 'TIETO.HE', 'EUR', None, None, None, None, False, ''), ('Nordea', 'NDA-FI.HE', 'EUR', None, None, None, None, False, ''), ('Kemira', 'KEMIRA.HE', 'EUR', None, None, None, None, False, ''), ('IHI Corporation', '7013.T', 'JPY', None, None, None, None, False, 'VETO V9 / seguimiento'), ('FMC Corporation', 'FMC', 'USD', None, None, None, None, True, 'Cartera'), ('FinVolution Group', 'FINV', 'USD', None, None, None, None, True, 'Cartera'), ('Ingredion', 'INGR', 'USD', None, None, None, None, True, 'Cartera'), ('Pfizer', 'PFE', 'USD', None, None, None, None, True, 'Cartera'), ('Adidas', 'ADS.DE', 'EUR', None, None, None, None, True, 'Cartera'), ('Porsche SE', 'PAH3.DE', 'EUR', None, None, None, None, True, 'Cartera'), ('Huhtamäki', 'HUH1V.HE', 'EUR', None, None, None, None, True, 'Cartera'), ('Vallourec', 'VK.PA', 'EUR', None, None, None, None, True, 'Cartera'), ('Mitsubishi Corporation', '8058.T', 'JPY', None, None, None, None, True, 'Cartera'), ('Nippon Steel', '5401.T', 'JPY', None, None, None, None, True, 'Cartera'), ('BWX Technologies', 'BWXT', 'USD', None, None, None, None, True, 'Cartera')]

def get_prices():
    prices = {}
    for name, symbol, ccy, strong, buy, reduce, sell, in_portfolio, note in WATCHLIST:
        try:
            hist = yf.Ticker(symbol).history(period="5d", interval="1d", auto_adjust=False)
            if hist.empty or "Close" not in hist:
                prices[symbol] = None
            else:
                s = hist["Close"].dropna()
                prices[symbol] = float(s.iloc[-1]) if len(s) else None
        except Exception:
            prices[symbol] = None
    return prices

def zone(price, strong, buy, reduce, sell):
    if any(v is None for v in (strong, buy, reduce, sell)):
        return "⚪ Sin umbral V9 completo"
    if price <= strong:
        return "🟢 COMPRA FUERTE"
    if price <= buy:
        return "🟢 COMPRA"
    if price >= sell:
        return "🔴 VENTA"
    if price >= reduce:
        return "🟠 REDUCIR"
    return "⚪ MANTENER"

def fmt(x, ccy):
    if x is None:
        return "—"
    prefix = {
        "EUR":"€","USD":"$","GBP":"£","CHF":"CHF ","SEK":"SEK ",
        "NOK":"NOK ","DKK":"DKK ","JPY":"¥","SGD":"S$"
    }.get(ccy, ccy + " ")
    return f"{prefix}{x:,.2f}".replace(",", "X").replace(".", ",").replace("X",".")

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    chunks = [text[i:i+3900] for i in range(0, len(text), 3900)]
    for chunk in chunks:
        r = requests.post(
            url,
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": chunk,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            },
            timeout=30
        )
        r.raise_for_status()

def main():
    prices = get_prices()
    rows = []

    for item in WATCHLIST:
        name, symbol, ccy, strong, buy, reduce, sell, in_portfolio, note = item
        price = prices.get(symbol)
        z = "⚠️ Sin cotización" if price is None else zone(price, strong, buy, reduce, sell)
        rows.append((name, symbol, ccy, strong, buy, reduce, sell, in_portfolio, note, price, z))

    active = [r for r in rows if r[-1] in ("🟢 COMPRA FUERTE","🟢 COMPRA","🟠 REDUCIR","🔴 VENTA")]
    active.sort(key=lambda r: (not r[7], r[0]))

    nearest = []
    for r in rows:
        name, symbol, ccy, strong, buy, reduce, sell, in_portfolio, note, price, z = r
        if price is not None and buy is not None and z == "⚪ MANTENER":
            d = (price - buy) / buy * 100
            if d >= 0:
                nearest.append((d, r))
    nearest = sorted(nearest, key=lambda x: x[0])[:10]

    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    msg = [f"<b>RADAR DIARIO V9 — {len(WATCHLIST)} EMPRESAS</b>\n{now}\n"]

    if active:
        msg.append("<b>SEÑALES ACTIVAS</b>")
        for r in active:
            name, symbol, ccy, strong, buy, reduce, sell, in_portfolio, note, price, z = r
            mark = " 📌 CARTERA" if in_portfolio else ""
            msg.append(f"• <b>{name}</b>{mark} — {fmt(price,ccy)} — {z}")
    else:
        msg.append("Sin señales activas en empresas con umbrales V9 completos.")

    if nearest:
        msg.append("\n<b>MÁS CERCA DE COMPRA</b>")
        for d, r in nearest:
            name, symbol, ccy, strong, buy, reduce, sell, in_portfolio, note, price, z = r
            mark = " 📌" if in_portfolio else ""
            msg.append(f"• {name}{mark}: {fmt(price,ccy)} | compra ≤ {fmt(buy,ccy)} | +{d:.1f}%")

    ok_quotes = sum(1 for r in rows if r[-2] is not None)
    complete = sum(1 for r in rows if all(v is not None for v in r[3:7]))
    pending = len(rows) - complete
    failed = len(rows) - ok_quotes

    msg.append(
        f"\nCobertura cotizaciones: {ok_quotes}/{len(rows)}"
        f"\nUmbrales V9 completos: {complete}/{len(rows)}"
        f"\nPendientes de valoración V9: {pending}"
    )

    if failed:
        bad = [r[0] for r in rows if r[-2] is None]
        msg.append("\nSin cotización: " + ", ".join(bad[:15]) + ("…" if len(bad) > 15 else ""))

    send_telegram("\n".join(msg))

if __name__ == "__main__":
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise SystemExit("Faltan TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID")
    main()
