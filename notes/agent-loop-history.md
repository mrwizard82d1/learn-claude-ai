# agent-loop.md — revision history (Phase 0, Session 0.1)

A reconstructed record of how my answers to the three loop questions evolved
across one working session (2026-06-16), from first draft to final. The final
version lives in [`agent-loop.md`](./agent-loop.md); this file captures the path.

**Provenance & fidelity.** git never saw v1–v4 (the note was uncommitted and
each revision overwrote the last in place). These versions were recovered from
the working session's transcript: v1 from the edit diff, v2–v5 from full file
reads. They are reproduced **verbatim, typos included** ("he user's",
"no requests information from tools", etc.) — the raw progression, not a
cleaned-up one. From here on, git is the versioning system; this file is a
one-time backfill of what predated the first commit.

---

## v1 — first draft

**Q1. Exact steps of one iteration:**
> The agent loop performs three steps (and some details like textual prompts to clarify things).
> - Read the text submitted.
> - Submit the text to the LLM
>   The text submitted to the LLM includes all the previous "context" of the LLM: all previous submissions and responses.
> - Display the "answer" presented by the LLM in response to the text submitted.

**Q2. Where a tool call fits:**
> The tool call is requested by the agent based on text found in the prompt and its own "reasoning" based on the description of the tool.

**Q3. What ends the loop:**
> The turn is finished when the agent presents its findings to you by printing text in response to the previous prompt and all the context known to the agent.

**Strong:** caught statelessness/context-replay (every call re-sends the whole history).
**Gap:** describes a *chat* loop (read → LLM → display), not an *agent* loop — no inner tool-call loop, and the model/harness division of labor is absent.
**Feedback that drove v2:** watch "whose code does what." Three questions: after the model requests a file, what happens *before* anything is displayed? Who executes the tool and how does the result re-enter? Can text and a tool request share one response?

---

## v2 — "edited pretty significantly"

**Q1:**
> The agent loop performs three steps (and some details like textual prompts to clarify things).
> - Read the text submitted.
> - Submit the text to the LLM
>   The text submitted to the LLM includes all the previous "context" of the LLM: all previous submissions and responses.
> - Loop over
>   - Ask a question to clarify the user's request (Is this an agent in operation?)
>   - Ask an agent to use a tool available to help answer he user's request
>   - Repeat while not finished and then display the complete answer

**Q2:**
> The agent requests a tool call based on text found in the prompt and its own "reasoning" based on the description of the tool. In response the tool performs its task and submits a textual response back to the agent who, in turn, returns that response to the model.

**Q3:**
> The turn finishes when all agents have responded to the model, and the model has synthesized all these responses into a coherent answer to the original prompt with the clarifications made by the user.

**Strong:** found the inner loop ("Loop over … repeat while not finished"); Q2 now has the execute-and-feed-back round trip.
**Gap:** introduced multiple "agents" (tools described as agents responding to the model) and used "agent" for two different things.
**Feedback that drove v3:** tools are not agents/minds — they're plain functions (`read_file`, `list_files`); one model, one loop. Pin terminology: *agent* = the whole program, *model* = the LLM inside it, *harness* = the code that executes tools. (Multi-agent orchestration is real but is a Phase 3 topic.)

---

## v3 — tools, not agents

**Q1:**
> The agent loop performs three steps (and some details like textual prompts to clarify things).
> - Read the text submitted.
> - Submit the text to the model
>   The text submitted to the model includes all the previous "context" of the model: all previous submissions and responses.
> - The agent loops over
>   - Invoke a single tool to gain additional information
>   - Submit that information to the model
>   - Repeat while the model is not finished and then display the complete answer

**Q2:** *(unchanged from v2)*
> The agent requests a tool call based on text found in the prompt and its own "reasoning" based on the description of the tool. In response the tool performs its task and submits a textual response back to the agent who, in turn, returns that response to the model.

**Q3:**
> The turn finishes when all agents have responded to the agent, and the agent has synthesized all these responses into a coherent answer to the original prompt with the clarifications made by the user.

**Strong:** `LLM` → `model`; "Invoke a single tool" replaces "Ask an agent"; the agentic inner loop is clean.
**Gap:** Q3 is still tool/agent-centric ("all agents responded … agent synthesized") — implies a fixed set of helpers we wait on, and a separate "synthesis" step.
**(Also raised the broad question: "Is the LLM just another tool specializing in natural language?")**
**Feedback that drove v4/v5:** the terminator is *model-centric*. There's no fixed set to wait on; the model decides each step. The single condition the harness checks: does the model's latest reply contain a tool request? No request = done. There's no separate synthesis step — the final answer is just the reply with no tool call in it.

---

## v4 — Q3 reworked (Q1 & Q2 unchanged from v3)

**Q3:**
> The turn finishes when all tools have supplied responses to the agent, and the agent has used the model to synthesize all these responses into a coherent answer to the original prompt (possibly with additional clarifications).

**Strong:** dropped the plural "agents"; "used the model to synthesize" treats the model as a component.
**Gap:** still tool-centric ("all tools have supplied responses") — implies waiting on a known set rather than looping as long as the model keeps asking.
**Feedback that drove v5:** flip to the harness's binary check — *does the reply contain a tool request?*

---

## v5 — final (Q1 & Q2 unchanged from v3)

**Q3:**
> The turn finishes when the model's latest reply contains no requests information from tools. This could occur early if the model needed no tools, it may occur after consulting all tools, or it may occur after consulting some tools. (And prompting the user for additional information feels like "yet another tool.")

**Landed.** The terminator is now model-centric and precise: the loop ends on the reply that contains no tool request. The early/all/some elaboration shows there's no fixed set to wait on. The parenthetical is a genuine insight — asking the user can itself be modeled as a tool (real systems implement it exactly that way), so the dichotomy holds: everything the model emits is either final text or a tool request.

**Session 0.1 complete.** All three landed: statelessness/context-replay (Q1), request → execute → feed-back (Q2), model-decides-to-stop (Q3).
