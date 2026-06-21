# Project Janus: Synapse Edge 2026 - Operations Manual

This document outlines the core architectural boundaries, hardware constraints, software mandates, and validation principles governing Project Janus. As the autonomous maintainer (Synapse Edge Architect), all future actions must strictly align with these parameters.

---

## 1. Immutable Hardware & Memory Constraints

Operating within the thermal and spatial limits of a 20-liter Micro-ATX chassis (Jonsbo Z20) requires absolute resource fencing. The system enforces strict physical partitions:

### 1.1 CPU Core & Thread Partitioning

The Intel i7-14700K (20 Cores / 28 Threads) is hard-capped to **180W PL1/PL2** in the BIOS and divided as follows:

* **Performance-Cores (8 Cores / 16 Threads):** Allocated exclusively to **VM 1 (Talos Tensor Worker)** to verify guesses in speculative decoding.
* **Efficient-Cores (10 Threads / Threads 16–25):** Fenced with CPU affinity mask `0x03FF0000` for the Rust control plane (Rig/TensorZero) and transient WASM sandboxes.
* **Hypervisor Overhead (Threads 26-27):** Reserved exclusively for hypervisor operations, LUKS decryption, and ZFS I/O tasks.

### 1.2 System RAM Allocation (128 GB DDR5)

Memory allocation is meticulously partitioned to enforce a **4 GB unallocated physical buffer** at all times to prevent host-level out-of-memory (OOM) panic:

* **VM 1 (Talos Tensor Worker):** **88 GB** total (84 GB locked Hugepages + 4 GB standard pageable RAM).
* **VM 2 (Brain Worker):** **24 GB** standard RAM.
* **Host OS Overhead:** **12 GB** (ZFS ARC max is capped at 8.0 GB to protect host stability).
* **Safety Cushion:** $\ge$ **4 GB** must remain completely unallocated ($128 - (88 + 24 + 12) = 4$ GB).

### 1.3 GPU VRAM Partitioning (16 GB GDDR7)

The ZOTAC RTX 5070 Ti (Blackwell SM120) utilizes hardware-accelerated **NVFP4 (4-bit floating point)** math to execute large parameter models within a 16 GB envelope:

* **Engine A (Deep Planning 70B):** **11.5 GB** VRAM allocated for speculative drafting, while GGUF verify weights are cached in DDR5.
* **Engine B (Reflexive Execution 7B):** **4.5 GB** VRAM static fence. Vision encoder projection is offloaded to system CPU/RAM (utilizing 2.0 GB of the Hugepages pool via Kubelet) to protect the VRAM limit.

### 1.4 Dual-Disk ZVOL Storage Topology

To prevent ZFS write-amplification and drive fragmentation on the Seagate FireCuda NVMe, VM 1 is provisioned with two strictly segregated virtual disks:

1. **OS Disk (30 GiB):** Formatted with default `volblocksize=16K` for Talos system logs and container states.
2. **AI Data Disk (1198 GiB):** Formatted strictly with `volblocksize=1M` for weights and Letta's asynchronous `io_uring` database streams.

---

## 2. No-Python Production Mandate

To guarantee sub-millisecond orchestration latency and eliminate runtime overhead, Python is strictly banned from production control paths:

* **Rust-Native Control Plane:** All orchestrators, gateways (TensorZero), and agents are built using the **Rig Framework**, operating within a $<150$ MB RSS memory fence (replacing resource-heavy Python frameworks).
* **WASM Sandboxing:** Any custom tools or executable agent code must be compiled to WebAssembly (WASM) and run inside isolated **Wasmtime** runtimes. Sandboxes must instantiate in $<10$ ms and reclaim linear memory immediately on termination.

---

## 3. Open Knowledge Format (OKF) Validation

The entire system architecture is governed by YAML frontmatter blocks embedded in markdown files (`docs/*.md`).

* **Topological Solver:** System changes must be mathematically verified via `python scripts/validate_okf.py`. This script builds a DAG of dependencies, resolves derived template expressions (e.g., `${vm1_hugepages_gb + vm1_standard_ram_gb}`), and validates assertions.
* **Strict Preservation Rule:** The agent must **only** modify frontmatter metadata variables and checks. Under no circumstances may body text below the `---` divider be altered, summarized, or removed.

---

## 4. Stateless Compute vs. Stateful Edge-Node Split

Janus operates under a decoupled, crash-safe distributed resilience topology:

* **Stateless Compute Node (Jonsbo Z20):** Has no UPS. Operates with an immutable operating system (Talos) and declarative GitOps (ArgoCD). On boot, the Rust Janitor Daemon purges stale WASM handles and reconstructs Letta memory state from cold NUC ledger replays.
* **Stateful Edge-Node (Intel NUC):** Connected to an **Eaton 3S 550 UPS**. Hosts ClickHouse (highly compressed columnar trace logs) and MinIO. Decoupled telemetry is streamed asynchronously over a 2.5G network loop to prevent SSD write wear on the compute NVMe.
