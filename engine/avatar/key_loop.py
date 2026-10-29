#!/usr/bin/env python3
"""Avatar-Video (Greenscreen-MP4) in freigestellte PNG-Einzelbilder zerlegen.

Aufruf: python3 key_loop.py <video.mp4> <outdir> [hoehe=760]
Nutzt denselben Freisteller wie die Posen (key.py). Zwei Durchgänge mit gestreamtem Dekodieren
(wenig Speicher): 1) gemeinsame Box über alle Frames bestimmen (nichts springt), 2) freistellen,
zuschneiden, auf <hoehe> skalieren und speichern.
"""
import os, subprocess, sys, json
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from key import key  # noqa: E402

src, out = sys.argv[1], sys.argv[2]
H = int(sys.argv[3]) if len(sys.argv) > 3 else 760
os.makedirs(out, exist_ok=True)
probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'json', src]))
w, h = probe['streams'][0]['width'], probe['streams'][0]['height']
fs = w * h * 3


def frames():
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-vf', 'fps=30', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    while True:
        buf = p.stdout.read(fs)
        if len(buf) < fs:
            break
        yield np.frombuffer(buf, np.uint8).reshape(h, w, 3)
    p.wait()


box = None
for f in frames():  # Durchgang 1: Box (grob über Grün-Dominanz, schnell)
    a = f.astype(np.int16)
    m = (a[..., 1] - np.maximum(a[..., 0], a[..., 2])) < 40
    ys, xs = np.where(m)
    if len(xs) == 0:
        continue
    b = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
box = (max(int(box[0]) - 6, 0), max(int(box[1]) - 6, 0), min(int(box[2]) + 6, w), h)
n = 0
for f in frames():  # Durchgang 2: freistellen und speichern
    sub = f[box[1]:box[3], box[0]:box[2]]
    rgb, al = key(sub)
    im = Image.fromarray(np.dstack([rgb, al * 255]).clip(0, 255).astype(np.uint8), 'RGBA')
    im = im.resize((round(im.width * H / im.height), H), Image.LANCZOS)
    im.save(f'{out}/{n:04d}.png', compress_level=1)
    n += 1
print(n, 'Frames ->', out, 'Box', box)
