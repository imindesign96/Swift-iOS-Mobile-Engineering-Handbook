# Swift / iOS Mobile Engineering Handbook
## Master Specification & Codex Execution Contract

> **Document role:** Single source of truth for generating the entire Swift / iOS Mobile Engineering Handbook.
>
> **Primary consumer:** OpenAI Codex or another coding agent.
>
> **Language:** Vietnamese explanations; Swift/API terminology remains in English.
>
> **Target:** iOS engineers from Foundation to Senior / Global Interview level.
>
> **Baseline:** Prefer modern Swift (Swift 6+) and current Apple platform conventions. Before writing version-sensitive material, verify against current official Apple / Swift documentation. Never silently assume a version-specific behavior.

---

# 0. CODEX EXECUTION CONTRACT

## 0.1 Mission

Using this specification, create and maintain a complete repository:

```text
Swift-iOS-Mobile-Engineering-Handbook/
```

The repository must become a production-quality Markdown handbook covering:

- Swift language fundamentals
- Swift type system
- Memory / ARC / ownership
- Swift Concurrency
- UIKit
- SwiftUI
- Networking
- Persistence
- Architecture
- Testing
- Security
- Performance
- Production debugging
- Instruments / observability
- Mobile System Design
- Global interview preparation
- Coding exercises
- Debugging labs
- Hands-on projects

This is **not** a short interview cheat sheet.

The output must be usable as:

1. A sequential book.
2. A searchable engineering reference.
3. A global iOS interview preparation handbook.
4. A production debugging playbook.
5. A practical curriculum with exercises and projects.

---

## 0.2 Source of truth

This file is authoritative.

Codex MUST NOT:

- redesign the handbook structure without an explicit instruction;
- remove major sections because they seem too long;
- replace deep explanations with short summaries;
- generate empty placeholder chapters;
- write superficial definition-only content;
- invent Apple/Swift behavior that cannot be supported;
- pretend private SwiftUI/UIKit implementation details are public facts;
- duplicate the same explanation across many chapters.

If a future instruction conflicts with this file, the newest explicit user instruction wins.

---

## 0.3 Repository structure

Create a repository similar to:

```text
Swift-iOS-Mobile-Engineering-Handbook/
├── README.md
├── SUMMARY.md
├── SPECIFICATION.md
├── GLOSSARY.md
├── CROSS_REFERENCE_INDEX.md
├── PRODUCTION_PLAYBOOK.md
├── INTERVIEW_PLAYBOOK.md
├── assets/
│   └── diagrams/
├── templates/
│   ├── chapter-template.md
│   ├── interview-question-template.md
│   ├── production-case-template.md
│   └── adr-template.md
├── Phase-01-Swift-Foundation/
├── Phase-02-Memory-Runtime/
├── Phase-03-Concurrency/
├── Phase-04-iOS-Platform/
├── Phase-05-Networking/
├── Phase-06-Architecture/
├── Phase-07-Persistence/
├── Phase-08-Testing/
├── Phase-09-Production/
├── Phase-10-Mobile-System-Design/
└── Phase-11-Interview/
```

Each chapter is one independent `.md` file.

---

## 0.4 File naming

Use:

```text
NN-topic-slug.md
```

Example:

```text
01-how-a-swift-program-runs.md
02-optionals-and-nil-safety.md
03-value-vs-reference-semantics.md
```

Use stable ASCII filenames even though chapter titles are Vietnamese.

---

## 0.5 Definition of Done for Codex

A chapter is NOT complete merely because a file exists.

A chapter is complete only when it satisfies the quality gate defined later in this document, including where applicable:

- Story / problem
- Objectives
- Prerequisites
- Used Later
- Mental Model
- What / Why / How / When / What-if
- runnable Swift examples
- runtime implications
- memory implications
- concurrency implications
- architecture notes
- production case
- debugging / Instruments
- common mistakes
- best practices
- questions after major sections
- interview questions by level
- coding/debugging exercises
- cheat sheet
- chapter summary
- references

Never create a fake “DONE” chapter containing only headings.

---

## 0.6 Generation strategy

Generate content incrementally.

Recommended workflow:

```text
Specification
    ↓
SUMMARY / Knowledge Map
    ↓
Phase
    ↓
Chapter
    ↓
Quality Gate
    ↓
Cross-reference update
    ↓
Phase Review
```

When creating a chapter:

1. Read this specification.
2. Read prerequisite chapters if they already exist.
3. Avoid repeating them.
4. Write the chapter.
5. Validate code snippets conceptually.
6. Add cross references.
7. Update `SUMMARY.md` if needed.
8. Update `CROSS_REFERENCE_INDEX.md` for important concepts/production issues.
9. Mark chapter complete only when the quality gate passes.

---

## 0.7 Accuracy rules

For Swift / Apple APIs that may vary by version:

- Prefer Apple Developer Documentation.
- Prefer Swift.org documentation.
- Prefer Swift Evolution proposals.
- Prefer WWDC sessions.
- Prefer Swift Standard Library source where relevant.

Distinguish clearly between:

```text
Documented behavior
```

and:

```text
Implementation inference / observed behavior
```

Never present an undocumented implementation guess as a guaranteed API contract.

---

# PART 1 — VISION, GOALS & PHILOSOPHY

# 1. Vision

Build a Vietnamese Swift/iOS engineering handbook with the depth of a serious technical book.

It should connect concepts normally scattered across:

- Swift Language Guide
- Swift Evolution
- Apple Documentation
- WWDC
- production experience
- architecture literature
- interview preparation material

The handbook does not replace official documentation. It provides the **knowledge map and engineering mental models** connecting the pieces.

---

# 2. Target audience

## 2.1 Foundation / Fresher

Approximate experience:

```text
0–1 YOE
```

Goals:

- understand Swift;
- understand basic iOS applications;
- build UIKit/SwiftUI screens;
- networking;
- local persistence basics;
- basic testing;
- pass Junior interviews.

## 2.2 Junior

Approximate experience:

```text
1–2 YOE
```

Goals:

- strong Swift fundamentals;
- ARC;
- closures;
- protocols;
- generics;
- UIKit/SwiftUI;
- networking;
- MVVM;
- dependency injection;
- testing;
- concurrency basics.

## 2.3 Middle

Approximate experience:

```text
2–5 YOE
```

Goals:

- Swift Concurrency;
- memory;
- performance;
- architecture;
- modularization;
- offline/caching;
- production debugging;
- Instruments;
- security;
- mobile system design fundamentals.

## 2.4 Senior / Staff-oriented

