---
type: SOP
description: Systematically transforms draft documentation into a highly detailed, scientific textbook format with complex Mermaid diagrams, without hallucinating architectures.
---

# Title: Optimize Janus Documentation (Academic & Textbook Style)

## Step 1: Context & Source Material Gathering
- Identify the target Markdown document.
- Read the entire document to grasp the core concepts, commands, and intentions.

## Step 2: Technical Consistency Check
- Trigger the `docs-consistency-checker` skill to ensure the concepts align with the Janus baseline.
- Wait for the ✅ signal. (Resolve 🛑 or ⚠️ signals before proceeding).

## Step 3: Textbook Transformation & Refinement
Rewrite the document applying the following standards:
- **Academic Expansion:** Convert bullet points or brief notes into fully articulated paragraphs explaining the underlying engineering principles.
- **Diagrammatic Generation:** Identify at least one core concept or workflow in the document and generate a highly detailed, nested Mermaid diagram (Flowchart, Sequence, or Architecture/C4 style) to visually explain it.
- **Heading Standardization:** Rewrite all headings to be highly descriptive, optically consistent, and logically tiered (H1 -> H2 -> H3).
- **Zensical Styling:** Wrap critical constraints, prerequisites, or operational context in MkDocs Material Admonitions (`!!! abstract`, `!!! danger`, `!!! note`).

## Step 4: Anti-Hallucination Audit
- Review the generated scientific text.
- Ensure that the expanded textbook explanations rely *only* on known computer science/engineering principles applicable to the provided stack (Talos, Proxmox, ZFS, AI Agents).
- Ensure no fake configuration parameters or IPs were generated to fill space.

## Step 5: Output
- Present the optimized, textbook-style document as a code diff for user review.
