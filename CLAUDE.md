# Jonas Noen · Reels & Karussells (Cloud-Workflow)

Dieses Repo ist das Gedächtnis und der öffentliche Ablageort für alle automatisch erstellten
Posts von **@jonas.noen** (Instagram) und **Jonas NOEN** (TikTok). Jede neue Claude-Sitzung,
auch eine geplante Aufgabe, liest zuerst diese Datei und `register.json`.

**Alles ist öffentlich.** Keine Zugangsdaten, Tokens, Passwörter, Entwürfe oder privaten Daten
hier ablegen. Nur fertige, freigegebene Medien, die Post-Liste und Quellcode der Animationen.

## Wochenplan (tägliche Aufgabe, ein Post pro Tag, Zeitzone Europe/Berlin)

| Mo | Di | Mi | Do | Fr | Sa | So |
|---|---|---|---|---|---|---|
| Tipp-Reel | YouTube-Short | Tipp-Reel | Karussell | Tipp-Reel | YouTube-Short | Tipp-Reel |

- Veröffentlichungszeit: **18:30 Uhr** (über Metricool planen, autoPublish).
- **Höchstens ein Post pro Tag.** Vorher prüfen, ob heute schon etwas in `register.json` oder
  in Metricool geplant/veröffentlicht ist. Wenn ja: nichts tun.
- **Niemals Duplikate:** Kein Short, dessen `sourceVideoId` schon in `register.json` steht.
  Kein Reel/Karussell mit gleichem Thema UND Blickwinkel wie ein bestehender Eintrag.
- **Fallback:** Findet sich an einem Short-Tag kein passender, noch nicht geposteter Short,
  oder klappt der Download nicht, stattdessen ein animiertes Tipp-Reel posten. Gleiches gilt,
  wenn an einem Karussell-Tag etwas schiefgeht.
- Ein fertiges, noch nicht gepostetes Element mit Status `ready` in `register.json`
  (z. B. K001) wird bevorzugt verwendet, wenn sein Typ an dem Tag dran ist.

## Ablauf eines Karussells

1. Thema wie beim Reel prüfen (keine Duplikate, Fakten mit offizieller Quelle, keine
   erfundenen Zahlen). 7 Slides: Cover mit Jonas-Figur → Problem → 3–4 Schritte mit einem
   durchgehenden konkreten Beispiel → Zusammenfassung „Zum Speichern“ mit ehrlichem
   Praxischeck und einer Frage an die Zuschauer. Absender „JONAS NOEN“, Slide-Nummer.
2. Vorlage: `carousels/K001/source/slides.html` (gleicher Look wie die Reels, Anton-
   Überschriften, Manrope-Text, helle Karten, farbige Akzente, Figur aus `guy.js`).
3. Rendern: `NODE_PATH=/opt/npm-tools/node_modules node engine/carousel/shot.cjs slides.html <outdir>`
   (Schriften per `npm i` aus `engine/package.json` als `node_modules` neben `slides.html`).
   Ergibt `ig-01..07.png` (1080×1350) und `tt-01..07.png` (1080×1920, TikTok-sichere Ränder).
   Alle 14 Bilder ansehen: nichts abgeschnitten, nichts überlappt.
