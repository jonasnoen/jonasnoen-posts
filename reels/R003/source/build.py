#!/usr/bin/env python3
"""Deutsche Fassung des Ukiyo-e-Videos: Szenen auf deutsche Sätze retimen, Untertitel-Tafeln ersetzen, Musik drunter."""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 720, 1280
SRC = '/mnt/user-data/attachments/4bca40a0-be09-5d7d-8090-3a6b2605bdea/2bc6a2dd-Video-67558.mp4'
MUSIC = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/jonasnoen-posts/assets/music/lofi-105.mp3'
os.makedirs('ov', exist_ok=True)
F4 = 'fnt/crimson400.ttf'; F5 = 'fnt/crimson500.ttf'
CJK = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
if not os.path.exists(CJK):
    CJK = subprocess.run(['fc-match', '-f', '%{file}', 'Noto Sans CJK JP:bold'], capture_output=True, text=True).stdout

# Originale Satzanfänge (Untertitelwechsel im englischen Video, Sekunden)
ORIG = [0.0, 6.0, 9.0, 11.0, 15.5, 18.0, 21.5, 23.5, 27.0, 30.0, 33.0, 35.0, 38.5, 40.5, 45.5, 48.0, 50.5, 54.5, 57.5, 61.5, 64.5, 67.5, 70.0, 73.0, 76.5, 80.0]
VEND = 84.28
# Deutsche Untertitel (Text der Tafel) + erstes/letztes Wort im Transkript
DE = [
 'Es war einmal ein Creator, der entdeckte, dass Claude Videos machen kann.',
 'Doch bald nutzten es alle.',
 'Und er hatte eine Frage:',
 'Wenn alle dieselbe KI haben – wie macht er etwas anderes?',
 'Dann entdeckte er fünf Skills.',
 'Und jeder öffnete eine völlig andere Welt.',
 'Der erste war HyperFrames von HeyGen.',
 'Eine Welt, in der HTML zu Motion Graphics wird',
 'und Code zu einer filmischen Geschichte.',
 'Der zweite war OneTake. Eine Welt ohne Schnitte,',
 'in der die Kamera nie stillsteht',
 'und die ganze Geschichte in einer einzigen Einstellung spielt.',
 'Der dritte war Collage B-Roll.',
 'Hier werden Papierschnitte, Rastertexturen und geschichtete Illustrationen lebendig,',
 'und Googles Gemini hilft bei den Bildern.',
 'Der vierte war Claude Animation Base.',
 'Hier wird Claudes kleines Maskottchen zum Star handgemalter Cartoons.',
 'Und zum Schluss: Lemo Opuscar.',
 '43 verschiedene Filmstile, ganze Filme nur aus Code,',
 'ganz ohne klassisches Videomodell.',
 'Fünf Skills. Fünf verschiedene Welten.',
 'Und alle warten auf GitHub darauf, entdeckt zu werden.',
 'Denn der Creator hatte endlich etwas verstanden.',
 'Die Zukunft gehört nicht dem, der KI benutzt.',
 'Sie gehört dem, der damit etwas anderes erschafft.',
 'Lern nicht nur KI. Lern, was du damit erschaffen kannst.',
]
S = [0.0, 5.04, 7.2, 9.12, 13.92, 16.4, 19.52, 22.56, 26.0, 28.88, 32.56, 34.48, 38.24, 40.72, 46.08, 48.88, 51.68, 56.16, 58.96, 63.56, 66.16, 69.2, 72.48, 75.52, 78.64, 81.92]
import re
out = subprocess.run(['ffmpeg','-i','voice_de.mp3','-af','silencedetect=n=-40dB:d=0.12','-f','null','-'],capture_output=True,text=True).stderr
SIL = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', out)]
seg = []
for k, s in enumerate(S):
    nxt = S[k+1] if k+1 < len(S) else 86.0
    cand = [x for x in SIL if s + 0.3 < x <= nxt]
    seg.append((s, max(cand) if cand else nxt - 0.05))
