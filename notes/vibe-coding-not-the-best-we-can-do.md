# Vibe Coding - Is this really the best we can do?

An "article" from Dave Farley at https://tessl.io/blog/vibe-coding-is-not-the-best-we-can-do.

## Introduction

- "Natural language programming has a place."
- "But if those ideas (AI-generated tests) are treated as replacements for precise intent and independent verification, they become a bad trade."

## Use this Talk as Agent Context

Tessl has a skill from this talk, but not immediately linkable.

## What are Tests For?

- Tests are a form of measurement.
  - Not the goal but a mechanism to check whether we have achieved our goal(s).
  
## What is a Program For?

- Three goals
  - Helps **us** to organize our thinking about a problem
  - Communicates our understanding to other **humans**
  - Tells the computer what to do
- Three results (of a programming language)
  - Relatively simple and consistent grammar
  - Precise expression of intent
  - Repeatable, deterministic execution
  
## Where Does Natural Language Fall Short?

- Natural language is too vague to replace programming languages
  - Even with only people implementing, variations occur
  - Result may be plausible, but it may not be repeatable
- Yet unexpectedly we need not inspect every generated line of code
- We need a way to
  - Specify intent more precisely
  - Communicate that intent to humans
  - Verify that the machine produced the behavior we intended
  
## What Problems does AI Programming Create?

- Three problems
  - Specification
    - How do we say what we want with enough precision to get what we wanted
  - Verification
    - How to confirm that we got what we actually wanted
  - Incrementalism
    - "How do we keep learning and changing in small, controlled steps when agents can produce large changes very quickly?"
    
"So the bottleneck is not code generation. We have sped up the coding bit, which was often not the hardest part. The bottleneck is specification, verification, and release. If we do not speed up assurance to match generation, we have only moved the constraint."
    
## Executable specifications are the program

"The future I described is one where the program moves closer to a precise description of what we want, encoded as executable specifications, with AI translating those specifications into implementation."

- A BDD-style specification can describe the behavior we want in a form that is 
  - Readable by humans
  - Executable by machines
- This description provides both
  - Specification (of behavior)
  - Verification (of behavior)
- A programmers job shifts
  - Define 
    - Outcomes
    - Edge cases
    - Non-functional requirements
      - Performance
      - Security
      - Reliability
      - Other "-ilities" that matter for our application
  
  "The point is that AI works **inside** a stronger specification and verification loop." (Emphasis added.)
  
## How do we keep incrementalism?

- Incrementalism, in one sense, moves from coding to continuous delivery
  - "We still work iteratively in small steps. The AI may generate the code, but we still gather feedback, validate every change, build systems incrementally, and treat changes as experiments."
- Consequences
  - Specifications **must be version controlled**
  - Acceptance tests must run **in a deployment pipeline**
  - May mean keeping some tests hidden from AI to prevent "example only" passing code

"If we can specify what we want precisely, verify that we got it, and preserve incremental learning, then the generated code becomes less important than the behavior we can prove."

"AI assistants may become similar (to generated assembly). We may care less about the code the generate line by line, but only if we have a reliable way to verify the behavior we wanted. Without that, vibe coding is not the best we can do. It is just a faster way to create uncertainty."

