# Lamar PPP OS

### An AI-native operating system for infrastructure

A working prototype exploring how AI could change the way infrastructure developers discover, evaluate, bid, structure, finance and eventually operate PPP projects.

**Live demo:** https://lamar-ppp-os.onrender.com/app

> **Demo environment — public information + synthetic project data. Not Lamar internal data.**

---

## Why I built this

I came across a problem that interested me:

**What changes when AI is treated as part of the operating model of an infrastructure developer — rather than as another chatbot sitting beside it?**

PPP development is unusually suited to this question.

A single opportunity can move through:

**DISCOVER → BID → STRUCTURE → FINANCE → BUILD → OPERATE → LEARN**

But the intelligence created at each stage is often fragmented across documents, models, teams, advisors and systems.

My hypothesis was simple:

> An opportunity should enter the system once.  
> Intelligence about that project should compound throughout its lifecycle.

So instead of writing a strategy deck about what AI might do, I started building the operating system I imagined.

This repository is that experiment.

---

# The Product

Lamar PPP OS currently demonstrates a connected workflow:

**Opportunity Radar**  
↓  
**Document Intelligence**  
↓  
**Bid Agent**  
↓  
**Bid Intelligence**  
↓  
**Project Brain / Deal Room**  
↓  
**Human Decision Gate**

The important part is not any individual screen.

It is the shared state underneath them.

---

## 1. Opportunity Radar

The system begins before an RFP reaches someone's inbox.

A synthetic GCC infrastructure opportunity universe is scored across factors such as:

- strategic fit
- sector fit
- commercial attractiveness
- financing readiness
- delivery confidence
- operating resilience
- risk-adjusted pursuit quality

The objective is not to let AI decide what Lamar should pursue.

It is to continuously surface where human attention may have the highest value.

---

## 2. Document Intelligence

Once an opportunity moves into investigation, a **Document Agent** processes the tender package.

The demo tender contains:

- 7 synthetic tender documents
- 486 pages
- 22 analyzed sections

The agent converts unstructured tender material into structured project intelligence:

- requirements
- obligations
- key dates
- risks
- clarifications
- evidence references

Every extracted conclusion retains its source evidence.

The system is therefore designed around:

**Evidence → Interpretation → Structured State**

rather than:

**Document → Chat Answer**

---

## 3. Bid Intelligence

The **Bid Agent** reasons over the structured tender intelligence.

For the demo water PPP, it identifies issues including:

- USD 10 million bid security
- minimum equity commitment
- 36-month COD schedule
- 96% annual availability requirement
- residual energy-price exposure
- long-lead desalination equipment

It then creates governed workstreams such as:

- Financing & Security
- EPC Schedule Challenge
- Commercial Risk Allocation
- Authority Clarifications

The current deterministic evaluation produces:

**Bid Readiness Score: 81 / 100**

**Recommendation: CONDITIONAL PURSUE**

The recommendation is deliberately not an approval.

---

# The Project Brain

The core architectural idea is the **Project Brain**.

Instead of each agent producing an isolated answer, agents read from and write to shared project state.

The Project Brain stores objects such as:

- opportunities
- documents
- requirements
- obligations
- risks
- financial assumptions
- milestones
- decisions
- evidence
- agent runs
- relationships
- approvals

This allows intelligence created in one workflow to become context for another.

For example:

**Tender evidence**  
→ creates a **contractual requirement**  
→ which becomes a **bid issue**  
→ which creates a **workstream**  
→ which may change a **financial assumption**  
→ which may affect a **human investment decision**

The system remembers not only **what** it knows.

It is designed to remember **why**.

---

# Deal Room

The Deal Room exposes the shared Project Brain.

In the current demo it contains:

- 19 shared project records
- 34 evidence references
- 2 specialist agent runs
- 4 human decision gates
- a connected relationship graph

Individual intelligence records can be inspected to see:

- their source
- evidence
- ownership
- approval status
- connected Project Brain records
- causal relationships

This makes agent reasoning inspectable rather than invisible.

---

# Agent Architecture

Not everything should be an agent.

The architecture intentionally separates different kinds of work.

| Capability | System |
|---|---|
| Interpret documents | LLM / Document Agent |
| Reason across project state | Specialist Agents |
| Financial calculations | Deterministic Python |
| Compliance checks | Rules |
| Structured project state | Database / Project Brain |
| Semantic document retrieval | Vector Retrieval |
| Project relationships | Graph |
| Visual / site intelligence | Vision Models |
| Workflow orchestration | Agents |
| Consequential decisions | Humans |

The principle is:

> **LLMs interpret. Engines calculate. Rules constrain. Agents coordinate. Humans authorize.**

---

# Human Governance

The prototype deliberately prevents the AI layer from representing consequential recommendations as approved decisions.

Examples requiring human authority include:

