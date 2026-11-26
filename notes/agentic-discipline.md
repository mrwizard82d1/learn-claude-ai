# Agentic Discipline

## Video from Robert Martin published 2026-10

Robert Martin **does not** use acceptance tests as a "test vice"; however, he uses other tools to constrain the code written by an agent. His focus is on metrics measured by tools that he has written: crap, mutate, and dry. His focus is far less on acceptance testing but controlling the implementation using tools. 

In this video, he begins by implementing the functionality for an application **without** using any of these tools. He then begins a cycle of:

- Measure
- Fix
- Measure

This cycle demonstrates using these tools to improve the code quality.

His demo application did not seem particularly complex. A "single user". Usingn I/O to render (changing) images, but no real user input. However, the original implementation still offered many opportunities to improve against these metrics.

Finally, he discussed our new work of using UI to build developer-specific tools that help an individual developer to accomplish tasks: not only typical developer tasks (the tools above) but an "editor" for the "scripts" that he used for this video.

Overall, I would characterize Martin's work as complementary to Farley's work. Dave Farley emphasizes write acceptance tests and then asks agents to satisfy these acceptance tests (no emphasis on software engineering). Robert Martin does not attempt to constrain the entire application (except in his original - and undocumented - prompt). However, Martin wants the generated work product to be "well engineered". I think both perspectives are valuable, and I would like "my process" to include both because I think both are valuable.
