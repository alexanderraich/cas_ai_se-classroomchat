# Classroom Chat — SDD-Übung (CAS AI SE)

Klassenraum-Messenger als Lernprojekt für **Specification-Driven Development** (SDD).
Aufgabenstellung: [spec/03 SDD Aufgabenblatt.pdf](spec/03%20SDD%20Aufgabenblatt.pdf).

Live-Deployment: Render.com (Free Plan, in-memory State, Cold-Start ~30 s nach 15 min Idle).
Repo: https://github.com/alexanderraich/cas_ai_se-classroomchat

## Status — alle 7 Schritte abgeschlossen

| Schritt | Inhalt | Artefakt |
| ------- | ------ | -------- |
| 1 | DDD-Domänenmodell (Klassendiagramm) | [diagrams/domaenenmodell.puml](docs/diagrams/domaenenmodell.puml) |
| 2 | Feature-Katalog (F1–F5) | [schritt2-feature-katalog.md](docs/schritt2-feature-katalog.md) |
| 3 | Use Cases & funktionale Anforderungen (FA-01..FA-24, ohne FA-07/08) | [schritt3-use-cases.md](docs/schritt3-use-cases.md) |
| 4 | Requirements Quality Check (finalisiert nach Schritt-6-Refinement) | [schritt4-quality-check.md](docs/schritt4-quality-check.md) |
| 5 | HTML-Mockup mit simuliertem Verhalten | [mockups/index.html](docs/mockups/index.html) |
| 6 | Flask-App + Render-Deployment + Live-Updates | [schritt6-architektur.md](docs/schritt6-architektur.md) |
| 7 | SWOT-Reflexion (Organisationsperspektive) | [schritt7-swot.md](docs/schritt7-swot.md) |

## Architektur (Schritt 6)

- **Backend:** Python 3.11 · Flask 3 · Gunicorn (`--workers 1 --threads 4 --timeout 60`).
  Workers=1, weil State im Prozess-RAM gehalten wird.
- **Frontend:** Server-gerendertes Jinja2 + Vanilla-JS-Polling (`fetch` alle 2 s) — quasi-SPA ohne Framework.
- **State (In-Memory):** `users` (uid → name), `groups` (gid → name, owner_id), `messages` (gid → list). Kein `members`-Set.
- **Open-Membership-Modell:** Jeder eingeloggte Benutzer sieht alle Gruppen und kann mitschreiben. Nur der Owner kann umbenennen/löschen. (Pivot weg von Closed Membership während Schritt 6 — siehe Refinement-Hinweise in Schritt 3/4.)
- **Live-Updates:** `GET /g/<gid>/state.json` liefert kompletten Sichtzustand (Gruppen mit `msg_count`, Userliste, Messages, Owner-Flag). Client diff-rendert DOM-Slots, kein Full-Reload.
- **UX-Detail:** Unread-Badge per `localStorage.cc_seen` (vergleicht zuletzt gesehene `msg_count` pro Gruppe). Enter sendet, Shift+Enter = Zeilenumbruch.
- **Robustheit:** 404-Handler redirected auf `/` (nach Cold-Start sind alte URLs aus Browser-History tot). Favicon-Route gibt 204 (kein Log-Spam).

### Endpunkte

| Methode + Pfad | Zweck |
| -------------- | ----- |
| `GET /` | Redirect zu `/groups` oder `/login` |
| `GET/POST /login` · `POST /logout` | Identität (Name → reuse-by-name, case-insensitive) |
| `GET /groups` · `POST /groups` | Gruppen-Übersicht / neue Gruppe anlegen |
| `GET /g/<gid>` | Gruppen-Ansicht (Sidebar + Feed + Composer) |
| `GET /g/<gid>/state.json` | JSON-State für Polling |
| `POST /g/<gid>/messages` | Nachricht senden |
| `POST /g/<gid>/rename` · `POST /g/<gid>/delete` | Owner-only |
| `GET /favicon.ico` | 204 |

## Repo-Struktur

```
app.py                     # Flask-App, alle Routes
render.yaml                # Render-Deploy-Manifest
requirements.txt
templates/
├── base.html              # Layout + Flash + {% block head %}
├── login.html
└── group.html             # Haupt-UI inkl. Polling-Skript
static/style.css
docs/
├── schritt2-feature-katalog.md
├── schritt3-use-cases.md
├── schritt4-quality-check.md
├── schritt6-architektur.md
├── schritt7-swot.md
├── diagrams/
│   ├── domaenenmodell.puml / .png
│   └── use-case-diagramm.puml / .png
└── mockups/
    ├── index.html
    └── style.css
spec/
└── 03 SDD Aufgabenblatt.pdf
```

## Lokal ausprobieren

```sh
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py            # http://127.0.0.1:5050
```

