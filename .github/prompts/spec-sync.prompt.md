---
description: "Use when code in app.py / templates / static may have drifted from the SDD specs (Schritt 2/3/4/6) — diff implementation against specs, list mismatches, propose minimal edits to either side. Read-only by default; never commits."
agent: agent
argument-hint: "Optional: scope (e.g. 'Schritt 3 only', 'endpoints', 'state.json fields')"
tools: [search, edit, runCommands]
---

# /spec-sync — Reconcile specs with implementation

You synchronize the SDD artifacts with the current implementation state of the Classroom Chat project.

## Inputs

- Project README: [README.md](../../README.md)
- Implementation:
  - [app.py](../../app.py) — Flask routes + in-memory state
  - [templates/group.html](../../templates/group.html) — UI + polling client
  - [templates/base.html](../../templates/base.html), [templates/login.html](../../templates/login.html)
  - [static/style.css](../../static/style.css)
  - [render.yaml](../../render.yaml)
- Specs (source of truth for requirements):
  - [docs/schritt2-feature-katalog.md](../../docs/schritt2-feature-katalog.md) — features F1..F5
  - [docs/schritt3-use-cases.md](../../docs/schritt3-use-cases.md) — use cases + FA list
  - [docs/schritt4-quality-check.md](../../docs/schritt4-quality-check.md) — quality check
  - [docs/schritt6-architektur.md](../../docs/schritt6-architektur.md) — architecture + endpoint table
- Diagrams: [docs/diagrams/domaenenmodell.puml](../../docs/diagrams/domaenenmodell.puml), [docs/diagrams/use-case-diagramm.puml](../../docs/diagrams/use-case-diagramm.puml)

If the user supplies an argument, narrow the scope accordingly; otherwise cover everything below.

## Procedure

1. **Inventory the implementation**
   - List every Flask route from `app.py` (HTTP method + path + purpose, one line each).
   - List every field returned by `/g/<gid>/state.json` (top-level keys + nested keys for `groups[]`, `users[]`, `messages[]`).
   - List the stable DOM IDs and form IDs in `templates/group.html` (`#group-list`, `#user-list`, `#feed`, `#composer-form`, `#new-group-form`, `#rename-form`, `#delete-form`, etc.).
   - Note the gunicorn flags from `render.yaml`.

2. **Inventory the specs**
   - Extract the full FA-ID list from Schritt 3 (note any explicitly removed IDs such as FA-07 / FA-08).
   - Extract the endpoint table from Schritt 6.
   - Extract the feature list F1..F5 from Schritt 2.
   - Note the actor list from the use case diagram.

3. **Build the diff** — present it as a single table:

   | Area | Spec says | Code does | Status | Recommendation |
   | ---- | --------- | --------- | ------ | -------------- |
   | …    | …         | …         | ✅ / ⚠️ / ❌ | update spec / update code / no action |

   One row per concrete divergence. Do not list matches.

4. **Check the hard invariants** (call them out explicitly if violated):
   - In-memory state ⇒ `--workers 1` in `render.yaml`.
   - Open Membership ⇒ no `members` set in `app.py`, no FA-07 / FA-08 in the specs, no member-management routes.
   - `/g/<gid>/state.json` is the single source of truth for the polling UI; every UI-visible field must originate there.
   - Owner-only routes (`/rename`, `/delete`) are protected by `require_owner`.
   - 404 handler redirects to `/`.

5. **Recommendations** — group into two lists:
   - **Update specs** (when code is correct, spec is stale).
   - **Update code** (when spec is correct, code drifted).

   For each item give: target file, one-sentence rationale, and a concrete edit sketch (the minimal patch — do not paste the full file).

6. **Stop.** Do **not** apply edits automatically. Wait for the user to confirm which recommendations to take.

## Out of scope

- Do not invent new features. Only document drift.
- Do not render diagrams; only consider the PlantUML source.
- Do not run git commands or commit anything.
- Do not start the Flask server.
