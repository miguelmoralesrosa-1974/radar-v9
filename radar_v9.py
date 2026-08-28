import os, json
from datetime import datetime
from pathlib import Path
import requests
import yfinance as yf

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
STATE_FILE = Path("radar_state.json")

WATCHLIST = [('Diploma', 'DPLM.L', 'GBP', 60, 70, 87.5, 98, False, ''), ('Halma', 'HLMA.L', 'GBP', 33, 38, 50, 56, False, ''), ('Lifco', 'LIFCO-B.ST', 'SEK', 260, 290, None, None, False, ''), ('Addtech', 'ADDT-B.ST', 'SEK', None, None, None, None, False, ''), ('Indutrade', 'INDT.ST', 'SEK', 196, 238, 350, 392, False, ''), ('Lagercrantz', 'LAGR-B.ST', 'SEK', 190, 231, 340, 381, False, ''), ('Games Workshop', 'GAW.L', 'GBP', 155, 170, 212.5, 238, False, ''), ('Belimo', 'BEAN.SW', 'CHF', 575, 625, None, None, False, ''), ('IMCD', 'IMCD.AS', 'EUR', 90, 105, 154, 172, False, ''), ('Geberit', 'GEBN.SW', 'CHF', 405, 492, 724, 811, False, ''), ('Schindler', 'SCHP.SW', 'CHF', None, None, None, None, False, ''), ('Beijer Ref', 'BEIJ-B.ST', 'SEK', None, None, None, None, False, ''), ('ABB', 'ABBN.SW', 'CHF', 66, 72, 90, 101, False, ''), ('Munich Re', 'MUV2.DE', 'EUR', 450, 500, None, None, False, ''), ('Hannover Re', 'HNR1.DE', 'EUR', None, None, None, None, False, ''), ('Allianz', 'ALV.DE', 'EUR', 303, 368, 541, 606, False, ''), ('Amadeus IT', 'AMS.MC', 'EUR', None, None, None, None, False, ''), ('Publicis', 'PUB.PA', 'EUR', None, None, None, None, False, ''), ('Ahold Delhaize', 'AD.AS', 'EUR', 27, 32.8, 48.2, 54, False, ''), ('Pandora', 'PNDORA.CO', 'DKK', 578, 702, 1033, 1157, False, ''), ('ASML', 'ASML.AS', 'EUR', 1100, 1250, 1650, 1900, False, ''), ('Intuitive Surgical', 'ISRG', 'USD', 285, 345, 598, 669, True, 'Cartera'), ('SAP', 'SAP.DE', 'EUR', 160, 190, 265, 297, True, 'Cartera'), ('Nemetschek', 'NEM.DE', 'EUR', 60, 70, 103, 115, True, 'Cartera'), ('LVMH', 'MC.PA', 'EUR', 435, 460, 616, 690, True, 'Cartera'), ('Sampo', 'SAMPO.HE', 'EUR', 8.5, 9.5, 13.2, 14.8, False, ''), ('BMW', 'BMW.DE', 'EUR', None, None, None, None, True, 'Cartera'), ('Nestlé', 'NESN.SW', 'CHF', None, None, None, None, False, ''), ('Sika', 'SIKA.SW', 'CHF', None, None, None, None, False, ''), ('Deutsche Börse', 'DB1.DE', 'EUR', None, None, None, None, False, ''), ('DNB', 'DNB.OL', 'NOK', None, None, None, None, True, 'Cartera'), ('Borregaard', 'BRG.OL', 'NOK', None, None, None, None, True, 'Cartera'), ('Qt Group', 'QTCOM.HE', 'EUR', None, None, None, None, True, 'Cartera'), ('Valmet', 'VALMT.HE', 'EUR', None, None, None, None, True, 'Cartera'), ('Tokmanni', 'TOKMAN.HE', 'EUR', None, None, None, None, True, 'Cartera'), ('Obayashi', '1802.T', 'JPY', None, None, None, None, False, ''), ('Shimano', '7309.T', 'JPY', None, None, None, None, True, 'Cartera'), ('Osaka Soda', '4046.T', 'JPY', None, None, None, None, False, ''), ('SIA Engineering', 'S59.SI', 'SGD', None, None, None, None, False, ''), ('Singapore Exchange', 'S68.SI', 'SGD', None, None, None, None, False, ''), ('Keppel', 'BN4.SI', 'SGD', None, None, None, None, True, 'Cartera'), ('Hongkong Land', 'H78.SI', 'USD', None, None, None, None, False, ''), ('Cellnex', 'CLNX.MC', 'EUR', None, None, None, None, True, 'Cartera'), ('Viscofan', 'VIS.MC', 'EUR', None, None, None, None, True, 'Cartera'), ('CIE Automotive', 'CIE.MC', 'EUR', None, None, None, None, True, 'Cartera'), ('Saint-Gobain', 'SGO.PA', 'EUR', None, None, None, None, True, 'Cartera'), ('Microsoft', 'MSFT', 'USD', None, None, None, None, True, 'Cartera'), ('Oracle', 'ORCL', 'USD', None, None, None, None, True, 'Cartera'), ('Danaher', 'DHR', 'USD', None, None, None, None, False, ''), ('Texas Instruments', 'TXN', 'USD', None, None, None, None, False, ''), ('Qualcomm', 'QCOM', 'USD', None, None, None, None, True, 'Cartera'), ('KLA', 'KLAC', 'USD', None, None, None, None, False, ''), ('TSMC', 'TSM', 'USD', None, None, None, None, False, ''), ('Berkshire Hathaway', 'BRK-B', 'USD', None, None, None, None, False, ''), ('Newmont', 'NEM', 'USD', None, None, None, None, False, 'Vendida; solo watchlist'), ('Cameco', 'CCJ', 'USD', None, None, None, None, False, ''), ('NexGen Energy', 'NXE', 'USD', None, None, None, None, False, ''), ('Repsol', 'REP.MC', 'EUR', None, None, None, None, False, ''), ('Occidental Petroleum', 'OXY', 'USD', None, None, None, None, False, ''), ('Rio Tinto', 'RIO.L', 'GBP', None, None, None, None, True, 'Cartera'), ('Vale', 'VALE', 'USD', None, None, None, None, False, ''), ('SQM', 'SQM', 'USD', None, None, None, None, False, ''), ('Croda', 'CRDA.L', 'GBP', None, None, None, None, False, ''), ('Sanoma', 'SANOMA.HE', 'EUR', None, None, None, None, False, ''), ('Tietoevry', 'TIETO.HE', 'EUR', None, None, None, None, False, ''), ('Nordea', 'NDA-FI.HE', 'EUR', None, None, None, None, False, ''), ('Kemira', 'KEMIRA.HE', 'EUR', None, None, None, None, False, ''), ('IHI Corporation', '7013.T', 'JPY', None, None, None, None, False, 'VETO V9 / seguimiento'), ('FMC Corporation', 'FMC', 'USD', None, None, None, None, True, 'Cartera'), ('FinVolution Group', 'FINV', 'USD', None, None, None, None, True, 'Cartera'), ('Ingredion', 'INGR', 'USD', None, None, None, None, True, 'Cartera'), ('Pfizer', 'PFE', 'USD', None, None, None, None, True, 'Cartera'), ('Adidas', 'ADS.DE', 'EUR', None, None, None, None, True, 'Cartera'), ('Porsche SE', 'PAH3.DE', 'EUR', None, None, None, None, True, 'Cartera'), ('Huhtamäki', 'HUH1V.HE', 'EUR', None, None, None, None, True, 'Cartera'), ('Vallourec', 'VK.PA', 'EUR', None, None, None, None, True, 'Cartera'), ('Mitsubishi Corporation', '8058.T', 'JPY', None, None, None, None, True, 'Cartera'), ('Nippon Steel', '5401.T', 'JPY', None, None, None, None, True, 'Cartera'), ('BWX Technologies', 'BWXT', 'USD', 145, 160, 225, 252, True, 'Cartera')]


