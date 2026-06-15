# Toy Agent — Phase 0.2

A ~minimal coding agent, implemented four ways, for the "understand the machine" session of the [learning plan](../../claude-code-learning-plan.md). Following Thorsten Ball's *[How to Build an Agent](https://ampcode.com/notes/how-to-build-an-agent)*.

The point of building it yourself: see that an agent is **an LLM, a loop, and a set of tools** — nothing more magical than that. Claude Code is this same loop with more tools and better context management.

## The loop (identical in all four implementations)

```
1. Send the conversation (+ tool definitions) to the model.
2. The model replies with text and/or "tool_use" requests.
3. If it requested no tools  -> print its text. The turn is done.
4. If it requested tools      -> run each one, append the results as a
                                 "tool_result", and GO BACK TO STEP 1.
```

That backward arrow in step 4 is the entire idea. The model can't touch your
files; it can only *ask* (a `tool_use` block), and your code decides what
actually happens (the `tool_result` you send back). You own the keyboard; the
model drives.

## The wire protocol (what step 1–2 actually exchange)

Request body to `POST https://api.anthropic.com/v1/messages`:

```jsonc
{
  "model": "claude-opus-4-8",
  "max_tokens": 16000,
  "tools": [ { "name": "read_file", "description": "...", "input_schema": {...} } ],
  "messages": [ { "role": "user", "content": "what's in agent.py?" } ]
}
```

When the model wants a tool, the response `content` contains a block like
`{"type":"tool_use","id":"toolu_…","name":"read_file","input":{"path":"agent.py"}}`
and `stop_reason` is `"tool_use"`. You run the tool and send the next request
with two more messages appended: the assistant's turn (echoed back verbatim)
and a user turn carrying
`{"type":"tool_result","tool_use_id":"toolu_…","content":"<file contents>"}`.
Loop until `stop_reason` is `"end_turn"`.

## Two SDK views, two raw-HTTP views

| Impl | How it calls Claude | Why |
|---|---|---|
| `python/` | Official `anthropic` SDK, manual loop | Clearest read of the loop |
| `csharp/` | Official `Anthropic` .NET SDK, manual loop | Typed/explicit; familiar |
| `fsharp/` | Raw HTTP + `System.Text.Json` | Functional (recursion); shows the wire protocol |
| `clojure/` | Raw HTTP + `clj-http`/`cheshire` | Lisp/REPL; shows the wire protocol |

The SDK versions hide the JSON; the raw versions show it. Read across them and
the invariant (the loop) stands out from the language noise.

## Tools (same two everywhere — both read-only and safe)

- `list_files(directory=".")` — list a directory.
- `read_file(path)` — read a file.

The agent can explore this repo and answer questions about it. It cannot write
or delete anything. **Exercise:** add an `edit_file` tool (string-replace or
create). That's the step in Ball's article where it starts to feel like a real
coding agent — and it's where you'll feel the weight of "the model is driving."

## Running

Set your key once: `export ANTHROPIC_API_KEY=sk-ant-...`

- **Python:** `cd python && uv sync && uv run agent.py` (uv creates the `.venv` and installs `anthropic`)
- **C#:** `cd csharp && dotnet run`
- **F#:** `cd fsharp && dotnet run`
- **Clojure:** `cd clojure && clojure -M -m agent`

Then ask it something like: `what files are in the python directory, and what does agent.py do?`

> Simplifications for clarity: `max_tokens` is 16000 (non-streaming, stays under
> SDK timeouts); extended thinking is left off so the loop is the only thing to
> follow. Real agents stream and usually enable adaptive thinking.
