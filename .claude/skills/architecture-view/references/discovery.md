# Discovery — entry points & IPC seams (what static imports miss)

Run this FIRST for whole-system / "I don't know the architecture" (Unknown or
Candidates) scope, and ideally from a FRESH session — a prior *localized* query anchors
the model's altitude and can hide system-level structure (e.g. a second executable).

## 1. Enumerate ALL entry points / executables — never assume one .exe
Find every runnable root:
- `.csproj` with `<OutputType>Exe</OutputType>` or `WinExe` (each = a separate process)
- every `static ... Main(` / `Program.Main`
- Windows services (`ServiceBase`), `Worker` / `BackgroundService` hosts
- multiple startup projects in the `.sln`; scheduled tasks / CLI tools

A solution with N executables is **N processes** — map them as separate top-level nodes,
not one blob.

## 1b. Triage the entry points — then CONFIRM scope before building
Enumeration is for **recall** (find them all); scoping is for **precision** (keep the
right ones). Do NOT treat every executable as part of the architecture — over-including
peripheral tools is as wrong as missing a core one.
- Classify each as likely **core** (participates in the product's runtime / IPC graph —
  the WCF mesh, shared domain assemblies) or likely **peripheral** (a standalone utility:
  installer, db-migrator, dev/benchmark tool, test host, one-off script).
- Give the **signal** for each call; don't just assert it.
- **Present the list and ask the user to confirm scope before drawing.** "Is this part of
  the core product?" is domain knowledge in their head (like an IPC boundary) — never
  silently include a red herring nor silently drop a real one.
- Compute the **evidence profile over the CONFIRMED scope only.** Peripheral executables
  don't just add nodes — they skew the `X of N` counts and the layering/candidate read,
  perturbing the whole assessment. Lock scope first, then count.

## 2. Hunt IPC / integration seams — these have NO static import edge
Separate processes are joined by **contract + config resolved at runtime**, so an
import-following sweep will not see the edge. Search for the markers:
- **WCF**: `[ServiceContract]` / `[OperationContract]` interfaces; `<system.serviceModel>`
  endpoints/bindings in `App.config` / `Web.config`; `ChannelFactory`, `ClientBase<>`.
- **Named pipes**: `NamedPipeServerStream` / `NamedPipeClientStream`, pipe names.
- **gRPC / REST**: `.proto`, `HttpClient`, `[ApiController]`, service URLs in config.
- **Queues / bus**: MSMQ, RabbitMQ, Azure Service Bus, Kafka clients.
- **Shared state**: a common database, files, registry, memory-mapped files.

## 3. Draw them as explicit CROSS-PROCESS edges
- Render IPC edges distinctly (dashed, labeled `WCF` / `pipe` / `HTTP`) and note
  "contract + config, not a call — verify against .config".
- The wire is runtime (so `[inferred]`), but the **contract is real code you CAN cite**
  (`[ServiceContract]` interface, config endpoint). Ground the edge in that evidence —
  do NOT draw it on the user's say-so alone. (If the user *tells* you a boundary exists,
  confirm it in the contract/config before drawing it solid; agreement is not proof.)
- **If two components clearly should communicate but no static edge exists, FLAG THE GAP
  AND ASK** — never silently omit. The right move is:
  > "I see `TrayClient` and `RPA.Agent` as separate executables with a WCF
  > `[ServiceContract]`, but I can't trace the call statically — confirm the boundary?"

This is the fix for the RPA miss: enumerate the executables, hunt the WCF contract, and
draw + question the seam instead of dropping the whole `RPA.Agent` hierarchy.
