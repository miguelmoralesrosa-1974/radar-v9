import os, json
from datetime import datetime
from pathlib import Path
import requests
import yfinance as yf

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
STATE_FILE = Path("radar_state.json")

WATCHLIST = [('Diploma', 'DPLM.L', 'GBP', 57.6, 69.9, 102.8, 115.1, False, ''), ('Halma', 'HLMA.L', 'GBP', 30.8, 37.4, 54.9, 61.5, False, ''), ('Lifco', 'LIFCO-B.ST', 'SEK', None, 320, None, None, False, ''), ('Addtech', 'ADDT-B.ST', 'SEK', None, None, None, None, False, ''), ('Indutrade', 'INDT.ST', 'SEK', 196, 238, 350, 392, False, ''), ('Lagercrantz', 'LAGR-B.ST', 'SEK', 190, 231, 340, 381, False, ''), ('Games Workshop', 'GAW.L', 'GBP', 154.5, 187.6, 275.9, 309.1, False, ''), ('Belimo', 'BEAN.SW', 'CHF', None, None, None, None, False, ''), ('IMCD', 'IMCD.AS', 'EUR', 90, 105, 150, 170, False, ''), ('Geberit', 'GEBN.SW', 'CHF', 405, 492, 724, 811, False, ''), ('Schindler', 'SCHP.SW', 'CHF', None, None, None, None, False, ''), ('Beijer Ref', 'BEIJ-B.ST', 'SEK', None, None, None, None, False, ''), ('ABB', 'ABBN.SW', 'CHF', 60, 66, 85, 90, False, ''), ('Munich Re', 'MUV2.DE', 'EUR', None, None, None, None, False, ''), ('Hannover Re', 'HNR1.DE', 'EUR', None, None, None, None, False, ''), ('Allianz', 'ALV.DE', 'EUR', 303, 368, 541, 606, False, ''), ('Amadeus IT', 'AMS.MC', 'EUR', None, None, None, None, False, ''), ('Publicis', 'PUB.PA', 'EUR', None, None, None, None, False, ''), ('Ahold Delhaize', 'AD.AS', 'EUR', 27, 32.8, 48.2, 54, False, ''), ('Pandora', 'PNDORA.CO', 'DKK', 578, 702, 1033, 1157, False, ''), ('ASML', 'ASML.AS', 'EUR', 1100, 1250, 1650, 1900, False, ''), ('Intuitive Surgical', 'ISRG', 'USD', 335, 406, 598, 669, True, 'Cartera'), ('SAP', 'SAP.DE', 'EUR', 145, 176, 259, 290, True, 'Cartera'), ('Nemetschek', 'NEM.DE', 'EUR', 60, 70, 103, 115, True, 'Cartera'), ('LVMH', 'MC.PA', 'EUR', 435, 460, 625, 700, True, 'Cartera'), ('Sampo', 'SAMPO.HE', 'EUR', 8.5, 9.5, 13.2, 14.8, False, ''), ('BMW', 'BMW.DE', 'EUR', None, None, None, None, True, 'Cartera'), ('Nestlé', 'NESN.SW', 'CHF', None, None, None, None, False, ''), ('Sika', 'SIKA.SW', 'CHF', None, None, None, None, False, ''), ('Deutsche Börse', 'DB1.DE', 'EUR', None, None, None, None, False, ''), ('DNB', 'DNB.OL', 'NOK', None, None, None, None, True, 'Cartera'), ('Borregaard', 'BRG.OL', 'NOK', None, None, None, None, True, 'Cartera'), ('Qt Group', 'QTCOM.HE', 'EUR', None, None, None, None, True, 'Cartera'), ('Valmet', 'VALMT.HE', 'EUR', None, None, None, None, True, 'Cartera'), ('Tokmanni', 'TOKMAN.HE', 'EUR', None, None, None, None, True, 'Cartera'), ('Obayashi', '1802.T', 'JPY', None, None, None, None, False, ''), ('Shimano', '7309.T', 'JPY', None, None, None, None, True, 'Cartera'), ('Osaka Soda', '4046.T', 'JPY', None, None, None, None, False, ''), ('SIA Engineering', 'S59.SI', 'SGD', None, None, None, None, False, ''), ('Singapore Exchange', 'S68.SI', 'SGD', None, None, None, None, False, ''), ('Keppel', 'BN4.SI', 'SGD', None, None, None, None, True, 'Cartera'), ('Hongkong Land', 'H78.SI', 'USD', None, None, None, None, False, ''), ('Cellnex', 'CLNX.MC', 'EUR', None, None, None, None, True, 'Cartera'), ('Viscofan', 'VIS.MC', 'EUR', None, None, None, None, True, 'Cartera'), ('CIE Automotive', 'CIE.MC', 'EUR', None, None, None, None, True, 'Cartera'), ('Saint-Gobain', 'SGO.PA', 'EUR', None, None, None, None, True, 'Cartera'), ('Microsoft', 'MSFT', 'USD', None, None, None, None, True, 'Cartera'), ('Oracle', 'ORCL', 'USD', None, None, None, None, True, 'Cartera'), ('Danaher', 'DHR', 'USD', None, None, None, None, False, ''), ('Texas Instruments', 'TXN', 'USD', None, None, None, None, False, ''), ('Qualcomm', 'QCOM', 'USD', None, None, None, None, True, 'Cartera'), ('KLA', 'KLAC', 'USD', None, None, None, None, False, ''), ('TSMC', 'TSM', 'USD', None, None, None, None, False, ''), ('Berkshire Hathaway', 'BRK-B', 'USD', None, None, None, None, False, ''), ('Newmont', 'NEM', 'USD', None, None, None, None, False, 'Vendida; solo watchlist'), ('Cameco', 'CCJ', 'USD', None, None, None, None, False, ''), ('NexGen Energy', 'NXE', 'USD', None, None, None, None, False, ''), ('Repsol', 'REP.MC', 'EUR', None, None, None, None, False, ''), ('Occidental Petroleum', 'OXY', 'USD', None, None, None, None, False, ''), ('Rio Tinto', 'RIO.L', 'GBP', None, None, None, None, True, 'Cartera'), ('Vale', 'VALE', 'USD', None, None, None, None, False, ''), ('SQM', 'SQM', 'USD', None, None, None, None, False, ''), ('Croda', 'CRDA.L', 'GBP', None, None, None, None, False, ''), ('Sanoma', 'SANOMA.HE', 'EUR', None, None, None, None, False, ''), ('Tietoevry', 'TIETO.HE', 'EUR', None, None, None, None, False, ''), ('Nordea', 'NDA-FI.HE', 'EUR', None, None, None, None, False, ''), ('Kemira', 'KEMIRA.HE', 'EUR', None, None, None, None, False, ''), ('IHI Corporation', '7013.T', 'JPY', None, None, None, None, False, 'VETO V9 / seguimiento'), ('FMC Corporation', 'FMC', 'USD', None, None, None, None, True, 'Cartera'), ('FinVolution Group', 'FINV', 'USD', None, None, None, None, True, 'Cartera'), ('Ingredion', 'INGR', 'USD', None, None, None, None, True, 'Cartera'), ('Pfizer', 'PFE', 'USD', None, None, None, None, True, 'Cartera'), ('Adidas', 'ADS.DE', 'EUR', None, None, None, None, True, 'Cartera'), ('Porsche SE', 'PAH3.DE', 'EUR', None, None, None, None, True, 'Cartera'), ('Huhtamäki', 'HUH1V.HE', 'EUR', None, None, None, None, True, 'Cartera'), ('Vallourec', 'VK.PA', 'EUR', None, None, None, None, True, 'Cartera'), ('Mitsubishi Corporation', '8058.T', 'JPY', None, None, None, None, True, 'Cartera'), ('Nippon Steel', '5401.T', 'JPY', None, None, None, None, True, 'Cartera'), ('BWX Technologies', 'BWXT', 'USD', None, None, None, None, True, 'Cartera')]

