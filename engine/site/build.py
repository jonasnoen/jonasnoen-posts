#!/usr/bin/env python3
"""Baut die öffentliche Vorlagen-Sammlung (GitHub Pages, Ordner docs/) aus register.json.

Jeder Eintrag mit Feld "vorlage" ({titel, text, hinweis}) wird eine Karte, neueste zuerst.
Aufruf (im Repo-Hauptordner): python3 engine/site/build.py
Ziel-URL: https://jonasnoen.github.io/jonasnoen-posts/
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data = json.load(open(os.path.join(ROOT, 'register.json'), encoding='utf-8'))
entries = data if isinstance(data, list) else data['entries']


def num(e):
    m = re.search(r'\d+', e.get('id', ''))
    return (e.get('createdAt', ''), int(m.group()) if m else 0)


items = [e for e in entries if e.get('vorlage')][::-1]  # Reihenfolge in register.json = zeitlich; neueste zuerst
TYP = {'reel': 'Reel', 'carousel': 'Karussell', 'clip': 'Video'}

cards = []
for i, e in enumerate(items):
    v = e['vorlage']
    tag = 'Neu' if i == 0 else TYP.get(e.get('type'), 'Post')
    cards.append(f'''<article class="card{' new' if i == 0 else ''}">
  <div class="meta"><span class="tag">{html.escape(tag)}</span><span>{html.escape(TYP.get(e.get('type'), 'Post') if i == 0 else e.get('id', ''))}{(' ' + html.escape(e.get('id', ''))) if i == 0 else ''}</span></div>
  <h2>{html.escape(v['titel'])}</h2>
  <pre id="v{i}">{html.escape(v['text'])}</pre>
  <button type="button" data-copy="v{i}">Kopieren</button>
  <p class="hint">{html.escape(v.get('hinweis', ''))}</p>
</article>''')

page = f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Claude-Vorlagen von Jonas</title>
<meta name="description" content="Alle Prompt-Vorlagen aus den Reels und Karussells von @jonas.noen zum Kopieren.">
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
footer{{color:var(--muted);font-size:14px;margin-top:32px}}
footer a{{color:var(--violet)}}
</style></head><body><main>
<div class="kick">// Claude-Vorlagen</div>
<h1>Kopieren, <em>einfügen</em>, fertig.</h1>
<p class="lead">Alle Prompts aus meinen Reels und Karussells. Die neueste Vorlage steht oben.</p>
{''.join(cards)}
<footer>Jeden Tag ein neuer Claude-Tipp: <a href="https://www.instagram.com/jonas.noen/">@jonas.noen auf Instagram</a> · <a href="https://www.tiktok.com/@jonas.noen">TikTok</a></footer>
</main>
<script>
document.querySelectorAll('button[data-copy]').forEach(b=>b.addEventListener('click',async()=>{{
  const t=document.getElementById(b.dataset.copy).innerText;
  try{{await navigator.clipboard.writeText(t);b.textContent='Kopiert ✓';}}catch(e){{b.textContent='Bitte markieren und kopieren';}}
  setTimeout(()=>b.textContent='Kopieren',2000);}}));
</script>
</body></html>
'''
os.makedirs(os.path.join(ROOT, 'docs'), exist_ok=True)
open(os.path.join(ROOT, 'docs', 'index.html'), 'w', encoding='utf-8').write(page)
open(os.path.join(ROOT, 'docs', '.nojekyll'), 'w').write('')
print(len(items), 'Vorlagen -> docs/index.html')