Goals:

- architecture trade-offs;
- concurrency depth;
- performance;
- scalability of codebase;
- SDK design;
- modular architecture;
- migration strategy;
- observability;
- mobile system design;
- technical decision making and leadership.

YOE is not a strict proxy for skill.

---

# 3. Final learning outcome

After completing the handbook, a reader should be able to:

1. Explain Swift from type system and value semantics to concurrency.
2. Understand ARC, ownership and memory leaks.
3. Work effectively with UIKit and SwiftUI.
4. Build a testable networking layer.
5. Handle authentication, token refresh, cancellation and retry.
6. Correctly use async/await, Task, Actor, MainActor and Sendable.
7. Identify data races and logical races.
8. Build scalable application architecture.
9. Write useful tests.
10. Debug performance using Instruments.
11. Analyze production crashes and memory issues.
12. Design Feed, Chat, Download Manager and Offline-first features.
13. Perform well in global iOS interviews from Junior to Senior.

---

# 4. Core philosophy

Every important chapter must answer:

```text
What?
Why?
How?
When?
What if?
Production?
```

## What?

What is the concept?

## Why?

Why does it exist?

## How?

How does it work?

## When?

When should it be used or avoided?

## What if?

What breaks if it is used incorrectly?

## Production?

How does the concept manifest in a real application, and how do we debug it?

---

# 5. Problem-driven learning

Do not begin chapters with dry definitions where a problem can motivate the concept.

Bad:

> ARC is Automatic Reference Counting.

Preferred:

```text
Open Product Detail
    ↓
Close screen
    ↓
Open again
    ↓
Memory keeps increasing
    ↓
Why was the previous screen not released?
```

Then introduce ARC.

---

# 6. Production-first mindset

Important topics must go beyond API syntax.

Example:

```text
20 requests
    ↓
access token expires
    ↓
20 refresh attempts
    ↓
race condition
    ↓
random logout
```

Then design:

```text
Single refresh operation
+
waiting requests
+
retry
```

---

# 7. Global interview mindset

Interview preparation must expose depth.

A simple question such as:

> Struct vs Class?

may lead to:

```text
Value Semantics
    ↓
Reference Semantics
    ↓
Identity
    ↓
ARC
    ↓
Copy-on-Write
    ↓
Concurrency
    ↓
Performance
```

Teach the knowledge, not memorized interview phrases.

---

# 8. One shared sample domain

Use one consistent sample project:

# Global Commerce iOS App

Features:

```text
Authentication
User Profile
Product Catalog
Search
Favorites
Cart
Checkout
Payment
Orders
Notifications
Offline Cache
```

Prefer examples such as:

```swift
protocol ProductRepository {
    func fetchProducts() async throws -> [Product]
}
```

rather than unrelated toy examples.

---

# PART 2 — CHAPTER SPECIFICATION

# 9. Standard chapter structure

Use this logical flow:

```text
Story / Problem
    ↓
Objectives
    ↓
Prerequisites
    ↓
Used Later
    ↓
Mental Model
    ↓
Concept
    ↓
Why
    ↓
How
    ↓
Swift Code
    ↓
iOS Runtime Behavior
    ↓
Memory / Concurrency Impact
    ↓
Architecture Notes
    ↓
Production Case
    ↓
Debug / Instruments
    ↓
Common Mistakes
    ↓
Best Practices
    ↓
Interview Questions
    ↓
Exercises
    ↓
Cheat Sheet
    ↓
Chapter Summary
```

Not every small chapter requires every optional section, but critical chapters should be comprehensive.

---

# 10. Story / Problem

Do not open important chapters with a dictionary definition.

Example ARC:

```text
ProductDetail opens repeatedly
    ↓
memory grows
    ↓
ViewController does not deinit
```

Question:

> Why is the object still alive?

---

# 11. Objectives

Objectives must be verifiable.

Good:

```text
After this chapter you can:
- explain actor isolation;
- identify actor reentrancy;
- distinguish data race from logical race;
- debug duplicate work caused by reentrancy.
```

Bad:

> Understand actors better.

---

# 12. Prerequisites

Specify knowledge required before reading the chapter.

Example:

```yaml
prerequisites:
  - async/await
  - Task
  - value/reference semantics
```

Reference prior chapters rather than rewriting them.

---

# 13. Used Later

Explain where the knowledge reappears.

Example:

```yaml
used_later:
  - Dependency Injection
  - Repository
  - MVVM
  - Testing
  - Modularization
```

---

# 14. Mental Model

Mental models are mandatory for difficult concepts.

Example:

```text
struct
   ↓
value semantics
   ↓
independent values
```

```text
class
   ↓
reference semantics
   ↓
shared identity
```

For ARC:

```text
Owner
   ↓ strong
Object
   ↓ reference count reaches 0
deinit
```

---

# 15. What / Why / How / When / What-if

Do not only explain syntax.

For `@MainActor`, explain:

- What isolation means.
- Why UI state needs controlled isolation.
- How calls cross isolation boundaries.
- When code belongs on MainActor.
- What happens when heavy work is unnecessarily isolated there.

---

# 16. Swift code requirements

Examples should:

- be syntactically valid;
- be readable;
- use meaningful names;
- avoid unnecessary cleverness;
- use the Commerce domain where possible;
- identify platform/version requirements when relevant.

---

# 17. iOS runtime behavior

Framework chapters must explain runtime/lifecycle.

Example UIKit:

```text
init
 ↓
loadView
 ↓
viewDidLoad
 ↓
viewWillAppear
 ↓
viewDidAppear
```

Explain:

- which calls repeat;
- what owns the view;
- when release may occur;
- how lifecycle interacts with asynchronous work.

SwiftUI:

```text
State mutation
    ↓
Observation
    ↓
body evaluation
    ↓
new view description
    ↓
framework reconciles affected UI
```

Do not say simplistically that SwiftUI “rerenders everything”.

---

# 18. Memory implications

For reference/closure/lifecycle chapters, explicitly reason about ownership.

Example:

```text
ViewController
     ↓ owns
ViewModel
     ↓ owns
closure
     ↓ captures
ViewController
```

Then evaluate whether a cycle exists.

Do not automatically prescribe `[weak self]`.

---

# 19. Concurrency implications

When mutable state or asynchronous behavior exists, ask:

```text
Who owns the state?
Which isolation domain?
Can multiple tasks access it?
Is cancellation handled?
Can ordering change?
```

---

# 20. Architecture notes

Explain architecture implications without turning every chapter into a Clean Architecture chapter.

Example Protocol:

