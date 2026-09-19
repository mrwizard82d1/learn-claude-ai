# Rendering PlantUML to an image (and the gotchas)

The deliverable is a **picture the user can see**, not `.puml` text. Render it and show
the PNG.

## Command
```
plantuml -tpng file.puml      # → file.png next to it
```
- Needs **Java**. Class/component/package/state/deployment diagrams also need
  **Graphviz (`dot`)**; sequence & activity do not.
- Render locally — do NOT send the code's structure to a public PlantUML server.
- Put outputs in a gitignored working dir if the input/repo is untracked.
- After rendering, DISPLAY the PNG to the user (read/attach it). If `plantuml` exits
  non-zero, it prints `Error line N` — fix and re-render before showing anything.

## Gotchas — write render-SAFE PlantUML the first time
These each cause a hard parse error (often reported on the *next* line, or on a
participant's first *use* rather than its declaration — so the reported line can
mislead):

- **No `__double_underscores__` in labels/names** — `__` toggles creole underline and
  breaks parsing. Write `init`/`ctor` instead of `__init__`; if you must show it,
  escape or reword.
- **No arrow-like tokens inside label text** — `->`, `<-`, `-->` inside a message or
  edge label confuse the parser. Reword ("calls", "then", "to").
- **No `\n` in a single-line note** — `note over X : a\nb` is malformed. Use a block:
  ```
  note over X
    line one
    line two
  end note
  ```
- **Keep participant/component NAMES simple** — avoid `\n` combined with leading
  punctuation like `/`, `(`, `[` inside a quoted name (e.g. `"Foo\n/ Bar"` fails, and
  the error surfaces at the name's first use, not its declaration). Prefer a plain
  single-line name; convey extra detail with a `note`.
- **Prefer ASCII** in labels; fancy dashes/quotes are usually fine but not worth the
  risk when a render is blocking.
- Color syntax on edges is `-[#red]->` / `.[#red].>`, not `--> #red`.

## Confidence marks (carry through to the image)
Solid = observed, dashed = inferred; always include the legend block. See the per-view
reference files for the exact arrow syntax.
