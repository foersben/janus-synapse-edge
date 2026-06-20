# **Project Janus 2026: Architectural Overhaul & Modernization Strategy**

This document outlines the complete transition of the Janus AI cluster from a heavy, multi-language, network-dependent stack to a hyper-optimized, Rust-native, self-healing 2026 architecture.

Designed for a headless Intel i7-14700K / RTX 5070 Ti (Blackwell) / 128GB RAM system, every change strictly adheres to the principles of zero-maintenance, compile-time safety, and hardware-native execution.

## **1\. Orchestration & Execution Layer**

### **1.1 Core Framework Transition**

* **What is replaced:** Heavy Python orchestration frameworks (CrewAI, Agent Zero, NemoClaw) and their cumbersome Dockerized execution environments.
* **How it is changed:** We transition entirely to the **Rig Framework**, compiling all agent logic natively in Rust. Additionally, instead of spawning heavy Docker containers for code sandboxing, tool execution is moved to **WebAssembly (WASM) runtimes** (via Wasmtime or Spin) embedded directly within the Rust binary.
* **Why it is changed:** Python environments introduce massive RAM overhead (2GB+ just for the runtime), unpredictable garbage collection pauses, and fragile dependency management. Docker container orchestration for ephemeral agent tasks is too slow for real-time reflex loops, and ungraceful shutdowns leave fragmented, corrupted container network bridges. WASM sandboxing guarantees instant (microsecond-level) startup, near-zero memory footprint, and mathematically secure isolation that self-cleans on process termination.
* **Expected Outcome:** Sub-millisecond orchestration latency. The entire agentic control plane will consume less than 150MB of RAM, freeing up gigabytes of DDR5 for model weights. WASM tool execution will allow agents to securely compile and run isolated sub-routines in microseconds with 0% risk of orphaned host resources.

## **2\. Inference Core (The Dual-Engine)**

### **2.1 Engine A (Deep Reasoning) Evolution**

* **What is replaced:** PowerInfer relying on experimental activation sparsity (ReLU).
* **How it is changed:** Transition to **llama.cpp** using 4-bit GGUF quantization. Execution is strictly pinned to the 8 physical P-Cores with **Multi-Token Prediction (MTP) Speculative Decoding**. A tiny 1.5B/3B draft model resides in the 5070 Ti's VRAM, while the P-Cores handle the 70B verification pass.
* **Why it is changed:** Modern top-tier 70B models have abandoned ReLU for SwiGLU, breaking PowerInfer's sparsity optimizations. Speculative decoding mathematically bypasses the DDR5 memory bandwidth bottleneck by guessing tokens directly in VRAM and batch-verifying them on the CPU.
* **Expected Outcome:** Sustainable 15-20+ tokens/second on a 70B parameter model operating predominantly out of system DDR5 RAM, without causing thermal throttling or cache-incoherence on the i7-14700K.

### **2.2 Engine B (Reflex & Vision) Unification**

* **What is replaced:** Standard vLLM/SGLang configurations and a separate isolated NemoVision pod for web scraping.
* **How it is changed:** Deployment of a unified **llama.cpp** container utilizing a heterogeneous GPU/CPU split, hosting **Qwen2-VL** to handle both text reflex actions and visual DOM parsing in a single memory space.
* **Why it is changed:** Running separate text and vision models fractures the VRAM pool. By decoupling the vision projection layer (`mmproj`) to execute on system CPU/RAM and keeping the core text layers in VRAM, Qwen2-VL runs within a strict 4.5GB VRAM static fence, protecting the GPU from context memory spikes.
* **Expected Outcome:** Instantaneous visual web-scraping and UI analysis. Engine B will fit perfectly into a fenced ~4.5GB VRAM slice while maintaining blindingly fast tool-calling speeds.

### **2.3 Context Management Optimization**

