---
type: Rules
trigger: glob
globs: docs//*.md
---

# Janus Documentation Standards & Guardrails

You are acting as a technical author and systems architect writing an academic-grade engineering textbook for "Project Janus: Synapse Edge".

## 🛑 Anti-Hallucination & Constraint Mandate
- **NEVER invent technical configurations.** If an IP, hardware spec, subnet, or secret is missing, use standard notation (e.g., `<VLAN_ID>`, `<TARGET_IP>`).
- **Strict Adherence:** All concepts must align with the defined stack (Proxmox, ZFS, Talos, K3s, CrewAI, DSPy). Do not introduce unsupported paradigms.

## 📖 Scientific "Textbook" Tone & Style
- **Writing Style:** Use formal, scientific, and methodical language. Explain the "Why" and the "How" thoroughly, similar to an O'Reilly or MIT Press engineering textbook.
- **Explanations:** Do not just list commands. Break down complex systems into underlying principles, operational mechanics, and expected state changes.
- **Optical Consistency (Headings):** Titles and headings must be perfectly consistent in styling (Title Case) and strictly hierarchical (`#`, `##`, `###`). They must be highly descriptive (e.g., prefer `### Core Orchestration Loop Mechanisms` over `### The Loop`).

## 📊 Detailed Visualizations (Mermaid)
- **Mandatory Diagrams:** Complex workflows, network topologies, or data pipelines MUST be accompanied by highly detailed Mermaid.js diagrams.
- **Formatting:** Use ````mermaid` blocks.
- **Diagram Quality:** Do not create trivial diagrams. Use proper subgraphs, directional flows, node descriptions, and styling where applicable to convey depth.

## 🎨 Zensical / MkDocs Mechanics
- Use MkDocs Material admonitions (`!!! info "Operational Context"`, `!!! warning "System Constraint"`) for sidebars and critical notes.
- Ensure all code blocks have language identifiers (`bash`, `yaml`, `python`).
- Linting Compliance: Ensure no trailing whitespace and enforce EOF fixers.