4. Ins Repo unter `carousels/K###/`, Eintrag in `register.json` mit `type: "carousel"`.
5. Metricool: ZWEI Posts (Formate unterscheiden sich):
   - Instagram: `media` = die 7 `ig-0X.png` Raw-URLs (mit Commit-SHA), `instagramData.type: "POST"`.
   - TikTok: `media` = die 7 `tt-0X.png`, `tiktokData.title` Pflicht, `privacyOption: "PUBLIC_TO_EVERYONE"`.

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
6. **Animation – Stil „reel2“ (aktueller Standard, Vorbild adilet.fndr).**
   Vorlage: `engine/reel2/scene.html` (Beispiel-Thema „Zeig Claude deinen Stil“). Für jedes neue
   Thema `PH` (Phrasen), die Szenen `p0…pN`, `AVP` (Posen) und `EXTRA_CUES` (Sounds) neu
   schreiben; Hintergrund, Überschrift, Avatar, Übergänge und Mischung beibehalten.
   - **Aufbau (wie adilet.fndr):** Oben links Label (`// SCHRITT 1 · KOPIEREN`), oben rechts Zähler
     (`SCHRITT 1/3`, aus `PROGRESS`), große Überschrift (Manrope 800) Wort für Wort synchron zur
     Stimme; 1–3 Akzentwörter pro Phrase in **kursiver Serifenschrift** (Instrument Serif) farbig
     (dunkel: Gelb/Lavendel, hell: Rot/Violett). Mitte (y≈450–1180): eine klare Code-Grafik pro
     Phrase (Badges 1/2/3, Stempel, Karten, Mini-Chat) – **keine KI-Illustrationen**.
     Unten links die **Fortschritts-Karte** (`PROGRESS`: Titel + 3–4 Schritte, füllt sich mit Haken).
     Unten rechts der Avatar. Kapitel wechseln zwischen **hell und dunkel** (`light:true` in `PH`,
     typisch: Problem/Trick hell, Schritte dunkel, Merksatz/Outro hell).
   - **Hook:** In Phrase 0 steht die komplette Überschrift ab Frame 0 und knallt mit `impact` rein.
   - **Schnelle Schnitte:** neue Phrase alle 1–3 Sekunden, leichter Push-in, Wechsel nur per
     kurzem Abblenden ins Dunkle (`rgba(23,20,31,…)`). KEINE weißen Blitze.
   - **Avatar = lippensynchrones Video aus Gesten-Loops (Standard):**
     `AVP` legt pro Phrase einen Loop fest: `loop:think` (Problem/Frage), `loop:explain` (offene
     Hände, Erklärung), `loop:talk` (Zeigefinger, Schritte), `loop:neutral` (ruhig, Merksatz),
     `loop:happy` (lacht, winkt – **immer fürs Outro**, nicht ernst enden).
     Ablauf pro Reel (ca. 13 Cent):
     1. `node render.cjs track base.mp4` → Avatar-Spur (Greenscreen) aus den Loops, harter Schnitt pro Phrase.
     2. `base.mp4` und `voice.mp3` nach `reels/R###/source/` committen + pushen, beide per
        `creative_attach_reference_file` (Raw-URL mit Commit-SHA) auf einen ElevenLabs-Flow legen.
     3. `creative_generate_in_flow` mit `node_type: video-generation`, `model_id: veed-lipsync`,
        `connect_from: [Video-Node, Audio-Node]` (vorher `estimate_only`, ca. 0,65 Cent/Sekunde).
     4. Ergebnis als `lipsync.mp4` in den Arbeitsordner → `render.cjs` nutzt es automatisch für das
        ganze Reel (Greenscreen wird freigestellt).
     Klappt Lipsync nicht: ohne `lipsync.mp4` rendern (Loops ohne Lippensynchronität) und in der
     Push-Nachricht erwähnen. Standbild-Posen (`surprised`, `thumbs`, `wave`, `think`, `point`) nur
     als Notlösung; deren Mund folgt dezent der Lautstärke. **Nie** die Figur skalieren/pulsieren
     lassen (wirkt wie Zittern). Posenwechsel als harter Schnitt beim Phrasenwechsel – **kein Überblenden**
     (sieht verwaschen aus, vom Nutzer abgelehnt) und kein Pop.
   - Farben: lila Grundton (`#1f1a2c → #110e17`, violetter Schein, Lampe, Staub), helle Karten
     `#f6efe4` / Chat `#f7f3fb` mit dunkler Schrift, Akzente Violett `#8b6cf0`/`#b9a6ff`, sparsam
     Gelb `#ffc65c`, Grün `#3ccf8e`, Rot `#ef5a4c`. **Nicht nur Lila.**
   - Kein Roboterkopf, keine erfundenen echten Produkt-Screenshots, keine fremden Logos.
   - 1080×1920, 30 fps. Kerninhalte nicht ganz rechts oben (Plattform-UI), Text nicht hinter Avatar.
   - Alter Stil (Cartoon-`guy()` + große Untertitel) liegt in `reels/R001/source/` – nur noch Archiv.
7. **Sound.** Effekte und Musik liegen fertig in `assets/sfx/` und `assets/music/` und werden
   **immer wiederverwendet**. Nur wenn ein benötigter Sound fehlt: einmal mit ElevenLabs
   erzeugen (`eleven_text_to_sound_v2`, ca. 0,3 Cent; Musik `eleven_music_v2_5`, ca. 15 Cent,
   nur instrumental), kurz schneiden, normalisieren, in `assets/` ablegen, in `assets/README.md`
   eintragen und committen. `render.cjs` legt `whoosh` auf jeden Phrasenwechsel und `impact` auf
   Sekunde 0; weitere Effekte über `EXTRA_CUES` in der Szene. Musik läuft bei ca. 10 % Lautstärke
   unter der Stimme, Track wechselt automatisch nach Reel-Nummer.