print([(round(a,2),round(b,2)) for a,b in seg])

# Neue Zeitachse: Satz i startet bei N[i]; Video-Abschnitt i wird auf N[i+1]-N[i] gestreckt
LEAD, GAP = 0.35, 0.3
N = [0.0]
for k in range(1, len(DE)):
    prev_need = LEAD + (seg[k - 1][1] - seg[k - 1][0]) + GAP
    vid = ORIG[k] - ORIG[k - 1]
    N.append(N[-1] + max(prev_need, 0.8 * vid))
last_need = LEAD + (seg[-1][1] - seg[-1][0]) + 0.9
TOTAL = N[-1] + max(last_need, 0.8 * (VEND - ORIG[-1]))
bounds = ORIG + [VEND]; nb = N + [TOTAL]
CTA = os.path.exists('cta.mp3'); EXTRA = 4.0 if CTA else 0.0; T2 = TOTAL + EXTRA
def remap(t):
    for k in range(len(bounds) - 1):
        if bounds[k] <= t <= bounds[k + 1]:
            return nb[k] + (t - bounds[k]) * (nb[k + 1] - nb[k]) / (bounds[k + 1] - bounds[k])
    return TOTAL

# --- Video retimen (nur Bild) ---
parts = []
for k in range(len(bounds) - 1):
    f = (nb[k + 1] - nb[k]) / (bounds[k + 1] - bounds[k])
    parts.append(f'[0:v]trim={bounds[k]:.3f}:{bounds[k+1]:.3f},setpts=(PTS-STARTPTS)*{f:.5f}[v{k}]')
fc = ';'.join(parts) + ';' + ''.join(f'[v{k}]' for k in range(len(parts))) + f'concat=n={len(parts)}:v=1:a=0,fps=30,setsar=1,tpad=stop_mode=clone:stop_duration={EXTRA:.2f}[v]'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-filter_complex', fc, '-map', '[v]', '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', 'retimed.mp4'], check=True)

# --- Untertitel-Tafeln ---
INK = (36, 24, 10); FILL = (241, 231, 202)
def seal(d, x, y, s=26):
    d.rounded_rectangle([x, y, x + s, y + s], radius=3, fill=(178, 64, 50))
    fz = ImageFont.truetype(CJK, int(s * 0.72))
    d.text((x + s / 2, y + s / 2 + 1), '絵', font=fz, fill=(250, 235, 225), anchor='mm')
def wrap(d, text, font, maxw):
    out, line = [], ''
    for w in text.split():
        t = (line + ' ' + w).strip()
        if d.textlength(t, font=font) > maxw and line: out.append(line); line = w
        else: line = t
    out.append(line); return out
def caption(text, path):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 20, 918, 700, 1070
    d.rectangle([x0, y0, x1, y1], fill=FILL, outline=INK, width=2)
    d.rectangle([x0 + 5, y0 + 5, x1 - 5, y1 - 5], outline=INK, width=1)
    seal(d, x0 + 22, (y0 + y1) // 2 - 13)
    size = 31
    while True:
        font = ImageFont.truetype(F4, size); lines = wrap(d, text, font, 560)
        if len(lines) <= 3 or size <= 24: break
        size -= 1
    lh = size * 1.22; ty = (y0 + y1) / 2 - lh * (len(lines) - 1) / 2
    for j, l in enumerate(lines):
        d.text((x0 + 60 + 560 / 2 + 6, ty + j * lh), l, font=font, fill=INK, anchor='mm')
    im.save(path)
def label(text, box, path, size=32, spacing=2, inner=True, fill=(240, 229, 200), gh=False):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=fill, outline=INK if inner else None, width=2 if inner else 0)
    if inner: d.rectangle([x0 + 4, y0 + 4, x1 - 4, y1 - 4], outline=INK, width=1)
    font = ImageFont.truetype(F4, size)
    tw = sum(d.textlength(ch, font=font) + spacing for ch in text) - spacing
    x = (x0 + x1) / 2 - tw / 2 + (14 if gh else 0); y = (y0 + y1) / 2
    if gh:
        d.ellipse([x - 34, y - 13, x - 8, y + 13], fill=INK)
    for ch in text:
        d.text((x, y), ch, font=font, fill=INK, anchor='lm'); x += d.textlength(ch, font=font) + spacing
    im.save(path)

