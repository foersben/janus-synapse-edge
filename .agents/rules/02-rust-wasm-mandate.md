---
type: Rules
trigger: model_decision
description: Enforce Rust-native and WebAssembly sandboxing constraints for all custom tools and runtimes.
---

# Rust & WASM Mandate

This rule file governs all workflows related to creating, modifying, or deploying tools and custom executables within the Janus architecture.

## Core Directives

1. **No Python in Production:**
   * Python is strictly prohibited in the production path.
   * All production components and agent frameworks must be compiled natively in Rust using the **Rig Framework**.
2. **WebAssembly Sandboxing:**
   * Custom agent tools and runtime scripts must be written in Rust, compiled to the WebAssembly target (`wasm32-wasi` or `wasm32-unknown-unknown`), and run inside the **Wasmtime** engine.
   * Spawning Docker containers or native OS processes for ephemeral code execution is strictly prohibited.
3. **Low-Overhead Compilation:**
   * All WASM modules must optimize for size and cold-start latency ($<10$ ms instantiation target).
