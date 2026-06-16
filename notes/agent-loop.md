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

---

<!-- Session 0.3 will add a second section here: mapping these mechanics
     onto Claude Code features (CLAUDE.md, /clear, /compact, subagents). -->
