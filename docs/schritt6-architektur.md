# Schritt 6 — Architektur & Deployment (TRL4-Prototyp)

## Purpose

Web-basierter Klassenraum-Messenger als TRL4-Prototyp. Nutzer melden sich mit einem Anzeigenamen an, erstellen Gruppen, verwalten Mitglieder und tauschen Textnachrichten aus. Datenhaltung ist bewusst flüchtig (In-Memory).

## Components

- **Browser-UI** — server-gerenderte HTML-Seiten (Jinja2-Templates), kein JS-Framework.
- **Flask-App** — HTTP-Routen für Login, Gruppen, Mitglieder, Nachrichten.
- **In-Memory-Store** — Python-Dicts für `users`, `groups`, `messages` im Prozess­speicher.

## Endpoints

| Methode | Pfad                              | Zweck                        | Use Case |
| ------- | --------------------------------- | ---------------------------- | -------- |
| GET     | `/`                               | Login-Form ODER Gruppensicht | UC-1, UC-7 (implizit) |
| POST    | `/login`                          | Anzeigenamen setzen          | UC-1     |
| POST    | `/logout`                         | Sitzung beenden              | —        |
| POST    | `/groups`                         | Gruppe erstellen             | UC-2     |
| GET     | `/g/<gid>`                        | Gruppen-Feed anzeigen        | UC-7, UC-8 |
| POST    | `/g/<gid>/messages`               | Nachricht senden             | UC-8     |
| POST    | `/g/<gid>/rename`                 | Gruppe umbenennen            | UC-3     |
| POST    | `/g/<gid>/members`                | Mitglied hinzufügen          | UC-4     |
| POST    | `/g/<gid>/members/<name>/remove`  | Mitglied entfernen           | UC-5     |
| POST    | `/g/<gid>/delete`                 | Gruppe löschen               | UC-6     |

## Stack

- **Python 3.11+**
- **Flask** (Server + Templating)
- **Gunicorn** (WSGI-Server in Render)
- HTML/CSS (kein JS-Build)
- **Render Web Service** (Hosting)

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

## Limitations (bewusst)

- **Persistenz:** Gruppen, Mitgliedschaften und Nachrichten gehen bei Restart/Redeploy verloren (FA-16).
- **Authentifizierung:** Nur Anzeigename via signiertem Cookie — Identitäts-Spoofing möglich.
- **Concurrency:** Reine In-Memory-Dicts ohne Locks; bei Gunicorn mit > 1 Worker wäre Zustand pro Worker getrennt → wir starten mit `--workers=1`.
- **Skalierung:** Nicht für Produktion; nur Lernzweck (TRL4).

## Mapping Anforderungen → Implementation

| FA      | Wo umgesetzt                                        |
| ------- | --------------------------------------------------- |
| FA-01   | `GET /` zeigt `login.html` ohne Cookie              |
| FA-02   | Validierung in `validate_name()` (Länge 1–32)      |
| FA-03   | `Flask-Session` (signed cookie)                     |
| FA-04   | `POST /groups`                                      |
| FA-05   | `validate_groupname()` (Länge 1–64)                |
| FA-06   | `POST /g/<gid>/rename`                              |
| FA-07   | `POST /g/<gid>/members`                             |
| FA-08   | `POST /g/<gid>/members/<name>/remove`               |
| FA-09   | `POST /g/<gid>/delete`                              |
| FA-10   | `@require_owner`-Decorator                          |
| FA-11   | Sidebar in `base.html`                              |
| FA-12   | `POST /g/<gid>/messages`                            |
| FA-13   | Template rendert Autor + UTC-Timestamp via `<time>` |
| FA-14   | `validate_message()` (Länge 1–2000)                |
| FA-15   | `messages[gid]` ist append-only Liste              |
| FA-16   | Reine Modul-Variablen, keine DB                     |
| FA-17   | `@require_member`-Decorator                         |
| FA-18   | Jinja2 escaped per default                          |
| FA-19   | Empty-State im Template                             |
| FA-20   | `@require_login`-Decorator                          |
