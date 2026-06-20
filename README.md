# **🚀 Project Janus: Synapse Edge 2026**

> **[View the Complete Engineering Plan & Live Documentation](<https://foersben.github.io/janus-synapse-edge/>)**

**Project Janus** is a rigorous exercise in **Constraint Engineering**. It serves as a proof-of-concept that datacenter-grade autonomous AI orchestration is achievable on thermally and spatially constrained consumer-grade hardware. By leveraging aggressive hardware-software co-design, local virtualized memory substrates, and a "crash-safe" edge resilience philosophy, this system optimizes the **NVIDIA Blackwell (SM120)** architecture to its absolute limit within a compact 20-liter physical footprint.

---

## **🎥 Technical Deep Dive: The Janus Concept**

> [!TIP]
> **Executive Summary:** This AI-synthesized architectural briefing provides a high-fidelity conceptual summary of Project Janus. It explores the **Constraint Engineering** conflict and the subsequent implementation of the **Dual-Engine inference stack** and **local virtualized memory substrates**.
>
> <div align="center">
> <video src="https://github.com/user-attachments/assets/6bbdf2fa-93d3-4994-b12f-b6944c4dd21f" width="60%" controls>
>   Your browser does not support
> </video>
>
> _Concept Summary generated via NotebookLM • **Technical Tier: Multimodal Infrastructure Synthesis**_
>
> </div>

---

## **🧬 The Meaning Behind the Name (The Mythology)**

The project identity is built on three pillars of the system's design:

- **Janus (The Duality):** Named for the Roman god of transitions, doors, and dualities, representing our **Dual-Engine** inference paradigm. The architecture simultaneously hosts a deep-reasoning planner (**llama.cpp 70B Speculative Decoding**) and a hyper-fast rapid executor (**llama.cpp 8B Heterogeneous Split**). This duality extends to the logical walls cryptographically separating multi-tenant profiles.
- **Synapse (The Memory):** Reflects the sophisticated local **Dreaming** pipeline. During idle phases, the **Letta (formerly MemGPT)** engine consolidates active token-space memory state, summarizing chronological history from the local Recall database and paging entity relationship graphs into the high-density Archival tier. Simultaneously, the **Nous Hermes Native GEPA** engine searches for Pareto-efficient YAML configurations.
- **Edge (The Resilience):** Signifies the **Zero-Trust Bare Metal** local network and the distributed **Edge-Tier Resiliency**. While the main compute host is deliberately "Crash-Safe" (No-UPS), the primary telemetry database is isolated to a battery-backed Intel NUC node, replaying transaction logs on boot to restore the stateless local Letta state.

---

## **📂 The Engineering Plan: 12-Phase Roadmap**

The core of this project is its exhaustive documentation, structured as a sequential engineering specification.

1.  **[Physical Foundations](https://foersben.github.io/janus-synapse-edge/01.%20Physical%20Assembly%2C%20BIOS%20%26%20Bare-Metal%20Security/)**: Thermal clearances, 14700K undervolting, and DMA protection.
2.  **[Cryptographic Boundary & Proxmox Sideloading](https://foersben.github.io/janus-synapse-edge/02.%20Debian%20Substrate%2C%20LUKS%20Encryption%20%26%20Proxmox%20Sideloading/)**: LUKS-native block encryption and Proxmox sideloading with human-in-the-loop protocols.
3.  **[Hypervisor Optimization (Core Pinning)](https://foersben.github.io/janus-synapse-edge/03.%20Proxmox%20Kernel%20%26%20Hypervisor%20Optimization/)**: Real-time P-Core pinning, ZFS ARC tuning, and hugepages configs.
4.  **[Talos Linux & K3s Topology](https://foersben.github.io/janus-synapse-edge/04.%20Virtualization%20%26%20Kubernetes%20%28Talos%20%2B%20K3s%29/)**: Immutable OS deployment for GitOps-managed compute VM.
5.  **[Core AI Inference (The Dual-Engine)](https://foersben.github.io/janus-synapse-edge/05.%20Core%20AI%20Inference%20Deployment%20%28The%20Dual-Engine%29/)**: Coordinating llama.cpp speculative decoding (70B) and llama.cpp CPU/GPU split (8B).
6.  **[Data Layer & Letta Memory](https://foersben.github.io/janus-synapse-edge/06.%20Data%20Layer%20%26%20Memory%20Substrate/)**: Letta cognitive memory virtualisation in local token-space, paged asynchronously via `io_uring`.
7.  **[TensorZero Gateway & Network DMZ](https://foersben.github.io/janus-synapse-edge/07.%20API%20Gateway%2C%20Orchestration%20%26%20Network%20Firewall/)**: High-performance TensorZero gateway routing and secure Rig webhooks.
8.  **[Rig Framework & WASM Sandboxing](https://foersben.github.io/janus-synapse-edge/08.%20Agent%20Workflows%20%26%20UI%20Layer/)**: Compiling Rust-native agents with Rig and spawning transient Wasmtime sandboxes.
9.  **[Autonomous Idle-Loops & GEPA Dreaming](https://foersben.github.io/janus-synapse-edge/09.%20The%20Autonomous%20Dynamic%20_Idle-Loop_%20%26%20_Dreaming/)**: Letta state consolidation and Genetic-Pareto Prompt Evolution (GEPA).
10. **[OTLP Telemetry & GitOps (ArgoCD)](https://foersben.github.io/janus-synapse-edge/10.%20Observability%2C%20Telemetry%20%26%20GitOps/)**: Async OTLP event tracing to ClickHouse on the NUC, and ArgoCD ConfigMap hot-reloading.
11. **[Automated Healing & Disaster Recovery](https://foersben.github.io/janus-synapse-edge/11.%20Disaster%20Recovery%20%26%20Automated%20Healing/)**: Autonomic Rust Janitor Daemon, WASM sandboxes cleanup, and ClickHouse state replay.
12. **[Multi-Tenant Privacy Tiers](https://foersben.github.io/janus-synapse-edge/12.%20Multi-Tenant%20Profiles%20%26%20Privacy%20Tiers/)**: Software-defined isolated Letta sandboxes, Hindsight 2.0 graph filtering, and resource priority classes.

---

## **🧬 Architectural Pillars**

### **1. Hardware-Software Co-Design (The Blackwell Strategy)**

We maximize a Micro-ATX thermal envelope (Jonsbo Z20) by strictly fencing resources. The **RTX 5070 Ti** is leveraged for its native **NVFP4 (4-bit floating point)** math, effectively doubling parameter residency and enabling **70B parameter models** to run at interactive speeds on a single consumer GPU.

| Component | Specification | Role & Constraint Strategy |
| :--- | :--- | :--- |
| **Compute** | Intel i7-14700K (20 Cores) | Hard-capped to 180W. 8 P-Cores pinned for speculative verification; 10 E-Cores (Threads 16-25) with CPU affinity mask `0x03FF0000` for Rig, WASM, and gateway control planes, leaving threads 26-27 reserved for hypervisor decryption and storage overhead. |
| **RAM** | 128GB DDR5 Crucial | Coordinated Dual-Layer Hugepages (84GB locked in Proxmox host, 56GB partitioned in Talos guest) for llama.cpp weights and Letta archival paging. |
| **GPU** | ZOTAC RTX 5070 Ti (16GB) | Blackwell SM120 leveraging NVFP4 acceleration. |
| **Network** | NETGEAR MS308E 2.5G | Prevents latency spikes in interactive loops during high-frequency trace synchronization. |
| **Edge-Node** | Intel NUC10i5FNH | UPS-backed ClickHouse analytical database and timeseries VictoriaMetrics time-series store. |

### **2. The "Dual-Engine" Inference Stack**

Instead of a monolithic approach, the system uses a bifurcated, hardware-pinned inference pipeline:

- **Engine A (Deep Planning):** **llama.cpp** hosts 4-bit GGUF 70B models. It utilizes **Multi-Token Prediction (MTP) Speculative Decoding**, loading a 1.5B/3B draft model inside VRAM to guess tokens, while the physical P-Cores verify guesses against the larger GGUF parameters cached in DDR5.
- **Engine B (Reflexive Execution):** **llama.cpp** runs 8B models (e.g., Qwen2-VL) inside a **4.5GB VRAM static fence**, utilizing a heterogeneous split (CPU-bound vision projection) and declarative adapter swapping.

### **3. Virtualized Cognitive Memory Substrate**

Standard vector RAG is replaced with **Virtualized Cognitive Memory** (Core, Recall, and Archival tiers) driven locally inside the Rig control plane by **Letta**:

- **Local I/O Acceleration (`io_uring`)**: Archival memory blocks and speculative model weights are streamed directly from virtual ZFS 1M recordsizes using zero-copy `io_uring` system calls, bypassing virtualization context-switches.
- **Hindsight 2.0**: Dynamically parses entity relationship graphs locally within the Letta Archival database partitions, executing silent, zero-latency prompt warm-starts.

### **4. The Autonomous "Idle-Loop"**

The cluster capitalizes on downtime. When the TensorZero watcher detects zero traffic and <5% utilization for 45 minutes, it triggers:

1.  **Dreaming**: Letta memory consolidation, paging chronological Recall data into deep Archival tiers.
2.  **Genetic Prompt Evolution (GEPA)**: Operating in Rig/Rust, the agent mutates prompt YAML configurations, runs benchmark sweeps inside secure Wasmtime sandboxes, and commits optimized YAML back to this repository via Gitea/ArgoCD.

---

## **🛡️ Resilience & Zero-Trust Security**

- **Crash-Safe Design**: Because the main server lacks a UPS, it is designed for failure. A custom **Rust Janitor Daemon** runs on boot, terminates stranded Wasmtime process handles, and replays transaction logs from the ClickHouse NUC database to restore the local Letta memory state.
- **Air-Gapped Browsing**: Direct agent-to-web HTTP connections are banned. Scraping is delegated to Playwright inside `outbound-dmz` containers. Rig grabs page screenshots, passing the image buffer to Qwen2-VL (Engine B) for visual DOM parsing inside VRAM, protecting core AI logic from browser-exploit payloads.
- **GitOps Management**: Every manifest is managed by **ArgoCD**. Prompts mutated by GEPA are pushed to `/prompts` and hot-reloaded declaratively by TensorZero in microseconds, preserving static VRAM caches.

---

## **📂 GitOps Repository Navigation**

The AI landscape moves too fast for manual updates. This Mono-Repo is structured into distinct logical boundaries to ensure dynamic agent updates ("Hot-Reloading") never flush the massive VRAM Cache-Augmented Generation (CAG) memory.

- **/infrastructure**: Cold-Restart files. Includes bare-metal recovery configs like `talos-machineconfig.yaml`.
- **/cluster-tools**: The foundations: ArgoCD manifests, NVIDIA device plugins, and OpenEBS LocalPV storage classes.
- **/apps**: Core execution engines and gateways (llama.cpp, TensorZero, AnythingLLM).
- **/agents**: High-velocity logic: WASM tool modules, Rig agent definitions, and System Prompts mapped to Kubernetes ConfigMaps for instant, zero-downtime hot-reloading.

---

## **🛠️ Getting Started**

To replicate this setup, follow the **[Phase 1 Documentation](<https://foersben.github.io/janus-synapse-edge/01.%20Physical%20Assembly%2C%20BIOS%20%26%20Bare-Metal%20Security/>)**. This is not a "one-click install"; it is a complex infrastructure project requiring physical assembly and kernel-level tuning.

---

## **🛠️ The 2026 Architectural Modernization (What & Why)**

Project Janus underwent a complete architectural modernization to transition from a heavy, multi-language, network-dependent stack to a hyper-optimized, Rust-native, self-healing **2026 Synapse Edge** design. The table below outlines the core changes made and the engineering rationale driving each transition:

| What Replaced What | Why It Was Changed (The Engineering Rationale) | Technical Outcome |
| :--- | :--- | :--- |
| **SurrealDB (on NUC)** $\rightarrow$ **Letta Memory (Local)** | Traversing a physical network bridge introduced millisecond latencies that stalled GPU execution. Graph databases suffered index corruption during ungraceful power failures. Letta virtualizes cognitive state locally. | Zero-latency, network-decoupled active memory loops. The Intel NUC is repurposed strictly for cold ClickHouse backups. |
| **ZFS Caching** $\rightarrow$ **Asynchronous `io_uring`** | Standard Linux kernel file operations forced costly CPU context-switches and virtualization scheduling overhead during huge database sweeps. | Zero-copy DMA streams GGUF weights and Letta archival pages at near-native NVMe speeds ($3,500\text{ MB/s+}$) under LUKS block decryption. |
| **CrewAI / Agent Zero** $\rightarrow$ **Rust-native Rig Framework** | Python orchestration stacks consumed $2\text{ GB+}$ of system memory and introduced stop-the-world garbage collection pauses, stalling the reflex loops. | Pinned strictly to the **10 Intel E-Cores (Threads 16–25)** using CPU affinity mask `0x03FF0000` (leaving threads 26-27 reserved for hypervisor LUKS and ZFS overhead), the entire agent control plane executes inside a **$<150\text{ MB}$ RSS memory fence**. |
| **Docker Sandboxing** $\rightarrow$ **WebAssembly (Wasmtime)** | Spawning Docker containers for ephemeral tool execution took seconds, consumed massive RAM, and left corrupted loopback network interfaces on crash. | Confined linear memory sandboxes spin up in **$<10\text{ ms}$**, executing code in microseconds with immediate resource reclamation. |
| **PowerInfer Inference** $\rightarrow$ **llama.cpp Speculative Decoding** | Modern LLMs abandoned ReLU for SwiGLU, making PowerInfer's activation sparsity obsolete. Single-threaded FP16 loading on consumer GPUs is bandwidth-blocked. | Multi-Token Prediction (MTP) speculative decoding (1.5B draft in VRAM, full verification on **8 physical P-Cores**) delivers **$15\text{-}20\text{+ t/s}$** on 70B models. |
| **LiteLLM / n8n Gateways** $\rightarrow$ **TensorZero Rust Gateway** | LiteLLM added heavy memory footprints and execution overhead. Manual JSON/prompt routing logic was hard-coded in Python scripts. | Unified Rust gateway delivers sub-millisecond declarative routing (`tensorzero.yaml`), ConfigMap hot-reloading, and OTLP ClickHouse streams. |
| **NemoVision Visual MCP** $\rightarrow$ **Air-Gapped Playwright + Qwen2-VL** | Direct DOM parsers exposed the cluster to browser exploits. Independent multi-modal OCR pods saturated system VRAM. | Qwen2-VL runs inside Engine B's **$4.5\text{ GB}$ static VRAM fence** using a llama.cpp heterogeneous split to offload vision patches to CPU/RAM. |
| **Python Janitor Daemon** $\rightarrow$ **Autonomic Rust Janitor** | The legacy Python daemon was slow to load and relied on cleaning up Docker networks, risking network fragmentation on boot. | Compiled Rust binary executes WASM process handle cleanups and replays all ClickHouse transaction logs generated since the last daily storage flush. |

---

> _Project Janus is a demonstration of what is possible when engineering constraints are treated as creative catalysts rather than roadblocks._
