---
type: Rules
trigger: model_decision
description: Invoke this protocol whenever the user requests a "global documentation update", "architecture refactor", "schema upgrade", or changes affecting more than 3 interdependent markdown/configuration files.
---

# SKILL: The 3-Phase Architecture Refactor Protocol

**Trigger:** Invoke this protocol whenever the user requests a "global documentation update", "architecture refactor", "schema upgrade", or changes affecting more than 3 interdependent markdown/configuration files.

**Core Philosophy:** LLMs hallucinate variables and break dependency chains if forced to mass-edit multiple files in a single prompt. You MUST execute widespread changes in these 3 strict, sequential phases. You must STOP and ask for user approval between each phase.

### Exception: The Surgical Strike Bypass

If the user provides explicit, pre-calculated fixes (exact file names, the exact contradictions, and the exact resolutions) AND the request is not changing the global schema structure, treat the prompt as a "Surgical Strike."

1. Bypass Phase 1 (State Mapping) and Phase 2 (Tooling Upgrade).
2. Proceed immediately to Phase 3.
3. Apply the specific text/YAML edits, run `just validate`, and report the final status.

## PHASE 1: Discovery & State Mapping (Read-Only)

1. Do not modify any files.
2. Read all target files. Parse their current state, frontmatter, and dependencies.
3. Generate or update a state map file in `.agents/memory/` (e.g., `architecture_state_map.md`).
4. In this map, explicitly write out the Dependency Tree (what relies on what) and the Current Variables.
5. Identify logical gaps between the user's request and the current state.
6. **STOP.** Output: *"Phase 1 Complete. State map updated. Please approve the logic before I write validation scripts."*

## PHASE 2: Tooling & Validation Upgrade

1. Do not modify the target text files yet.
2. If the user's request introduces new constraints (e.g., a new OKF format, new math, or new YAML rules), update the CI/CD scripts FIRST.
3. Rewrite the relevant python/bash scripts (e.g., `scripts/validate_okf.py`) to support the new logic.
4. Run the validation script on the *existing* files to ensure it catches the current errors.
5. **STOP.** Output: *"Phase 2 Complete. Tooling upgraded. Please approve before I initiate the mass refactor."*

## PHASE 3: The Mass Refactor & Self-Correction

1. Methodically update the target files one by one.
2. **STRICT PRESERVATION:** Never summarize, rephrase, or alter markdown body text unless explicitly instructed. Only touch the targeted variables/frontmatter.
3. Once all files are updated, automatically run the validation script (e.g., `just validate`).
4. If the script fails, you must autonomously read the error loop, self-correct the variables, and re-run the script until a perfect pass state is achieved.
5. **STOP.** Output: *"Phase 3 Complete. Refactoring finished and mathematically validated."*