# Yahoo Finance cotiza muchas acciones de Londres en peniques (GBp).
# Nuestros umbrales V9 están expresados en libras (GBP).
LONDON_PENCE_SYMBOLS = {
    "DPLM.L","HLMA.L","GAW.L","RIO.L","CRDA.L"
}

def normalize_price(symbol, price):
    if price is None:
        return None
    if symbol in LONDON_PENCE_SYMBOLS:
        return price / 100.0
    return price

def get_prices():
    prices = {}
    for name, symbol, ccy, strong, buy, reduce, sell, in_portfolio, note in WATCHLIST:
        try:
            hist = yf.Ticker(symbol).history(period="5d", interval="1d", auto_adjust=False)
            if hist.empty or "Close" not in hist:
                prices[symbol] = None
            else:
                s = hist["Close"].dropna()
                raw = float(s.iloc[-1]) if len(s) else None
                prices[symbol] = normalize_price(symbol, raw)
        except Exception:
            prices[symbol] = None
    return prices

def zone(price, strong, buy, reduce, sell):
    if any(v is None for v in (strong, buy, reduce, sell)):
        return "SIN_UMBRAL"
    if price <= strong:
        return "COMPRA_FUERTE"
    if price <= buy:
        return "COMPRA"
    if price >= sell:
        return "VENTA"
    if price >= reduce:
        return "REDUCIR"
    return "MANTENER"

