# Physical view & +1 Scenarios — PlantUML (deployment / use case)

Both are **low-derivability from code.** Draw a best-effort draft, label it clearly as
needing human confirmation, and say what you'd need to confirm it.

## Physical (deployment) — topology
Serves: "where does it run?" Source of truth: config, IaC, ops docs, humans — NOT code.
```plantuml
@startuml
node "Client Workstation" {
  artifact "RPA UI (VB)"
}
node "App Server" {
  artifact "Scheduler Service"
  artifact "Worker Host"
}
node "DB Server" {
  database "RPA DB"
}
"RPA UI (VB)" ..> "Scheduler Service" : RPC? (INFERRED — verify)
"Worker Host" ..> "RPA DB" : reads/writes (INFERRED — verify)
@enduml
```
Everything here is inferred unless you read deployment config. State that explicitly.

## +1 Scenarios (use case)
Serves: "what are the key things users do?" Source of truth: requirements/domain, not
code. Propose from observed entry points (UI handlers, endpoints, CLI commands), then
confirm with the people who know.
```plantuml
@startuml
left to right direction
actor Operator
actor Scheduler as "Scheduler (time-triggered)"
rectangle "RPA System" {
  usecase "Run Job Batch" as UC1
  usecase "Retry Failed Job" as UC2
  usecase "View Results" as UC3
}
Operator --> UC1
Operator --> UC3
Scheduler --> UC1
UC1 ..> UC2 : <<extend>> on failure (inferred)
@enduml
```
Use cases derived from code entry points are a starting hypothesis, not the real
requirements — always route them past a domain expert.
