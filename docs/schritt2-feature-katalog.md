# Schritt 2 — Feature-Katalog (MVP)

Abgeleitet aus dem vereinfachten DDD-Domänenmodell (`Benutzer`, `Gruppe`, `Nachricht`).
Schema pro Feature: **Anwendungsfälle · Geschäftsnutzen · High-Level-Lösungsidee**.

---

## F1 — Identität (Anzeigename)

- **Anwendungsfälle:** Eine Besucherin öffnet die App und gibt einen Anzeigenamen ein; der Name wird für die Sitzung gemerkt und neben ihren Nachrichten angezeigt.
- **Geschäftsnutzen:** Reibungsloser Einstieg ohne Registrierung — Lernende können in Sekunden mitchatten; Nachrichten erhalten einen wiedererkennbaren Autor.
- **Lösungsidee:** Beim ersten `GET /` wird, falls kein `user_id`-Cookie existiert, ein Namensformular angezeigt. `POST /join` legt `(user_id, anzeigename)` im In-Memory-Benutzerspeicher ab und setzt ein signiertes Cookie.

## F2 — Gruppenverwaltung

- **Anwendungsfälle:** Ein Benutzer erstellt eine Gruppe (wird zu deren Eigentümer); der Eigentümer benennt sie um, fügt Mitglieder hinzu/entfernt sie; der Eigentümer löscht die Gruppe.
- **Geschäftsnutzen:** Eine Klasse kann sich ohne Admin selbst in Themen-/Team-Kanäle organisieren.
- **Lösungsidee:** In-Memory-`gruppen`-Dict mit Schlüssel `group_id` und Inhalt `{name, owner_id, mitglieder:set}`. Routen: `POST /groups`, `POST /groups/<id>/members`, `DELETE /groups/<id>/members/<uid>`, `DELETE /groups/<id>`. Server-seitige Prüfung: nur `owner_id == current_user`.

## F3 — Mitgliedschaft & Navigation

- **Anwendungsfälle:** Ein Benutzer sieht die Liste seiner Gruppen und wechselt zwischen ihnen; die Nachrichten der aktiven Gruppe werden geladen.
- **Geschäftsnutzen:** Klare Trennung der Konversationen; Benutzer sehen nur, was für sie relevant ist.
- **Lösungsidee:** `GET /` rendert eine Seitenleiste aus `gruppen`, gefiltert nach Mitgliedschaft. Die aktive Gruppe ist ein Pfadparameter `/g/<id>`. Server-seitig gerenderte HTML-Seiten, vollständiger Reload — kein JS-Framework für TRL4 nötig.

## F4 — Nachricht senden

- **Anwendungsfälle:** Ein Mitglied einer Gruppe schreibt eine Textnachricht; sie erscheint im Gruppenfeed mit Autor und Zeitstempel.
- **Geschäftsnutzen:** Kernfunktion des Produkts — ermöglicht Konversation.
- **Lösungsidee:** `POST /g/<id>/messages` mit Formularfeld `text`. Anhängen an die In-Memory-Liste `nachrichten[group_id]`. Redirect zurück auf `/g/<id>` (Post-Redirect-Get).

## F5 — Antworten / Threads

- **Anwendungsfälle:** Ein Benutzer antwortet auf eine bestimmte Nachricht; Antworten werden eingerückt oder unter der Elternnachricht gruppiert dargestellt.
- **Geschäftsnutzen:** Hält Gruppenchats mit mehreren Themen lesbar; bewahrt den Konversationskontext.
- **Lösungsidee:** Dieselbe Route `POST /g/<id>/messages` mit optionalem `parent_id`. Darstellung: Top-Level-Nachrichten in Reihenfolge, Antworten eine Ebene eingerückt (keine tiefen Bäume im MVP).

## F6 — Eigene Nachrichten bearbeiten & löschen

- **Anwendungsfälle:** Der Autor bearbeitet den Text seiner Nachricht; der Autor löscht seine Nachricht (Soft-Delete: angezeigt als „gelöscht").
- **Geschäftsnutzen:** Benutzer können Tippfehler/Fehler ohne Admin-Eingriff korrigieren; reduziert soziale Reibung.
- **Lösungsidee:** `POST /messages/<id>/edit` und `POST /messages/<id>/delete`. Server prüft `author_id == current_user`. Soft-Delete setzt `geloescht=true`, im Render wird `text` ausgeblendet.

## F7 — Quasi-Echtzeit-Aktualisierung

- **Anwendungsfälle:** Ein Benutzer sieht neue Nachrichten anderer, ohne manuell neu zu laden.
- **Geschäftsnutzen:** Konversationen wirken für den Klassenraum-Einsatz „echtzeitig genug".
- **Lösungsidee:** Einfachster Weg passend zur Spezifikation: HTML-`<meta http-equiv="refresh" content="5">` auf der Gruppenansicht ODER ein winziges `setInterval`-Fetch, das das Feed-Fragment nachlädt. Keine WebSockets im MVP.

---

## Offene Fragen

1. Soll **F5 (Antworten/Threads)** für das MVP ebenfalls entfallen? Es erhöht die UI-Komplexität; das vereinfachte Domänenmodell lässt es später trotzdem zu.
2. **F7 (Auto-Refresh)** für die allererste Iteration weglassen (manueller Reload) und später nachziehen?
3. Fehlt aus deiner Sicht etwas — z.B. *Gruppe verlassen*, *Liste Online-Mitglieder*, *Nachrichten-Suche*?