```text
ViewModel
   ↓ depends on
ProductRepository
   ↓ implemented by
APIProductRepository
```

Discuss loose coupling and testability.

---

# 21. Production Case Template

Use:

```text
Context
    ↓
Symptom
    ↓
Hypotheses
    ↓
Investigation
    ↓
Root Cause
    ↓
Fix
    ↓
Prevention
```

---

# 22. Debug / Instruments

When relevant, explicitly name tools and what to inspect.

Examples:

| Problem | Primary tools |
|---|---|
| Memory leak | Memory Graph / Leaks |
| Allocation growth | Allocations |
| CPU | Time Profiler |
| UI hitch | Instruments / rendering diagnostics |
| Crash | Crash report / symbolication |
| Network | Network diagnostics / logging |

---

# 23. Historical Note

Use only when history helps explain current design.

Examples:

```text
Completion Handler
    ↓
GCD
    ↓
async/await
    ↓
Actor
```

or:

```text
ObservableObject
    ↓
Observation
```

---

# 24. Myth vs Reality

Use where misconceptions are common.

Example:

**Myth:** `await` means “run on background thread”.

**Reality:** `await` marks a potential suspension point; it is not a thread-switch instruction.

---

# 25. Interview Trap

Identify hidden depth.

Example:

> Should every escaping closure capture `weak self`?

A strong answer reasons from ownership and lifetime instead of applying a universal rule.

---

# 26. Common Mistakes

Examples:

SwiftUI:

```text
- heavy work in body;
- unstable ForEach identity;
- wrong state ownership;
- multiple sources of truth.
```

Concurrency:

```text
- uncontrolled Task.detached;
- ignoring cancellation;
- assuming actors solve all logical races;
- uncontrolled shared mutable state.
```

---

# 27. Best Practices

Never present context-dependent advice as an absolute law.

Bad:

> Always use struct.

Better:

> Prefer struct when value semantics match the domain; use class when shared identity/lifecycle is necessary.

---

# 28. Questions after major sections

After each substantial concept group, include short review questions.

Example after Value Semantics:

1. What does value semantics mean?
2. Does assigning an Array always copy its full storage immediately?
3. Why can value semantics simplify reasoning?
4. How does Copy-on-Write affect performance?

---

# 29. Interview questions at chapter end

Divide by depth:

```text
Foundation
Junior
Middle
Senior
Production
```

---

# 30. Interview answer depths

For important questions provide:

```text
30-second answer
2–3 minute answer
Deep Dive
```

---

# 31. Exercises

Where applicable:

```text
Easy
Medium
Hard
Debugging Lab
Engineering / Design Exercise
```

---

# 32. Cheat Sheet

Short and precise.

Example:

```text
weak
- non-owning
- normally Optional
- becomes nil after deallocation

unowned
- non-owning
- assumes lifetime validity
- invalid access can fail
```

---

# 33. Chapter Summary

The summary must answer:

1. What problem motivated the chapter?
2. What is the central mental model?
3. What usage rule matters most?
4. What mistake is most dangerous?
5. What production lesson should be remembered?

---

# 34. Chapter metadata

Recommended front matter:

```yaml
title: "ARC and Ownership"
phase: "Memory & Runtime"
difficulty: 4
importance: 5
interview_frequency: 5

levels:
  - L2
  - L3
  - L4

prerequisites:
  - Classes
  - Reference Semantics
  - Closures

used_later:
  - UIKit Lifecycle
  - Coordinator
  - SwiftUI
  - Async Code

competencies:
  - Swift
  - Memory
  - Debugging
  - Production
  - Interview

tags:
  - ARC
  - strong
  - weak
  - unowned
  - retain-cycle
```

---

# PART 3 — BOOK-WIDE CONVENTIONS

# 35. Knowledge dependency

The handbook is a graph, not an article collection.

Example:

```text
Class
  ↓
Reference Semantics
  ↓
ARC
  ↓
Closure Capture
  ↓
Retain Cycle
```

Do not reteach ARC in every later chapter.

Cross-reference it.

---

# 36. Chapter naming

Prefer problem/question-oriented titles.

Examples:

```text
Why does a ViewController fail to deinit?
What makes SwiftUI update a screen?
What actually happens at await?
How does an iPhone request reach a server?
```

Technical subtitles may be added.

---

# 37. Markdown

Use heading levels:

```text
#
##
###
####
```

Avoid deeper headings.

Tables only when comparison truly benefits.

---

# 38. Callouts

Standard forms:

> **Note**
>
> Supplemental information.

> **Tip**
>
> Practical guidance.

> **Warning**
>
> Likely bug or misunderstanding.

> **Production**
>
> Real application behavior.

---

# 39. Diagrams

Priority:

```text
Simple ASCII
    ↓
Mermaid
    ↓
Image only when genuinely needed
```

Prefer horizontal flows for simple diagrams.

Use Mermaid for complex flows:

- `flowchart`
- `sequenceDiagram`
- `classDiagram`
- `stateDiagram`
- `erDiagram`
- `mindmap`

Do not use Mermaid for decoration.

---

# 40. Swift baseline

Prefer modern Swift.

For version-dependent APIs:

- state required Swift version;
- state required iOS version;
- identify legacy patterns only when educationally useful;
- do not silently mix incompatible APIs.

---

# 41. Naming convention

Prefer Commerce-domain names:

```text
User
Product
ProductRepository
Cart
Checkout
Payment
Order
Notification
```

Avoid excessive `Foo`, `Bar`, `A`, `B`.

---

# 42. Architecture baseline

Start simple and evolve.

Typical flow:

```text
View
 ↓
ViewModel
 ↓
Repository
 ↓
Remote / Local
```

Later:

```text
View
 ↓
ViewModel
 ↓
UseCase
 ↓
Repository
 ↓
Remote / Local
```

Do not force Clean Architecture into beginner chapters.

---

# 43. UIKit / SwiftUI conventions

Keep framework-specific examples focused.

UIKit:

```text
ViewController
 ↓
ViewModel
 ↓
Repository
```

SwiftUI:

```text
View
 ↓
ViewModel / Model layer where appropriate
 ↓
Repository
```

Do not duplicate the whole project twice.

---

# 44. Concurrency questions required in async code

Ask:

```text
Which task owns this work?
Which isolation domain owns the state?
Can it be cancelled?
Can it outlive the screen?
Can ordering change?
Is MainActor used correctly?
```

---

# 45. Memory questions required for object graphs

Ask:

```text
Who creates the object?
Who owns it?
Who releases it?
When should deinit happen?
```

