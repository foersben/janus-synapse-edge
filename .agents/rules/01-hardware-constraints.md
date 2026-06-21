---
type: Rules
trigger: model_decision
description: Rules for parsing, respecting, and validating OKF YAML frontmatter and maintaining Project Janus hardware limits.
---

# Hardware Constraints & OKF Validation

This rule file governs all changes to system memory, CPU pinning, and storage configurations.

## Core Directives

1. **Never Propose Exceeding Limits:** Any change to infrastructure must stay within:
   * **RAM:** 128 GB physical limit.
   * **VRAM:** 16 GB physical limit.
   * **CPU Cores:** 28 threads (20 physical cores).
2. **Mandatory 84GB Hugepage Lock:**
   * VM 1 (Talos Tensor Worker) must lock exactly 84 GB for Hugepages (`vm1_hugepages_gb: 84`) to prevent memory fragmentation during model weight loading.
3. **Mandatory 4GB Host Buffer:**
   * The physical host memory buffer must remain $\ge$ 4 GB at all times.
   * Enforced via the formula: `hardware.ram_gb_total - (vm1_ram_gb_total + vm2_ram_gb + host_ram_gb) >= 4`.
4. **OKF Frontmatter Validation:**
   * Every `.md` documentation file must contain valid YAML frontmatter with `type`, `dependencies`, and `exports`.
   * Dynamic variables must use derived templates (e.g., `${vm1_hugepages_gb + vm1_standard_ram_gb}`).
   * Run `just validate` to verify any modifications to documentation before staging.
