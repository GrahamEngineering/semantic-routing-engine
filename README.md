# Semantic Routing Engine (SRE)
> **Open Source API &harr; SDK Interface for Intent-Driven Agent Architectures**  
> Licensed under the Apache License, Version 2.0  
> **Release:** v1.1.0 (The "Chef's Kiss" Interactive Edition)

The **Semantic Routing Engine** is an ultra-fast, deterministic decision-making interface designed to bridge casual, messy human intent ($human_1$) into rigid machine execution ($math_1$).

Instead of forcing users or developers to memorize brittle slash commands (`/ledger`, `/rollback`, `/deploy`), the engine evaluates natural conversational speech (*"show me the ledger thing"*, *"can we undo that last change"*, *"ship to prod"*) and dispatches them deterministically to registered SDK tools in **sub-10ms**—running entirely on local CPU with **zero GPU requirements and zero cloud tether**.

---

## ⚡ Live & Interactive Demo (v1.1)

You can test the engine live in your browser:
* **Live Web Instance:** [https://didyoulosetheplot.com](https://didyoulosetheplot.com)
* **Practical Implementations & Prior Art Vault:** [https://didyoulosetheplot.com/implementations.html](https://didyoulosetheplot.com/implementations.html) (or locally via [`demo/implementations.html`](demo/implementations.html))
* **Local Offline Cockpit:** Double-click [`demo/index.html`](demo/index.html) in any browser.

### Key Interactive Features in the Cockpit:
1. **Zero-GPU Intent Evaluation:** Pure client-side token vector overlap and Jaccard scoring evaluating in `<3ms`.
2. **"What Are You?" Probe:** Ask the engine what it is, and it explains its deterministic translation role and why $human_1 \neq math_1$.
3. **Voice / Mic Ingress:** Tap 🎙️ to use speech-to-intent routing via browser speech recognition.
4. **Visual Ingress (Camera):** Tap 📷 to activate local camera streams with guaranteed local privacy.
5. **Zen Mode / Stash HUD:** Click **"Stash HUD"** to fade the guiding interface away into a clean, distraction-free workspace.

---

## 🏛️ The Core Architectural Theorem

$$\text{human}_1 \neq \text{math}_1$$

Traditional computing demands that humans think like compilers. When an operator is tired, multi-tasking, or operating under high cognitive load, forcing them to type rigid syntax (`/admin rollback --hard`) leads to human error.

The Semantic Routing Engine acts as an adaptive cognitive impedance matcher:
* It starts calibration at baseline confidence ($60\%$).
* It identifies the operator's persona (Mathematician, VMware Sysadmin, Tired Engineer).
* If ambiguous, it asks exactly **1–2 targeted disambiguation questions**.
* It locks in at **98.2% asymptotic convergence** (preserving the 1.8% vigilance margin).

---

## 🚀 Quickstart

### 1. Zero-Dependency Python SDK
```python
from semantic_router import SemanticRouter

router = SemanticRouter(threshold=0.45)

@router.route("system_rollback", [
    "go back to where we started",
    "undo that last change",
    "revert to previous snapshot"
])
def rollback_handler(query, context, metadata):
    return {"status": "reverted", "target": "state_snapshot_0"}

# Test query
res = router.execute("can we undo that last change please?")
print(res)
# -> {'status': 'routed', 'matched_route': 'system_rollback', 'confidence': 0.884, ...}
```

### 2. Standalone HTTP / OpenAI Gateway
```bash
python api_gateway.py
```
Exposes drop-in endpoints on port `8089`:
* `POST /v1/route`: Direct semantic routing.
* `POST /v1/chat/completions`: Full OpenAI-compatible chat endpoint with deterministic tool dispatch.

---

## 📦 What Happens Without a GPU?
**It runs even faster.**  
The core router uses zero-dependency token vector mathematics and set intersection theorems ($Jaccard(Q, U)$). It runs with sub-3ms latency and `<15MB` RAM footprint on an ancient laptop or Raspberry Pi. GPUs are completely optional and only used if you choose to bind heavy local LLMs like Qwen or LLaMA.

---

## 🛡️ Downstream Practical Applications & Defensive Prior Art

Want to see how downstream systems consume the real-time semantic and affective telemetry vectors emitted by this engine?

Explore our dedicated **[Defensive Publications & Prior Art Disclosures](https://github.com/GrahamEngineering/defensive-publications)** vault. It documents real-world reference architectures, mathematical formulations, and UI flight deck integrations built directly on top of the Semantic Routing Engine—published openly under Apache 2.0 to establish irrevocable prior art (35 U.S.C. § 102) and protect freedom to operate against patent trolls:

* **[DISC-001: Affective Telemetry Modulation (The German House Dynamic Invariant)](https://github.com/GrahamEngineering/defensive-publications/blob/main/disclosures/001-affective-canvas-german-house.md)**: Real-time UI modulation where canvas borders, pulsing frequencies, and color palettes dynamically attune to human vocal stress, urgency, and colloquial prompts (bridging the *"Phone Guy / Monkey Brain"* intuition to the *"Super-Brain"* mathematical execution).
* *(More disclosures staging continuously...)*

---

## 📄 License
Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.