# Schritt 3 — Use Cases & funktionale Anforderungen

Ableitung der Use Cases aus dem [Feature-Katalog](schritt2-feature-katalog.md) gemäss UML-Block im REQ-Skript.
Format pro Use Case: Name · Akteur · Vorbedingung · Hauptszenario · Alternativen/Fehler · Nachbedingung.
Im Anschluss: konsolidierte Liste **funktionaler Anforderungen** (FA-x), eindeutig referenzierbar.

**Übersicht:**

![Use-Case-Übersicht](diagrams/use-case-diagramm.png)

> Quelle: [diagrams/use-case-diagramm.puml](diagrams/use-case-diagramm.puml)

---

## Akteure

- **Gast** — Person ohne Sitzung; hat noch keinen Anzeigenamen gesetzt.
- **Eingeloggter Benutzer** — Person mit Anzeigename und gültiger Sitzung. Sieht im **Open-Membership**-Modell alle Gruppen.
- **Gruppen-Eigentümer** — Eingeloggter Benutzer, der eine Gruppe erstellt hat; in seinen eigenen Gruppen mit erweiterten Rechten (Umbenennen, Löschen).

> Es gibt keine systemweite Admin-Rolle und keine explizite Mitgliedschaft pro Gruppe (per Schritt-1- bzw. Schritt-6-Vereinfachung entfernt).

---

## UC-1 — App betreten und Anzeigename festlegen

- **Akteur:** Gast
- **Vorbedingung:** Browser hat kein gültiges Sitzungs-Cookie.
- **Hauptszenario:**
  1. Gast öffnet die Startseite.
  2. System zeigt das Namensformular an.
  3. Gast gibt einen Anzeigenamen ein und sendet ab.
  4. System validiert den Namen, erzeugt eine Sitzung und leitet auf die Gruppenübersicht weiter.
- **Alternativen / Fehler:**
  - 3a. Name ist leer oder zu lang → System zeigt Fehlermeldung, Schritt 2.
  - 0a. Bestehende gültige Sitzung → System überspringt Formular und leitet direkt auf die Gruppenübersicht weiter.
- **Nachbedingung:** Mitglied ist eingestiegen und hat eine Sitzung.

## UC-2 — Gruppe erstellen

- **Akteur:** Eingeloggter Benutzer
- **Vorbedingung:** Akteur hat eine Sitzung.
- **Hauptszenario:**
  1. Akteur tippt einen Gruppennamen in das Feld „Neue Gruppe…" und sendet ab.
  2. System erstellt die Gruppe, setzt den Akteur als Eigentümer und navigiert direkt in die neue Gruppe.
- **Alternativen / Fehler:**
  - 1a. Name ist leer/zu lang → Eingabe wird verworfen, Fokus bleibt im Feld.
- **Nachbedingung:** Neue Gruppe existiert; Akteur ist Eigentümer; Gruppe ist für alle eingeloggten Benutzer sichtbar (Open Membership).

## UC-3 — Gruppe umbenennen

- **Akteur:** Gruppen-Eigentümer
- **Vorbedingung:** Akteur ist Eigentümer der Zielgruppe.
- **Hauptszenario:**
  1. Eigentümer öffnet die Gruppen-Einstellungen.
  2. System zeigt aktuellen Namen.
  3. Eigentümer gibt neuen Namen ein und speichert.
  4. System aktualisiert den Namen, schliesst das Einstellungs-Dropdown und lockt die Sidebar/Header per Live-Update neu (UC-9).
- **Alternativen / Fehler:**
  - 0a. Akteur ist nicht Eigentümer → System verweigert Zugriff (HTTP 403).
- **Nachbedingung:** Gruppenname ist aktualisiert; allen eingeloggten Benutzern wird der neue Name binnen ca. 2 s angezeigt.

## UC-6 — Gruppe löschen

- **Akteur:** Gruppen-Eigentümer
- **Vorbedingung:** Akteur ist Eigentümer.
- **Hauptszenario:**
  1. Eigentümer wählt „Gruppe löschen".
  2. System fragt zur Bestätigung.
  3. Eigentümer bestätigt.
  4. System löscht Gruppe und alle Nachrichten der Gruppe.
