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

## sfx/
| Datei | Länge | Einsatz |
|---|---|---|
| `whoosh.mp3` | 0,7 s | jeder Phrasenwechsel (automatisch) |
| `impact.mp3` | 1,0 s | Hook bei Sekunde 0 (automatisch) |
| `pop.mp3` | 0,4 s | Badge / Karte erscheint |
| `click.mp3` | 0,2 s | Stempel, Auswahl |
| `typing.mp3` | 0,5 s | Tippen im Chatfenster (mehrfach hintereinander) |
| `ding.mp3` | 0,6 s | Haken / richtig |

Erzeugt mit ElevenLabs `eleven_text_to_sound_v2` (ca. 0,3 Cent pro Effekt), geschnitten und normalisiert.

## music/
| Datei | Stil |
|---|---|
| `lofi-105.mp3` | Lo-Fi-Tech-Beat, 105 BPM, 30 s Loop |
| `groove-115.mp3` | Marimba-Elektro-Groove, 115 BPM, 30 s Loop |

Erzeugt mit ElevenLabs `eleven_music_v2_5` (ca. 15 Cent pro Track), rein instrumental
(per Transkription geprüft: kein Gesang). Wechselt automatisch nach Reel-Nummer.
