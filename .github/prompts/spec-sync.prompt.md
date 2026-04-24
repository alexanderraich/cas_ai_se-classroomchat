---
description: "Use when code in app.py / templates / static has drifted from the SDD specs (Schritt 2/3/4/6) — diff implementation against specs, list mismatches, propose minimal edits to either side."
agent: agent
argument-hint: "Optional: Bereich (z. B. 'nur Schritt 3' oder 'Endpoints')"
tools: [search, edit, runCommands]
---

# /spec-sync — Spezifikationen mit Code abgleichen

Du synchronisierst die SDD-Artefakte mit dem aktuellen Implementierungsstand des Classroom-Chat-Projekts.

## Kontext

- Projekt-README: [README.md](../../README.md)
- Implementierung: [app.py](../../app.py), [templates/group.html](../../templates/group.html)
- Specs (Quelle der Wahrheit für Anforderungen):
  - [docs/schritt2-feature-katalog.md](../../docs/schritt2-feature-katalog.md) — Features F1..F5
  - [docs/schritt3-use-cases.md](../../docs/schritt3-use-cases.md) — UCs + FA-Liste
  - [docs/schritt4-quality-check.md](../../docs/schritt4-quality-check.md) — Quality Check
  - [docs/schritt6-architektur.md](../../docs/schritt6-architektur.md) — Architektur + Endpoint-Tabelle
- Diagramme: [docs/diagrams/domaenenmodell.puml](../../docs/diagrams/domaenenmodell.puml), [docs/diagrams/use-case-diagramm.puml](../../docs/diagrams/use-case-diagramm.puml)

## Vorgehen

1. **Inventarisieren**
   - Liste alle Routen aus `app.py` (Methode + Pfad + Zweck).
   - Liste alle Felder, die `state.json` zurückgibt.
   - Liste alle stabilen DOM-IDs / Forms in `templates/group.html`.
2. **Spec-Stand sammeln**
   - Extrahiere alle FA-IDs aus Schritt 3 und die Endpoint-Tabelle aus Schritt 6.
   - Extrahiere die aktuelle Feature-Liste F1..F5 aus Schritt 2.
3. **Diff bilden** — präsentiere als Tabelle:

   | Bereich | Spec sagt | Code tut | Status | Empfehlung |
   | ------- | --------- | -------- | ------ | ---------- |
   | …       | …         | …        | ✅ / ⚠️ / ❌ | spec / code anpassen |

4. **Invarianten prüfen** (hart, nicht ignorieren):
   - In-Memory-State ⇒ `--workers 1` in `render.yaml`
   - Open Membership ⇒ kein `members`-Set in `app.py`, kein FA-07/08 in den Specs
   - `/g/<gid>/state.json` ist Single Source of Truth fürs Polling
5. **Vorschläge** — gruppiert nach „Spec nachziehen" vs. „Code anpassen". Begründe jede Empfehlung in einem Satz. Nenne pro Vorschlag den genauen Datei-Pfad und ggf. eine konkrete Edit-Skizze.
6. **Stop**. Führe Edits **nicht** automatisch aus. Warte auf Bestätigung des Users, welche Vorschläge übernommen werden.

## Out-of-Scope

- Keine neuen Features erfinden. Nur Drift dokumentieren.
- Keine Diagramme rendern (nur Puml-Quelltext berücksichtigen).
- Keine Git-Commits ohne ausdrückliche Freigabe.