- Bid / No-Bid
- contractual commitments
- investment approval
- financing commitments
- engineering decisions
- operating decisions

The Project Brain can preserve machine recommendations.

It cannot convert them into human authorization.

**AI recommends. Humans authorize.**

---

# Financial Twin

The repository also contains a deterministic infrastructure financial engine.

The demo model supports:

- capex
- debt/equity structure
- interest rate
- debt tenor
- concession period
- revenue
- opex
- growth assumptions
- debt service
- DSCR
- equity cash flows
- NPV
- IRR

This matters because the long-term system should connect operational intelligence to economic consequences.

A construction risk should not simply be labelled **HIGH**.

Eventually the system should be able to reason:

**Delay risk**  
→ **COD scenario**  
→ **revenue timing**  
→ **debt-service consequence**  
→ **equity IRR / NPV impact**  
→ **decision**

---

# Where this could go

The current prototype focuses on the front of the PPP lifecycle.

The same Project Brain architecture can extend into:

### STRUCTURE
Contract obligations, risk allocation, consortium responsibilities and financing assumptions.

### FINANCE
Scenario modelling, lender requirements, covenants, sensitivities and investment committee intelligence.

### BUILD
Schedule intelligence, procurement signals, change orders, contractor performance and construction risk.

### OPERATE
Asset performance, availability, energy consumption, maintenance and contractual deductions.

### LEARN
Institutional memory across projects.

Over time, the system could answer questions such as:

> We have seen this risk before. What happened?

or:

> Which assumptions made during bidding eventually proved wrong during operations?

That is where the Project Brain becomes more valuable with every project.

---

# Current Architecture

```text
                     ┌──────────────────────┐
                     │  Opportunity Radar   │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │    Document Agent    │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │  Document Intelligence│
                     └──────────┬───────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │                        │
                    │     PROJECT BRAIN      │
                    │                        │
                    │ Evidence               │
                    │ Requirements           │
                    │ Obligations            │
                    │ Risks                  │
                    │ Decisions              │
                    │ Agent Runs             │
                    │ Relationships          │
                    │ Approvals              │
                    │                        │
                    └───────────┬────────────┘
                                │
                  ┌─────────────┼─────────────┐
                  │             │             │
                  ▼             ▼             ▼
             Bid Agent     Finance Engine   Risk Engine
                  │             │             │
                  └─────────────┼─────────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │      Deal Room       │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │ Human Decision Gate  │
                     └──────────────────────┘
```

---

# What is actually implemented

This is not a Figma concept.

The repository contains working implementations for:

- FastAPI backend
- React + TypeScript frontend
- Opportunity scoring engine
- Synthetic GCC infrastructure opportunity universe
- Synthetic PPP tender package
- Evidence-first Document Agent
- Structured document intelligence
- Deterministic Bid Agent
- Bid readiness evaluation
- Bid issue generation
- Bid workstream generation
- Persistent shared Project Brain
- Agent run observability
- Project Brain relationship graph
- Causal record inspection
- Human approval states
- Deterministic financial engine
- Risk and scenario engines
- Executive brief engine
- Automated backend tests
- Automated frontend build validation
- GitHub Actions CI

---

# Technology

### Backend

- Python
- FastAPI
- Pydantic
- deterministic domain engines
- pytest

### Frontend

- React 19
- TypeScript
- Vite
- Lucide

### Architecture direction

A production implementation could extend the current domain architecture with:

- PostgreSQL for persistent structured state
- object storage for project documents
- vector retrieval for evidence
- graph persistence for project relationships
- LLM providers for interpretation/reasoning
- vision models for construction/site intelligence
- project and financial system integrations

The prototype intentionally avoids pretending these integrations exist when they do not.

---

# Run locally

### Backend

```bash
pip install -r requirements.txt
uvicorn lamar_os.api.app:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Tests

```bash
pytest -v
```

### Executive brief demo

```bash
python -m demo.executive_brief
```

---

# Why this repository exists

This is not a Lamar product.

It is an independent prototype inspired by a public problem statement and built using public information and synthetic project data.

I built it because I wanted to demonstrate something more useful than saying:

> “I am interested in AI and infrastructure.”

I wanted to show how I approach an unfamiliar industry:

**learn the system → form a thesis → break it into workflows → build → test → connect the pieces → ship.**

There are certainly assumptions here that would change after sitting with the people who actually develop, finance, construct and operate these projects.

That is partly the point.

The prototype is not intended to prove that I already know Lamar's business better than Lamar.

It is intended to show what I would bring into the room on day one:

**curiosity, structured thinking, speed and the ability to build.**

---

## Demo Notice

**DEMO ENVIRONMENT — PUBLIC INFORMATION + SYNTHETIC PROJECT DATA. NOT LAMAR INTERNAL DATA.**

This is an independent prototype and is not affiliated with, commissioned by, or endorsed by Lamar Holding.
