# Process view — PlantUML (sequence / activity / communication)

Serves: "how does it run — control flow, concurrency, timing?" Derivability: **Partial.**
Call *structure* is visible; **actual parallelism/concurrency is runtime — mark it
`[inferred]` and frame as a hypothesis to verify by running/profiling.**

## Confidence legend
```plantuml
legend right
  --  observed: call/flow seen in code
  ..  inferred: concurrency/dispatch not confirmable statically — verify
endlegend
```

## Sequence — trace ONE behavior end to end
```plantuml
@startuml
actor User
User -> MainForm : clicks "Run Jobs"
MainForm -> JobScheduler : RunAll(jobs)
== inferred: parallel dispatch (Task.WhenAll) ==
par for each job (INFERRED — verify)
  JobScheduler -> Worker : Execute(job)
  Worker --> JobScheduler : result
end
JobScheduler --> MainForm : summary
@enduml
```
`par ... end` shows parallel fragments — label them INFERRED unless you saw the
concurrency construct directly.

## Activity — parallel processing via fork/join
```plantuml
@startuml
start
:receive job batch;
fork
  :process job A;
fork again
  :process job B;
fork again
  :process job C;
end fork
:aggregate results;
note right: fork/join here is INFERRED from\nTask.WhenAll / Parallel.ForEach — verify at runtime
stop
@enduml
```
`fork` / `fork again` / `end fork` = concurrent branches. This is the diagram for
"illustrate the parallel processing" — but concurrency is the confabulation zone, so
the note and INFERRED labels are mandatory.

## Communication (collaboration) — who-talks-to-whom for a behavior
```plantuml
@startuml
object MainForm
object JobScheduler
object Worker
MainForm -> JobScheduler : 1: RunAll()
JobScheduler -> Worker : 2: Execute() [xN, inferred parallel]
@enduml
```
