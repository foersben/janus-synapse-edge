---
type: SOP
title: Complex Feature Multi-Agent Lifecycle Workflow
description: Sequential multi-role pipeline for complex documentation and system planning expansions.
tags: [architecture, management, multi-agent, documentation]
---

# Complex Feature Implementation Workflow

This operational checklist outlines how to execute advanced system planning and documentation updates by passing the active context through multiple specialized agent states.

## 📋 Phase 1: Planning (Role: Lead Orchestrator)

1. Read the user's planning or documentation request completely.
2. Adopt the **Lead Orchestrator** role instructions.
3. Propose the documentation outline, target files, and navigation updates in `zensical.toml`.
4. Delegate work packages to Architect and Writer personas.

## 📋 Phase 2: Blueprint Scaffolding (Role: Core System Architect)

1. Adopt the **Core System Architect** instructions.
2. Define the core hardware-software constraints, VRAM resource limits, and network allocations.
3. Scaffold structural outlines and empty Markdown page briefs in `docs/` or under target directories.

## 📋 Phase 3: Textbook Elaboration & Diagramming (Role: Systems Technical Writer)

1. Adopt the **Systems Technical Writer & Detail Engineer** constraints.
2. Elaborate the Architect's blueprints into rich, detailed, academic-grade textbook text (O'Reilly/MIT Press style).
3. Code and embed highly detailed, multi-level Mermaid.js diagrams showing topologies or execution sequence flows.
4. Apply appropriate MkDocs admonitions and ensure strict compliance with Markdown code syntax block styling.

## 📋 Phase 4: Validation & Quality Gate (Role: Documentation QA Validator)

1. Adopt the **Documentation QA Validator & Reviewer** role.
2. Execute the OKF validation script:

   ```bash
   python scripts/validate_okf.py
   ```

3. Run the consistency checker skill to verify that the updates do not introduce any contradictions with the core Janus constraints.
4. Verify markdown formatting and fix any broken links or trailing whitespaces.