Hinweis: Port 5000 ist auf macOS oft durch AirPlay belegt → App nutzt 5050.
Multi-User-Test: zwei verschiedene Browser (oder Inkognito-Fenster) → mit unterschiedlichen Namen einloggen, gleiche Gruppe öffnen, Live-Updates beobachten.

**Diagramme rendern** (benötigt PlantUML + Graphviz):

```sh
brew install plantuml graphviz
plantuml -tpng -o "$PWD/docs/diagrams" docs/diagrams/*.puml
```

## Deployment (Render.com)

`render.yaml` definiert:

```
startCommand: gunicorn app:app --workers 1 --threads 4 --timeout 60 --bind 0.0.0.0:$PORT
```

Push auf `main` → Render baut & deployed automatisch. Free Plan: nach 15 min Idle Cold-Start (~30 s) — In-Memory-State geht dabei verloren (dokumentiert als FA-16).

## Wichtige Pivots & Lessons Learned

1. **Closed → Open Membership.** Ursprüngliche Specs (FA-07/08) sahen explizite Mitgliederverwaltung vor. Im Klassenraum-Szenario unnötige Reibung → entfernt, alle Eingeloggten sehen alles. Specs in Schritt 3/4 entsprechend zurück-synchronisiert.
2. **Auto-Reload vs. Tippen.** Erste Iteration mit `<meta refresh>` zerstörte aktive Composer-Eingabe. Lösung über JSON-Polling + DOM-Diffing, ohne Full-Reload.
3. **Cold-Start-404s.** Browser-History hielt alte UUIDs, die nach Render-Restart nicht mehr existierten. 404-Handler + Decorator-Redirects mit Flash-Message lösten das.
4. **Multi-User-Sichtbarkeit.** Login erstellte initial immer neue UUID → User sahen sich gegenseitig nicht. Fix: User per Name (case-insensitive) wiederverwenden.
5. **Spec-Code-Sync.** Refactoring während Schritt 6 erforderte Rück-Synchronisation aller Schritt-2/3/4/6-Dokumente. Dokumentiert in den jeweiligen Refinement-Hinweisen.

## Tooling

- VS Code + GitHub Copilot — für SDD-Generierung & Reviews
- PlantUML — Diagramme
- Python · Flask · Gunicorn
- GitHub · Render.com

## In einer neuen Session weiterarbeiten

Wenn du das Projekt in einem frischen Editor-/Chat-Kontext fortsetzt:

1. **Repo klonen / öffnen**
   ```sh
   git clone https://github.com/alexanderraich/cas_ai_se-classroomchat.git
   cd cas_ai_se-classroomchat
   git pull --rebase            # falls bereits geklont
   ```
2. **Virtuelle Umgebung & Abhängigkeiten**
   ```sh
   python3.11 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Lokal starten** — `python app.py` → http://127.0.0.1:5050
   Smoke-Test: zwei Browser, Login mit verschiedenen Namen, gleiche Gruppe öffnen, Nachricht senden → andere Seite zeigt Update innerhalb von ~2 s.
4. **Kontext für KI-Assistenten laden** (in Reihenfolge lesen lassen):
   1. Diese `README.md` (Architektur + Lessons Learned)
   2. `spec/03 SDD Aufgabenblatt.pdf` (Original-Aufgabenstellung)
   3. `docs/schritt2-feature-katalog.md` → `docs/schritt7-swot.md` (sequenziell)
   4. `app.py` und `templates/group.html` (aktueller Implementierungsstand)
5. **Wichtige Invarianten beim Weiterentwickeln**
   - **In-Memory-State** ⇒ Gunicorn `--workers 1` lassen. Mehr Worker = State-Inkonsistenz.
   - **Open Membership** ist bewusst (FA-07/08 entfernt). Keine Member-Sets wieder einführen, ohne Schritt 2/3/4 erneut zu refinen.
   - **Polling-Endpoint** `/g/<gid>/state.json` ist die Single Source of Truth für die UI. Neue Daten dort ergänzen, dann Client-Renderer in `group.html` anpassen.
   - **Stabile DOM-IDs** in `group.html` (`#group-list`, `#user-list`, `#feed`, `#composer-form`, …) — der Polling-Renderer hängt daran.
   - **Spec ↔ Code synchron halten:** Wenn du FAs änderst, gleichzeitig Schritt 3, 4 und 6 nachziehen (siehe Refinement-Hinweise dort als Vorlage).
6. **Deployment**: Push auf `main` → Render baut automatisch. Logs im Render-Dashboard. Cold-Start-Reset des State ist erwartet (FA-16).
7. **Häufige Fallstricke**
   - Port 5000 belegt (macOS AirPlay) → bleib bei 5050.
   - `dquote>`-Hänger in zsh: mehrzeilige Strings entstehen durch unbalancierte `"`. Mit `Ctrl+C` abbrechen.
   - 404 nach Render-Restart: erwartet, 404-Handler leitet auf `/`.

## Lizenz

Lernprojekt im Rahmen des CAS AI SE — keine produktive Nutzung vorgesehen.