ZONE_LABELS = {
    "COMPRA_FUERTE":"🟢 COMPRA FUERTE",
    "COMPRA":"🟢 COMPRA",
    "MANTENER":"⚪ MANTENER",
    "REDUCIR":"🟠 REDUCIR",
    "VENTA":"🔴 VENTA",
    "SIN_UMBRAL":"⚪ Sin umbral V9 completo",
    "SIN_COTIZACION":"⚠️ Sin cotización",
}

def fmt(x, ccy):
    if x is None:
        return "—"
    prefix = {
        "EUR":"€","USD":"$","GBP":"£","CHF":"CHF ","SEK":"SEK ",
        "NOK":"NOK ","DKK":"DKK ","JPY":"¥","SGD":"S$"
    }.get(ccy, ccy + " ")
    decimals = 0 if ccy == "JPY" else 2
    txt = f"{x:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X",".")
    return prefix + txt

def load_state():
    try:
        if STATE_FILE.exists():
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    for i in range(0, len(text), 3900):
        r = requests.post(
            url,
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": text[i:i+3900],
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            },
            timeout=30
        )
        r.raise_for_status()

def main():
    previous = load_state()
    prices = get_prices()
    rows = []
    new_state = {}

    for item in WATCHLIST:
        name, symbol, ccy, strong, buy, reduce, sell, in_portfolio, note = item
        price = prices.get(symbol)
        z = "SIN_COTIZACION" if price is None else zone(price, strong, buy, reduce, sell)
        prev = previous.get(symbol, {}).get("zone")
        prev_price = previous.get(symbol, {}).get("price")
        changed = prev is not None and prev != z

        # Cambio diario aproximado respecto a la última ejecución del radar.
        change_pct = None
        if price is not None and prev_price not in (None, 0):
            change_pct = (price - prev_price) / prev_price * 100

        rows.append(
            (name, symbol, ccy, strong, buy, reduce, sell,
             in_portfolio, note, price, z, prev, changed, change_pct)
        )
        new_state[symbol] = {
            "zone": z,
            "price": price,
            "updated": datetime.now().isoformat()
        }

    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    msg = [f"<b>RADAR V9 — ALERTAS IMPORTANTES</b>\n{now}\n"]

    # 1) Solo COMPRA FUERTE como señal de entrada.
    strong_buy = [r for r in rows if r[10] == "COMPRA_FUERTE"]
    strong_buy.sort(key=lambda r: (not r[7], r[0]))

    newly_strong = [
        r for r in strong_buy
        if r[11] not in ("COMPRA_FUERTE", None)
    ]

    if newly_strong:
        msg.append("<b>🚨 NUEVA COMPRA FUERTE</b>")
        for r in newly_strong:
            name,symbol,ccy,strong,buy,reduce,sell,in_portfolio,note,price,z,prev,changed,change_pct = r
            mark = " 📌 CARTERA" if in_portfolio else ""
            discount = ((strong - price) / strong * 100) if strong and price is not None else None
            extra = f" | {abs(discount):.1f}% por debajo del umbral" if discount is not None and discount >= 0 else ""
            msg.append(
                f"• <b>{name}</b>{mark} — {fmt(price,ccy)}\n"
                f"  Compra fuerte ≤ {fmt(strong,ccy)}{extra}"
            )

    # Seguimos mostrando las que YA están en compra fuerte para que no se pierdan.
    existing_strong = [
        r for r in strong_buy
        if r[11] == "COMPRA_FUERTE" or r[11] is None
    ]
    if existing_strong:
        msg.append("\n<b>🟢 SIGUEN EN COMPRA FUERTE</b>")
        for r in existing_strong:
            name,symbol,ccy,strong,buy,reduce,sell,in_portfolio,note,price,z,prev,changed,change_pct = r
            mark = " 📌" if in_portfolio else ""
            msg.append(
                f"• {name}{mark}: {fmt(price,ccy)} | umbral ≤ {fmt(strong,ccy)}"
            )

    # 2) Posiciones en cartera: alertas defensivas.
    # La valoración por sobreprecio (REDUCIR/VENTA) sí puede ser señal directa.
    portfolio_reduce_sell = [
        r for r in rows
        if r[7] and r[10] in ("REDUCIR","VENTA")
    ]
    if portfolio_reduce_sell:
        msg.append("\n<b>⚠️ CARTERA — REDUCIR / VENDER POR VALORACIÓN</b>")
        for r in portfolio_reduce_sell:
            name,symbol,ccy,strong,buy,reduce,sell,in_portfolio,note,price,z,prev,changed,change_pct = r
            threshold = sell if z == "VENTA" else reduce
            msg.append(
                f"• <b>{name}</b> — {fmt(price,ccy)} — {ZONE_LABELS[z]}\n"
                f"  Umbral: {fmt(threshold,ccy)}"
            )

    # 3) Caídas fuertes en posiciones de cartera.
    # NO ordenamos vender solo por precio: activamos revisión defensiva.
    portfolio_falls = [
        r for r in rows
        if r[7] and r[13] is not None and r[13] <= -7.0
    ]
    if portfolio_falls:
        portfolio_falls.sort(key=lambda r: r[13])
        msg.append("\n<b>🛡️ CARTERA — CAÍDA FUERTE / REVISAR TESIS</b>")
        for r in portfolio_falls:
            name,symbol,ccy,strong,buy,reduce,sell,in_portfolio,note,price,z,prev,changed,change_pct = r
            msg.append(
                f"• <b>{name}</b> — {fmt(price,ccy)} — {change_pct:.1f}% desde la última revisión\n"
                f"  Revisar resultados/noticias y tesis V9 antes de decidir vender."
            )

    # 4) Empresas muy cerca de Compra Fuerte (máx. 5), no de compra normal.
    near_strong = []
    for r in rows:
        name,symbol,ccy,strong,buy,reduce,sell,in_portfolio,note,price,z,prev,changed,change_pct = r
        if price is not None and strong is not None and price > strong:
            d = (price - strong) / strong * 100
            if d <= 10:
                near_strong.append((d, r))
    near_strong.sort(key=lambda x: x[0])
    near_strong = near_strong[:5]

    if near_strong:
        msg.append("\n<b>🎯 CERCA DE COMPRA FUERTE</b>")
        for d,r in near_strong:
            name,symbol,ccy,strong,buy,reduce,sell,in_portfolio,note,price,z,prev,changed,change_pct = r
            mark = " 📌" if in_portfolio else ""
            msg.append(
                f"• {name}{mark}: {fmt(price,ccy)} | fuerte ≤ {fmt(strong,ccy)} | +{d:.1f}%"
            )

    # Si no hay nada relevante, mensaje corto.
    meaningful = bool(newly_strong or existing_strong or portfolio_reduce_sell or portfolio_falls or near_strong)
    if not meaningful:
        msg.append(
            "Sin alertas relevantes hoy: ninguna empresa en Compra Fuerte, "
            "ninguna posición en zona Reducir/Venta y ninguna caída defensiva ≥7%."
        )

    ok_quotes = sum(1 for r in rows if r[9] is not None)
    complete = sum(1 for r in rows if all(v is not None for v in r[3:7]))
    pending = len(rows) - complete

    msg.append(
        f"\nCobertura: {ok_quotes}/79"
        f"\nUmbrales V9 completos: {complete}/79"
        f"\nPendientes V9: {pending}"
    )

    save_state(new_state)
    send_telegram("\n".join(msg))

if __name__ == "__main__":
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise SystemExit("Faltan TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID")
    main()
