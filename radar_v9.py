import os
import time
from datetime import datetime
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")

# name, symbol, ccy, strong_buy, buy, reduce, sell, in_portfolio, note
WATCHLIST = [
    ("Diploma","DPLM:LSE","GBP",57.6,69.9,102.8,115.1,False,""),
    ("Halma","HLMA:LSE","GBP",30.8,37.4,54.9,61.5,False,""),
    ("Lifco","LIFCO-B:OMX","SEK",None,320,None,None,False,""),
    ("Addtech","ADDT-B:OMX","SEK",None,None,None,None,False,""),
    ("Indutrade","INDT:OMX","SEK",196,238,350,392,False,""),
    ("Lagercrantz","LAGR-B:OMX","SEK",190,231,340,381,False,""),
    ("Games Workshop","GAW:LSE","GBP",154.5,187.6,275.9,309.1,False,""),
    ("Belimo","BEAN:SIX","CHF",None,None,None,None,False,""),
    ("IMCD","IMCD:EURONEXT","EUR",90,105,150,170,False,""),
    ("Geberit","GEBN:SIX","CHF",405,492,724,811,False,""),
    ("Schindler","SCHP:SIX","CHF",None,None,None,None,False,""),
    ("Beijer Ref","BEIJ-B:OMX","SEK",None,None,None,None,False,""),
    ("ABB","ABBN:SIX","CHF",60,66,85,90,False,""),
    ("Munich Re","MUV2:XETR","EUR",None,None,None,None,False,""),
    ("Hannover Re","HNR1:XETR","EUR",None,None,None,None,False,""),
    ("Allianz","ALV:XETR","EUR",303,368,541,606,False,""),
    ("Amadeus IT","AMS:BME","EUR",None,None,None,None,False,""),
    ("Publicis","PUB:EURONEXT","EUR",None,None,None,None,False,""),
    ("Ahold Delhaize","AD:EURONEXT","EUR",27.0,32.8,48.2,54.0,False,""),
    ("Pandora","PNDORA:CSE","DKK",578,702,1033,1157,False,""),
    ("ASML","ASML:EURONEXT","EUR",1100,1250,1650,1900,False,""),
    ("Intuitive Surgical","ISRG:NASDAQ","USD",335,406,598,669,True,"Cartera"),
    ("SAP","SAP:XETR","EUR",145,176,259,290,True,"Cartera"),
    ("Nemetschek","NEM:XETR","EUR",60,70,103,115,True,"Cartera"),
    ("LVMH","MC:EURONEXT","EUR",435,460,625,700,True,"Cartera"),
    ("Sampo","SAMPO:OMX","EUR",8.5,9.5,13.2,14.8,False,""),
    ("BMW","BMW:XETR","EUR",None,None,None,None,True,"Cartera"),
    ("Nestlé","NESN:SIX","CHF",None,None,None,None,False,""),
    ("Sika","SIKA:SIX","CHF",None,None,None,None,False,""),
    ("Deutsche Börse","DB1:XETR","EUR",None,None,None,None,False,""),
    ("DNB","DNB:OSE","NOK",None,None,None,None,True,"Cartera"),
    ("Borregaard","BRG:OSE","NOK",None,None,None,None,True,"Cartera"),
    ("Qt Group","QTCOM:OMX","EUR",None,None,None,None,True,"Cartera"),
    ("Valmet","VALMT:OMX","EUR",None,None,None,None,True,"Cartera"),
    ("Tokmanni","TOKMAN:OMX","EUR",None,None,None,None,True,"Cartera"),
    ("Obayashi","1802:TSE","JPY",None,None,None,None,False,""),
    ("Shimano","7309:TSE","JPY",None,None,None,None,True,"Cartera"),
    ("Osaka Soda","4046:TSE","JPY",None,None,None,None,False,""),
    ("SIA Engineering","S59:SGX","SGD",None,None,None,None,False,""),
    ("Singapore Exchange","S68:SGX","SGD",None,None,None,None,False,""),
    ("Keppel","BN4:SGX","SGD",None,None,None,None,True,"Cartera"),
    ("Hongkong Land","H78:SGX","USD",None,None,None,None,False,""),
    ("Cellnex","CLNX:BME","EUR",None,None,None,None,True,"Cartera"),
    ("Viscofan","VIS:BME","EUR",None,None,None,None,True,"Cartera"),
    ("CIE Automotive","CIE:BME","EUR",None,None,None,None,True,"Cartera"),
    ("Saint-Gobain","SGO:EURONEXT","EUR",None,None,None,None,True,"Cartera"),
    ("Microsoft","MSFT:NASDAQ","USD",None,None,None,None,True,"Cartera"),
    ("Oracle","ORCL:NYSE","USD",None,None,None,None,True,"Cartera"),
    ("Danaher","DHR:NYSE","USD",None,None,None,None,False,""),
    ("Texas Instruments","TXN:NASDAQ","USD",None,None,None,None,False,""),
    ("Qualcomm","QCOM:NASDAQ","USD",None,None,None,None,True,"Cartera"),
    ("KLA","KLAC:NASDAQ","USD",None,None,None,None,False,""),
    ("TSMC","TSM:NYSE","USD",None,None,None,None,False,""),
    ("Berkshire Hathaway","BRK.B:NYSE","USD",None,None,None,None,False,""),
    ("Newmont","NEM:NYSE","USD",None,None,None,None,False,"Vendida; solo watchlist"),
    ("Cameco","CCJ:NYSE","USD",None,None,None,None,False,""),
    ("NexGen Energy","NXE:NYSE","USD",None,None,None,None,False,""),
    ("Repsol","REP:BME","EUR",None,None,None,None,False,""),
    ("Occidental Petroleum","OXY:NYSE","USD",None,None,None,None,False,""),
    ("Rio Tinto","RIO:LSE","GBP",None,None,None,None,True,"Cartera"),
    ("Vale","VALE:NYSE","USD",None,None,None,None,False,""),
    ("SQM","SQM:NYSE","USD",None,None,None,None,False,""),
    ("Croda","CRDA:LSE","GBP",None,None,None,None,False,""),
    ("Sanoma","SANOMA:OMX","EUR",None,None,None,None,False,""),
    ("Tietoevry","TIETO:OMX","EUR",None,None,None,None,False,""),
    ("Nordea","NDA-FI:OMX","EUR",None,None,None,None,False,""),
    ("Kemira","KEMIRA:OMX","EUR",None,None,None,None,False,""),
    ("IHI Corporation","7013:TSE","JPY",None,None,None,None,False,"VETO V9 / seguimiento"),

    # Añadidas por cartera actual
    ("FMC Corporation","FMC:NYSE","USD",None,None,None,None,True,"Cartera"),
    ("FinVolution Group","FINV:NYSE","USD",None,None,None,None,True,"Cartera"),
    ("Ingredion","INGR:NYSE","USD",None,None,None,None,True,"Cartera"),
    ("Pfizer","PFE:NYSE","USD",None,None,None,None,True,"Cartera"),
    ("Adidas","ADS:XETR","EUR",None,None,None,None,True,"Cartera"),
    ("Porsche SE","PAH3:XETR","EUR",None,None,None,None,True,"Cartera"),
    ("Huhtamäki","HUH1V:OMX","EUR",None,None,None,None,True,"Cartera"),
    ("Vallourec","VK:EURONEXT","EUR",None,None,None,None,True,"Cartera"),
    ("Mitsubishi Corporation","8058:TSE","JPY",None,None,None,None,True,"Cartera"),
    ("Nippon Steel","5401:TSE","JPY",None,None,None,None,True,"Cartera"),
    ("BWX Technologies","BWXT:NYSE","USD",None,None,None,None,True,"Cartera"),
]