* **What is replaced:** Standard 8-bit or 16-bit KV Caching.
* **How it is changed:** Implementation of **llama.cpp context capping and prefix caching** configured in the container arguments.
* **Why it is changed:** As agents operate autonomously overnight, their context windows swell massively. Standard KV caches will rapidly consume the VRAM limit of the 5070 Ti, causing a silent OOM (Out of Memory) crash.
* **Expected Outcome:** High-efficiency context preservation. The 7B reflex model will be able to manage up to an 8k context window within its VRAM partition, with the CPU-bound vision encoder offloading raw visual processing overhead.

## **3\. Memory, State & I/O Subsystem**

### **3.1 The Virtualization of Memory**

* **What is replaced:** The external bitemporal SurrealDB GraphRAG system running on the Intel NUC, accessed via a 2.5G network.
* **How it is changed:** Implementation of **Letta (MemGPT framework)** directly into the local Rust/Rig workflow. Letta manages memory virtually (Core, Recall, Archival) directly within the LLM's token-space. The NUC is repurposed purely for cold S3 backup storage and raw transaction logging.
* **Why it is changed:** Querying an external database over a network introduces I/O latency that stalls the GPU during reflex loops. Graph databases are prone to index shattering during ungraceful shutdowns. Token-space memory management is hardware-agnostic and network-free.
* **Expected Outcome:** Zero-latency memory recall. The headless server becomes entirely self-contained for active cognition. If the network bridge to the NUC drops, the agent's immediate execution loop will not silently fail.

### **3.2 Storage I/O Bypass**

* **What is replaced:** Standard Kubernetes Persistent Volumes routing through the standard Linux kernel block layer.
* **How it is changed:** Implementation of **io\_uring** directly in the Rust architecture (using native guest OS bindings inside Talos Linux) to stream Letta's "Archival" memory and llama.cpp GGUF weights straight from the virtualized block devices.
* **Why it is changed:** The standard Linux kernel introduces context-switching overhead when rapidly pulling gigabytes of archival text or model weights. io\_uring allows asynchronous, zero-copy reads, which seamlessly bypasses guest-OS kernel scheduling overhead while letting the host-level AES-NI hardware handle the LUKS decryption transparently.
* **Expected Outcome:** Near-instantaneous cold boots for the 70B model (cutting load times from \~12 seconds to \~4 seconds) and seamless paging of Letta's Archival memory into the Core context window without stalling the LLM.

## **4\. API Gateway & Observability**

### **4.1 High-Performance Declarative Routing**

* **What is replaced:** LiteLLM acting as the primary intelligent router and decision engine.
* **How it is changed:** We transition completely to **TensorZero** as our unified, high-performance, Rust-native gateway. The routing, prompt templating, schema validation, adaptive A/B testing, and provider failovers are defined declaratively in tensorzero.yaml managed via GitOps. Rig acts as the application core, sending structured requests directly to the local TensorZero gateway.
* **Why it is changed:** Python-based LiteLLM adds significant latency and consumes over 2GB of RAM. TensorZero is written from the ground up in Rust, delivering sub-millisecond P99 overhead (\<1ms) and structured, type-safe schema enforcement. It natively integrates with local endpoints and external providers (OpenRouter) with built-in, declarative fallback pipelines.
* **Expected Outcome:** Blazing-fast gateway routing. Elimination of Python runtime memory bloat. Complete decoupling of LLM schema details from the Rig application code, allowing prompt and provider changes to be hot-reloaded declaratively via GitOps without restarting the application.

### **4.2 Zero-Overhead Observability**

* **What is replaced:** The heavy Prometheus/Grafana stack and standard Python logging.
* **How it is changed:** We route TensorZero’s built-in structured inference and feedback traces asynchronously to a **ClickHouse** database hosted on the UPS-backed Intel NUC, while exporting system-level metrics to a highly compressed **VictoriaMetrics** instance. Langfuse/Langsmith is integrated strictly via OpenTelemetry (OTLP) exporting.
* **Why it is changed:** Prometheus is RAM-hungry and write-heavy, contributing to SSD wear on the primary node. ClickHouse is optimized for high-density, analytical queries of prompt logs, keeping the main node's SSDs protected from transaction write wear-and-tear. VictoriaMetrics handles timeseries telemetry with a fraction of Prometheus's RAM footprint.
* **Expected Outcome:** Complete traceability of agent "thought processes" (waterfall traces) and system metrics (VRAM fences, thermal safety throttling) while consuming \<100MB of RAM on the compute node.

