# The agent loop — my notes

> Phase 0, Session 0.1. Written after reading Thorsten Ball,
> *How to Build an Agent* (https://ampcode.com/notes/how-to-build-an-agent).
> Goal: articulate the mechanism in my own words, not copy the article.

## 1. What are the exact steps of one iteration of the loop?

<!-- 3-6 lines. What goes in, what comes back, what happens next? -->

The agent loop performs three steps (and some details like textual prompts 
to clarify things).

- Read the text submitted.
- Submit the text to the model
  The text submitted to the model includes all the previous "context" of the model: 
  all previous submissions and responses.
- The agent loops over
  - Invoke a single tool to gain additional information
  - Submit that information to the model
  - Repeat while the model is not finished and then display the complete answer

## 2. Where does a "tool call" fit?

<!-- Who requests it, who executes it, how does the result re-enter? -->

The agent requests a tool call based on text found in the prompt and 
its own "reasoning" based on the description of the tool. In response the 
tool performs its task and submits a textual response back to the agent who,
in turn, returns that response to the model.

## 3. What ends the loop?

<!-- What signal tells you the turn is done? -->

The turn finishes when the model's latest reply contains no requests 
information from tools. This could occur early if the model needed no tools, 
it may occur after consulting all tools, or it may occur after consulting 
some tools. (And prompting the user for additional information feels like 
"yet another tool.")

---

## Broader reflections — is the LLM "just another tool"?

*A question I raised mid-session, with the resolution we reached.*

**The question.** Is the LLM just another tool — one specializing in understanding
and producing natural language — that consumes text from the user and from other
tools and synthesizes the next answer in the conversation?

**What's right about it.** The symmetry is real: tool results re-enter the
conversation as ordinary text the model reads like anything else. From the
model's side there is no special "tool channel" — user text, tool output, and
prior replies are all just tokens in the context it consumes. (Same statelessness
insight as Q1; it's the foundation of Phase 1 — managing context is the game.)

**Where it breaks: control.** Tools are passive — they run only when called and
decide nothing. The model is the *only* component that decides what happens next:
whether to call a tool, which one, with what arguments, or to stop. The LLM isn't
a peer among the tools; it's the decider they're wired around. (Which is also why
the loop ends when the *model* stops asking — agency lives there.)

**The truer inversion.** It's the other way round: the tools are the *model's*
tools. The model is a brain in a vat — it can read and emit text but cannot touch
a file, run a command, or see a result. The harness gives it hands (tools that
act) and feeds back senses (results as text). It decides but cannot act; the
harness acts but does not decide. ("AI drives the keyboard, I own the thinking" —
made literal, roles reversed from the human version: the model supplies intent,
my code is the actuator.)

**One refinement.** "Specializes in natural language" undersells it. It also emits
structured output (the tool request with its arguments), and its real specialty
isn't language per se but *choosing the next move, expressed as tokens*. Language
is the medium; deciding is the function.

### The expert analogy

I also tried: the model is like an expert who draws on her knowledge, may ask me
to clarify, and may consult specialized expertise. Apt in that it centers the
model as the reasoner/decider — but it misleads in three ways, and each is a
Phase 1 lever:

1. **Tools aren't consulted experts; they're instruments.** A human expert
   consults another *mind*. `read_file` is not a mind — it reasons about nothing.
   Most tools are the expert's reference book, lab test, or telephone: they fetch
   a fact or perform an act, supplying no judgment. (Consulting an actual
   specialist *is* a real pattern — a sub-agent, another instance of the same
   brain — but that's Phase 3, and even then it's exposed to the orchestrator
   *as a tool*.)
2. **The expert remembers; the model is an amnesiac.** A real expert accumulates
   understanding across the conversation. The model retains nothing — every turn
   it is re-handed the entire transcript. The honest picture is a brilliant
   amnesiac who must be re-briefed with the whole case file before every question.
3. **The expert can act; the model cannot.** She can walk to the shelf herself.
   The model can only instruct an assistant (the harness) and react to what comes
   back.

**Refined analogy:** a brilliant, broadly-knowledgeable consultant who is
(a) amnesiac between every exchange — re-read her the full file each time;
(b) unable to act — she only directs an assistant; and (c) working from stale,
sometimes-confabulated memory — which is *why* you hand her instruments, so she
reads the actual current file instead of recalling what it used to say.

**Why this matters.** The three places the analogy breaks are exactly where the
engineering lives:
- Managing the amnesiac's case file → context engineering (`CLAUDE.md`, `/clear`, `/compact`).
- Choosing her instruments → tool design.
- Grounding her stale memory in reality → why agentic coding reads real files instead of trusting recall.

Phase 1, in a sentence: learning to be a good handler for a paralyzed, amnesiac genius.

### The REPL / trampoline analogy (a Lisp framing of the same thing)

I also tried: the agent loop is the **read–eval–print loop** of a Lisp
interpreter — except `eval` isn't just reducing a form in the interpreter's
environment; it has an "out" to seek more information, from the human or from
tools. That framing is apt (the outer loop *is* a REPL; the conversation *is* the
persisting environment), but three refinements make it sharper:

1. **The "out" isn't an escape hatch — it's `eval`'s normal return.** `eval`
   returns one of two kinds of result: a *value* (final text → print) or a
   *request* ("perform this effect, then call me again"). An ordinary return,
   not a `condition`/non-local exit. (And since asking the human is just another
   tool, both "outs" are the same mechanism: request an effect from outside.)
2. **`eval` is delegated to a stochastic oracle, not computed by the
   interpreter.** A Lisp REPL applies fixed reduction rules deterministically.
   Here the harness evaluates *nothing* — it hands the whole environment to the
   model and asks *it* what to do next. The evaluator is external and
   non-deterministic; the harness is a dumb dispatcher.
3. **The environment is threaded explicitly, because the evaluator is amnesiac.**
   Not a mutable environment held inside the interpreter — the entire
   conversation is re-passed on every `eval` and the extended conversation comes
   back. Pure state-passing (`eval : Env → (Result, Env)`), closer to a fold than
   to a stateful REPL.

**The construct underneath it is a trampoline.** "Returns either a value or a
request to continue" is exactly `clojure.core/trampoline`: call `f`, and while
the result is a function (a "bounce"), keep calling; stop when it's a plain
value. Map it — a **tool request** is a bounce (do the effect, re-enter `eval`);
**text with no tool** is the value (stop, print). That *is* the inner loop, and
it restates the Q3 terminator in one line: **the loop ends when `eval` returns a
value instead of a bounce.** So there are two nested loops — the **outer** REPL
(per human turn) and the **inner** trampoline (per `eval`, until a value).

**And the effects have a name:** the model only *describes* effects ("read this
file"); the harness *performs* them. That's functional-core / imperative-shell
(or, heavier: a free monad — the model emits effect descriptions, the harness is
the interpreter that runs them). The pure decider proposes; the impure shell
disposes — the brain-in-a-vat point again, in FP vocabulary.

**Refined statement:** the agent loop is a REPL whose `eval` is delegated to a
stochastic oracle, threaded over an explicit (stateless) environment, structured
as a trampoline that bounces on effect-requests and halts on a value — with
effects pushed out to an imperative shell.

### Capstone — there is no evaluator; the "decision" is emergent

The tempting picture: the model has a *goal* (produce a definitive answer) plus a
*criterion* that checks "good enough yet?", and that check decides tool-call vs.
stop. **No such module exists.** The model is a next-token predictor: given the
whole context, it generates the most probable continuation, token by token.
Emitting a tool request is just generating tokens that form a tool-use block;
"answering" is generating text with *no* tool-use block. Tool-vs-stop isn't
decided by an internal critic — it **emerges** from the same generation that
produces every other token.

- **Probabilistic vs. binary.** The generation is probabilistic (sampling a token
  distribution — no threshold, no gate). The only **binary 0/1** in the system is
  the *harness's* structural check on the output: "reply contains a tool request?
  y/n." The decision I keep intuiting is real, but it lives in the dumb harness,
  not as a judgment inside the model.
- **No notion of correctness.** The model can stop, confidently, on a *wrong*
  answer. Stopping ≠ correctness (the confabulation point).
- **Blackboard contrast.** A blackboard architecture puts the intelligence in a
  *control/scheduler* that decides which knowledge source runs and whether the
  solution is complete. The agent loop puts the intelligence in a single
  knowledge source (the model) and makes control trivial. (Multi-agent
  orchestration — Phase 3 — is closer to a real blackboard.)
- **Multiple questions.** No AND operator, no completeness checker; coverage of a
  multi-part prompt is *emergent, not guaranteed* → structure the request
  (enumerate) and verify coverage yourself.

Reframe: the model's "function" isn't *"can I answer?"* (evaluation) but *"what's
the next token?"* (generation). An answer or a tool-request emerges from that.

### It's tokens all the way down (the mechanistic floor)

The whole engine is next-token prediction — autoregressive: predict a distribution
over the *single* next token, sample one, append, repeat, each token conditioned on
all prior tokens (including the ones just emitted). The model never plans a whole
output atomically; even a tool call is built token by token.

**A tool call is not a different mechanism** — it's the same generation emitting
tokens in a *structured shape*: a tool-use block (name + arguments) instead of
prose. Same predictor, same token stream, different serialization. (So it's not a
"condensation" of a thought — just output in a structured format rather than a
paragraph.)

**Why it produces that format, and only when apt** — two ingredients, both just
more tokens to condition on:
1. **Training** — the model was trained on tool-use, so "emit a tool-use block in
   this format when the context calls for it" is baked into the weights.
2. **The tool schemas are in the context** — every request includes the tool
   names, descriptions, and argument schemas. Prediction is conditioned on *"here
   are the tools and what they're for."* This is why tool descriptions carry so
   much weight (the tool-design lever): they're literally part of the input the
   next token is computed over.

So the "mini language" is a **learned serialization protocol**: the model was
trained to *write* it (tool-use blocks) and *read* it (schemas, results); the
harness *parses* and *acts* on it.

**The round trip is tokens too.** When the model finishes a tool-use block,
generation pauses (`stop_reason: "tool_use"`). The harness parses it, runs the
tool, and appends the result back as more tokens (a `tool_result` block). Next
round, the model resumes doing the only thing it does — predict the next token —
over a context that now contains the result. Nothing is injected into the model's
"mind"; the result is just text appended to the growing sequence.

**Unifying picture:** input tokens (system + tool schemas + conversation + tool
results) → the model predicts output tokens (prose and/or tool-use blocks) → the
harness parses any tool-use tokens, executes, appends result tokens → repeat. One
growing token sequence that *both* the model and the harness write into, marked by
roles (user / assistant / tool). Tool-calling isn't an exception to "predict the
next token" — it *is* that, emitting tokens in a structured sub-format the harness
recognizes and acts on. No second mechanism under the hood.

---

## Session 0.3 — Claude Code features as context management

*Read: Anthropic, "Effective context engineering for AI agents." The point: the
context window (everything the model sees each turn) is a **finite** resource
that **degrades** as it fills ("context rot"). Since the model is a stateless
amnesiac conditioned on the whole window every turn, curating that window isn't
tidiness — it's steering. Each Claude Code feature below is a control for doing
that.*

Feature → the context problem it solves → how:

- **`CLAUDE.md`** — *Problem:* the amnesiac forgets my conventions/architecture
  every turn, and I don't want to re-type them each session. *How:* a file the
  harness auto-injects into the window on **every** turn — a standing briefing
  that survives the amnesia. *Caveat:* always-on means it always consumes window
  space and attention, so keep it **high-signal**; a bloated `CLAUDE.md` is itself
  pollution.
- **`/compact`** — *Problem:* the conversation only grows (full history re-sent
  every turn) and the window is finite. *How:* replaces the long history with a
  shorter summary — lossy compression to keep the gist and free room.
- **`/clear`** — *Problem:* the current context has become stale/tangled/off-track
  and is degrading outputs (rot). *How:* discards the whole conversation for a
  clean window. (Contrast `/compact`: clear **throws away**, compact **summarizes
  and keeps**. `CLAUDE.md` survives a clear — it's re-injected.)
- **`/rewind`** — *Problem:* recent turns or edits went wrong, but an earlier
  state was good, and I don't want to nuke everything. *How:* back up to an
  earlier **checkpoint**, undoing the conversation (and optionally file edits)
  after it. git-reset / undo for the session.
- **subagents** — *Problem:* a big, noisy sub-task (dozens of file reads, dead
  ends) would flood my main window with junk. *How:* run it in a **separate
  context window**; only a distilled result returns to the parent. Context
  **isolation** — quarantine the noise.

**Synthesis — one resource, three kinds of move.** These aren't a random toolbox;
they're all answers to the essay's single question — *the window is finite and
degrades, so control what's in it*:

| Move | Features |
|---|---|
| Inject good context, persistently | `CLAUDE.md` |
| Manage a full / rotting window | `/compact` (compress) · `/clear` (wipe) · `/rewind` (roll back) |
| Prevent pollution up front | subagents (isolate noisy sub-work) |

**The 0.3 payoff:** once I saw the loop as "a stateless model conditioned on a
finite, degrading window," each of these features stopped being an arbitrary
command and became an obvious *consequence* of the mechanism. Phase 0 goal met —
I understand the tool from the mechanism up.
