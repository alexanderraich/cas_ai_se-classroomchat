# Schritt 7 — SWOT-Reflexion

Reflexion des Erlebten aus der Perspektive der **Organisation Swiss Re** zur Frage: *Was bedeutet die in dieser Übung praktizierte AI-gestützte Specification-Driven Development (SDD) für uns?*

Bezugsrahmen: GitHub Copilot in VS Code (kein Perplexity, da nicht im genehmigten Tool-Stack), iteratives Vorgehen über Schritte 1–6 (DDD → Feature-Katalog → Use Cases & Anforderungen → Quality Check → Mockup → Flask-Prototyp + Render-Deployment).

---

## SWOT-Matrix

|                | **Hilfreich (intern)**                                       | **Hinderlich (intern)**                                                      |
| -------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| **Stärken**    | Hohe Geschwindigkeit von der Idee zum lauffähigen Prototyp; konsistente Spec-Artefakte aus einem Fluss; Reduktion mechanischer Routinearbeit (PUML-Diagramme, FA-Tabellen, Boilerplate). | — |
| **Schwächen**  | — | Halluzinations- und Drift-Risiko in Spec-Artefakten; Über-Engineering tendenziell, wenn der Mensch nicht aktiv kürzt; Compliance-Hürden (welcher Tool-Stack ist genehmigt?). |
|                | **Hilfreich (extern)**                                       | **Hinderlich (extern)**                                                      |
| **Chancen**    | Verkürzung der Vor-Studien­phase; Demokratisierung von Software­design über Engineering hinaus (Fach­bereiche schreiben verifizierbare Specs); reproduzierbare Audits durch versionierte Artefakte. | — |
| **Risiken**    | — | Vendor-Lock-in (GitHub/Microsoft); Daten­abfluss bei unklaren Prompts; regulatorischer Druck (FINMA, EU-AI-Act) auf nachvollziehbare AI-Nutzung; Erosion von Engineering-Fertigkeiten bei zu starker Delegation. |

---

## Stärken (Strengths)

- **Time-to-Prototype dramatisch verkürzt.** Aus 0 wurden in einem Nachmittag: DDD-Modell, Use-Case-Katalog, FA-Tabelle (24 Anforderungen), Quality Check, interaktives Mockup, lauffähige Flask-App mit Live-Updates und Live-Deployment auf Render. Klassisch wären dafür Tage statt Stunden veranschlagt.
- **Konsistenz zwischen Artefakten.** Da PUML, Markdown-Specs und Code im selben Werkzeug entstehen, ist das Risiko inkonsistenter Schichten kleiner als bei Tool-Brüchen (Confluence ↔ Visio ↔ Jira ↔ IDE). Refactorings (Open-Membership-Pivot, FA-07/08-Streichung) wurden in einem Rutsch durch alle Schritte gezogen.
- **Mechanische Arbeit eliminiert.** Sophist-Schablonen-Sätze, FA→Implementation-Mapping-Tabellen, Boilerplate-Decorators (`@require_login` etc.) — Aufgaben, die Engineers normalerweise demotivieren, werden in Sekunden generiert.
- **Niedrige kognitive Hürde für Domain Experts.** Das DDD-Diagramm und die Cohn-User-Stories sind für Fachbereiche lesbar; AI kann Fachsprache in formale Anforderungen übersetzen.

## Schwächen (Weaknesses)

- **Halluzination & Spec-Drift.** Die AI generiert auch dann plausibel klingende Anforderungen, wenn der Kontext widersprüchlich ist. Ohne menschliches Review entstehen leicht „Phantom-Features", die in der Implementierung später als Bugs auftauchen (im Verlauf passiert: FA-07/08 wurden generiert, dann durch Open-Membership-Pivot wieder gestrichen).
- **Tendenz zur Über-Engineerung.** Erste Iterationen enthielten Threads, Reaktionen, Rollen, Anhänge — alles, was man als Messenger „kennt", aber nicht im MVP braucht. Aktiver Mensch musste konsequent zurückschneiden.
- **Compliance-Komplexität.** Tool-Stack ist organisations­seitig vorgegeben (Copilot ja, Perplexity nein). Das schränkt Methoden ein und zwingt zur Anpassung von externen Übungs­anleitungen. Datenklassifikation der Prompts ist heute oft unklar.
- **Wissens­transfer leidet.** Wer die Spec nicht selbst formuliert, internalisiert sie weniger — Risiko, dass Engineers nur noch „Reviewer" werden.

