# Jonas Noen · Reels & Karussells (Cloud-Workflow)

Dieses Repo ist das Gedächtnis und der öffentliche Ablageort für alle automatisch erstellten
Posts von **@jonas.noen** (Instagram) und **Jonas NOEN** (TikTok). Jede neue Claude-Sitzung,
auch eine geplante Aufgabe, liest zuerst diese Datei und `register.json`.

**Alles ist öffentlich.** Keine Zugangsdaten, Tokens, Passwörter, Entwürfe oder privaten Daten
hier ablegen. Nur fertige, freigegebene Medien, die Post-Liste und Quellcode der Animationen.

## Ablauf eines Reels

1. **Abgleich zuerst.** `register.json` lesen. In Metricool (`getScheduledPosts`, Marke
   `blogId 7001759`) prüfen, was geplant oder veröffentlicht ist. Einträge mit Status `sending`
   oder `unknown` zuerst klären, nie blind erneut senden.
2. **Thema.** Ein praktischer Claude-/KI-Tipp auf Deutsch, den man sofort nachmachen kann.
   Keine Duplikate: Thema UND Blickwinkel mit allen Einträgen in `register.json` vergleichen.
   Keine erfundenen Zahlen, Tests, Zeitersparnisse oder Ergebnisse. Aktuelle Produktaussagen
   mit einer frischen offiziellen Quelle prüfen.
3. **Skript.** 20–30 Sekunden, ca. 60–75 Wörter. Starker Hook in den ersten 2 Sekunden
   (Problem des Zuschauers). Ein Gedanke. Ende: „Folg mir für mehr Claude-Tipps.“
4. **Stimme.** ElevenLabs, Jonas' eigener Klon **„Jonas Noen“, voice_id `74F3tCXf85gKkgYnJulQ`**,
   Modell `eleven_v4`, genau 1 Generation (ca. 7 US-Cent). Danach mit ffmpeg
   `atempo=1.15` beschleunigen (Jonas spricht sonst zu langsam). Pausen zwischen Sätzen
   kürzen, ohne die Stimme weiter zu beschleunigen.
5. **Wort-Zeitstempel.** ElevenLabs `creative_transcribe_audio` (scribe) auf die
   ORIGINAL-Audiodatei, dann alle Zeiten durch 1,15 teilen → `words.json`.
6. **Animation.** Vorlage ist `reels/R001/source/scene.html` (vom Nutzer freigegebener Look).
   Für jedes neue Thema eigene Szenen bauen, aber Stil, Figur und Untertitel beibehalten:
   - Lila Grundton: Verlauf `#1f1a2c → #110e17`, weicher violetter Schein, Lampe mit warmem
     Lichtkegel, Schreibtisch, dezente Staubpartikel.
   - Helle Flächen für Inhalte (Chatfenster `#f7f3fb`, Karten Warm White `#f6efe4`) mit
     dunkler Schrift. Violett `#8b6cf0` / `#b9a6ff` als Hauptakzent, dazu sparsam Gelb
     `#ffc65c`, Grün `#3ccf8e` (richtig/gut) und Rot `#ef5a4c` (falsch). **Nicht nur Lila** –
     der Nutzer findet reine Lila-Optik langweilig.
   - Untertitel: Anton, GROSSBUCHSTABEN, ~100 px, dunkle Kontur, max. 3 Wörter, aktives Wort
     abwechselnd Gelb / Lavendel, zu lange Zeilen automatisch verkleinern. Position y≈1440.
   - Figur = Jonas als Cartoon: kurze dunkelbraune Haare mit strubbeligem Oberkopf und
     Geheimratsecken, kurze Seiten, dünne silberne Brille mit doppeltem Steg, Bartstoppeln,
     schwarzes T-Shirt. Funktion `guy()` in der Vorlage wiederverwenden.
   - Szenenwechsel: KEINE weißen Blitze. Nur kurzes Abblenden ins Dunkle (`rgba(23,20,31,…)`).
   - Kein Roboterkopf, keine erfundenen echten Produkt-Screenshots, keine fremden Logos.
   - 1080×1920, 30 fps. Kerninhalte nicht unter y≈1500 und nicht ganz rechts (Plattform-UI).
7. **Rendern.** In einem Arbeitsordner: `scene.html`, `words.json`, `voice.mp3` (beschleunigt)
   und `engine/render.cjs` zusammenlegen, `npm i` mit `engine/package.json` (Schriften), dann
   `NODE_PATH=/opt/npm-tools/node_modules node render.cjs stills stills` (Kontrollbilder,
   Zeiten über `TS=1.5,4,...`) und `node render.cjs full reel.mp4`. Danach Lautheit
   normalisieren: `ffmpeg -i reel.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -ar 48000 -movflags +faststart final.mp4`.
8. **Prüfen.** Kontrollbilder ansehen: Text abgeschnitten? Überlappungen? Figur verdeckt Text?
   Untertitel synchron? Weiße Blitze? Erst dann weiter.
9. **Ablegen.** `reels/R###/reel.mp4` + `reels/R###/source/` committen und pushen. Den
   Eintrag in `register.json` VOR dem Posten mit Status `sending` anlegen.
10. **Posten über Metricool** (`createScheduledPost`, `blogId 7001759`), Medien-URL:
    `https://raw.githubusercontent.com/jonasnoen/jonasnoen-posts/<commit-sha>/reels/R###/reel.mp4`
    (immer mit Commit-SHA, nicht `main`). Provider `instagram` und `tiktok`, `autoPublish: true`.
    - `instagramData`: `type: "REEL"`, `showReelOnFeed: true`, `isAiGenerated: true`
    - `tiktokData`: `title` ist PFLICHT (kurzer Titel), `privacyOption: "PUBLIC_TO_EVERYONE"`, `isAigc: true`
    - Datum mindestens ein paar Minuten in der Zukunft, Zeitzone Europe/Berlin.
11. **Nachtragen.** Metricool-Post-ID und Status in `register.json` speichern und pushen.
    Unklare Antwort beim Posten → Status `unknown`, NICHT erneut senden, Jonas per
    Push-Nachricht bitten, in Metricool nachzusehen. Mit dem nächsten Thema normal weitermachen.

## Caption

Deutsch, 3–5 kurze Absätze: Problem → der konkrete Tipp (wörtlich zum Abschreiben) → was dann
passiert → Aufforderung zum Speichern. 4–6 Hashtags, immer `#JonasNoen`. Kein künstliches
Engagement-Bait, keine Reichweitenversprechen.

## Kosten pro Reel

ElevenLabs-Stimme ca. 7 US-Cent, Transkription praktisch 0. Rendern, GitHub, Metricool: 0.

## Weitere Referenzen

- Jonas' Design Guidelines (lokal auf seinem Mac, nicht hier): Manrope, Video-Hintergrund
  `#030616`, Purple `#AD72FF`. Für Reels gilt aber der freigegebene Look oben (Vorlage R001),
  weil der Nutzer ihn ausdrücklich bevorzugt.
- Karussells: noch nicht eingerichtet. Altes Karussell-System lag lokal unter
  `z_JN_tiktok:insta` (Buffer + WordPress) und ist nicht mehr aktiv.
