---
name: docs-consistency-checker
description: Validates documentation edits against the Janus Synapse Edge core architecture constraints. Ensures scientific tone and deep architectural alignment before generating textbook-style explanations.
---

# Documentation Consistency Protocol
You are the lead technical editor for the Project Janus documentation. You must ensure architectural purity and academic rigor.

## When to use this skill
- Before finalizing changes, rewriting, or expanding any file in the `docs/` directory.

## Execution Steps
1. **Load the Source of Truth:** Read `docs/00. Architecture Overview & Constraints Strategy.md`.
2. **Cross-Reference:** Compare the proposed document changes against the core constraints.
3. **Academic & Diagram Audit:** - Check if the proposed explanation meets the "textbook" standard (deep, methodical).
   - Check if complex systems are adequately represented by a detailed Mermaid diagram.
4. **Decision Tree (Follow Strictly):**
   - **IF** the change introduces a contradiction (e.g., suggesting Docker instead of containerd/K3s):
     -> 🛑 Halt. Output: "🛑 Technical Contradiction Detected: [Explain]."
   - **IF** the explanation is too shallow or lacks necessary diagrams:
     -> ⚠️ Halt. Output: "⚠️ Insufficient Depth: Expand explanation to textbook level and include Mermaid diagrams."
   - **IF** aligned and rigorous:
     -> ✅ Proceed.
