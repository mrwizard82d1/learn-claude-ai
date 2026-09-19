# Architectural models & the interpretation lens

The diagram shows *structure*; the **lens** decides what that structure *means* — and
which edges are smells. Same picture, different verdict under different models.

## Three lenses (chosen in Protocol step 1; default = Unknown)

- **Named model** — user names the intended architecture. Evaluate the diagram against
  its invariant; flag every edge that violates it. State the invariant explicitly so
  the user can see *why* an edge is (or isn't) a smell.
- **Unknown (default)** — assume nothing. Describe the observed structure in plain
  terms (clusters, dependency direction, cycles, chokepoints). If there's no coherent
  pattern, SAY SO. This is the normal case for unfamiliar/legacy code.
- **Candidates** — propose the 1–3 known styles the code most resembles. For EACH:
  evidence for, evidence against, and a fit rating. Rank them. Include **"Ad hoc /
  Big Ball of Mud"** (Foote & Yoder) as a genuine candidate — sometimes it wins, and
  that is a useful, honest answer, not a failure.

## Named models — the invariant to check, and its smell

| Model | Core invariant | Smell to flag |
|---|---|---|
| **Layered / N-tier** | Deps point one way down the stack; no upward or skip edges | upward edge; layer-skipping; cycles |
| **Imperative Shell / Functional Core** | Core is pure & dependency-free; shell does I/O and calls inward (shell→core) | **core importing I/O / external / impure deps**; core depending on shell. (shell→core is HEALTHY here, even if it looks "upward") |
| **Hexagonal / Ports & Adapters** | Domain depends only on ports (interfaces); adapters depend on domain | domain importing a concrete adapter or external SDK directly |
| **MVC / MVVM** | View↔Model decoupled via Controller/ViewModel | View reaching into Model/data directly; fat controller |
| **Pipes & Filters** | Stages independent, connected only by data flow | a stage reaching around the pipe into another's internals |
| **Event-driven / pub-sub** | Producers/consumers decoupled via bus | direct producer→consumer calls bypassing the bus |
| **Plugin / microkernel** | Core knows only plugin contract | core importing a specific plugin |

## The key insight (from a real dry run)
The *same* edge can be healthy or a smell depending on the model. Example: an
interop-layer module importing a units module is a "wrong-way / cycle" under **strict
layering**, but under **Imperative Shell / Functional Core** it's the *expected*
shell→core direction. So always evaluate against the model the user actually intends —
and when they don't know, offer candidates rather than assuming a strict stack.

## Discipline
Do not confabulate. Under Candidates, projecting a clean style onto messy code is the
failure mode. Evidence both ways, rank by fit, and report the **drift** between
intended and actual — that gap is usually the most valuable finding.
