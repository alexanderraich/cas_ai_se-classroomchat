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
- **Mitglied** — Eingestiegener Benutzer mit Anzeigename; Mitglied in 0..n Gruppen.
- **Gruppen-Eigentümer** — Mitglied, das eine Gruppe erstellt hat oder als Eigentümer geführt wird; in seinen eigenen Gruppen mit erweiterten Rechten.

> Es gibt keine systemweite Admin-Rolle (per Schritt-1-Vereinfachung entfernt).

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

- **Akteur:** Mitglied
- **Vorbedingung:** Mitglied hat eine Sitzung.
- **Hauptszenario:**
  1. Mitglied wählt „Neue Gruppe".
  2. System zeigt Formular für Gruppennamen.
  3. Mitglied gibt Namen ein und bestätigt.
  4. System erstellt die Gruppe, setzt das Mitglied als Eigentümer und Erstmitglied, leitet in die neue Gruppe weiter.
- **Alternativen / Fehler:**
  - 3a. Name ist leer/zu lang → Fehlermeldung, Schritt 2.
- **Nachbedingung:** Neue Gruppe existiert; Akteur ist Eigentümer und Mitglied.

## UC-3 — Gruppe umbenennen

- **Akteur:** Gruppen-Eigentümer
- **Vorbedingung:** Akteur ist Eigentümer der Zielgruppe.
- **Hauptszenario:**
  1. Eigentümer öffnet die Gruppen-Einstellungen.
  2. System zeigt aktuellen Namen.
  3. Eigentümer gibt neuen Namen ein und speichert.
  4. System aktualisiert den Namen.
- **Alternativen / Fehler:**
  - 0a. Akteur ist nicht Eigentümer → System verweigert Zugriff (HTTP 403).
- **Nachbedingung:** Gruppenname ist aktualisiert.

## UC-4 — Mitglied zur Gruppe hinzufügen

- **Akteur:** Gruppen-Eigentümer
- **Vorbedingung:** Akteur ist Eigentümer; Zielbenutzer existiert.
- **Hauptszenario:**
  1. Eigentümer öffnet Mitgliederverwaltung der Gruppe.
  2. Eigentümer wählt einen Benutzer aus der Liste verfügbarer Benutzer.
  3. System fügt den Benutzer als Mitglied hinzu.
- **Alternativen / Fehler:**
  - 2a. Benutzer ist bereits Mitglied → System zeigt Hinweis, kein Doppeleintrag.
- **Nachbedingung:** Zielbenutzer ist Mitglied der Gruppe.

## UC-5 — Mitglied aus Gruppe entfernen

- **Akteur:** Gruppen-Eigentümer
- **Vorbedingung:** Akteur ist Eigentümer; Zielmitglied ist Teil der Gruppe.
- **Hauptszenario:**
  1. Eigentümer öffnet Mitgliederverwaltung.
  2. Eigentümer wählt „Entfernen" beim Zielmitglied.
  3. System entfernt das Mitglied.
- **Alternativen / Fehler:**
  - 2a. Zielmitglied ist der Eigentümer selbst → System verweigert (Eigentümer kann sich nicht entfernen).
- **Nachbedingung:** Zielbenutzer ist kein Mitglied mehr; bestehende Nachrichten bleiben sichtbar (mit Autorname).

## UC-6 — Gruppe löschen

- **Akteur:** Gruppen-Eigentümer
- **Vorbedingung:** Akteur ist Eigentümer.
- **Hauptszenario:**
  1. Eigentümer wählt „Gruppe löschen".
  2. System fragt zur Bestätigung.
  3. Eigentümer bestätigt.
  4. System löscht Gruppe, Mitgliedschaften und alle Nachrichten der Gruppe.
- **Nachbedingung:** Gruppe existiert nicht mehr; Akteur landet auf der Gruppenübersicht.

## UC-7 — Gruppen wechseln

