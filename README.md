# **🚀 Project Janus: Synapse Edge**

> **[View the Complete Engineering Plan & Live Documentation](<https://foersben.github.io/janus-synapse-edge/>)**

**Project Janus** is a rigorous exercise in **Constraint Engineering**. It serves as a proof-of-concept that datacenter-grade autonomous AI orchestration is achievable on thermally constrained consumer hardware. By leveraging aggressive hardware-software co-design, bi-temporal memory substrates, and a "crash-safe" edge resilience philosophy, this system optimizes the **NVIDIA Blackwell (SM120)** architecture to its absolute limit.

## **🧬 The Meaning Behind the Name (The Mythology)**

The project identity is built on three pillars of the system's design:

- **Janus (The Duality):** Named for the Roman god of transitions and dualities, representing our **Dual-Engine** inference paradigm. The architecture simultaneously hosts a deep-reasoning orchestrator (**PowerInfer 70B**) and a hyper-fast rapid executor (**SGLang 8B**). This duality extends to the "Logical Walls" cryptographically separating multi-tenant profiles.
- **Synapse (The Memory):** Reflects the sophisticated **Dreaming** pipeline. During downtime, the system analyzes logs to forge implicit relationships within a SurrealDB knowledge graph, consolidating memories like a biological brain via the Spectron subsystem.
- **Edge (The Resilience):** Signifies the **Zero-Trust Bare Metal** local network and the distributed **Edge-Tier Brain**. While the main compute host is deliberately "Crash-Safe" (No-UPS), the primary memory and state orchestration are isolated to a battery-backed Intel NUC edge-node.

---

## **📂 The Engineering Plan: 12-Phase Roadmap**

The core of this project is its exhaustive documentation, structured as a sequential engineering specification.

1. **[Physical Foundations](https://foersben.github.io/janus-synapse-edge/01.%20Physical%20Assembly%2C%20BIOS%20%26%20Bare-Metal%20Security/)**: Thermal clearances, 14700K hard-capping, and DMA protection.
2. **[Cryptographic Boundary](https://foersben.github.io/janus-synapse-edge/02.%20Proxmox%20Base%20Installation%20%26%20ZFS%20Encryption/)**: ZFS-native AES-256-GCM encryption with human-in-the-loop cold-boot protocols.
3. **[Hypervisor Optimization](https://foersben.github.io/janus-synapse-edge/03.%20Proxmox%20Kernel%20%26%20Hypervisor%20Optimization/)**: Real-time P-Core pinning and ZFS ARC tuning for IOps-heavy GraphRAG.
4. **[Immutable Orchestration](https://foersben.github.io/janus-synapse-edge/04.%20Virtualization%20%26%20Kubernetes%20%28Talos%20%2B%20K3s%29/)**: Talos Linux & K3s deployment for an immutable, GitOps-managed compute tier.
5. **[The Dual-Engine Paradigm](https://foersben.github.io/janus-synapse-edge/05.%20Core%20AI%20Inference%20Deployment%20%28The%20Dual-Engine%29/)**: Coordinating PowerInfer (70B) and SGLang (8B) via NVFP4 hardware acceleration.
6. **[Bi-Temporal Memory](https://foersben.github.io/janus-synapse-edge/06.%20Data%20Layer%20%26%20Memory%20Substrate/)**: SurrealDB Graph/Vector/Relational hybrid on a battery-backed Edge-Node.
7. **[Traffic Control](https://foersben.github.io/janus-synapse-edge/07.%20API%20Gateway%2C%20Orchestration%20%26%20Network%20Firewall/)**: LiteLLM and n8n ingress/egress policies.
8. **[Agent Synthesis](https://foersben.github.io/janus-synapse-edge/08.%20Agent%20Workflows%20%26%20UI%20Layer/)**: Multi-agent task delegation and AnythingLLM integration.
9. **[Autonomous Dreaming](https://foersben.github.io/janus-synapse-edge/09.%20The%20Autonomous%20Dynamic%20_Idle-Loop_%20%26%20_Dreaming/)**: Knowledge consolidation and evolutionary coding via AlphaEvolve.
10. **[GitOps Lifecycle](https://foersben.github.io/janus-synapse-edge/10.%20Observability%2C%20Telemetry%20%26%20GitOps/)**: Continuous delivery via ArgoCD and real-time telemetry (Langfuse/Prometheus).
11. **[Automated Healing](https://foersben.github.io/janus-synapse-edge/11.%20Disaster%20Recovery%20%26%20Automated%20Healing/)**: The Python Janitor Daemon and recovery from hard power-loss.
12. **[Multi-Tenant Privacy](https://foersben.github.io/janus-synapse-edge/12.%20Multi-Tenant%20Profiles%20%26%20Privacy%20Tiers/)**: Logical isolation of Developer and Psychologist profiles.

---

## **🧬 Architectural Pillars**

### **1. Hardware-Software Co-Design (The Blackwell Strategy)**

We maximize a Micro-ATX thermal envelope (Jonsbo Z20) by strictly fencing resources. The **RTX 5070 Ti** is leveraged for its native **NVFP4 (4-bit floating point)** math, effectively doubling parameter residency and enabling **70B parameter models** to run at interactive speeds on a single consumer GPU.

| Component | Specification | Role & Constraint Strategy |
| :--- | :--- | :--- |
| **Compute** | Intel i7-14700K (28 Threads) | Hard-capped to 180W. P-Cores pinned for AI reasoning; E-Cores for background tasks. |
| **RAM** | 128GB DDR5 Crucial | Talos Guest-OS Hugepages (56GB locked) for PowerInfer cold-neuron spillover. |
| **GPU** | ZOTAC RTX 5070 Ti (16GB) | Blackwell SM120 leveraging NVFP4 acceleration. |
| **Network** | NETGEAR MS308E 2.5G | Prevents "jitter" in interactive chats during high-velocity GraphRAG network traversals. |
| **Edge-Node** | Intel NUC10i5FNH | UPS-backed "Long-Term Memory". Acts as a ZFS RAM Shock Absorber to protect NVMe endurance. |

### **2. The "Dual-Engine" Inference Stack**

Instead of a monolithic approach, the system uses a bifurcated inference pipeline:

- **Engine A (Deep Orchestrator):** **PowerInfer** hosts 70B reasoning models. It maps "hot" neurons to the 11GB VRAM budget and spills "cold" neurons to DDR5, bypassing the PCIe bottleneck via clever neuron-mapping.
- **Engine B (Rapid Executor):** **SGLang** runs 8B models (e.g., Qwen 2.5) with `--mem-fraction-static` for instant, zero-latency tool-calling and function execution.

### **3. Bi-Temporal Memory Substrate**

Standard vector RAG is replaced with a **SurrealDB** graph/vector ledger running on the battery-backed Intel NUC.

- **Hindsight (Vectorize.io)**: Separates objective facts from subjective beliefs into distinct memory networks.
- **Spectron Subsystem**: Forges implicit relationships during "idle hours," consolidating agent memories like a biological brain.

### **4. The Autonomous "Idle-Loop"**

The cluster capitalizes on downtime. When Prometheus detects <5% utilization for 45 minutes, it triggers:

1. **Dreaming**: GraphRAG consolidation and memory pruning on the NUC.
2. **Evolutionary Training (AlphaEvolve)**: The system sandboxes historical failures, uses LLMs to rewrite its own agent Python code, tests it in a Woodpecker CI pipeline, and auto-commits optimized logic to this repository.

---

## **🛡️ Resilience & Zero-Trust Security**

- **Crash-Safe Design**: Because the main server lacks a UPS, it is designed for failure. A custom **Python Janitor Daemon** queries the UPS-backed NUC database on boot, identifies interrupted tasks, and performs a "Nuke & Pave" on corrupted sandboxes to resume work.
- **Air-Gapped Privacy**: LiteLLM acts as a local traffic cop. _Tier 0 (Private)_ profiles are hard-locked to local inference with total egress blocks, ensuring sensitive data never leaves the local 2.5G backbone.
- **GitOps Management**: Every manifest, from Kubernetes ConfigMaps to hardware pinning, is managed by **ArgoCD**, ensuring the entire cluster can be reconstructed from this repository in minutes.

---

## **📂 GitOps Repository Navigation**

The AI landscape moves too fast for manual updates. This Mono-Repo is structured into distinct logical boundaries to ensure dynamic agent updates ("Hot-Reloading") never flush the massive VRAM Cache-Augmented Generation (CAG) memory.

- **/infrastructure**: Cold-Restart files. Includes bare-metal recovery configs like `talos-machineconfig.yaml`.
- **/cluster-tools**: The foundations: ArgoCD manifests, NVIDIA device plugins, and OpenEBS LocalPV storage classes.
- **/apps**: Core execution engines and gateways (PowerInfer, SGLang, LiteLLM, n8n, AnythingLLM, Langfuse).
- **/agents**: High-velocity logic: Python tool scripts, CrewAI swarms, and System Prompts mapped to Kubernetes ConfigMaps for instant hot-reloading.

---

## **🛠️ Getting Started**

To replicate this setup, follow the **[Phase 1 Documentation](<https://foersben.github.io/janus-synapse-edge/01.%20Physical%20Assembly%2C%20BIOS%20%26%20Bare-Metal%20Security/>)**. This is not a "one-click install"; it is a complex infrastructure project requiring physical assembly and kernel-level tuning.

---

> _Project Janus is a demonstration of what is possible when engineering constraints are treated as creative catalysts rather than roadblocks._
