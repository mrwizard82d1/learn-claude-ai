# Using AI on existing / legacy code — a working model

> Phase 1 side-note (2026-09). Grounded in Michael Feathers, *Working Effectively
> with Legacy Code* ("legacy code = code without tests"). Sparked by real bugs:
> changes I thought "looked good" that other developers and a client found wrong
> (later confirmed by Claude). Most of my day-to-day is maintaining existing,
> sometimes-bad code — not greenfield — so I need a model for *that*.

## Why my "looked good" changes went wrong (the diagnosis)

Explained entirely by the Phase 0 mental model:
- **The amnesiac can't see the whole system.** On greenfield, code and intent are
  built together in context, so the model's picture matches the code. On legacy,
  the real system ≫ the context window; the model sees only the slice it read and
  **confabulates the rest**.
- **Legacy code is dense with invisible invariants** — implicit coupling,
  load-bearing weirdness, a Chesterton's fence every few lines. The agent makes a
  *locally plausible* change that violates an invariant it never saw.
- **On legacy, plausibility ≠ correctness** — precisely because the invariants are
  invisible. "Looks good" is the confabulation trap, for the model *and* for me.
- **No tests = no red/green net.** I shipped on "looks good"; my teammates and the
  client became the test suite — late, expensive feedback. (That Claude *confirmed*
  the errors afterward is the tell: the error-finding worked; I applied it too late.)

## Reframe: AI isn't worse at legacy — its use *shifts*

The bottleneck on legacy was never typing new code; it's **understanding** an
opaque system and **verifying** I didn't break it. AI helps with *both* — if I
point it at comprehension and characterization, not just "make the change." The
failure is using a greenfield reflex ("agent, implement X") on a brownfield problem.

## The loop — Feathers' change algorithm, AI-accelerated

The inversion: spend the agent's speed on **understanding and characterizing**, not
just changing.

