# Schritt 2 — Feature-Katalog (MVP)

Abgeleitet aus dem vereinfachten DDD-Domänenmodell (`Benutzer`, `Gruppe`, `Nachricht`).
Schema pro Feature: **Anwendungsfälle (User Stories nach Cohn) · Geschäftsnutzen · High-Level-Lösungsidee**.

## Übersicht

**Verwandte Artefakte:**

- 📐 Domänenmodell (DDD-Klassendiagramm): [diagrams/domaenenmodell.puml](diagrams/domaenenmodell.puml)
- 🖥️ Interaktives HTML-Mockup: [mockups/index.html](mockups/index.html)

**Domänenmodell:**

![Domänenmodell](diagrams/domaenenmodell.png)

**Use-Case-Übersicht** (Detail-Beschreibung siehe [Schritt 3](schritt3-use-cases.md)):

![Use-Case-Übersicht](diagrams/use-case-diagramm.png)

---

## F1 — Identität (Anzeigename)

- **Anwendungsfälle:**
  - Als neuer Benutzer möchte ich beim Öffnen der App einen Anzeigenamen eingeben, damit meine Nachrichten einem wiedererkennbaren Absender zugeordnet werden können.
  - Als wiederkehrender Benutzer möchte ich beim erneuten Aufruf nicht erneut nach meinem Namen gefragt werden, damit ich ohne Reibung weiterchatten kann.
- **Geschäftsnutzen:** Reibungsloser Einstieg ohne Registrierung — Lernende können in Sekunden mitchatten; Nachrichten erhalten einen wiedererkennbaren Autor.
- **Lösungsidee:** Beim ersten `GET /` wird, falls kein `user_id`-Cookie existiert, ein Namensformular angezeigt. `POST /join` legt `(user_id, anzeigename)` im In-Memory-Benutzerspeicher ab und setzt ein signiertes Cookie.

## F2 — Gruppenverwaltung

- **Anwendungsfälle:**
  - Als Benutzer möchte ich eine neue Gruppe erstellen, damit für ein Thema oder Team ein eigener Kanal existiert.
  - Als Gruppen-Eigentümer möchte ich meine Gruppe umbenennen, damit der Name den tatsächlichen Zweck widerspiegelt.
  - Als Gruppen-Eigentümer möchte ich meine Gruppe löschen, damit nicht mehr genutzte Kanäle die Übersicht nicht belasten.
- **Geschäftsnutzen:** Eine Klasse kann sich ohne Admin selbst in Themen-/Team-Kanäle organisieren.
- **Lösungsidee:** In-Memory-`gruppen`-Dict mit Schlüssel `group_id` und Inhalt `{name, owner_id}`. Routen: `POST /groups`, `POST /g/<id>/rename`, `POST /g/<id>/delete`. Server-seitige Prüfung: nur `owner_id == current_user` darf umbenennen/löschen.

## F3 — Sichtbarkeit & Navigation

- **Anwendungsfälle:**
  - Als eingeloggter Benutzer möchte ich alle Gruppen in einer Seitenleiste sehen, damit ich ohne Einladung an jeder Konversation teilnehmen kann.
  - Als eingeloggter Benutzer möchte ich zwischen Gruppen wechseln können, damit ich gezielt die Nachrichten der gerade relevanten Gruppe lesen kann.
  - Als eingeloggter Benutzer möchte ich sehen, welche anderen Benutzer im System bekannt sind, damit ich weiß, mit wem ich potenziell chatten kann.
- **Geschäftsnutzen:** TRL4-Vereinfachung **Open Membership**: in einer Klasse hat jeder Zugang zu jeder Gruppe — keine Einladungs-Bottlenecks. Die Sichtbarkeit aller Benutzer macht die Anwesenheit spürbar.
- **Lösungsidee:** `GET /` rendert eine Seitenleiste aus `gruppen` (alle Gruppen, alphabetisch) und `users` (alle bekannten Benutzer). Die aktive Gruppe ist ein Pfadparameter `/g/<id>`.

## F4 — Nachricht senden

- **Anwendungsfälle:**
  - Als eingeloggter Benutzer möchte ich in einer Gruppe eine Textnachricht schreiben und absenden, damit ich mit den anderen Benutzern kommunizieren kann.
  - Als eingeloggter Benutzer möchte ich neben jeder Nachricht den Autor und den Zeitstempel sehen, damit ich den Verlauf der Konversation nachvollziehen kann.
  - Als eingeloggter Benutzer möchte ich mit der Enter-Taste senden können (Shift+Enter für Zeilenumbruch), damit der Chat-Flow ungebremst ist.
- **Geschäftsnutzen:** Kernfunktion des Produkts — ermöglicht Konversation.
- **Lösungsidee:** `POST /g/<id>/messages` mit Formularfeld `text`, gesendet via `fetch`. Anhängen an die In-Memory-Liste `nachrichten[group_id]`. Composer leert sich client-seitig, kein Full-Reload.

## F5 — Live-Updates & Aktivitäts-Indikator

- **Anwendungsfälle:**
  - Als eingeloggter Benutzer möchte ich neue Nachrichten anderer Benutzer sehen, ohne die Seite manuell neu zu laden, damit der Chat sich anfühlt wie ein Echtzeit-Messenger.
  - Als eingeloggter Benutzer möchte ich an einem Zähler neben dem Gruppennamen erkennen, in welchen Gruppen ungelesene Nachrichten vorliegen, damit ich diese gezielt öffnen kann.
- **Geschäftsnutzen:** Erhöht die wahrgenommene Reaktivität und reduziert kognitiven Aufwand (welche Gruppe wurde aktualisiert?).
- **Lösungsidee:** Browser pollt `GET /g/<id>/state.json` alle 2 s und tauscht nur DOM-Inhalte aus (Sidebar, Benutzerliste, Feed). Ungelesen-Zähler client-seitig via `localStorage` (pro Gruppe: zuletzt gesehene Anzahl). Komposer-Fokus und Scroll-Position bleiben erhalten.

---

## Bewusst nicht im MVP

- Mitgliederverwaltung pro Gruppe (TRL4-Vereinfachung: **Open Membership** — alle eingeloggten Benutzer sehen alle Gruppen)
- Antworten / Threads
- Bearbeiten / Löschen eigener Nachrichten
- Anhänge, Reaktionen, Rollen, 1:1-DMs
- Tipp-/Lese-Indikatoren, echte Online-Präsenz (nur Liste bekannter Benutzer)
- Echtzeit-Push (WebSocket / SSE) — stattdessen 2-Sekunden-Polling