---

# 46. Networking flow convention

Prefer:

```text
View
 ↓
ViewModel
 ↓
Repository
 ↓
API Client
 ↓
URLSession
 ↓
Server
```

Do not use direct URLSession calls from views in production architecture examples.

---

# 47. Persistence flow

```text
Repository
   ├── Remote
   └── Local Store
```

Local implementation may involve:

- UserDefaults
- Keychain
- FileManager
- SQLite
- Core Data
- SwiftData

depending on requirements.

---

# 48. Testing terminology

Use and distinguish:

- Unit Test
- Integration Test
- UI Test
- Mock
- Stub
- Fake
- Spy when relevant

---

# 49. Performance dimensions

Always consider:

```text
CPU
Memory
Network
Disk
Battery
UI responsiveness
```

---

# 50. Security baseline

Do not store secrets carelessly.

Discuss:

- Keychain
- token lifecycle
- privacy-aware logging
- transport security
- deep-link validation
- sensitive data exposure

where relevant.

---

# 51. Debugging flow

Standard flow:

```text
Symptom
 ↓
Collect evidence
 ↓
Hypotheses
 ↓
Experiment / Measure
 ↓
Root Cause
 ↓
Fix
 ↓
Regression Prevention
```

---

# PART 4 — ROADMAP & KNOWLEDGE ARCHITECTURE

# 52. Phase architecture

```text
Phase 1  Swift Foundation
Phase 2  Memory & Runtime
Phase 3  Concurrency
Phase 4  iOS Platform
Phase 5  Networking
Phase 6  Architecture
Phase 7  Persistence
Phase 8  Testing
Phase 9  Production
Phase 10 Mobile System Design
Phase 11 Interview
```

---

# 53. Phase 1 — Swift Foundation

Must cover at least:

```text
Swift overview
Variables & constants
Type system
Optional
Control flow
Functions
Closures
Enum
Struct
Class
Properties
Methods
Extensions
Protocols
Generics
Error Handling
Collections
String
Pattern Matching
Result
some / any
associatedtype
Codable fundamentals
```

Critical interview questions include:

- `let` vs `var`
- Optional and nil safety
- `if let` vs `guard let`
- Struct vs Class
- Value vs Reference
- `==` vs `===`
- Protocol-oriented programming
- Generic constraints
- `some` vs `any`
- associatedtype
- throws / try / try? / try!
- Result

---

# 54. Phase 2 — Memory & Runtime

Must cover:

```text
Stack / Heap mental model
Value Semantics
Reference Semantics
Identity
Copy semantics
Copy-on-Write
ARC
Strong
Weak
Unowned
Closure Capture
Escaping closures
Capture lists
Retain cycles
Memory leaks
deinit
Ownership graph
Delegates
Timers / observers / tasks and lifetime
```

---

# 55. Phase 3 — Concurrency

Must cover both legacy fundamentals and modern Swift:

```text
Thread basics
GCD
Serial / Concurrent Queue
sync / async
Deadlock
DispatchGroup
Semaphore
OperationQueue overview
async / await
Suspension
Task
Structured Concurrency
async let
TaskGroup
Cancellation
Actor
Actor isolation
MainActor
Global Actor
Sendable
@Sendable
nonisolated
strict concurrency
actor reentrancy
logical race
legacy migration
```

---

# 56. Phase 4 — iOS Platform

Must cover:

```text
App Lifecycle
Scene lifecycle
UIView
UIViewController
Navigation
Auto Layout
Intrinsic Content Size
Hugging / Compression Resistance
UITableView
UICollectionView
Reuse
Diffable Data Source
Delegate
SwiftUI fundamentals
State
Binding
Observation
Environment
Identity
ForEach
NavigationStack
task
animation basics
```

---

# 57. Phase 5 — Networking

Must cover:

```text
HTTP fundamentals
URLSession
URLRequest
HTTP status codes
Codable
CodingKeys
Networking layer
Endpoint abstraction
Error modeling
Timeout
Retry
Cancellation
Authentication
Access token
Refresh token
Single-flight refresh
Pagination
HTTP caching
Offline/cache integration
Certificate / transport security concepts
```

---

# 58. Phase 6 — Architecture

Must cover:

```text
MVC
Massive ViewController
MVVM
ViewModel responsibilities
Coordinator
Repository
Dependency Injection
Constructor Injection
Service Locator trade-offs
Singleton trade-offs
UseCase / Interactor
Clean Architecture principles
Modularization
SPM modules
Feature boundaries
Circular dependency prevention
Migration strategy
```

---

# 59. Phase 7 — Persistence

Must cover:

```text
UserDefaults
Keychain
FileManager
SQLite concepts
Core Data concepts
Managed Object Context
Core Data concurrency
SwiftData
Migration
Cache persistence
Offline-first
Synchronization
Conflict resolution
```

---

# 60. Phase 8 — Testing

Must cover:

```text
Unit Test
Integration Test
UI Test
XCTest / modern Apple testing approaches where applicable
Mock / Stub / Fake
Dependency Injection
Async testing
ViewModel testing
Networking testing
Flaky tests
Test pyramid
Snapshot testing
TDD
Code coverage limitations
```

---

# 61. Phase 9 — Production

Must cover:

```text
Logging
Crash analysis
Symbolication
Memory leak
Memory pressure
Instruments
Time Profiler
Allocations
Leaks / Memory Graph
Scrolling performance
Image loading / decoding
App launch
Battery / energy
Network diagnostics
Release-build bugs
Device-specific bugs
Background execution
Concurrency incidents
Observability
Regression prevention
```

---

# 62. Phase 10 — Mobile System Design

Must cover:

```text
Image Loader
Feed
Chat
Download Manager
Offline-first app
Video feed
Authentication
Notification routing
Analytics SDK
Feature flags
Networking SDK
Caching layer
Search autocomplete
Large-scale modular architecture
UIKit → SwiftUI migration
```

---

# 63. Phase 11 — Interview

This is synthesis rather than new theory.

Include:

```text
Swift Core review
Memory review
Concurrency review
UIKit / SwiftUI review
Networking review
Architecture review
Testing review
Performance review
Production scenarios
Coding interviews
Mobile System Design
Behavioral engineering
Mock interviews
```

---

# PART 5 — KNOWLEDGE GRAPH, RUNTIME GRAPH & PRODUCTION GRAPH

# 64. Knowledge Graph

Examples:

```text
Struct
  ↓
Value Semantics
  ↓
Copy
  ↓
Copy-on-Write
  ↓
Performance / Concurrency
```