8. **Rendern.** Arbeitsordner mit `scene.html`, `words.json`, `voice.mp3` (beschleunigt) und
   `engine/reel2/render.cjs`; Schriften per `npm i` mit `engine/package.json` (oder `node_modules`
   verlinken). Dann
   `NODE_PATH=/opt/npm-tools/node_modules ASSETS=<repo>/assets node render.cjs stills stills`
   (Kontrollbilder, Zeiten über `TS=0.1,1.5,...`) und
   `REEL=R### NODE_PATH=/opt/npm-tools/node_modules ASSETS=<repo>/assets node render.cjs full final.mp4`
   – das mischt Stimme, Musik und Effekte und normalisiert die Lautheit (-14 LUFS) in einem Schritt.
   **Prüfen:** Kontrollbilder ansehen: Text abgeschnitten? Überlappungen? Avatar verdeckt Text?
   Wörter synchron? Mund offen in Sprechpassagen? Weiße Blitze? Erst dann weiter.
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

## Clips aus Jonas' YouTube-Videos

**NUR der Kanal „JONAS NØEN“, @jonasnoen, Channel-ID `UC2fWOn9AWZjHZyHaxoXS3wQ`.**
Das vidIQ-Konto hat auch den Kanal „Cryptocat-Guru“ (`UC09Itc3_iZi9BCNp-oZ21Kg`).
Davon NIEMALS Videos, Clips, Titel oder Inhalte verwenden. Vor jedem Clip die Channel-ID
des Quellvideos prüfen; passt sie nicht exakt, abbrechen.

Bevorzugt: **bereits auf YouTube veröffentlichte Shorts** von Jonas wiederverwenden
(vom Nutzer so gewünscht). Ablauf:
1. `vidiq_user_videos` mit `channelId: "UC2fWOn9AWZjHZyHaxoXS3wQ"`, `videoType: ["short"]`,
   `privacyStatus: ["public"]`. Nur Videos aus genau dieser Liste sind erlaubt.
2. Einen Short wählen, der noch nicht in `register.json` steht (Feld `sourceVideoId`)
   **und dessen `publishedAt` höchstens 14 Tage zurückliegt** (Vorgabe des Nutzers).
   Gibt es keinen solchen Short, an diesem Tag ein animiertes Tipp-Reel posten.
   Unter den passenden bevorzugt den mit den meisten YouTube-Aufrufen. Schon vorher auf Instagram gepostet:
   Reel vom 28.09.2026 „Strategie für den Sales-Erfolg mit KI!“ (vermutlich der Sales-Short
   `Xdgfbc4q7rQ`) – nicht doppelt posten.
3. `vidiq_video_upload` mit dem Shorts-Link (kostenlos), per `vidiq_job_poll` warten,
   die zurückgegebene `videoUrl` herunterladen.
4. Ins Repo legen (`clips/C###/clip.mp4`), Eintrag mit `type: "clip"`, `sourceVideoId`,
   `channelId`, Titel. Dann über Metricool wie ein Reel posten (eigene Caption auf Deutsch,
   TikTok-Titel nicht vergessen). `isAiGenerated` nur setzen, wenn der Short KI-Inhalte zeigt.

Alternative, falls keine passenden Shorts mehr übrig sind: `vidiq_generate_clips` mit dem
YouTube-Link eines Long-Form-Videos desselben Kanals (9 vidIQ-Credits pro Minute).

## Caption

Deutsch, 3–5 kurze Absätze: Problem → der konkrete Tipp (wörtlich zum Abschreiben) → was dann
passiert → Aufforderung zum Speichern. 4–6 Hashtags, immer `#JonasNoen`. Kein künstliches
Engagement-Bait, keine Reichweitenversprechen.

## Kosten pro Reel

ElevenLabs-Stimme ca. 7 US-Cent, Transkription ca. 1–3 Cent, Lipsync (Veed) ca. 13 Cent → zusammen
ca. 23 Cent. Avatar-Posen, Gesten-Loops, Sounds, Musik: 0 (liegen in `assets/`, einmalig ca. 5 US-Dollar).
Rendern, GitHub, Metricool: 0.

## Weitere Referenzen

- Jonas' Design Guidelines (lokal auf seinem Mac, nicht hier): Manrope, Video-Hintergrund
  `#030616`, Purple `#AD72FF`. Für Reels gilt aber der freigegebene Look oben (Vorlage R001),
  weil der Nutzer ihn ausdrücklich bevorzugt.
- Altes Karussell-System lag lokal unter `z_JN_tiktok:insta` (Buffer + WordPress) und ist
  nicht mehr aktiv. Karussells laufen jetzt über den Ablauf oben.