- **Akteur:** Mitglied
- **Vorbedingung:** Mitglied ist in mindestens einer Gruppe.
- **Hauptszenario:**
  1. Mitglied sieht in der Seitenleiste die Liste seiner Gruppen.
  2. Mitglied wählt eine Gruppe aus.
  3. System lädt und zeigt die Nachrichten dieser Gruppe.
- **Nachbedingung:** Aktive Gruppe ist gewechselt.

## UC-8 — Nachricht senden

- **Akteur:** Mitglied
- **Vorbedingung:** Mitglied ist in der aktiven Gruppe.
- **Hauptszenario:**
  1. Mitglied tippt Text in das Eingabefeld.
  2. Mitglied sendet ab.
  3. System legt Nachricht mit Autor und Zeitstempel an.
  4. System zeigt die Nachricht im Feed.
- **Alternativen / Fehler:**
  - 1a. Text ist leer → Sende-Schaltfläche bleibt deaktiviert.
  - 0a. Mitglied ist nicht (mehr) Mitglied der Gruppe → System verweigert (HTTP 403).
- **Nachbedingung:** Nachricht ist im Feed der Gruppe sichtbar (nach manuellem Reload).

---

## Funktionale Anforderungen (konsolidiert)

| ID    | Anforderung                                                                                                                              | Quelle (UC / Feature)   |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| FA-01 | Das System MUSS jedem Benutzer ohne Registrierung das Setzen eines Anzeigenamens beim ersten Aufruf ermöglichen.                          | UC-1, F1                |
| FA-02 | Das System MUSS Anzeigenamen mit 1–32 sichtbaren Zeichen akzeptieren und längere/leere ablehnen.                                          | UC-1, F1                |
| FA-03 | Das System MUSS die Sitzung eines Benutzers über einen signierten Browser-Cookie erkennen und über App-Aufrufe hinweg wiederverwenden, solange der Server-Prozess läuft. | UC-1, F1 |
| FA-04 | Das System MUSS einem Mitglied das Erstellen einer neuen Gruppe ermöglichen; der Ersteller wird automatisch Eigentümer und Erstmitglied. | UC-2, F2                |
| FA-05 | Das System MUSS Gruppennamen mit 1–64 sichtbaren Zeichen akzeptieren.                                                                     | UC-2, UC-3, F2          |
| FA-06 | Das System MUSS dem Eigentümer einer Gruppe erlauben, deren Namen zu ändern.                                                              | UC-3, F2                |
| FA-07 | Das System MUSS dem Eigentümer einer Gruppe erlauben, Mitglieder hinzuzufügen.                                                            | UC-4, F2                |
| FA-08 | Das System MUSS dem Eigentümer einer Gruppe erlauben, Mitglieder (ausser sich selbst) zu entfernen.                                       | UC-5, F2                |
| FA-09 | Das System MUSS dem Eigentümer einer Gruppe erlauben, die Gruppe inkl. aller Mitgliedschaften und Nachrichten zu löschen.                 | UC-6, F2                |
| FA-10 | Das System MUSS Schreib-/Konfigurationsaktionen an einer Gruppe nur dem Eigentümer erlauben (HTTP 403 sonst).                             | UC-3..6, F2             |
| FA-11 | Das System MUSS jedem Mitglied seine Mitgliedschaften (Liste der eigenen Gruppen) anzeigen.                                              | F3                      |
| FA-12 | Das System MUSS einem Mitglied das Senden einer Textnachricht in einer Gruppe ermöglichen, in der es Mitglied ist.                        | UC-8, F4                |
| FA-13 | Das System MUSS jede Nachricht mit Autor (Anzeigename) und Erstellungszeitpunkt darstellen.                                               | UC-8, F4                |
| FA-14 | Das System MUSS Nachrichtentexte mit 1–2000 Zeichen akzeptieren.                                                                          | UC-8, F4                |
| FA-15 | Das System MUSS Nachrichten in chronologischer Reihenfolge (älteste zuerst) anzeigen.                                                     | UC-8, F4                |
| FA-16 | Das System MUSS Nachrichten und Gruppen für die Lebensdauer des laufenden Prozesses im Speicher halten (keine Persistenz im MVP).         | Architektur-Constraint  |
| FA-17 | Das System MUSS verhindern, dass Nicht-Mitglieder Nachrichten einer Gruppe lesen oder schreiben.                                          | UC-8, F3, F4            |

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
| FA-04 | Auf Anforderung eines angemeldeten Mitglieds MUSS das System dem Mitglied die Möglichkeit bieten, eine neue Gruppe anzulegen, und MUSS den Ersteller automatisch als Eigentümer und Erstmitglied der neuen Gruppe eintragen.        |
| FA-05 | Bei der Erstellung oder Umbenennung einer Gruppe MUSS das System einen Gruppennamen nur akzeptieren, wenn er zwischen 1 und 64 sichtbaren Zeichen lang ist.                                                                          |
| FA-06 | Auf Anforderung des Eigentümers einer Gruppe MUSS das System dem Eigentümer die Möglichkeit bieten, den Namen seiner Gruppe zu ändern.                                                                                                  |
| FA-07 | Auf Anforderung des Eigentümers einer Gruppe MUSS das System dem Eigentümer die Möglichkeit bieten, weitere Benutzer als Mitglieder zur Gruppe hinzuzufügen.                                                                              |
| FA-08 | Auf Anforderung des Eigentümers einer Gruppe MUSS das System dem Eigentümer die Möglichkeit bieten, Mitglieder — mit Ausnahme des Eigentümers selbst — aus der Gruppe zu entfernen.                                                  |
| FA-09 | Auf Anforderung des Eigentümers einer Gruppe MUSS das System dem Eigentümer die Möglichkeit bieten, die Gruppe inklusive aller Mitgliedschaften und Nachrichten zu löschen.                                                              |
| FA-10 | Bei jeder schreibenden oder konfigurierenden Anfrage an eine Gruppe MUSS das System die Anfrage nur ausführen, wenn der anfragende Benutzer der Eigentümer der Gruppe ist; andernfalls MUSS das System die Anfrage mit HTTP 403 ablehnen. |
| FA-11 | Beim Aufruf der Anwendung MUSS das System dem angemeldeten Mitglied die Liste seiner eigenen Gruppen anzeigen.                                                                                                                       |
| FA-12 | Auf Anforderung eines Mitglieds einer Gruppe MUSS das System dem Mitglied die Möglichkeit bieten, eine Textnachricht in dieser Gruppe zu senden.                                                                                       |
| FA-13 | Bei der Darstellung jeder Nachricht MUSS das System den Anzeigenamen des Autors sowie den Erstellungszeitpunkt anzeigen, wobei der Zeitpunkt in UTC gespeichert und in der lokalen Zeitzone des Browsers angezeigt wird.              |
| FA-14 | Bei der Eingabe einer Nachricht MUSS das System den Text nur akzeptieren, wenn er zwischen 1 und 2000 Zeichen lang ist.                                                                                                              |
| FA-15 | Bei der Anzeige des Nachrichten-Feeds einer Gruppe MUSS das System die Nachrichten in chronologisch aufsteigender Reihenfolge (älteste zuerst) sortieren.                                                                            |
| FA-16 | Während des Betriebs MUSS das System Gruppen und Nachrichten ausschliesslich im Speicher des laufenden Prozesses halten; ein Neustart führt zum Verlust dieser Daten (Architektur-Constraint des MVP).                              |
| FA-17 | Bei jedem lesenden oder schreibenden Zugriff auf Nachrichten einer Gruppe MUSS das System prüfen, ob der anfragende Benutzer Mitglied der Gruppe ist, und Nicht-Mitgliedern den Zugriff verweigern.                                  |

---

## Qualitätssicherung

- **Peer-Review** der Use Cases und der Anforderungstabelle (vollständige Abdeckung aller Features F1–F4, eindeutige Akteure, klare Vor-/Nachbedingungen).
- Übergang in Schritt 4 (Requirements Quality Check) mit dieser Tabelle als Eingabe.