def get_price(symbol):
    url = "https://api.twelvedata.com/price"
    r = requests.get(url, params={"symbol": symbol, "apikey": TWELVE_DATA_API_KEY}, timeout=20)
    data = r.json()
    if "price" not in data:
        return None
    try:
        return float(data["price"])
    except (TypeError, ValueError):
        return None

def zone(price, strong, buy, reduce, sell):
    # Requiere los 4 umbrales para clasificar sin ambigüedad.
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
    syms = {
        "EUR":"€","USD":"$","GBP":"£","CHF":"CHF ","SEK":"SEK ",
        "NOK":"NOK ","DKK":"DKK ","JPY":"¥","SGD":"S$"
    }
    s = syms.get(ccy, ccy + " ")
    return f"{s}{x:,.2f}".replace(",", "X").replace(".", ",").replace("X",".")

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    chunks = [text[i:i+3900] for i in range(0, len(text), 3900)]
    for ch in chunks:
        requests.post(
            url,
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": ch,
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            },
            timeout=20
        ).raise_for_status()

def main():
    rows = []
    for name, symbol, ccy, strong, buy, reduce, sell, in_portfolio, note in WATCHLIST:
        p = get_price(symbol)
        z = "⚠️ Sin cotización" if p is None else zone(p, strong, buy, reduce, sell)
        rows.append((name, symbol, ccy, p, strong, buy, reduce, sell, in_portfolio, note, z))
        time.sleep(0.15)

    active = [
        r for r in rows
        if r[10] in ("🟢 COMPRA FUERTE","🟢 COMPRA","🟠 REDUCIR","🔴 VENTA")
    ]

    # Priorizamos posiciones en cartera.
    active.sort(key=lambda r: (not r[8], r[0]))

    nearest = []
    for r in rows:
        name, symbol, ccy, p, strong, buy, reduce, sell, in_portfolio, note, z = r
        if p is not None and buy is not None and z == "⚪ MANTENER":
            d = (p - buy) / buy * 100
            if d >= 0:
                nearest.append((d, r))
    nearest = sorted(nearest, key=lambda x: x[0])[:12]

    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    msg = [f"<b>RADAR DIARIO V9 — {len(WATCHLIST)} EMPRESAS</b>\n{now}\n"]

    if active:
        msg.append("<b>Zonas activas</b>")
        for r in active:
            name, symbol, ccy, p, strong, buy, reduce, sell, in_portfolio, note, z = r
            portfolio = " 📌 CARTERA" if in_portfolio else ""
            msg.append(f"• <b>{name}</b>{portfolio} — {fmt(p,ccy)} — {z}")
    else:
        msg.append("No hay empresas en zonas activas con los umbrales V9 completos actualmente definidos.")

    if nearest:
        msg.append("\n<b>Más próximas a Compra</b>")
        for d, r in nearest:
            name, symbol, ccy, p, strong, buy, reduce, sell, in_portfolio, note, z = r
            portfolio = " 📌" if in_portfolio else ""
            msg.append(
                f"• {name}{portfolio}: {fmt(p,ccy)} | compra ≤ {fmt(buy,ccy)} | distancia {d:.1f}%"
            )

    portfolio_count = sum(1 for r in rows if r[8])
    pending = sum(1 for r in rows if r[10] == "⚪ Sin umbral V9 completo")
    failed = sum(1 for r in rows if r[10] == "⚠️ Sin cotización")

    msg.append(
        f"\nUniverso: {len(WATCHLIST)} | En cartera: {portfolio_count} | "
        f"Umbrales V9 incompletos: {pending} | Sin cotización: {failed}"
    )

    send_telegram("\n".join(msg))

if __name__ == "__main__":
    missing = [
        k for k, v in [
            ("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN),
            ("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID),
            ("TWELVE_DATA_API_KEY", TWELVE_DATA_API_KEY),
        ] if not v
    ]
    if missing:
        raise SystemExit("Faltan variables: " + ", ".join(missing))
    main()
