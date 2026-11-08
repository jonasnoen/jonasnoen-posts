# Wiederverwendbare Bausteine für Reels

Alles hier wird einmal erzeugt und dann in jedem Reel wiederverwendet. **Nicht neu erzeugen,
wenn es schon da ist.** Nur fehlende Bausteine ergänzen und hier eintragen.

## avatar/
Jonas als 3D-Memoji-Figur (KI-generiert mit ElevenLabs `gpt-image-2.5-sunburst`,
Referenz `reference.png`, auf Greenscreen erzeugt und mit `engine/avatar/key.py` freigestellt).

| Pose | Einsatz |
|---|---|
| `surprised` | Hook / Problem |
| `think` | Frage, Zweifel |
| `point` | Erklärung, Schritte |
| `thumbs` | Ergebnis, Bestätigung |
| `wave` | Outro „Folg mir“ |

Jede Pose hat eine `_talk`-Version mit offenem Mund (nur der Mund unterscheidet sich, alles andere
pixelgleich). Neue Pose: auf Grün `#00B140` mit Referenzbild erzeugen, Mund-offen-Version per
Bildbearbeitung, dann `python3 engine/avatar/key.py pose.png pose_offen.png <name> assets/avatar`.
Kosten ca. 7 Cent pro Bild.

## sfx/  (Version 2, seit 03.11.2026)
Reihenfolge in der Vorschau: impact, riser, whoosh ×3, pop, click, stamp, typing, ding, sparkle, outro.

| Datei | Länge | Einsatz |
|---|---|---|
| `whoosh.mp3`, `whoosh_2.mp3`, `whoosh_3.mp3` | 0,4–0,5 s | jeder Phrasenwechsel (automatisch, die drei Varianten reihum) |
| `impact.mp3` | 1,2 s | Hook bei Sekunde 0 (automatisch), tiefer Kino-Schlag |
| `outro.mp3` | 1,2 s | Folgen-Karte im Outro (automatisch) |
| `riser.mp3` | 0,85 s | Spannung vor einer Auflösung („Der Trick:“), Cue ca. 0,8 s VOR dem Wort setzen |
| `sparkle.mp3` | 0,8 s | Ergebnis / Aha-Moment wird gezeigt |
| `pop.mp3` | 0,3 s | Badge / Karte erscheint – hell und luftig (seit 03.11. auf Wunsch von Jonas) |
| `pop_soft.mp3` | 0,5 s | weicher, tieferer Pop (vorherige Version), nur gezielt einsetzen |
| `click.mp3` | 0,07 s | Auswahl, Häkchen setzen, Button |
| `stamp.mp3` | 0,5 s | Stempel („FALSCH“, „RICHTIG“), Einsatz setzt ca. 0,1 s verzögert ein |
| `typing.mp3` | 0,7 s | Tippen im Chatfenster (mehrfach hintereinander) |
| `ding.mp3` | 0,8 s | Haken / richtig |
| `chalk.mp3` | 1,0 s | Kreide kratzt auf der Tafel (seit 08.11.2026, R009 Stil `kreidetafel`), beim Anschreiben/Zeichnen |

Varianten: Gibt es `<name>_2.mp3`, `<name>_3.mp3` …, wechselt `render.cjs` sie automatisch reihum ab.
Erzeugt mit ElevenLabs `eleven_text_to_sound_v2` (Flow „SFX-Bibliothek v2“, zusammen ca. 0,5 US-Cent), Stille
abgeschnitten, Lautheit an die alte Bibliothek angeglichen (Spitze max. −1 dBFS). Die alte Version liegt in `sfx/v1/`.
Fehlt ein Sound: einmal erzeugen, gleich bearbeiten (`silenceremove` + Pegel), hier eintragen.

## music/
| Datei | Stil |
|---|---|
| `lofi-105.mp3` | Lo-Fi-Tech-Beat, 105 BPM, 30 s Loop |
| `groove-115.mp3` | Marimba-Elektro-Groove, 115 BPM, 30 s Loop |

Erzeugt mit ElevenLabs `eleven_music_v2_5` (ca. 15 Cent pro Track), rein instrumental
(per Transkription geprüft: kein Gesang). Wechselt automatisch nach Reel-Nummer (nur Dateien direkt in `music/`; Sondertracks liegen in `music/special/` und werden nur gezielt per `MUSIC=special/<datei>` genutzt).

## avatar/loops/
| Datei | Inhalt | Einsatz |
|---|---|---|
| `talk.mp4` | Zeigefinger oben | `loop:talk` – Schritte |
| `think.mp4` | Hand am Kinn | `loop:think` – Problem, Frage |
| `explain.mp4` | offene Hände, erklärt | `loop:explain` – Erklärung, Trick |
| `neutral.mp4` | ruhig, Hände unten | `loop:neutral` – Merksatz |
| `happy.mp4` | lacht, winkt | `loop:happy` – Outro (immer) |

Alle 10 s, Greenscreen. Erzeugt mit HeyGen Avatar 4 über ElevenLabs (ca. 1 US-Dollar je Loop, einmalig) aus den Posen und
`loopsrc/talk10.mp3`. Der Renderer stellt den Loop frei (`engine/avatar/key_loop.py`), spielt ihn
vor/zurück ab und startet je Reel an anderer Stelle. Für lippensynchrone Reels baut `render.cjs track`
daraus die Avatar-Spur, die dann mit Veed Lipsync an die Stimme angepasst wird (siehe CLAUDE.md).

- `music/special/japan-koto.mp3` – japanisch (Koto, Shakuhachi), ruhig, 92 s, ElevenLabs Music v2.5, instrumental. Erstellt für R003 (Ukiyo-e-Stil). Leise gemastert (-19.5 LUFS) → im Mix ca. 0.25 statt 0.10.
- `music/special/japan-lofi.mp3` – japanischer Lo-Fi (Beat, Rhodes, Koto, Shakuhachi), 85 BPM, 92 s, ElevenLabs Music v2.5. Von Jonas für R003 gewählt (Mix 0.11).