LEVEL_SOURCE = {'DPLM.L': 'V9 recuperado', 'HLMA.L': 'V9 recuperado', 'LIFCO-B.ST': 'V9 recuperado parcial', 'GAW.L': 'V9 recuperado', 'BEAN.SW': 'V8/V9 recuperado parcial', 'IMCD.AS': 'V9 recuperado', 'ABBN.SW': 'V9 recuperado', 'MUV2.DE': 'V9 recuperado parcial', 'SAP.DE': 'V8/V9 recuperado', 'NEM.DE': 'V8/V9 recuperado', 'MC.PA': 'V8/V9 recuperado', 'ASML.AS': 'V9 recuperado', 'BWXT': 'V8 recuperado', 'ISRG': 'V6 previo / provisional'}

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
    # Clasificación parcial: usa cualquier umbral que sí esté definido.
    if strong is not None and price <= strong:
        return "COMPRA_FUERTE"
    if buy is not None and price <= buy:
        return "COMPRA"
    if sell is not None and price >= sell:
        return "VENTA"
    if reduce is not None and price >= reduce:
        return "REDUCIR"
    if any(v is not None for v in (strong, buy, reduce, sell)):
        return "MANTENER_PARCIAL"
    return "SIN_UMBRAL"

ZONE_LABELS = {
    "COMPRA_FUERTE":"🟢 COMPRA FUERTE",
    "COMPRA":"🟢 COMPRA",
    "MANTENER":"⚪ MANTENER",
    "MANTENER_PARCIAL":"⚪ MANTENER (niveles parciales)",
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
        change_pct = None
        if price is not None and prev_price not in (None, 0):
            change_pct = (price - prev_price) / prev_price * 100
        source = LEVEL_SOURCE.get(symbol, "pendiente")
        rows.append((name,symbol,ccy,strong,buy,reduce,sell,in_portfolio,note,price,z,prev,changed,change_pct,source))
        new_state[symbol] = {"zone":z,"price":price,"updated":datetime.now().isoformat()}

    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    msg = [f"<b>RADAR DIARIO V9 — 79 EMPRESAS</b>\n{now}"]

    changes = [r for r in rows if r[12] and r[10] not in ("SIN_UMBRAL","SIN_COTIZACION")]
    if changes:
        msg.append("\n<b>🔔 CAMBIOS DE ZONA</b>")
        for r in sorted(changes, key=lambda r:(not r[7],r[0])):
            name,symbol,ccy,strong,buy,reduce,sell,in_portfolio,note,price,z,prev,changed,change_pct,source = r
            mark = " 📌" if in_portfolio else ""
            msg.append(f"• <b>{name}</b>{mark}: {ZONE_LABELS.get(prev,prev)} → {ZONE_LABELS[z]} | {fmt(price,ccy)}")

    strong_rows = [r for r in rows if r[10] == "COMPRA_FUERTE"]
    if strong_rows:
        msg.append("\n<b>🚨 COMPRA FUERTE</b>")
        for r in sorted(strong_rows, key=lambda r:(not r[7],r[0])):
            name,symbol,ccy,strong,buy,reduce,sell,in_portfolio,note,price,z,prev,changed,change_pct,source = r
            mark = " 📌 CARTERA" if in_portfolio else ""
            msg.append(f"• <b>{name}</b>{mark}: {fmt(price,ccy)} | fuerte ≤ {fmt(strong,ccy)} | {source}")

    near = []
    for r in rows:
        name,symbol,ccy,strong,buy,reduce,sell,in_portfolio,note,price,z,prev,changed,change_pct,source = r
        if price is not None and strong is not None and price > strong:
            d = (price-strong)/strong*100
            if d <= 10:
                near.append((d,r))
    near.sort(key=lambda x:x[0])
    if near:
        msg.append("\n<b>🎯 CERCA DE COMPRA FUERTE</b>")
        for d,r in near[:8]:
            name,symbol,ccy,strong,buy,reduce,sell,in_portfolio,note,price,z,prev,changed,change_pct,source = r
            mark = " 📌" if in_portfolio else ""
            msg.append(f"• {name}{mark}: {fmt(price,ccy)} | fuerte ≤ {fmt(strong,ccy)} | +{d:.1f}%")

    portfolio = [r for r in rows if r[7]]
    if portfolio:
        msg.append("\n<b>📌 CARTERA — SITUACIÓN V9</b>")
        for r in sorted(portfolio, key=lambda r:r[0]):
            name,symbol,ccy,strong,buy,reduce,sell,in_portfolio,note,price,z,prev,changed,change_pct,source = r
            delta = f" | Δ {change_pct:+.1f}%" if change_pct is not None else ""
            if z == "SIN_UMBRAL":
                status = "⚪ valoración pendiente"
                levels = ""
            else:
                status = ZONE_LABELS.get(z,z)
                parts = []
                if strong is not None: parts.append(f"F≤{fmt(strong,ccy)}")
                if buy is not None: parts.append(f"C≤{fmt(buy,ccy)}")
                if reduce is not None: parts.append(f"R≥{fmt(reduce,ccy)}")
                if sell is not None: parts.append(f"V≥{fmt(sell,ccy)}")
                levels = " | " + " · ".join(parts) if parts else ""
            msg.append(f"• <b>{name}</b>: {fmt(price,ccy)} — {status}{levels}{delta}")

    defensive = [r for r in rows if r[7] and (
        r[10] in ("REDUCIR","VENTA") or
        (r[13] is not None and r[13] <= -7.0)
    )]
    if defensive:
        msg.append("\n<b>⚠️ CARTERA — REVISIÓN / SALIDA</b>")
        for r in defensive:
            name,symbol,ccy,strong,buy,reduce,sell,in_portfolio,note,price,z,prev,changed,change_pct,source = r
            if z in ("REDUCIR","VENTA"):
                threshold = sell if z=="VENTA" else reduce
                msg.append(f"• <b>{name}</b>: {fmt(price,ccy)} — {ZONE_LABELS[z]} | umbral {fmt(threshold,ccy)}")
            else:
                msg.append(f"• <b>{name}</b>: {fmt(price,ccy)} | caída {change_pct:.1f}% — revisar tesis V9.")

    known_watch = [r for r in rows if not r[7] and any(v is not None for v in r[3:7])]
    if known_watch:
        msg.append("\n<b>📋 WATCHLIST — NIVELES DISPONIBLES</b>")
        for r in sorted(known_watch,key=lambda r:r[0]):
            name,symbol,ccy,strong,buy,reduce,sell,in_portfolio,note,price,z,prev,changed,change_pct,source = r
            parts=[]
            if strong is not None: parts.append(f"F≤{fmt(strong,ccy)}")
            if buy is not None: parts.append(f"C≤{fmt(buy,ccy)}")
            if reduce is not None: parts.append(f"R≥{fmt(reduce,ccy)}")
            if sell is not None: parts.append(f"V≥{fmt(sell,ccy)}")
            msg.append(f"• {name}: {fmt(price,ccy)} — {ZONE_LABELS.get(z,z)} | " + " · ".join(parts))

    ok_quotes = sum(1 for r in rows if r[9] is not None)
    any_levels = sum(1 for r in rows if any(v is not None for v in r[3:7]))
    full_levels = sum(1 for r in rows if all(v is not None for v in r[3:7]))
    msg.append(
        f"\n<b>RESUMEN</b>\nCotizaciones: {ok_quotes}/79"
        f"\nCon algún nivel recuperado: {any_levels}/79"
        f"\nCon 4 niveles completos: {full_levels}/79"
        f"\nSin valoración recuperada: {79-any_levels}"
    )

    save_state(new_state)
    send_telegram("\n".join(msg))

if __name__ == "__main__":
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise SystemExit("Faltan TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID")
    main()
