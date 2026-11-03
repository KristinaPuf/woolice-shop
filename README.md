# Woolice Felts

Handmade needle-felted dog sculptures: shop, gallery and custom order form.

## Structure
```
index.html        (stranica, radi i na GitHub Pages i na Renderu)
static/images/    (sve slike)
app.py            (Flask backend: /order šalje porudžbinu na Telegram)
requirements.txt
.env              (BOT_TOKEN i CHAT_ID, nikad na GitHub)
.nojekyll
```

## Render
Start command: `gunicorn app:app`
Environment variables: `BOT_TOKEN`, `CHAT_ID`

## GitHub Pages
U `index.html` zameni `PUT_YOUR_RENDER_URL_HERE` adresom Render servisa.
