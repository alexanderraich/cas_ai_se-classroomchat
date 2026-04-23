# Schritt 4 — Requirements Quality Check

Bewertung der Anforderungen aus [Schritt 3](schritt3-use-cases.md#funktionale-anforderungen-konsolidiert) entlang von vier Kriterien (gemäss Aufgabenblatt):

1. **Konsistenz** — keine widersprüchlichen Aussagen.
2. **Eindeutigkeit** — jede Anforderung lässt nur eine Interpretation zu.
3. **Notwendigkeit** — jede Anforderung trägt zum MVP bei (kein Gold-Plating).
4. **Komplettheit** — alle Features F1–F5 sind durch Anforderungen abgedeckt; keine Lücken im Hauptpfad.

Vorgehen: Erste Beurteilung durch KI-Prompt (siehe unten), anschliessend manuelle Finalisierung.

> **Hinweis (Schritt-6-Refinement):** Im Verlauf der Implementierung wurden FA-07 und FA-08 (Mitglieder hinzufügen / entfernen) **gestrichen** zugunsten eines **Open-Membership**-Modells (alle eingeloggten Benutzer sehen alle Gruppen). Im Gegenzug kamen FA-21–FA-24 (Live-Update-Endpoint, Ungelesen-Zähler, Enter-Send, Benutzerliste) hinzu. Auch UC-4/UC-5 sind entfallen, neu ist UC-7 (Gruppe auswählen) explizit und UC-9 (Live-Updates).

---

## 1. Konsistenz

| Befund                                                                                                                                            | Bewertung |
| ------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| FA-16 sagt „keine Persistenz", FA-03 spricht von Wiedererkennung über Cookie. Persistenz ist hier auf den Browser-Cookie bezogen, nicht auf Server-Speicher — semantisch konsistent. | ✓ |
| FA-08 verbietet, dass der Eigentümer sich selbst entfernt; FA-09 erlaubt das Löschen der ganzen Gruppe. Konsistent: Der Weg „raus" ist Löschen.   | ✓ |
| FA-10 fordert HTTP 403 für Nicht-Eigentümer; alle besitzergebundenen UCs (UC-3..6) referenzieren das. Konsistent.                                 | ✓ |

## 2. Eindeutigkeit

| Befund                                                                                                                                  | Bewertung |
| --------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| FA-02 / FA-05 / FA-14: Längengrenzen klar in Zeichen quantifiziert.                                                                      | ✓ |
| FA-15: „chronologische Reihenfolge" mit Klarstellung „älteste zuerst" → eindeutig.                                                       | ✓ |
| FA-13: „Erstellungszeitpunkt" — Zeitzone offen. **Ergänzung:** Anzeige in lokaler Zeit des Browsers; Speicherung in UTC.                 | ⚠ präzisieren |
| FA-16: „Lebensdauer des laufenden Prozesses" — eindeutig (impliziert Datenverlust bei Restart, deckt sich mit Architektur-Limitation).   | ✓ |

**Manuelle Korrektur:** FA-13 wird um die Zeitzonen-Klarstellung ergänzt.

## 3. Notwendigkeit (MVP-Fokus)

| ID                   | Notwendig für MVP? | Begründung                                                                  |
| -------------------- | ------------------ | --------------------------------------------------------------------------- |
| FA-01 bis FA-03      | ✓ | Identität ist Voraussetzung für authentische Nachrichten.                                |
| FA-04, FA-09         | ✓ | Gruppen-Lebenszyklus ist die Organisations-Einheit der App.                              |
| FA-05, FA-06         | ✓ | Minimale Konfiguration einer Gruppe (Name).                                              |
| FA-07, FA-08         | — | **Entfallen mit Schritt-6-Refinement** (Open Membership; siehe Hinweis oben).            |
| FA-10                | ✓ | Sicherheits-Mindeststandard; ohne diese Anforderung bricht das Eigentümer-Modell.        |
| FA-11, FA-24         | ✓ | Sichtbarkeit aller Gruppen und Benutzer ist Kern des Open-Membership-Modells.            |
| FA-12 bis FA-15      | ✓ | Kernfunktion „Chatten“.                                                                  |
| FA-16, FA-17         | ✓ | Architektur-Constraint bzw. Sicherheits-Mindeststandard.                                 |
| FA-21, FA-22         | ✓ | Live-Update-Backbone; ohne diese Endpoints kein Quasi-Echtzeit-Erlebnis.                 |
| FA-23                | ✓ | UX-Mindeststandard für Messenger — Tastatur-Flow.                                       |

**Resultat:** Keine Anforderung als „überflüssig" verworfen.

## 4. Komplettheit

Mapping Features → Anforderungen → Use Cases:

| Feature                  | Anforderungen                 | Use Cases     | abgedeckt |
| ------------------------ | ----------------------------- | ------------- | --------- |
| F1 — Identität           | FA-01, FA-02, FA-03                    | UC-1             | ✓ |
| F2 — Gruppenverwaltung   | FA-04, FA-05, FA-06, FA-09, FA-10      | UC-2, UC-3, UC-6 | ✓ |
| F3 — Sichtbarkeit/Nav.   | FA-11, FA-17, FA-24                    | UC-7             | ✓ |
| F4 — Nachricht senden    | FA-12, FA-13, FA-14, FA-15, FA-23      | UC-8             | ✓ |
| F5 — Live-Updates        | FA-21, FA-22                           | UC-9             | ✓ |
| (querschnittlich)        | FA-16 (Persistenz-Constraint)          | —                | ✓ |

**Erkannte Lücken & Ergänzungen:**

| Neue ID | Ergänzte Anforderung                                                                                                                     | Grund                                       |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| FA-18   | Das System MUSS HTML-/Script-Inhalte in Nachrichten und Anzeigenamen escapen, sodass kein Markup im Browser ausgeführt wird (XSS-Schutz). | Sicherheits-Mindeststandard, fehlte bisher. |
| FA-19   | Das System MUSS bei einem leeren Gruppenfeed einen Hinweis („Noch keine Nachrichten") anzeigen.                                            | Empty-State (NN/g „Visibility of system status"), fehlte. |
| FA-20   | Das System MUSS bei jedem Server-Aufruf prüfen, ob die Sitzung gültig ist; ungültige Sitzungen werden zur Namenseingabe geleitet.          | Sitzungs-Lebenszyklus war implizit, jetzt explizit. |

---

## Finalisierte Anforderungstabelle (nach Schritt 4)

| ID    | Anforderung (final)                                                                                                                                                     |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FA-01 | Das System MUSS jedem Benutzer ohne Registrierung das Setzen eines Anzeigenamens beim ersten Aufruf ermöglichen.                                                         |
| FA-02 | Das System MUSS Anzeigenamen mit 1–32 sichtbaren Zeichen akzeptieren und längere/leere ablehnen.                                                                         |
| FA-03 | Das System MUSS die Sitzung eines Benutzers über einen signierten Browser-Cookie erkennen und über App-Aufrufe hinweg wiederverwenden, solange der Server-Prozess läuft. |
| FA-04 | Das System MUSS einem eingeloggten Benutzer das Erstellen einer neuen Gruppe ermöglichen; der Ersteller wird automatisch Eigentümer.                                     |
| FA-05 | Das System MUSS Gruppennamen mit 1–64 sichtbaren Zeichen akzeptieren.                                                                                                    |
| FA-06 | Das System MUSS dem Eigentümer einer Gruppe erlauben, deren Namen zu ändern.                                                                                             |
| FA-09 | Das System MUSS dem Eigentümer einer Gruppe erlauben, die Gruppe inkl. aller Nachrichten zu löschen.                                                                     |
| FA-10 | Das System MUSS Konfigurationsaktionen an einer Gruppe (Umbenennen, Löschen) nur dem Eigentümer erlauben (HTTP 403 sonst).                                              |
| FA-11 | Das System MUSS jedem eingeloggten Benutzer die Liste **aller** Gruppen anzeigen (Open Membership).                                                                      |
| FA-12 | Das System MUSS einem eingeloggten Benutzer das Senden einer Textnachricht in einer beliebigen Gruppe ermöglichen.                                                       |
| FA-13 | Das System MUSS jede Nachricht mit Autor (Anzeigename) und Erstellungszeitpunkt darstellen; Speicherung in UTC, Anzeige in lokaler Zeit des Browsers.                    |
| FA-14 | Das System MUSS Nachrichtentexte mit 1–2000 Zeichen akzeptieren.                                                                                                         |
| FA-15 | Das System MUSS Nachrichten in chronologischer Reihenfolge (älteste zuerst) anzeigen.                                                                                    |
| FA-16 | Das System MUSS Nachrichten und Gruppen für die Lebensdauer des laufenden Prozesses im Speicher halten (keine Persistenz im MVP).                                        |
| FA-17 | Das System MUSS verhindern, dass nicht eingeloggte Anfragen Nachrichten lesen oder schreiben (Redirect zur Anmeldung bzw. HTTP 403).                                     |
| FA-18 | Das System MUSS HTML-/Script-Inhalte in Nachrichten und Anzeigenamen escapen, sodass kein Markup im Browser ausgeführt wird (XSS-Schutz).                                |
| FA-19 | Das System MUSS bei einem leeren Gruppenfeed einen Hinweis („Noch keine Nachrichten") anzeigen.                                                                          |
| FA-20 | Das System MUSS bei jedem Server-Aufruf prüfen, ob die Sitzung gültig ist; ungültige Sitzungen werden zur Namenseingabe geleitet.                                        |
| FA-21 | Das System MUSS einen JSON-Endpoint `GET /g/<gid>/state.json` bereitstellen, der Gruppen, Benutzer und Nachrichten der aktiven Gruppe als Snapshot liefert.              |
| FA-22 | Das System MUSS pro Gruppe die Anzahl Nachrichten ausweisen, damit der Browser einen Ungelesen-Zähler client-seitig berechnen kann.                                      |
| FA-23 | Das System MUSS das Senden einer Nachricht per Enter-Taste unterstützen, wobei Shift+Enter einen Zeilenumbruch einfügt.                                                  |
| FA-24 | Das System MUSS in der Seitenleiste eine Liste aller bekannten Benutzer anzeigen (alphabetisch, eigener Name markiert).                                                  |

**Bewusst entfallen** (durch Schritt-6-Refinement, dokumentiert): FA-07 (Mitglied hinzufügen), FA-08 (Mitglied entfernen).

---

## Verwendeter KI-Prompt (zur Reproduzierbarkeit)

> Du bist Reviewer für Software-Anforderungen. Prüfe die folgende Liste FA-01..FA-17 entlang der Kriterien Konsistenz, Eindeutigkeit, Notwendigkeit für ein MVP und Komplettheit (Abdeckung der Features F1–F4). Markiere für jede Anforderung das stärkste Defizit (falls vorhanden) und schlage konkrete Umformulierungen oder Ergänzungen vor. Liefere am Ende eine Liste fehlender Anforderungen, die du für ein robustes MVP zwingend ergänzen würdest.

Die obigen drei Ergänzungen (FA-18..FA-20) und die Umformulierung von FA-13 sind das manuell finalisierte Resultat dieses Reviews.
