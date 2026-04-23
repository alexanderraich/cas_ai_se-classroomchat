# Schritt 6 — Architektur & Deployment (TRL4-Prototyp)

## Purpose

Web-basierter Klassenraum-Messenger als TRL4-Prototyp. Nutzer melden sich mit einem Anzeigenamen an, erstellen Gruppen, verwalten Mitglieder und tauschen Textnachrichten aus. Datenhaltung ist bewusst flüchtig (In-Memory).

## Components

- **Browser-UI** — server-gerenderte Jinja2-Templates plus inline Vanilla-JavaScript für Live-Updates (Polling auf JSON-Endpoint, DOM-Patches statt Full-Reload).
- **Flask-App** — HTTP-Routen für Login, Gruppen, Nachrichten und ein JSON-State-Endpoint.
- **In-Memory-Store** — Python-Dicts für `users`, `groups`, `messages` im Prozess­speicher.

## Endpoints

| Methode | Pfad                          | Zweck                                                                  | Use Case / FA |
| ------- | ----------------------------- | ---------------------------------------------------------------------- | ------------- |
| GET     | `/`                           | Login-Form ODER Redirect in die erste Gruppe                           | UC-1, UC-7    |
| POST    | `/login`                      | Anzeigenamen setzen (re-uses existing user by name)                    | UC-1          |
| POST    | `/logout`                     | Sitzung beenden                                                        | —             |
| POST    | `/groups`                     | Gruppe erstellen, Eigentümer = aktueller Benutzer                      | UC-2          |
| GET     | `/g/<gid>`                    | HTML-Initial-Render (Sidebar, Feed, Composer)                          | UC-7, UC-8    |
| GET     | `/g/<gid>/state.json`         | JSON-Snapshot (Gruppen, Benutzer, Nachrichten) für Polling             | UC-9, FA-21/22|
| POST    | `/g/<gid>/messages`           | Nachricht senden (per `fetch`, kein Redirect)                          | UC-8          |
| POST    | `/g/<gid>/rename`             | Gruppe umbenennen                                                      | UC-3          |
| POST    | `/g/<gid>/delete`             | Gruppe löschen                                                         | UC-6          |

## Stack

- **Python 3.11+**
- **Flask** (Server + Templating + JSON via `jsonify`)
- **Gunicorn** (WSGI-Server in Render, `--workers 1 --threads 4 --timeout 60`)
- HTML/CSS + Vanilla JavaScript (kein Build-Tool, kein Framework)
- **Render Web Service** (Hosting, Free Plan)

## Files

```
app.py                     # Flask-App: Routen, In-Memory-Store, Validierung
templates/
├── base.html              # Layout + Sidebar
├── login.html             # UC-1
└── group.html             # Feed + Composer + Settings
static/
└── style.css              # 1:1 vom Mockup übernommen
requirements.txt           # Flask, gunicorn
render.yaml                # Render-Service-Definition
README.md                  # Quickstart
```

## Deployment

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn app:app`
- **Repo → Render**: Render-Account mit GitHub verknüpfen, neuen *Web Service* anlegen, Repo wählen, `render.yaml` wird automatisch erkannt.

## Live-Update-Konzept (UC-9 / F5)

Der Browser ruft alle 2 s den JSON-Endpoint `GET /g/<gid>/state.json` auf und tauscht nur geänderte DOM-Bereiche aus (Sidebar, Benutzerliste, Feed). Vorteile gegenüber `<meta http-equiv="refresh">` oder Full-Reload:

- Composer-Fokus, eingegebener Text und Scroll-Position bleiben erhalten.
- Kein Page-Flash bei jedem Tick.
- Geringe Bandbreite (JSON «diff» statt komplettem HTML).

Formulare (Senden, Neue-Gruppe, Rename, Delete) werden ebenfalls per `fetch` abgesetzt; nach erfolgreicher Antwort triggert der Client direkt einen `tick()` oder navigiert auf die Redirect-URL. Der Ungelesen-Zähler je Gruppe wird client-seitig in `localStorage` geführt (`cc_seen[gid] = msg_count`).

## Limitations (bewusst)

- **Persistenz:** Gruppen, Benutzer und Nachrichten gehen bei Restart/Redeploy verloren (FA-16). Auf Render Free zusätzlich nach 15 min Idle (Cold-Start).
- **Authentifizierung:** Nur Anzeigename via signiertem Cookie — Identitäts-Spoofing möglich. Open-Membership-Modell verzichtet bewusst auf Mitgliederverwaltung.
- **Concurrency:** Reine In-Memory-Dicts ohne Locks; Gunicorn `--workers 1` zwingend, sonst hätte jeder Worker einen eigenen Zustand.
- **Polling statt Push:** 2-Sekunden-Latenz; bei vielen Clients linear ansteigende Last. WebSocket/SSE wären der nächste Schritt jenseits TRL4.
- **Skalierung:** Nicht für Produktion; nur Lernzweck (TRL4).

## Mapping Anforderungen → Implementation

| FA      | Wo umgesetzt                                                                |
| ------- | --------------------------------------------------------------------------- |
| FA-01   | `GET /` zeigt `login.html` ohne Cookie                                       |
| FA-02   | `validate_name()` (Länge 1–32)                                              |
| FA-03   | `Flask-Session` (signed cookie)                                              |
| FA-04   | `POST /groups` — Open Membership: kein Mitglieder-Set nötig                  |
| FA-05   | `validate_groupname()` (Länge 1–64)                                         |
| FA-06   | `POST /g/<gid>/rename`                                                       |
| FA-09   | `POST /g/<gid>/delete`                                                       |
| FA-10   | `@require_owner`-Decorator                                                   |
| FA-11   | `all_groups_sorted()` rendert in Sidebar; live aktualisiert via state.json   |
| FA-12   | `POST /g/<gid>/messages` (per fetch)                                         |
| FA-13   | Template + JS rendert Autor + UTC-ISO-Timestamp lokal formatiert             |
| FA-14   | `validate_message()` (Länge 1–2000)                                         |
| FA-15   | `messages[gid]` ist append-only Liste                                        |
| FA-16   | Reine Modul-Variablen, keine DB                                              |
| FA-17   | `@require_login` + `@require_member` (letzteres prüft nur Existenz)          |
| FA-18   | Jinja2 escaped per default; Client-Render via `textContent`                  |
| FA-19   | Empty-State im Template + im JS-Renderer                                     |
| FA-20   | `@require_login`-Decorator                                                   |
| FA-21   | `GET /g/<gid>/state.json` — `group_state()`                                  |
| FA-22   | `state.json` enthält `msg_count` je Gruppe; Client berechnet Ungelesen-Diff  |
| FA-23   | Composer-`keydown`-Handler im group.html `<script>`-Block                    |
| FA-24   | `all_users_sorted()` in Sidebar; live aktualisiert via state.json            |