- **Nachbedingung:** Gruppe existiert nicht mehr; Akteur landet auf der Startseite, andere Benutzer sehen die Gruppe binnen ca. 2 s nicht mehr in ihrer Sidebar.

## UC-7 — Gruppe auswählen

- **Akteur:** Eingeloggter Benutzer
- **Vorbedingung:** Mindestens eine Gruppe existiert.
- **Hauptszenario:**
  1. Akteur sieht in der Seitenleiste alle Gruppen (alphabetisch).
  2. Akteur wählt eine Gruppe aus.
  3. System lädt und zeigt die Nachrichten dieser Gruppe; der Ungelesen-Zähler dieser Gruppe wird zurückgesetzt.
- **Nachbedingung:** Aktive Gruppe ist gewechselt.

## UC-8 — Nachricht senden

- **Akteur:** Eingeloggter Benutzer
- **Vorbedingung:** Eine Gruppe ist aktiv.
- **Hauptszenario:**
  1. Akteur tippt Text in das Eingabefeld.
  2. Akteur drückt **Enter** oder klickt „Senden" (Shift+Enter fügt Zeilenumbruch ein).
  3. System legt Nachricht mit Autor und UTC-Zeitstempel an.
  4. System leert das Eingabefeld und zeigt die Nachricht im Feed.
- **Alternativen / Fehler:**
  - 1a. Text ist leer/whitespace → Anfrage wird gar nicht erst gesendet.
  - 0a. Sitzung ungültig (z. B. Cold-Start) → Browser wird auf die Startseite umgeleitet.
- **Nachbedingung:** Nachricht ist im Feed der Gruppe sichtbar; andere eingeloggte Benutzer sehen sie binnen ca. 2 s via UC-9.

## UC-9 — Live-Updates empfangen

- **Akteur:** Eingeloggter Benutzer
- **Vorbedingung:** Akteur hat eine Gruppensicht geöffnet.
- **Hauptszenario:**
  1. Browser pollt alle 2 s den Endpoint `GET /g/<gid>/state.json`.
  2. System liefert aktuellen Zustand (alle Gruppen, alle Benutzer, Nachrichten dieser Gruppe).
  3. Browser tauscht nur geänderte DOM-Bereiche aus (Sidebar, Benutzerliste, Feed); Komposer-Fokus und Scroll-Position bleiben erhalten.
  4. Für nicht-aktive Gruppen mit neuen Nachrichten zeigt der Browser einen Ungelesen-Zähler (basierend auf `localStorage`).
- **Alternativen / Fehler:**
  - 2a. Server liefert 404/302 (Gruppe gelöscht / Sitzung ungültig) → Browser navigiert zur Startseite.
  - 2b. Netzwerkfehler → Polling läuft beim nächsten Intervall weiter.
- **Nachbedingung:** Akteur sieht neue Nachrichten, neue Gruppen und neue Benutzer ohne manuellen Reload.

---

## Funktionale Anforderungen (konsolidiert)

