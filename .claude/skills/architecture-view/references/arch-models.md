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

## Evidence profile (quantifying the Candidates lens)

When the user wants weights, express them as an **evidence profile computed from the
edge inventory** — never as a conjured probability. The number must trace to counts.

**How to compute**
1. Take the **N observed** dependency edges from the inventory, **within the confirmed
   scope only** (see `discovery.md` — peripheral executables skew N). Handle inferred
   edges separately — don't let guesses drive the number.
2. Classify each edge by which candidate model's invariant it is *consistent with* and
   which it *violates*. An edge may support more than one model. An edge that violates
   *every* candidate's invariant counts toward **mud** (ad hoc / cross-cutting).
3. Report each bucket as `X of N edges`, then normalize to a percentage.

**Presentation (example — always show the counts, not just %):**
```
Evidence profile (from 20 observed edges — NOT a probability):
  Layered / inward      14/20  (70%)
  Client-server seams    2/20  (10%)
  Mud / cross-cutting    4/20  (20%)   <- violate every candidate
  (ambiguous edges counted toward >1 model: 3;  inferred edges excluded: 5)
Read: predominantly layered, with real client-server seams and a 20% mud pocket.
```

**Honesty rules**
- Label it **"evidence profile," not "probability" / "posterior."** Edges are not
  independent, so do NOT multiply likelihoods into a Bayesian number — that is false
  precision. The `%` is only a normalized count.
- Always show raw `X of N` beside any percentage.
- It is **debatable and updateable** (the honest part of the Bayesian spirit): the user
  can dispute an edge's classification or add edges, and the profile recomputes. Invite
  that revision explicitly.
- If most edges are mud, say the code is largely ad hoc — let mud win.

**Bonus reading — change difficulty.** The mud / cross-cutting fraction is a proxy for
coupling: the more edges violating every clean invariant, the more the code resists
*localized* change (each is a potential Chesterton's fence / wider blast radius). So the
profile doubles as a rough "how hard is change here" gauge, not just a style label —
which is exactly what a maintainer sizing a task wants.

## Discipline
Do not confabulate. Under Candidates, projecting a clean style onto messy code is the
failure mode. Evidence both ways, rank by fit, and report the **drift** between
intended and actual — that gap is usually the most valuable finding.