```text
Class
  ↓
Reference Semantics
  ↓
ARC
  ↓
Closure Capture
  ↓
Retain Cycle
```

```text
Protocol
  ↓
Generic / associatedtype
  ↓
DI
  ↓
Repository
  ↓
MVVM
  ↓
Modular Architecture
```

---

# 65. Concurrency graph

```text
Thread
  ↓
Shared Mutable State
  ↓
Race Conditions
  ↓
Synchronization
```

Modern branch:

```text
async/await
   ↓
Task
   ↓
Structured Concurrency
   ↓
Cancellation
   ↓
Actor
   ↓
Isolation
   ↓
Sendable / MainActor
   ↓
Reentrancy
```

---

# 66. Runtime Graph

Use runtime graphs throughout the book.

Example SwiftUI request flow:

```text
User Tap
 ↓
View
 ↓
ViewModel
 ↓
Task
 ↓
Repository
 ↓
URLSession
 ↓
Server
 ↓
Decode
 ↓
State Update
 ↓
UI Update
```

---

# 67. UIKit lifetime graph

```text
ViewController appears
    ↓
async work
    ↓
screen disappears
    ↓
references released?
   / \
 yes  no
 ↓     ↓
deinit investigate ownership
```

---

# 68. Authentication graph

```text
Request
 ↓
401
 ↓
Shared Refresh Operation
 ↓
New Token
 ↓
Retry waiting requests
```

---

# 69. Production mapping

Examples:

Memory leak maps to:

```text
ARC
Closure Capture
Delegate
Timer
Observer
Task lifetime
Coordinator
Cache
```

UI freeze maps to:

```text
Main Thread
MainActor
JSON decoding
Image decoding
Disk I/O
Synchronization
```

Duplicate API maps to:

```text
Task lifecycle
State machine
Actor
Networking
Idempotency
```

Stale data maps to:

```text
Cache policy
Repository
Persistence
TTL
Synchronization
Offline-first
```

---

# 70. Tool mapping

| Symptom | Tool / evidence |
|---|---|
| Memory leak | Memory Graph / Leaks |
| Allocation growth | Allocations |
| CPU | Time Profiler |
| UI hitch | Instruments / rendering diagnostics |
| Crash | Crash report / symbolication |
| Hang | Stack traces / profiler |
| Network | Network diagnostics / structured logs |
| Energy | Energy diagnostics |

---

# 71. Cross-reference index

Maintain `CROSS_REFERENCE_INDEX.md`.

Examples:

| Problem | Chapters |
|---|---|
| ViewController does not deinit | ARC, Closure Capture, Delegate, Task Lifetime |
| UI freezes | MainActor, Concurrency, Performance |
| SwiftUI does not update | State, Observation, Identity |
| Duplicate API | Task, Actor, Networking |
| Token refresh race | Authentication, Actor, Retry |
| Scroll lag | Images, Rendering, Performance |
| Stale data | Cache, Persistence, Sync |

---

# PART 6 — INTERVIEW & ASSESSMENT SPECIFICATION

# 72. Skill levels

Use:

| Level | Meaning |
|---|---|
| L1 | Foundation |
| L2 | Junior |
| L3 | Strong Junior |
| L4 | Middle |
| L5 | Strong Middle |
| L6 | Senior |

Do not equate level rigidly with years of experience.

---

# 73. Interview question template

For important questions:

```markdown
## Question

> ...

### Level

### Frequency

### Interviewer is testing

### 30-second answer

### 2–3 minute answer

### Deep Dive

### Example

### Common Wrong Answers

### Follow-up Questions

### Production Variant

### Senior Extension
```

---

# 74. Interview frequency

```text
★★★★★ very common
★★★★ common
★★★ possible
★★ less common
★ niche
```

---

# 75. Mandatory interview domains

The interview bank must include:

```text
Swift Core
Memory
Concurrency
UIKit
SwiftUI
Networking
Persistence
Architecture
Testing
Performance
Security
Production
Coding
Mobile System Design
Behavioral Engineering
```

---

# 76. Core interview questions to include

The handbook must comprehensively cover at least the following initial question bank.

## Swift Fundamentals

1. `let` vs `var`.
2. Strong typing.
3. Type inference.
4. Optional.
5. `String?` vs `String!` vs `String`.
6. Optional binding.
7. `if let` vs `guard let`.
8. Nil coalescing `??`.
9. Force unwrap risks.
10. Tuple.
11. Array vs Set vs Dictionary.
12. Collection ordering.
13. Switch and pattern matching.
14. Range operators.
15. Parameter labels.
16. Default / variadic parameters.

## Struct / Class / OOP

17. Struct vs Class.
18. Value vs Reference type.
19. Why Swift prefers value semantics where appropriate.
20. When class is required.
21. Copying a struct.
22. Copying a class reference.
23. `===` vs `==`.
24. Inheritance.
25. `final`.
26. Encapsulation.
27. Polymorphism in Swift.
28. Abstraction.

## Protocol-oriented Swift

29. Protocol.
30. Protocol Extension.
31. Default implementation.
32. Protocol inheritance.
33. `associatedtype`.
34. Generic vs associatedtype.
35. `some Protocol`.
36. `any Protocol`.
37. Opaque vs existential.
38. Protocol composition.
39. Protocol-oriented programming.
40. Dependency Injection through protocol.

## Closures

41. Closure.
42. Closure vs Function.
43. Trailing closure.
44. Variable capture.
45. `@escaping`.
46. Non-escaping.
47. `@autoclosure`.
48. Capture list.
49. `[weak self]`.
50. `[unowned self]`.
51. Closure retain cycle.

## ARC / Memory

52. ARC.
53. Strong reference.
54. Weak reference.
55. Unowned reference.
56. Why weak is usually Optional.
57. When weak.
58. When unowned.
59. Retain cycle.
60. Object-object retain cycle.
61. Closure retain cycle.
62. Weak delegate.
63. Memory leak.
64. Memory Graph.
65. Leaks / Allocations.
66. `deinit`.

## Generics / Errors

67. Generic function/type.
68. Generic constraints.
69. `where`.
70. Error protocol.
71. `throws`.
72. `try`, `try?`, `try!`.
73. do/catch.
74. Result.
75. async throws vs Result.
76. Custom error.

## UIKit

77. App lifecycle.
78. UIApplicationDelegate.
79. Scene lifecycle.
80. UIViewController lifecycle.
81. `viewDidLoad`.
82. `viewWillAppear` vs `viewDidAppear`.
83. Auto Layout.
84. Intrinsic Content Size.
85. Content Hugging.
86. Compression Resistance.
87. UITableView reuse.
88. UICollectionView.
89. Diffable Data Source.
90. Delegate pattern.