ovs = []
for k, t in enumerate(DE):
    p = f'ov/c{k:02d}.png'; caption(t, p)
    a = 0.0 if k == 0 else N[k] - 0.05
    b = (N[k + 1] - 0.05) if k + 1 < len(N) else (TOTAL - 0.05 if CTA else TOTAL + 1)
    ovs.append((p, a, b))
if CTA:
    caption('Kommentiere PROMPT und ich schick dir die Vorlage.', 'ov/cta.png'); ovs.append(('ov/cta.png', TOTAL - 0.05, T2 + 1))
label('Fünf Skills, fünf Welten', (118, 128, 603, 191), 'ov/h1.png', size=34, spacing=2.2)
label('Entdecke sie auf GitHub', (118, 695, 603, 749), 'ov/h2.png', size=31, spacing=2.0, gh=True)
label('Filmstile', (262, 766, 458, 804), 'ov/h3.png', size=26, spacing=0.5, inner=False, fill=(243, 235, 214))
for p, oa, ob in [('ov/h1.png', 62.9, 70.35), ('ov/h2.png', 64.2, 70.35), ('ov/h3.png', 57.6, 64.6)]:
    ovs.append((p, remap(oa), remap(ob)))

# --- Ton: Sätze an N[k]+LEAD legen, Musik drunter, -14 LUFS ---
inputs = ['-i', 'retimed.mp4']; for_ov = ''
for p, _, _ in ovs: inputs += ['-i', p]
chain = '[0:v]'
for j, (p, a, b) in enumerate(ovs):
    out = f'[o{j}]'
    for_ov += f'{chain}[{j+1}:v]overlay=0:0:enable=\'between(t,{a:.3f},{b:.3f})\'{out};'; chain = out
ai = len(ovs) + 1
inputs += ['-i', 'voice_de.mp3', '-stream_loop', '-1', '-i', MUSIC] + (['-i', 'cta.mp3'] if CTA else [])
aparts = []
for k, (s, e) in enumerate(seg):
    d = int((N[k] + LEAD) * 1000)
    aparts.append(f'[{ai}:a]atrim={max(0,s-0.04):.3f}:{e+0.12:.3f},asetpts=PTS-STARTPTS,adelay={d}|{d}[s{k}]')
nv = len(seg)
if CTA:
    dc = int((TOTAL + 0.25) * 1000); aparts.append(f'[{ai+2}:a]aresample=44100,adelay={dc}|{dc}[s{nv}]'); nv += 1
afc = ';'.join(aparts) + ';' + ''.join(f'[s{k}]' for k in range(nv)) + f'amix=inputs={nv}:normalize=0[vo];'
afc += f'[{ai+1}:a]volume={os.environ.get('MUSVOL','0.10')},atrim=0:{T2:.3f},afade=t=out:st={T2-1.5:.3f}:d=1.5[mu];[vo][mu]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]'
fc2 = for_ov.rstrip(';') + ';' + afc
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', fc2.replace(chain + ';', chain + ';', 1), '-map', chain, '-map', '[a]', '-t', f'{T2:.3f}',
                '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', 'final_de.mp4'], check=True)
json.dump({'N': N, 'TOTAL': TOTAL, 'factors': [(nb[k+1]-nb[k])/(bounds[k+1]-bounds[k]) for k in range(len(bounds)-1)]}, open('timing.json', 'w'), indent=1)
print('fertig', round(TOTAL, 2), 's; Streckfaktoren', [round(x, 2) for x in json.load(open('timing.json'))['factors']])
