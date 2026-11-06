#!/usr/bin/env python3
"""Baut die öffentliche Vorlagen-Sammlung (GitHub Pages, Ordner docs/) aus register.json.

Jeder Eintrag mit Feld "vorlage" ({titel, text, hinweis}) wird eine Karte, neueste zuerst.
Aufruf (im Repo-Hauptordner): python3 engine/site/build.py
Ziel-URL: https://jonasnoen.github.io/jonasnoen-posts/
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LANG = sys.argv[1] if len(sys.argv) > 1 else 'de'   # 'de' (Standard) oder 'en' (englischer Kanal, komplett getrennt)
EN = LANG == 'en'
T = {k: (en if EN else de) for k, de, en in [
    ('copy', 'Kopieren', 'Copy'), ('copied', 'Kopiert ✓', 'Copied ✓'), ('sel', 'Bitte markieren und kopieren', 'Please select and copy'),
    ('new', 'Neu', 'New'), ('steps', 'So gehst du vor', 'How it works'), ('ex', 'Beispiel', 'Example'),
    ('check', 'Check vor dem Abschicken', 'Check before you send'), ('kick', '// Claude-Vorlagen', '// Claude guides'),
    ('h1', 'Kopieren, <em>einfügen</em>, fertig.', 'Copy, <em>paste</em>, done.'),
    ('lead', 'Alle Guides und Prompts aus meinen Reels und Karussells. Das Neueste steht oben.', 'Every guide and prompt from my posts. Newest on top.'),
    ('title', 'Claude-Vorlagen von Jonas', 'Claude Guides – copy & paste prompts'),
    ('desc', 'Alle Prompt-Vorlagen aus den Reels und Karussells von @jonas.noen zum Kopieren.', 'Step-by-step Claude guides with copy-paste prompts for real tasks.'),
    ('foot', 'Jeden Tag ein neuer Claude-Tipp: <a href="https://www.instagram.com/jonas.noen/">@jonas.noen auf Instagram</a> · <a href="https://www.tiktok.com/@jonas.noen">TikTok</a>',
             'A new Claude guide every day.')]}
REG = os.path.join(ROOT, 'en', 'register.json') if EN else os.path.join(ROOT, 'register.json')
OUT = os.path.join(ROOT, 'docs', 'en') if EN else os.path.join(ROOT, 'docs')
data = json.load(open(REG, encoding='utf-8'))
entries = data if isinstance(data, list) else data['entries']


def num(e):
    m = re.search(r'\d+', e.get('id', ''))
    return (e.get('createdAt', ''), int(m.group()) if m else 0)


items = [e for e in entries if e.get('vorlage')][::-1]  # Reihenfolge in register.json = zeitlich; neueste zuerst
TYP = {'reel': 'Reel', 'carousel': 'Carousel' if EN else 'Karussell', 'clip': 'Video', 'guide': 'Guide'}

cards = []
n = 0


def copybox(text):
    global n
    n += 1
    return (f'<pre id="v{n}">{html.escape(text)}</pre>\n'
            f'  <button type="button" data-copy="v{n}">{T["copy"]}</button>')


for i, e in enumerate(items):
    v = e['vorlage']
    gd = e.get('guide')
    tag = (T['new'] if i == 0 else '') + (' · Guide' if gd else '')
    tag = tag.strip(' ·') or TYP.get(e.get('type'), 'Post')
    head = (f'<article class="card{' new' if i == 0 else ''}" id="{html.escape(e.get('id', ''))}">\n'
            f'  <div class="meta"><span class="tag">{html.escape(tag)}</span><span>{html.escape(TYP.get(e.get('type'), 'Post'))} {html.escape(e.get('id', ''))}</span></div>\n'
            f'  <h2>{html.escape((gd or {}).get('titel') or v['titel'])}</h2>')
    if gd:
        body = [f'  <p class="goal">{html.escape(gd.get('ziel', ''))}</p>']
        if gd.get('schritte'):
            body.append(f'  <h3>{T["steps"]}</h3>\n  <ol class="steps">' + ''.join(
                f'<li><b>{html.escape(st['titel'])}</b> {html.escape(st.get('text', ''))}</li>' for st in gd['schritte']) + '</ol>')
        prompts = gd.get('prompts') or [{'titel': v['titel'], 'text': v['text']}]
        for k, pr in enumerate(prompts, 1):
            body.append(f'  <h3>Prompt {k}: {html.escape(pr['titel'])}</h3>\n  ' + copybox(pr['text']))
            if pr.get('wann'):
                body.append(f'  <p class="hint">{html.escape(pr['wann'])}</p>')
        if gd.get('beispiel'):
            body.append(f'  <h3>{T["ex"]}</h3>\n  <p class="ex">{html.escape(gd['beispiel'])}</p>')
        if gd.get('check'):
            body.append(f'  <h3>{T["check"]}</h3>\n  <ul class="check">' + ''.join(f'<li>{html.escape(c)}</li>' for c in gd['check']) + '</ul>')
        body.append(f'  <p class="hint">{html.escape(v.get('hinweis', ''))}</p>')
    else:
        body = ['  ' + copybox(v['text']), f'  <p class="hint">{html.escape(v.get('hinweis', ''))}</p>']
    cards.append(head + '\n' + '\n'.join(body) + '\n</article>')

page = f'''<!doctype html>
<html lang="{LANG}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{T["title"]}</title>
<meta name="description" content="{T["desc"]}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@1&family=Manrope:wght@500;800&display=swap" rel="stylesheet">
<style>
:root{{--bg:#f6efe4;--card:#fff;--ink:#17141f;--muted:#5d566d;--violet:#8b6cf0;--red:#ef5a4c;--line:#e6dccb;--code:#f7f3fb}}
@media (prefers-color-scheme:dark){{:root{{--bg:#17141f;--card:#221d30;--ink:#f6efe4;--muted:#b8b1c8;--violet:#b9a6ff;--red:#ff8f6b;--line:#352d48;--code:#2b2440}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:500 17px/1.55 Manrope,system-ui,sans-serif}}
main{{max-width:640px;margin:0 auto;padding:40px 16px 64px}}
.kick{{font:800 13px Manrope;letter-spacing:.14em;text-transform:uppercase;color:var(--violet)}}
h1{{font:800 clamp(34px,8vw,48px)/1.05 Manrope;letter-spacing:-.02em;margin:10px 0 12px}}
h1 em{{font:400 1.15em/1 'Instrument Serif',serif;font-style:italic;color:var(--red)}}
.lead{{color:var(--muted);margin:0 0 28px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:22px;margin:0 0 18px}}
.card.new{{border:2px solid var(--violet)}}
.meta{{display:flex;gap:10px;align-items:center;font:800 12px Manrope;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}}
.tag{{background:var(--violet);color:#fff;border-radius:20px;padding:3px 10px}}
h2{{font:800 22px/1.25 Manrope;margin:12px 0}}
pre{{white-space:pre-wrap;word-break:break-word;background:var(--code);border-radius:14px;padding:16px;margin:0 0 12px;font:500 16px/1.6 Manrope}}
button{{font:800 15px Manrope;border:0;border-radius:12px;padding:12px 18px;background:var(--ink);color:var(--bg);cursor:pointer;min-height:44px}}
.hint{{color:var(--muted);font-size:15px;margin:12px 0 0}}
h3{{font:800 16px Manrope;margin:22px 0 8px;color:var(--violet)}}
.goal{{margin:0 0 4px;color:var(--muted)}}
.steps,.check{{margin:0;padding-left:22px}}.steps li,.check li{{margin:0 0 8px}}
.ex{{background:var(--code);border-radius:14px;padding:14px 16px;margin:0;font-size:15px}}
footer{{color:var(--muted);font-size:14px;margin-top:32px}}
footer a{{color:var(--violet)}}
</style></head><body><main>
<div class="kick">{T["kick"]}</div>
<h1>{T["h1"]}</h1>
<p class="lead">{T["lead"]}</p>
{''.join(cards)}
<footer>{T["foot"]}</footer>
</main>
<script>
document.querySelectorAll('button[data-copy]').forEach(b=>b.addEventListener('click',async()=>{{
  const t=document.getElementById(b.dataset.copy).innerText;
  try{{await navigator.clipboard.writeText(t);b.textContent='{T["copied"]}';}}catch(e){{b.textContent='{T["sel"]}';}}
  setTimeout(()=>b.textContent='{T["copy"]}',2000);}}));
</script>
</body></html>
'''
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page)
open(os.path.join(ROOT, 'docs', '.nojekyll'), 'w').write('')
print(len(items), 'Vorlagen ->', os.path.relpath(os.path.join(OUT, 'index.html'), ROOT))