## SwiftUI

91. SwiftUI vs UIKit.
92. Declarative UI.
93. Why View is a struct.
94. State.
95. Binding.
96. State object ownership concepts.
97. Environment.
98. Observation framework.
99. Observable model patterns.
100. Why/how body reevaluates.
101. View identity.
102. ForEach stable identity.
103. NavigationStack.
104. `.task`.
105. Async API in SwiftUI.
106. Heavy work in body.

## Networking

107. URLSession.
108. GET vs POST.
109. HTTP status codes.
110. Codable.
111. Encodable vs Decodable.
112. CodingKeys.
113. Networking layer design.
114. Cancel request.
115. Retry.
116. Token expiration.
117. Refresh-token race.
118. Certificate / transport security.
119. HTTP caching.
120. Pagination.

## Swift Concurrency

121. `async`.
122. `await`.
123. Suspension point.
124. async != background thread.
125. Task.
126. Structured concurrency.
127. Unstructured concurrency.
128. async let.
129. TaskGroup.
130. Task.detached.
131. Cancellation.
132. Actor.
133. Actor isolation.
134. MainActor.
135. `@MainActor`.
136. MainActor vs simplistic “main thread” mental model.
137. Sendable.
138. `@Sendable`.
139. Data race.
140. Race condition vs data race.
141. Actor limitations.
142. Actor reentrancy.
143. Logical race.
144. Strict concurrency.
145. nonisolated.
146. Legacy GCD migration.
147. When GCD is still relevant.

## GCD / Threading

148. Main queue.
149. Serial vs concurrent queue.
150. sync vs async.
151. Deadlock.
152. Barrier.
153. DispatchGroup.
154. Semaphore.
155. Mutex / locks concepts.
156. Priority inversion.
157. Thread explosion.
158. QoS.

## Architecture

159. MVC.
160. Massive View Controller.
161. MVVM.
162. ViewModel responsibility.
163. Should ViewModel import UIKit?
164. Clean Architecture.
165. Domain layer.
166. Repository.
167. UseCase / Interactor.
168. Coordinator.
169. Dependency Injection.
170. Constructor injection vs Service Locator.
171. Singleton trade-offs.
172. Modular architecture.
173. SPM modules.
174. Circular dependency.

## Persistence

175. UserDefaults use cases.
176. When not UserDefaults.
177. Keychain.
178. Core Data.
179. Managed Object Context.
180. Core Data concurrency.
181. SwiftData.
182. SwiftData vs Core Data.
183. Migration.
184. Offline-first.

## Testing

185. Unit / Integration / UI Test.
186. XCTest / platform testing tools.
187. Mock / Stub / Fake.
188. DI and testability.
189. Async testing.
190. ViewModel testing.
191. Networking mock.
192. Flaky tests.
193. Test pyramid.
194. Snapshot testing.
195. TDD.
196. Code coverage limitations.

## Performance / Production

197. Slow launch debugging.
198. Main thread blocking.
199. FPS / hitch.
200. Time Profiler.
201. Allocations.
202. Leaks.
203. Memory Graph.
204. Large images.
205. Downsampling.
206. Scrolling lag.
207. Large response / decoding.
208. Copy-on-Write.
209. Value semantics and performance.
210. Memory warning / pressure.
211. OS kill without ordinary crash log.

## Security

212. Keychain vs UserDefaults.
213. Token storage.
214. Certificate pinning trade-offs.
215. Secure Enclave.
216. Biometrics.
217. Sensitive logs.
218. ATS.
219. Deep-link security.
220. Universal Links vs custom URL schemes.

## Production Scenarios

221. API slow only in production.
222. UI freeze.
223. Memory grows after push/pop.
224. Random index-out-of-range.
225. Previous account data after logout/login.
226. Refresh-token concurrency issue.
227. Image list scroll lag.
228. Crash on low-memory device.
229. Wi-Fi works, cellular fails.
230. Async task updates dismissed screen.
231. Double-tap payment creates duplicate order.
232. Push received but UI stale.
233. Cache stale.
234. Offline conflict.
235. Background upload interrupted.
236. Strict-concurrency migration issues.
237. Actor code still duplicates work.
238. Rare crash across huge session volume.

## Mobile System Design

239. Instagram-like Feed.
240. Chat app.
241. Image loading library.
242. Offline-first news app.
243. TikTok-like video feed.
244. Search/autocomplete.
245. Notification center.
246. Analytics SDK.
247. Networking SDK.
248. Feature flag system.
249. Download manager.
250. Caching layer.
251. Authentication system.
252. Modular architecture for a very large team.
253. UIKit → SwiftUI migration.

The final bank may exceed 300 questions; quality and coverage matter more than hitting a number.

---

# 77. Production interview format

Use:

```text
Symptom
 ↓
Candidate asks questions
 ↓
Hypotheses
 ↓
Investigation
 ↓
Root Cause
 ↓
Fix
 ↓
Prevention
```

Do not reveal the root cause too early.

---

# 78. Coding interview

Three groups:

```text
Algorithms / Data Structures
Swift-specific Coding
iOS Engineering Coding
```

Representative problems:

- Reverse String
- Palindrome
- Two Sum
- Remove duplicates
- First non-repeating character
- Group anagrams
- Merge intervals
- Binary search
- LRU Cache
- Stack / Queue
- Linked list cycle
- Tree traversal
- BFS / DFS
- Top-K
- Debouncer
- Thread-safe cache
- Concurrent image downloader
- Rate limiter concept

Prefer Easy/Medium DSA plus strong Swift/iOS engineering exercises.

---

# 79. Interview assessment

Evaluate:

```text
Correctness
Depth
Reasoning
Production Awareness
Communication
```

Do not score only memorized terminology.

---

# PART 7 — CODING, LABS & HANDS-ON PROJECTS

# 80. Practice philosophy

Knowledge is considered internalized only after:

```text
Explain
 ↓
Implement
 ↓
Break
 ↓
Debug
```

---

# 81. Exercise types

Each phase should include:

```text
Concept Exercise
Coding Exercise
Debugging Lab
Engineering / Trade-off Exercise
```

---

# 82. Exercise difficulty

```text
Easy
Medium
Hard
```

Medium/Hard exercises should increasingly resemble production.

---

# 83. Main project

Use one evolving project:

# Global Commerce iOS App

Evolution by phase:

## Foundation

Domain models and pure Swift logic.

## Memory

Lifecycle and retain-cycle labs.

## Concurrency

Concurrent product/inventory/recommendation fetching.

## UI

Selected UIKit and SwiftUI features.

## Networking

Real networking abstraction.

## Architecture

Refactor into View/ViewModel/UseCase/Repository where appropriate.

## Persistence

Local cache, favorites, cart, offline behavior.

## Testing

Unit/integration/UI testing.

## Production

Inject intentional performance, memory and concurrency bugs.

---

# 84. Debugging lab format

Each lab includes:

```text
Bug Report
Code
Observed Symptom
Available Evidence
```

Reader must:

1. create hypotheses;
2. select tools;
3. measure;
4. identify root cause;
5. fix;
6. add regression protection.

---

# 85. Required practical projects

Examples:

- CLI Shopping Cart
- Concurrent Image Downloader
- Thread-safe Image Cache
- Token Refresh Manager
- Offline Notes
- Paginated Product List
- Modular Commerce Feature
- Production debugging challenge

---

# 86. Refactoring exercises

Include intentionally poor code such as:

```text
Massive ViewController
Massive ViewModel
God Service
Singleton-heavy architecture
```

Then require:

```text
Identify responsibilities
 ↓
Extract
 ↓
Inject dependencies
 ↓
Test
```

---

# 87. Code review exercises

Provide PR-like snippets containing:

- ARC bug
- concurrency bug
- state issue
- architecture smell
- missing test
- poor naming
- performance issue

Reader performs code review.

---

# 88. Capstone

Final Commerce app should demonstrate:

```text
Swift
UIKit and/or SwiftUI
Architecture
Dependency Injection
Networking
Authentication
Persistence
Offline Cache
Concurrency
Testing
Logging
Performance measurement
```

Avoid over-engineering for its own sake.

---

# PART 8 — PRODUCTION ENGINEERING & OBSERVABILITY

# 89. Production philosophy

Never teach:

```text
Bug
 ↓
Guess
 ↓
Change code
```

Teach:

```text
Symptom
 ↓
Evidence
 ↓
Hypotheses
 ↓
Measurement
 ↓
Root Cause
 ↓
Fix
 ↓
Regression Prevention
```

---

# 90. Mandatory production topics

Cover:

```text
Crash
Hang
Memory Leak
Memory Pressure
High CPU
Scrolling Lag
Slow Launch
Network Failure
Token Refresh Race
Duplicate Action
Stale Cache
Offline Conflict
Background Failure
Battery
Release-only Bug
Device-specific Bug
Concurrency Race
Lifecycle Issue
```

---

# 91. Logging

Teach structured, privacy-aware logging.

Avoid sensitive data.

Useful context:

```text
feature
screen
request/correlation id
safe session context
timestamp
error category
```

---

# 92. Crash analysis

Teach:

```text
Crash Report
 ↓
Symbolication
 ↓
Faulting Thread
 ↓
Stack
 ↓
App Frames
 ↓
Context
 ↓
Root Cause
```

Cover concepts such as:

- fatal error
- EXC_BAD_ACCESS
- index out of range
- nil force unwrap
- watchdog termination
- concurrency failures

---

# 93. Memory

Distinguish:

```text
Leak
→ object should die but remains alive

Pressure
→ legitimate objects consume too much memory
```

Cover:

- decoded image size
- cache growth
- ownership graph
- task lifetime
- observers / timers

---

# 94. CPU / UI performance

Use measurement first.

Examples:

```text
CPU high
 ↓
Time Profiler
 ↓
hot call tree
```

Scrolling:

```text
Image Decode
Layout
Main-thread Work
State Updates
Formatting
```

---

# 95. App launch

Discuss:

```text
Pre-main
Post-main
```

Potential costs:

- dependency initialization
- synchronous disk I/O
- migration
- framework loading
- early networking

---

# 96. Network resilience

Distinguish:

```text
Transport Error
HTTP Error
Decode Error
Business Error
```

Retry strategy must consider:

- retryability
- max attempts
- exponential backoff
- jitter
- cancellation
- idempotency

---

# 97. Duplicate action

Example:

```text
Double tap Pay
 ↓
2 Tasks
 ↓
2 POSTs
```

Discuss protection at multiple layers:

- UI
- task state
- state machine
- idempotency key
- server protection

---

# 98. Background / app lifecycle

Reason about:

```text
Foreground
Background
Suspended
Terminated
```

Long-running work must be designed for lifecycle interruptions.

---

# 99. Observability metrics

Discuss examples:

```text
Crash-free sessions
Hang rate
App launch
Screen load
API latency
Error rate
Memory
CPU
```

Do not require a specific vendor.

---

# 100. Incident response

For advanced chapters:

```text
Stabilize
 ↓
Understand
 ↓
Fix
 ↓
Prevent
```

Mitigation may precede perfect root-cause analysis when user impact is severe.

---

# PART 9 — MOBILE SYSTEM DESIGN & ARCHITECTURE

# 101. Mobile-specific constraints

Do not copy backend system design blindly.

Mobile constraints include:

```text
Memory
Battery
Network instability
Storage
App lifecycle
Background restrictions
Device diversity
Offline
```

---

# 102. Standard system design framework

Use:

```text
Requirements
 ↓
Constraints
 ↓
User Flow
 ↓
Data Flow
 ↓
Architecture
 ↓
State Ownership
 ↓
Networking
 ↓
Persistence
 ↓
Concurrency
 ↓
Cache / Offline
 ↓
Failure Handling
 ↓
Security
 ↓
Performance
 ↓
Observability
 ↓
Testing
 ↓
Trade-offs
```

---

# 103. Requirements

Separate:

```text
Functional Requirements
Non-functional Requirements
```

Example non-functional concerns:

- responsiveness;
- memory;
- offline behavior;
- battery;
- reliability.

---

# 104. Source of Truth

Every feature must explicitly define:

> What is authoritative?

Possible answers:

- server;
- local persistent store;
- in-memory model;
- combination with synchronization policy.

Do not allow multiple accidental sources of truth.

---

# 105. State ownership

Every design must answer:

```text
Who creates state?
Who owns it?
Who mutates it?
Who observes it?
```

---

# 106. Architecture layering

Typical scalable direction:

```text
View
 ↓
ViewModel
 ↓
UseCase
 ↓
Repository
 ↓
Remote / Local
```

Use only as much layering as complexity justifies.

---

# 107. Repository responsibilities

Repository may coordinate:

```text
Remote
Local
Cache
Synchronization
Error Mapping
```

It is not merely a class that renames URLSession calls.

---

# 108. Caching

Discuss:

```text
Memory Cache
Disk Cache
Remote
TTL
Invalidation
Refresh
Stale-while-revalidate where suitable
```

---

# 109. Offline strategies

Distinguish:

```text
Online-first
Cache-first
Offline-first
```

Explain trade-offs.

---

# 110. Required system design cases

Detailed chapters/labs should include:

## Image Loader

```text
Memory Cache
Disk Cache
Network
Decode
Resize
Duplicate Request Coalescing
Cancellation
Prefetch
```

## Feed

```text
Pagination
Refresh
Prefetch
Images
Cache
Offline
Analytics
```

## Chat

```text
Realtime
Ordering
Offline Queue
Retry
Local DB
Notifications
```

## Download Manager

```text
Queue
Resume
Retry
Background
Progress
Persistence
```

## Authentication

```text
Access Token
Refresh Token
Single Refresh
Waiting Requests
Logout
Keychain
```

## Search

```text
Debounce
Cancellation
Suggestions
Pagination
Caching
```

## Analytics SDK

```text
Event
Buffer
Batch
Offline
Retry
Upload
Privacy
```

## Large App Modularization

```text
Feature Modules
Core Modules
Dependency Rules
SPM
Build Time
Team Ownership
Migration
```

## UIKit → SwiftUI Migration

Discuss incremental migration, boundaries, risk and test strategy.

---

# 111. State machines

Complex flows such as checkout should prefer explicit state:

```text
Idle
Loading
Success
Failure
```

rather than many unrelated Boolean flags.

---

# 112. Architecture Decision Record

Use ADRs for important trade-offs.

Template:

```markdown
# ADR-XXX: Decision title

## Context
## Problem
## Options
## Decision
## Consequences
## Revisit Conditions
```

---

# 113. Anti-pattern catalog

The handbook must cover at least:

Architecture:

- Massive ViewController
- Massive ViewModel
- God Repository
- Singleton abuse
- business logic in View

Networking:

- URLSession from View
- infinite retry
- no error taxonomy
- hardcoded configuration

State:

- multiple sources of truth
- Boolean explosion
- mutation from many layers

Memory:

- blind weak-self usage
- observer/timer lifetime mistakes
- unbounded caches

Concurrency:

- uncontrolled detached tasks
- ignored cancellation
- shared mutable state
- misunderstanding actor safety

SwiftUI:

- heavy `body`
- unstable identity
- wrong state ownership
- unnecessary recomputation

For every anti-pattern explain:

```text
Symptom
Why problematic
Consequences
Refactor
Exceptions / context
```

---

# PART 10 — CROSS-CUTTING QUALITY REQUIREMENTS

# 114. Glossary

Maintain one canonical glossary for terms including:

```text
Value Semantics
Reference Semantics
Identity
Ownership
ARC
Retain Cycle
Isolation
Sendable
Suspension Point
Actor
MainActor
Cancellation
Source of Truth
Idempotency
Cache Invalidation
```

Do not redefine inconsistently in every chapter.

---

# 115. Cross-reference system

Each important chapter should link:

```text
Prerequisites
Related Chapters
Used Later
Production Issues
Interview Questions
```

---

# 116. Phase Review

Each phase must end with:

```text
Phase Summary
Cheat Sheet
Knowledge Map
Review Questions
Deep-dive Questions
Coding Exercises
Debugging Lab
Mini Project / Case Study
Mock Interview where appropriate
```

---

# 117. Phase completion

A phase is not complete until:

- all mandatory chapters pass quality gate;
- review content exists;
- cross references work;
- practical exercises exist;
- interview coverage for the phase exists.

---

# 118. Writing tone

Use clear Vietnamese suitable for learners, but do not oversimplify technical truth.

When explaining difficult material:

```text
Intuition
 ↓
Mental Model
 ↓
Precise Explanation
 ↓
Code
 ↓
Edge Cases
```

A beginner should understand the intuition, while a Middle/Senior should still find the explanation technically useful.

---

# 119. Explain every “why”

Do not write code such as:

```swift
private let repository: ProductRepository
```

without eventually teaching:

- why `private`;
- why `let`;
- why abstraction;
- who owns the dependency;
- how it affects testing.

Do not assume syntax is self-explanatory for Foundation chapters.

---

# 120. Avoid false absolutes

Avoid statements like:

```text
Always use struct.
Always use weak self.
Never use singleton.
MVVM is better than MVC.
Actor solves race conditions.
```

Replace with context, assumptions and trade-offs.

---

# 121. References

For technical claims prioritize primary sources:

1. Apple Developer Documentation
2. Swift.org
3. Swift Language Reference / Guide
4. Swift Evolution
5. WWDC
6. Apple sample code
7. Swift Standard Library source where appropriate

Architecture books/papers may supplement conceptual discussion.

---

# 122. Final repository validation

Before declaring the handbook complete, Codex should verify:

```text
[ ] README explains purpose and usage
[ ] SUMMARY contains all chapters
[ ] No empty placeholder chapter
[ ] Markdown links are valid
[ ] Mermaid syntax is reasonable
[ ] Code blocks have correct language tags
[ ] Repeated definitions are minimized
[ ] Glossary exists
[ ] Cross-reference index exists
[ ] Production playbook exists
[ ] Interview playbook exists
[ ] Every phase has a review
[ ] Initial interview question bank is mapped
[ ] Foundation → Senior learning path is coherent
```

---

# 123. Codex work command

When this file is given to Codex, the user may simply request:

> Read `SWIFT_IOS_HANDBOOK_SPECIFICATION.md` completely and treat it as the source of truth. Build the handbook repository according to the specification. Do not redesign the structure. Start by creating the repository skeleton, `README.md`, `SUMMARY.md`, templates, glossary/index placeholders with real structure, and the first complete chapter. Then continue chapter-by-chapter, ensuring each completed chapter passes the specification's quality gate. Never generate superficial placeholder content merely to finish faster.

---

# 124. Final success criterion

The completed handbook must allow a learner to progress coherently from:

```text
What is an Optional?
```

through:

```text
Why does this ViewController not deinit?
```

through:

```text
What actually happens across an await suspension point?
```

through:

```text
Why can actor-isolated code still contain a logical race?
```

and finally:

```text
How should I design a production-grade offline-first mobile feature
with concurrency, caching, synchronization, observability,
testing and failure handling?
```

without treating those topics as disconnected pieces of knowledge.

That is the standard for this project.