## Chancen (Opportunities)

- **Versicherungs­geschäft profitiert besonders** von formalen Anforderungen (FINMA-Audit, regulatorische Nachweise). AI-gestützte Sophist-Schablonen-Sätze + versionierte Markdown-Artefakte sind audit-freundlicher als unstrukturierte Confluence-Seiten.
- **Pilot-Programme im «kleinen Risiko»**: interne Tools, Hackathons, RFC-Drafts, PoCs. Hier ist die Geschwindigkeits­dividende sofort spürbar, das Risiko aber begrenzt.
- **Standardisierung von Spec-Workflows.** Wenn jede Abteilung dasselbe SDD-Schema (DDD → Features → UCs → FAs → Architecture) verwendet, sinken Onboarding-Kosten quer über die Organisation.
- **Demokratisierung**: Aktuare, Underwriter, Risk Officers können mit AI-Unterstützung selbst Anforderungs­dokumente erzeugen, die direkt in IT-Backlogs übergehen.

## Risiken (Threats)

- **Vendor-Lock-in.** Tiefe Integration mit GitHub Copilot bindet die Organisation an Microsoft-Cloud und -Vertragslogik. Strategie zur Multi-Provider-Fähigkeit (z. B. Anthropic, Mistral) sollte mitgedacht werden.
- **Datenabfluss / Vertraulichkeit.** Auch wenn Copilot-Enterprise keine Trainingsdaten ableitet — Prompts mit Tarif­logik, Kunden­daten, Verträgen sind sensibel. Klare Guardrails (DLP, Prompt-Klassifikation) zwingend.
- **Regulatorischer Wandel.** EU-AI-Act, FINMA-Erwartungen, Schweizer DSG-Revision. Die heute zulässige Nutzung kann morgen restriktiver werden — Architektur­entscheide müssen austauschbar bleiben.
- **Erosion von Software-Engineering-Kompetenz.** Wenn Junior-Engineers nie selbst Boilerplate schreiben, fehlt das Fundament für Debugging produktiver Systeme. Skill-Decay ist ein Mehrjahres-Risiko, nicht sofort sichtbar.
- **Verantwortungs­diffusion.** Wer haftet für eine fehlerhafte Spec, die AI generiert hat? Klärung von Roles & Responsibilities (Engineer = Owner, AI = Tool) muss vor Skalierung stehen.

---

## Handlungsempfehlungen für die Organisation

1. **SDD-Pilot-Programm** in einer abgegrenzten Linie (z. B. Internal Tools / Innovation Lab) mit klar definierten Erfolgs­metriken (Time-to-Prototype, Defect-Density, Audit-Readiness).
2. **Tool-Stack-Governance** verbindlich publizieren: welche AI-Werkzeuge dürfen mit welchen Datenklassen verwendet werden?
3. **Spec-Templates standardisieren** (DDD-PUML, FA-Tabelle in Sophist-Schablone, Mapping FA→Code). Versionierung in Git, nicht in Confluence.
4. **Reviewer-Disziplin trainieren**: Engineers werden geschult, AI-Output zu kürzen, nicht nur zu akzeptieren. „Bewusst-nicht-im-MVP"-Sektion ist Pflicht.
5. **Audit-Spuren mitdenken**: Welche Prompts haben welches Artefakt erzeugt? Reproducible-AI-Workflows (Prompt im Repo committen) als Standard.
6. **Multi-Provider-Strategie** vorbereiten, um Lock-in-Risiko zu mitigieren.

---

## Persönliches Fazit

Die Übung hat überzeugend demonstriert, dass AI-gestütztes SDD die Vor-Studien­phase eines Software-Vorhabens **um eine Grössenordnung** beschleunigen kann — bei gleichzeitig **höherer formaler Qualität** der Spec-Artefakte. Die Hauptarbeit verschiebt sich vom Schreiben zum **Kuratieren und Entscheiden**. Genau diese Verschiebung ist für eine traditionell schreibintensive Organisation wie Swiss Re Chance und Risiko zugleich: Wer das Kuratieren beherrscht, gewinnt; wer es delegiert, verliert die Kontrolle über sein eigenes Software­vermögen.