| ID    | Anforderung                                                                                                                                                | Quelle (UC / Feature)   |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| FA-01 | Das System MUSS jedem Benutzer ohne Registrierung das Setzen eines Anzeigenamens beim ersten Aufruf ermöglichen.                                            | UC-1, F1                |
| FA-02 | Das System MUSS Anzeigenamen mit 1–32 sichtbaren Zeichen akzeptieren und längere/leere ablehnen.                                                            | UC-1, F1                |
| FA-03 | Das System MUSS die Sitzung eines Benutzers über einen signierten Browser-Cookie erkennen und über App-Aufrufe hinweg wiederverwenden, solange der Server-Prozess läuft. | UC-1, F1                |
| FA-04 | Das System MUSS einem eingeloggten Benutzer das Erstellen einer neuen Gruppe ermöglichen; der Ersteller wird automatisch Eigentümer.                       | UC-2, F2                |
| FA-05 | Das System MUSS Gruppennamen mit 1–64 sichtbaren Zeichen akzeptieren.                                                                                       | UC-2, UC-3, F2          |
| FA-06 | Das System MUSS dem Eigentümer einer Gruppe erlauben, deren Namen zu ändern.                                                                                 | UC-3, F2                |
| FA-09 | Das System MUSS dem Eigentümer einer Gruppe erlauben, die Gruppe inkl. aller Nachrichten zu löschen.                                                        | UC-6, F2                |
| FA-10 | Das System MUSS Konfigurationsaktionen an einer Gruppe (Umbenennen, Löschen) nur dem Eigentümer erlauben (HTTP 403 sonst).                                  | UC-3, UC-6, F2          |
| FA-11 | Das System MUSS jedem eingeloggten Benutzer die Liste **aller** Gruppen anzeigen (Open Membership).                                                          | UC-7, F3                |
| FA-12 | Das System MUSS einem eingeloggten Benutzer das Senden einer Textnachricht in einer beliebigen Gruppe ermöglichen.                                          | UC-8, F4                |
| FA-13 | Das System MUSS jede Nachricht mit Autor (Anzeigename) und Erstellungszeitpunkt darstellen; Speicherung in UTC, Anzeige in lokaler Zeit des Browsers.       | UC-8, F4                |
| FA-14 | Das System MUSS Nachrichtentexte mit 1–2000 Zeichen akzeptieren.                                                                                             | UC-8, F4                |
| FA-15 | Das System MUSS Nachrichten in chronologischer Reihenfolge (älteste zuerst) anzeigen.                                                                        | UC-8, F4                |
| FA-16 | Das System MUSS Nachrichten und Gruppen für die Lebensdauer des laufenden Prozesses im Speicher halten (keine Persistenz im MVP).                            | Architektur-Constraint  |
| FA-17 | Das System MUSS verhindern, dass nicht eingeloggte Anfragen Nachrichten lesen oder schreiben (Redirect zur Anmeldung bzw. HTTP 403).                         | UC-7, UC-8              |
| FA-21 | Das System MUSS einen JSON-Endpoint `GET /g/<gid>/state.json` bereitstellen, der Gruppen, Benutzer und Nachrichten der aktiven Gruppe als Snapshot liefert. | UC-9, F5                |
| FA-22 | Das System MUSS pro Gruppe die Anzahl Nachrichten ausweisen, damit der Browser einen Ungelesen-Zähler client-seitig berechnen kann.                          | UC-9, F5                |
| FA-23 | Das System MUSS das Senden einer Nachricht per Enter-Taste unterstützen, wobei Shift+Enter einen Zeilenumbruch einfügt.                                     | UC-8, F4                |
| FA-24 | Das System MUSS in der Seitenleiste eine Liste aller bekannten Benutzer anzeigen (alphabetisch, eigener Name markiert).                                      | F3                      |

---

## Anforderungen in Sophist-Schablone (technische User Stories)

Dieselben funktionalen Anforderungen, formuliert nach der Sophist-Schablone für Anforderungssätze:

> `<Wann?> <unter welchen Bedingungen?>` **MUSS / SOLLTE / WIRD** `das System` (`<Wem?>` `die Möglichkeit bieten,`) `<Objekt> <Prozessverb>`.

Drei Satzformen werden verwendet:
- **Selbsttätige Systemaktivität** — das System handelt eigenständig.
- **Benutzerinteraktion** — das System bietet jemandem die Möglichkeit zu etwas.
- **Schnittstellenanforderung** — das System ist fähig zu etwas.

