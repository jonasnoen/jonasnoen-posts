#!/usr/bin/env python3
"""Sprech-Loop (Greenscreen-MP4) in freigestellte PNG-Einzelbilder zerlegen.

Aufruf: python3 key_loop.py <loop.mp4> <outdir> [hoehe=760]
Nutzt denselben Freisteller wie die Posen (key.py), schneidet alle Bilder auf dieselbe
Box zu (Vereinigung über alle Frames, damit nichts springt) und skaliert auf <hoehe>.
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
raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', src, '-vf', 'fps=30', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
n = len(raw) // (w * h * 3)
frames = np.frombuffer(raw, np.uint8)[: n * w * h * 3].reshape(n, h, w, 3)
keyed, box = [], None
for f in frames:
    rgb, al = key(f)
    arr = np.dstack([rgb, al * 255]).clip(0, 255).astype(np.uint8)
    ys, xs = np.where(arr[..., 3] > 8)
    b = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
    keyed.append(arr)
box = (max(box[0] - 4, 0), max(box[1] - 4, 0), min(box[2] + 4, w), h)
for i, arr in enumerate(keyed):
    im = Image.fromarray(arr, 'RGBA').crop(box)
    im = im.resize((round(im.width * H / im.height), H), Image.LANCZOS)
    im.save(f'{out}/{i:04d}.png', compress_level=1)
print(n, 'Frames ->', out, 'Box', box)