1. **Understand first — AI as archaeologist (read, don't write).** Before touching
   anything, have the agent map the change area: what it does, callers/callees,
   the invariants it assumes, the blast radius. Make the invisible invariants
   **explicit**. (This is "explore," weighted heavily because the system pre-exists.)
2. **Characterize — AI writes characterization tests** that capture what the code
   *actually does now* (quirks included). Highest-leverage AI use on legacy: it
   converts "code without tests" → "code with tests" in minutes. **Now there's a net.**
   - *Caveat (from the Phase-2 "TDD & AI gap" read):* AI writes tests that merely
     *confirm* the code and skip the "red." For characterization that's the goal —
     **but I must review that the pinned behavior matches reality and decide which
     behaviors are intended vs. latent bugs.** A blindly-accepted characterization
     test locks a bug in as "expected." This judgment is irreducibly mine.
3. **Change small, behind the net.** Prefer Feathers' *additive* moves — **sprout
   method/class, wrap method/class** — which add code rather than edit untested code
   in place, minimizing risk. The tests catch regressions immediately.
4. **Verify against the net, not "looks good."** Green tests are the acceptance
   criterion. "Looks good" is banned — it's the exact trap that burned me.
5. **Shift error-finding left — adversarial review as a pre-merge gate.** The review
   that caught the errors *after* shipping becomes a *before* gate: a separate
   reviewer pass (a review subagent — Phase 3) checks the diff against the invariants
   surfaced in step 1. I then review a *tested, characterized* change, not raw
   plausibility.

## Orientation — "walking the codebase" with Claude (expands step 1)

My proven manual method for an unfamiliar codebase: run the app (asking domain
experts about inputs/expected results), step through in a debugger, and build a
mental "picture" before siting changes. Slow, but grounded in observed reality.
Here's how to emulate it with Claude — with honest limits. It buys four things;
Claude maps onto each differently.

**1. Structural map — Claude's home turf (big speedup).**
- *Narrated tour:* point it at an entry point (`main`, a request handler, a CLI
  command) and have it walk me through the control flow — the debugger-walk done
  *statically* by following code paths.
- *Fan-out mapping (subagents):* "map these N modules in parallel — each:
  responsibilities, key public functions, dependencies." Distilled overview, cheap.

**2. Dynamic / runtime picture — the crucial nuance (what the debugger gave me).**
The amnesiac reads static text; it does **not** execute the program in its head, so
it can be confidently wrong about control flow. Claude doesn't replace the debugger;
it supercharges the loop around it. Everything runtime must be **made legible as
text**:
- *Have Claude run it:* Claude Code can execute the app / test suite / scripts and
  read the output — "run with input X; tell me what it returns and what the logs
  show."
- *Instrument:* add temporary logging, or write a characterization test that
  exercises a path, run it, read the *actual* values — the AI analog of watching
  variables. (A characterization test is a controlled dynamic probe, and doubles as
  the safety net.)
- *Real debugger, assisted:* for the gnarliest bits I still step through; Claude
  helps decide where to break and turns observations into an updated model. Limit:
  it can't watch a live debugger session unless I paste the state in.

**3. Domain / intent — Claude cannot replace the experts (but reshapes the ask).**
It doesn't know the business or *why*, and will confidently *guess* intent
(dangerous). So "ask the people who know" stays irreplaceable — but do the
static+dynamic pass first, then have Claude generate **targeted** questions for the
humans (not a blank stare). And mine what it *can* read: `git log`/blame, commit
messages, PRs, issues, comments — reconstructs a lot of "why" without a human.

**4. Change-siting** falls out once the above is done (seams, blast radius).

**The improvement over the old method:** build the picture in a **durable external
artifact**, not just my head (which decays). The target output is `notes/
orientation.md` → seeds the repo's `CLAUDE.md` → the persistent briefing for the
amnesiac. The "feel" becomes a committed asset.

**The discipline:** Claude's tour is fluent and confident, which makes a subtly
wrong summary *more* seductive than a debugger slog. Treat its architectural
narrative as a **hypothesis to confirm against running behavior and tests**, not as
ground truth. Trust, but verify against what actually executes — that keeps the
grounding the debugger gave me while shedding the tedium.

**The protocol:**
1. Point Claude at the repo → top-level map (entry points, major modules, how to
   run/test). Fan out with subagents if large.
2. Pick one real user-facing behavior with a known input/expected output (from an
   expert). Have Claude trace it end-to-end statically **and** run it (or a
   characterization test) to confirm the trace against reality.
3. Where static ≠ observed, or it's gnarly → instrument (logging / test) or
   debugger; feed observations back.
4. Have Claude generate targeted questions → ask the humans → capture answers.
5. Externalize into `notes/orientation.md` (seeds `CLAUDE.md`); record seams,
   invariants, open questions.
6. Site the change — with a mapped system and a test net.

## Context management (legacy ≫ context window)

- **A `CLAUDE.md` for the legacy repo is the highest-value artifact** — encode the
  non-obvious invariants, architecture, and "here be dragons" so the standing
  briefing compensates for the model's blindness to the wider system. (⇒ do the
  Phase-1 `CLAUDE.md` exercise on a *legacy* repo I maintain.)
- **"Read before you assert."** Make the agent read the change point + its
  dependencies + existing tests before proposing edits — no acting on confabulation.
- **Subagent fan-out for impact analysis:** "which of these modules touch X, and
  how?" — bounded, distilled, low-attention archaeology.

## Caveats
- AI can **lock in bugs** via unreviewed characterization tests — the intended-vs-bug
  call is mine.
- On bad code, plausible refactors can shift behavior *subtly* → tests-first is
  non-negotiable.
- This is **more disciplined than greenfield vibe-coding, not less** (suits me, and
  Uncle Bob).

## How this fuses the plan
Phase 0 (why the amnesiac confabulates) · Phase 2 (TDD / characterization discipline)
· Phase 3 (review subagents) · the `CLAUDE.md` exercise — all applied to my actual
daily job. Reference: Michael Feathers, *Working Effectively with Legacy Code*.
