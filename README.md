# Radar V9 → Telegram — 79 empresas

Versión ampliada del Radar V9. Incluye:

- Las 68 empresas de la Watchlist Maestra V9.
- 11 compañías adicionales detectadas en la cartera actual.
- Marcado `📌 CARTERA` en Telegram para priorizar posiciones que ya posees.
- Umbrales V9 ya disponibles para Compra fuerte, Compra, Reducir y Venta.
- Las compañías con valoración V9 incompleta aparecen como pendientes: el sistema no inventa niveles.
- Newmont permanece como watchlist, no como posición actual.
- IHI permanece con nota `VETO V9 / seguimiento`.

## Empresas añadidas por cartera

FMC Corporation, FinVolution Group, Ingredion, Pfizer, Adidas, Porsche SE,
Huhtamäki, Vallourec, Mitsubishi Corporation, Nippon Steel y BWX Technologies.

## Secrets necesarios

En tu repositorio de GitHub:

`Settings > Secrets and variables > Actions > New repository secret`

Añade:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `TWELVE_DATA_API_KEY`

## Configurar Telegram

1. Crea un bot con `@BotFather`.
2. Copia el token del bot.
3. Envía cualquier mensaje a tu nuevo bot.
4. Consulta `getUpdates` de la API de Telegram y localiza el `chat.id`.
5. Guarda token y chat id como los secrets indicados arriba.

## Fuente de cotizaciones

El script usa Twelve Data. Algunos mercados internacionales pueden requerir
un plan que cubra esa bolsa o un ticker distinto del propuesto.

Si un símbolo no se resuelve, el radar lo marca como `⚠️ Sin cotización`,
en lugar de utilizar un dato dudoso.

## GitHub Actions

El workflow se ejecuta de lunes a viernes a las 16:30 UTC, aproximadamente
18:30 en Madrid durante horario de verano.

También puedes ejecutarlo manualmente desde:

`Actions > Radar V9 Telegram > Run workflow`

## Actualizar los niveles V9

Los niveles están en `WATCHLIST`, dentro de `radar_v9.py`:

`strong_buy, buy, reduce, sell`

Cuando completemos un nuevo análisis V9 basta con reemplazar los `None`
correspondientes. El radar empezará a evaluar automáticamente esa empresa.

## Nota importante

Este radar es un sistema de vigilancia, no una orden automática de compra o
venta. Si una cotización cruza un umbral tras una noticia fundamental,
conviene revisar primero si el Fair Value V9 también ha cambiado.