| ID    | Anforderungssatz (Sophist-Schablone)                                                                                                                                                                                                |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FA-01 | Beim ersten Aufruf der App, sofern kein gültiges Sitzungs-Cookie vorliegt, MUSS das System dem Benutzer die Möglichkeit bieten, einen Anzeigenamen ohne vorherige Registrierung festzulegen.                                          |
| FA-02 | Bei der Eingabe eines Anzeigenamens MUSS das System die Eingabe nur akzeptieren, wenn sie zwischen 1 und 32 sichtbaren Zeichen lang ist; andernfalls MUSS das System die Eingabe ablehnen und eine Fehlermeldung anzeigen.            |
| FA-03 | Bei jedem HTTP-Request MUSS das System fähig sein, eine bestehende Sitzung anhand eines signierten Browser-Cookies zu erkennen und für die Lebensdauer des Server-Prozesses wiederzuverwenden.                                          |
| FA-04 | Auf Anforderung eines eingeloggten Benutzers MUSS das System dem Benutzer die Möglichkeit bieten, eine neue Gruppe anzulegen, und MUSS den Ersteller automatisch als Eigentümer der neuen Gruppe eintragen.                            |
| FA-05 | Bei der Erstellung oder Umbenennung einer Gruppe MUSS das System einen Gruppennamen nur akzeptieren, wenn er zwischen 1 und 64 sichtbaren Zeichen lang ist.                                                                          |
| FA-06 | Auf Anforderung des Eigentümers einer Gruppe MUSS das System dem Eigentümer die Möglichkeit bieten, den Namen seiner Gruppe zu ändern.                                                                                                  |
| FA-09 | Auf Anforderung des Eigentümers einer Gruppe MUSS das System dem Eigentümer die Möglichkeit bieten, die Gruppe inklusive aller Nachrichten zu löschen.                                                                                  |
| FA-10 | Bei jeder konfigurierenden Anfrage an eine Gruppe (Umbenennen, Löschen) MUSS das System die Anfrage nur ausführen, wenn der anfragende Benutzer der Eigentümer der Gruppe ist; andernfalls MUSS das System mit HTTP 403 antworten. |
| FA-11 | Beim Aufruf der Anwendung MUSS das System dem eingeloggten Benutzer die Liste aller Gruppen (alphabetisch sortiert) anzeigen.                                                                                                       |
| FA-12 | Auf Anforderung eines eingeloggten Benutzers MUSS das System dem Benutzer die Möglichkeit bieten, eine Textnachricht in einer beliebigen Gruppe zu senden.                                                                            |
| FA-13 | Bei der Darstellung jeder Nachricht MUSS das System den Anzeigenamen des Autors sowie den Erstellungszeitpunkt anzeigen, wobei der Zeitpunkt in UTC gespeichert und in der lokalen Zeitzone des Browsers angezeigt wird.              |
| FA-14 | Bei der Eingabe einer Nachricht MUSS das System den Text nur akzeptieren, wenn er zwischen 1 und 2000 Zeichen lang ist.                                                                                                              |
| FA-15 | Bei der Anzeige des Nachrichten-Feeds einer Gruppe MUSS das System die Nachrichten in chronologisch aufsteigender Reihenfolge (älteste zuerst) sortieren.                                                                            |
| FA-16 | Während des Betriebs MUSS das System Gruppen und Nachrichten ausschliesslich im Speicher des laufenden Prozesses halten; ein Neustart führt zum Verlust dieser Daten (Architektur-Constraint des MVP).                              |
| FA-17 | Bei jedem Zugriff auf eine Gruppen-Ressource MUSS das System prüfen, ob eine gültige Sitzung vorliegt, und nicht-eingeloggten Anfragen den Zugriff verweigern (Redirect bzw. HTTP 403).                                              |
| FA-21 | Auf Anforderung eines eingeloggten Benutzers MUSS das System einen Snapshot des aktuellen Zustands (Gruppen, Benutzer, Nachrichten der aktiven Gruppe) als JSON über `GET /g/<gid>/state.json` liefern.                              |
| FA-22 | Bei jeder Antwort auf den State-Endpoint MUSS das System je Gruppe die Anzahl bislang gespeicherter Nachrichten mitliefern, damit der Client einen Ungelesen-Zähler ableiten kann.                                                  |
| FA-23 | Bei der Eingabe einer Nachricht MUSS der Composer das Senden auslösen, sobald die Enter-Taste gedrückt wird, wobei Shift+Enter einen Zeilenumbruch einfügt.                                                                          |
| FA-24 | Beim Aufruf der Anwendung MUSS das System dem eingeloggten Benutzer eine alphabetisch sortierte Liste aller bekannten Benutzer in der Seitenleiste anzeigen, wobei der eigene Eintrag als solcher gekennzeichnet ist.                |

---

## Qualitätssicherung

- **Peer-Review** der Use Cases und der Anforderungstabelle (vollständige Abdeckung aller Features F1–F4, eindeutige Akteure, klare Vor-/Nachbedingungen).
- Übergang in Schritt 4 (Requirements Quality Check) mit dieser Tabelle als Eingabe.
