# **🚀 Project Janus: Synapse Edge**

**Mission:** To prove that datacenter-grade autonomous AI orchestration is possible on thermally constrained consumer hardware through aggressive constraint engineering, bi-temporal memory substrates, and a "crash-safe" edge resilience philosophy.

### **🧬 The Meaning Behind the Name**

The project identity is built on three pillars of the system's design:

* **Janus (The Duality):** Named for the Roman god of transitions, representing the **Dual-Engine** inference paradigm. The architecture simultaneously hosts a deep-reasoning orchestrator (**PowerInfer 70B**) and a hyper-fast rapid executor (**SGLang 8B**) on a single RTX 5070 Ti. This duality extends to the "Logical Walls" cryptographically separating the Developer (ns: architect) and Psychologist (ns: partner) multi-tenant profiles.  
* **Synapse (The Memory):** Reflects the sophisticated **Dreaming** pipeline. During downtime, the system analyzes logs to forge implicit relationships within a SurrealDB knowledge graph, consolidating memories like a biological brain via the Spectron subsystem.  
* **Edge (The Resilience):** Signifies the **Zero-Trust Bare Metal** local network and the distributed **Edge-Tier Brain**. While the main compute host is deliberately "Crash-Safe" (No-UPS), the primary memory and state orchestration are isolated to a battery-backed Intel NUC edge-node.

## **🖥️ Hardware Constraints & Compute Profile**

This server maximizes a Micro-ATX thermal envelope (Jonsbo Z20) by strictly fencing resources and offloading database IOps to a dedicated Edge-Node.

| Component | Specification | Role & Constraint Strategy |
| :---- | :---- | :---- |
| **Compute** | Intel i7-14700K (28 Threads) | BIOS hard-capped to 180W. P-Cores (0-15) pinned for real-time VM reasoning; E-Cores (16-25) for background orchestrators. |
| **RAM** | 128GB DDR5 Crucial | Enables 70B model residency via Talos Guest-OS Hugepages (56GB locked). |
| **GPU** | ZOTAC RTX 5070 Ti (16GB) | Blackwell SM120 architecture leveraging native NVFP4 (4-bit floating point) hardware acceleration. |
| **Network** | NETGEAR MS308E 2.5G | Prevents "jitter" in interactive chats during high-velocity GraphRAG network traversals. |
| **Edge-Node** | Intel NUC10i5FNH | UPS-backed "Long-Term Memory". Acts as a ZFS RAM Shock Absorber to protect NVMe endurance. |

## **🧠 Software Architecture & The "Dual-Engine"**

Instead of monolithic models, this cluster uses a highly optimized, bifurcated inference stack running on an immutable **Talos Linux \+ K3s** Kubernetes cluster.

* **Engine A (Deep Orchestrator):** Uses **PowerInfer** for 70B reasoning models quantized to NVFP4. It maps "hot" neurons to an 11GB VRAM budget and spills "cold" neurons to the DDR5 RAM, bypassing the PCIe bottleneck.  
* **Engine B (Rapid Executor):** Uses **SGLang** fenced with \--mem-fraction-static to run 8B models (e.g., Qwen 2.5) natively in the remaining \~4.5GB VRAM for instant, zero-latency tool-calling.

### **🗄️ The Bi-Temporal Memory Substrate**

Standard vector RAG is insufficient for autonomy. We utilize **SurrealDB** (Graph/Relational/Vector) acting as an append-only ledger on the Intel NUC. **Hindsight** (by Vectorize.io) runs as a local MCP container, separating objective facts from subjective beliefs into distinct memory networks, permanently curing agent "amnesia."

### **💤 The Autonomous "Idle-Loop"**

The system utilizes an Event-Driven architecture to capitalize on downtime. If Prometheus detects \<5% utilization for 45 minutes, it triggers:

1. **Dreaming (SurrealDB/Spectron):** GraphRAG background connection and memory consolidation on the NUC.  
2. **Training (AlphaEvolve/DSPy):** The main server sandboxes historical tasks, uses LLMs to rewrite agent Python source code, tests it in a Woodpecker CI pipeline, and auto-commits optimized code to the local Git repository.

## **🛡️ Zero-Trust Security & Disaster Recovery**

* **Bare-Metal Air-Gap:** The Proxmox host utilizes ZFS Native Encryption (AES-256-GCM). It requires a physical "Human-in-the-loop" USB keyboard passphrase upon cold boots. No remote decryption is permitted.  
* **Network DMZ & Egress Tiers:** **LiteLLM** acts as the internal traffic cop. *Tier 0 (Private)* profiles are hard-locked to local inference with total egress blocks. External web-scraping is strictly delegated to the **NemoVision** MCP pod, trapped in an outbound-only Kubernetes namespace.  
* **Automated Healing:** Because the main server lacks a UPS, a custom **Python Janitor Daemon** runs on boot. It queries the infallible UPS-backed NUC database for tasks marked as RUNNING during the power loss, forcefully executes a "Nuke & Pave" on the corrupted Docker sandboxes, and cleanly resumes the workflow.

## **📂 GitOps Repository Navigation**

The AI landscape moves too fast for manual updates. This Mono-Repo is managed entirely by **ArgoCD**. It is structured into distinct logical boundaries to ensure dynamic agent updates ("Hot-Reloading") never flush the massive VRAM Cache-Augmented Generation (CAG) memory.

* **/infrastructure**: Cold-Restart files. Includes bare-metal recovery configs like talos-machineconfig.yaml.  
* **/cluster-tools**: The foundations: ArgoCD manifests, NVIDIA device plugins, and OpenEBS LocalPV storage classes.  
* **/apps**: Core execution engines and gateways (PowerInfer, SGLang, LiteLLM, n8n, AnythingLLM, Langfuse).  
* **/agents**: High-velocity logic: Python tool scripts, CrewAI swarms, and System Prompts mapped to Kubernetes ConfigMaps for instant hot-reloading.

