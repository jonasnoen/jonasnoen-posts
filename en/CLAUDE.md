# Jonas Noen English · @jonasnoen.ai (eigener Kanal, komplett getrennt vom deutschen)

Englischer Ableger von @jonas.noen. **Gleiche Technik, gleicher Look, eigene Daten.** Jede Sitzung für den englischen Kanal
liest zuerst diese Datei, dann `en/register.json` und für alle technischen Details die Haupt-`CLAUDE.md` (Engine, Look,
Sounds, Lipsync, Guide-Aufbau, „Hype ja, Lügen nein“, Prompt-Pflicht). **Hier stehen nur die Abweichungen.**

## Getrennt halten
- **Metricool-Marke „Jonas Noen English“, blogId `7916347`** (Instagram `jonasnoen.ai`, TikTok `jonasnoen.ai`,
  X `jonasnoen`, LinkedIn eigenes englisches Profil). **Niemals** die deutsche Marke 7001759 benutzen.
- Liste: `en/register.json` (IDs `E001`, `E002` …; Starter-Guide `G002` ist kein Post).
- Dateien: `en/reels/E###/` (reel.mp4, reel_linkedin.mp4, source/), Karussells `en/carousels/EK###/`.
- Guide-Seite: `python3 engine/site/build.py en` → `docs/en/` → **https://jonasnoen.github.io/jonasnoen-posts/en/**
- **Kein Hinweis auf den deutschen Kanal oder Jonas' YouTube** (kein @jonas.noen, kein „JONAS NØEN“, keine deutschen Links)
  in Video, Caption, Guide oder Bio. Jonas' Gesicht und Stimme sind ausdrücklich erlaubt.

## Inhalt
- Englisch (US/UK-neutral, einfach, Hype erlaubt). Serie **„Claude Codes Part N“** (Reels) / **„Claude Prompts Part N“** (Karussells).
- Thema: zuerst den neuesten deutschen Post nehmen, der in `en/register.json` noch nicht adaptiert wurde (Feld `fromDe`),
  und ihn **für ein internationales Publikum neu schreiben** (keine deutschen Beispiele wie Mietrecht/Steuer/Bewerbung nach
  DE-Norm → internationale Beispiele: lease, resume, invoice …). Gibt es nichts Offenes: offenes Thema aus `themen/en.md`, sonst eigenes.
- Jeder Post hat `vorlage` + `guide` (wie DE, auf Englisch). Fakten mit offizieller Quelle prüfen.

## Video
- Formate wie DE (Creme ↔ Memoji im Wechsel nach dem letzten E-Reel; sonntags Stil-Experiment). In der kopierten
  `scene.html` **`const LANG='en';`** setzen (Outro „FOLLOW FOR MORE / CLAUDE PROMPTS / @jonasnoen.ai“, Pille „Comment PROMPT
  → get the guide“), Labels englisch (`// STEP 1 · …`, Zähler `counter:'STEP'`). Vorbild: `en/reels/E001/source/scene.html`.
- Stimme: Jonas' Klon `74F3tCXf85gKkgYnJulQ`, `eleven_v4`, Text englisch, `atempo=1.15` (Ziel 25–30 s).
- Creme-Gesichtsspur: `REEL=E### FACE_OFF=<Nummer × 27 + 13>` (z. B. E002 → 67), sonst wie DE (Sperrliste gilt).
- Skript-Ende (gesprochen): **„Comment PROMPT and I'll send you the full guide. Follow for more Claude prompts.“**

## Posten
- Zeit: **20:30 Europe/Berlin** (= 14:30 New York, 19:30 London). Höchstens ein Post pro Tag.
- **Instagram (REEL, isAiGenerated) + TikTok (title Pflicht, isAigc)** mit derselben Caption, Ende:
  „Comment PROMPT and I'll send you the full guide.“ 4–6 englische Hashtags (z. B. #ClaudeAI #AIPrompts #PromptEngineering #AITools).
- **X:** gleiches Reel, Kurzfassung der Caption (≤ 250 Zeichen inkl. „Comment PROMPT for the guide“).
- **LinkedIn:** eigene **Fassung des Videos ohne PROMPT** (dort keine Automatik): `NO_CTA=1 REEL=E### … node render.cjs full
  final_nocta.mp4` (+ gleiche Lautheits-Korrektur wie beim Reel), dann `python3 engine/tools/cut_cta.py final_nocta.mp4
  words.json en/reels/E###/reel_linkedin.mp4` (schneidet den gesprochenen PROMPT-Satz raus, Lippen bleiben synchron).
  Sachlichere Caption (Mehrwert, 1 Frage), endet mit „Full guide with all prompts → link in the first comment 👇“;
  `firstCommentText` = „Here's the full guide with all prompts, free to copy: https://jonasnoen.github.io/jonasnoen-posts/en/“.
- Flows (vom Nutzer eingerichtet): Instagram Kommentar PROMPT → DM → Link; TikTok Kommentar PROMPT → öffentliche Antwort mit Link.
- Danach Metricool-IDs in `en/register.json` (`platforms.instagram/tiktok/x/linkedin`), Status wie DE (`sending` → `scheduled`,
  unklar → `unknown`, nie doppelt senden).
