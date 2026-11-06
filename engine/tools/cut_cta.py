#!/usr/bin/env python3
"""LinkedIn-Fassung eines Reels: schneidet den gesprochenen PROMPT-Satz (inkl. Einblendung) heraus.

Aufruf: 1) Reel ohne PROMPT-Pille rendern: NO_CTA=1 REEL=… node render.cjs full final_nocta.mp4 (+ gleiche Lautheits-Korrektur)
        2) python3 engine/tools/cut_cta.py <final_nocta.mp4> <words.json> <reel_linkedin.mp4>
Schneidet von "Kommentiere"/"Comment" bis kurz vor "Folg"/"Follow". Bild und Ton werden gemeinsam
geschnitten (Lippen bleiben synchron), am Schnitt 50 ms Audio-Überblendung. Kein neues Rendern nötig.
"""
import json, re, subprocess, sys

src, words_path, out = sys.argv[1:4]
w = json.load(open(words_path))
w = w if isinstance(w, list) else w['words']
i = next(k for k, x in enumerate(w) if re.match(r'(kommentier|comment)', x['text'], re.I))
j = next(k for k in range(i + 1, len(w)) if re.match(r'(folg|follow)', w[k]['text'], re.I))
a, b = max(0, w[i]['start'] - 0.06), w[j]['start'] - 0.06
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src],
                           capture_output=True, text=True).stdout)
fc = (f"[0:v]trim=0:{a:.3f},setpts=PTS-STARTPTS[v0];[0:v]trim={b:.3f}:{dur:.3f},setpts=PTS-STARTPTS[v1];"
      f"[v0][v1]concat=n=2:v=1:a=0[v];"
      f"[0:a]atrim=0:{a + 0.05:.3f},asetpts=PTS-STARTPTS[a0];[0:a]atrim={b - 0.05:.3f}:{dur:.3f},asetpts=PTS-STARTPTS[a1];"
      f"[a0][a1]acrossfade=d=0.05[a]")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
                '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                '-movflags', '+faststart', out], check=True)
print(f'geschnitten {a:.2f}–{b:.2f} s ({w[i]["text"]} … vor {w[j]["text"]}), neu {dur - (b - a):.1f} s -> {out}')
