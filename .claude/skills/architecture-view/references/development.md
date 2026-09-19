# Development view — PlantUML (component / package)

Serves: "how is the code organized as modules, and which components interact to provide
behavior X?" Derivability: **High** — projects/assemblies/namespaces are visible; but
interface-based and DI wiring between components is often `[inferred]` → dash it.

## Confidence legend
```plantuml
legend right
  --  observed: dependency seen in code/project refs
  ..  inferred: wired at runtime (DI/config) — verify
endlegend
```

## Component diagram — components interacting for a behavior
```plantuml
@startuml
component "UI (VB)" as UI
component "Job Scheduler" as SCHED
component "Worker Pool" as WORK
component "Payment Gateway" as PAY
interface "IPaymentGateway" as IPAY

UI --> SCHED : triggers run (observed)
SCHED --> WORK : dispatches (observed)
WORK ..> IPAY  : uses (inferred via DI)
PAY - IPAY     : provides
@enduml
```
Use `-->` for observed dependencies, `..>` for runtime/DI-wired (inferred). Provided/
required interfaces (`- IPAY`, `..> IPAY`) show the contract between components.

## Package diagram — namespace/project structure
```plantuml
@startuml
package "Company.Rpa.UI" {}
package "Company.Rpa.Scheduling" {}
package "Company.Rpa.Workers" {}
package "Company.Rpa.Payments" {}
"Company.Rpa.UI" --> "Company.Rpa.Scheduling"
"Company.Rpa.Scheduling" --> "Company.Rpa.Workers"
"Company.Rpa.Workers" ..> "Company.Rpa.Payments"
@enduml
```
Altitude lever: collapse classes into their package to raise the view above the hairball.
