#!/usr/bin/env python3
"""Greenscreen-Freisteller für die Avatar-Posen.

Aufruf: python3 key.py <closed.png> <open.png> <name> <outdir>
- closed.png: Pose mit geschlossenem Mund (grüner Hintergrund)
- open.png:   gleiche Pose mit offenem Mund (aus Bildbearbeitung)
Ergebnis: <outdir>/<name>.png und <outdir>/<name>_talk.png, beide gleich groß,
freigestellt (RGBA), Grünstich entfernt, auf den Inhalt zugeschnitten.
Die offene Version übernimmt NUR den Mundbereich, alles andere stammt aus der
geschlossenen Version. So springt beim Mundwechsel nichts (kein Zittern).
"""
import sys
import numpy as np
from PIL import Image, ImageFilter


def key(rgb):
    a = rgb.astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    spill = g - np.maximum(r, b)          # wie "grün" ein Pixel ist
    alpha = 1.0 - np.clip((spill - 18.0) / (70.0 - 18.0), 0, 1)
    # Grünstich entfernen: Grün nie heller als der hellere der beiden anderen Kanäle
    g2 = np.minimum(g, np.maximum(r, b) * 1.02)
    out = np.stack([r, g2, b], -1)
    # Kante 1px weich, Inneres bleibt hart
    am = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    alpha = np.minimum(alpha, np.asarray(am, np.float32) / 255 + 0.0)
    return out, alpha


def mouth_mask(c, o):
    """Maske des Mundbereichs: Stelle mit größter Abweichung im unteren Gesicht."""
    d = np.abs(c.astype(np.int16) - o.astype(np.int16)).sum(-1).astype(np.float32)
    d = np.asarray(Image.fromarray(np.clip(d, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6)), np.float32)
    h, w = d.shape
    ys, xs = np.unravel_index(np.argmax(d), d.shape)
    # Ellipse um den Mund (Breite ~ 11 % der Bildhöhe)
    ry, rx = int(h * 0.075), int(h * 0.11)
    yy, xx = np.ogrid[:h, :w]
    e = ((yy - ys) / ry) ** 2 + ((xx - xs) / rx) ** 2
    m = np.clip((1.25 - e) / 0.5, 0, 1)
    return m, (xs, ys)


def main(cp, op, name, outdir):
    c = np.asarray(Image.open(cp).convert('RGB'))
    o = np.asarray(Image.open(op).convert('RGB').resize((c.shape[1], c.shape[0]), Image.LANCZOS))
    m, pos = mouth_mask(c, o)
    talk = (c * (1 - m[..., None]) + o * m[..., None]).astype(np.uint8)
    res = []
    for img in (c, talk):
        rgb, al = key(img)
        res.append(np.dstack([rgb, al * 255]).clip(0, 255).astype(np.uint8))
    a = res[0][..., 3] > 8
    ys, xs = np.where(a)
    box = (max(xs.min() - 4, 0), max(ys.min() - 4, 0), xs.max() + 5, ys.max() + 1)
    for suffix, arr in (('', res[0]), ('_talk', res[1])):
        Image.fromarray(arr, 'RGBA').crop(box).save(f'{outdir}/{name}{suffix}.png', optimize=True)
    print(name, 'mouth at', pos, 'box', box)


if __name__ == '__main__':
    main(*sys.argv[1:5])