## **5\. Autonomous Evolution (The Headless Dream)**

### **5.1 Safe System Optimization**

* **What is replaced:** DSPy code mutation and Woodpecker CI Docker sandbox testing (AlphaEvolve).
* **How it is changed:** Integration of **Nous Hermes Native GEPA (Genetic-Pareto Prompt Evolution)** during Letta's "Sleep-Time Compute" phase. Instead of rewriting raw Rust/Python code, the LLM iteratively evolves its own YAML system prompts and semantic tool descriptions.
* **Why it is changed:** Unsupervised automated fine-tuning (Unsloth) or raw code mutation on a headless server is catastrophic if a bad commit causes an infinite crash loop. Evolving *prompts* in token-space carries zero risk of breaking the compiled execution environment.
* **Expected Outcome:** The system will still get 95% of the performance gains of self-improvement (finding more token-efficient ways to use its tools and structure its memory) but with 0% risk of bricking the server overnight. Changes are safely hot-reloaded via GitOps without flushing the VRAM cache.

## **6\. Model Specialization (Multi-LoRA & Quantization-Aware Training)**

### **6.1 The Quantization-Aware Fine-Tuning Pipeline**

* **What is replaced:** Post-Training Quantization (PTQ) which causes severe reasoning and schema-parsing degradation in local 7B-8B models, and risky automated weight modifications of base models.
* **How it is changed:** Integration of **Axolotl (via Blackwell-targeted Docker images)** running PyTorch's **torchao NVFP4 Quantization-Aware Training (QAT)** backend on the physical P-cores and GPU (VM 1\) during *manually authorized operator maintenance windows*.
* **Why it is changed:** Straight 4-bit models lose significant edge-case capability in complex sequential JSON schemas and parallel tool-calling. QAT trains the LoRA adapter while dynamically simulating the 4-bit (NVFP4) quantization grid. This process allows the adapter to mathematical adjust its weights to recover accuracy degradation before physical quantization takes place.
* **Seed Datasets:** The training is initialized using premier agent datasets:
  1. **Toucan-1.5M:** To master multi-turn, multi-agent trajectories on 495+ real Model Context Protocol (MCP) environments.
  2. **hermes-agent-reasoning-traces:** To inject high-density reasoning steps into the model's inner dialogue.
  3. **When2Call:** To train boundary-awareness, teaching the agent when to call a tool, when to ask follow-up questions, and when an input is outside its capabilities.
* **Expected Outcome:** Super-specialized, highly accurate 7B models that execute with native Blackwell speed while recovering up to 71% of the accuracy degradation typically lost during 4-bit quantization.

### **6.2 Multi-LoRA Hot-Swappable Serving**

* **What is replaced:** Loading multiple distinct 7B models into VRAM simultaneously (causing immediate memory exhaustion), or sequential model loading which introduces 10+ second cold-start latency.
* **How it is changed:** Implementation of **llama.cpp Declarative Adapter Swapping**. We load exactly *one* base model (e.g., Qwen2-VL-7B in GGUF) into Engine B's 4.5GB static VRAM fence, keeping all specialized adapters in system memory.
* **Why it is changed:** The gateway dynamically triggers adapter swaps in system DDR5 memory during tool-calling sequences, loading the required LoRA weights onto the base model without flushing VRAM or causing cold-start model switching latency.
* **Expected Outcome:** Absolute VRAM conservation. We can run dozens of hyper-specialized agent profiles simultaneously within the same 4.5GB VRAM slot, completely neutralizing OOM risks.
