# Classroom Chat — SDD-Übung (CAS AI SE)

Klassenraum-Messenger als Lernprojekt für **Specification-Driven Development** (SDD).
Aufgabenstellung: [spec/03 SDD Aufgabenblatt.pdf](spec/03%20SDD%20Aufgabenblatt.pdf).

## Status

| Schritt | Inhalt | Status |
| ------- | ------ | ------ |
| 1 | DDD-Domänenmodell (Klassendiagramm) | ✅ [diagrams/domaenenmodell.puml](docs/diagrams/domaenenmodell.puml) |
| 2 | Feature-Katalog (F1–F4) | ✅ [schritt2-feature-katalog.md](docs/schritt2-feature-katalog.md) |
| 3 | Use Cases & funktionale Anforderungen (FA-01..FA-17) | ✅ [schritt3-use-cases.md](docs/schritt3-use-cases.md) |
| 4 | Requirements Quality Check (final FA-01..FA-20) | ✅ [schritt4-quality-check.md](docs/schritt4-quality-check.md) |
| 5 | HTML-Mockup mit simuliertem Verhalten | ✅ [mockups/index.html](docs/mockups/index.html) |
| 6 | Code-Generierung & Render-Deployment (TRL4) | ⏳ offen |
| 7 | SWOT-Reflexion | ⏳ offen |

## Repo-Struktur

```
docs/
├── schritt2-feature-katalog.md
├── schritt3-use-cases.md
├── schritt4-quality-check.md
├── diagrams/
│   ├── domaenenmodell.puml      # PlantUML
│   ├── domaenenmodell.png       # gerendert
│   ├── use-case-diagramm.puml
│   └── use-case-diagramm.png
└── mockups/
    ├── index.html               # Single-File-Mockup, alle UCs
    └── style.css
spec/
└── 03 SDD Aufgabenblatt.pdf
```

## Lokal ausprobieren

**Mockup**: `docs/mockups/index.html` direkt im Browser öffnen oder über die VS-Code-Extension *Live Preview*.

**Diagramme rendern** (benötigt PlantUML + Graphviz):

```sh
brew install plantuml graphviz   # einmalig
plantuml -tpng -o "$PWD/docs/diagrams" docs/diagrams/*.puml
```

## Tooling

- VS Code + GitHub Copilot (firmen-approved) — für SDD-Generierung & Reviews
- PlantUML — Diagramme
- Schritt 6 (geplant): Python · Flask · Gunicorn · GitHub · Render.com

## Lizenz

Lernprojekt im Rahmen des CAS AI SE — keine produktive Nutzung vorgesehen.
