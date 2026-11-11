# Semantic Routing Engine (SRE)
> **Open Source API <-> SDK Interface for Intent-Driven Agent Architectures**  
> Licensed under the Apache License, Version 2.0

The **Semantic Routing Engine** is a high-speed, deterministic decision and routing layer that connects conversational **APIs** (OpenAI-compatible endpoints, REST, WebSockets) to execution **SDKs** (tools, databases, cluster controllers, and rollback engines).

Instead of forcing users to remember rigid slash-commands (`/ledger`, `/deploy`), the Semantic Routing Engine parses casual, natural language queries (*"show me the ledger thing"*, *"ship it to prod"*, *"go back to where we started"*) and dispatches them deterministically to registered SDK handlers.

---

## Features

- **Blazing Fast**: Sub-10ms evaluation using zero-dependency vector token matching.
- **Drop-in OpenAI Gateway**: Exposes `/v1/chat/completions` so existing AI interfaces can use it immediately.
- **Python SDK Decorators**: Simple `@router.route("route_name", ["utterance 1", "utterance 2"])` interface.
- **Deterministic Tool Dispatch**: Guarantees that recognized business operations trigger strictly verified code paths.
- **Zero Cloud Lock-in**: 100% self-hosted and offline-capable.

---

## Quickstart

### 1. Install & Run
```bash
git clone https://github.com/your-org/semantic-routing-engine.git
cd semantic-routing-engine
python api_gateway.py
```
The gateway will start on `http://0.0.0.0:8089`.

### 2. Test Direct Routing
```bash
curl -X POST http://localhost:8089/v1/route \
  -H "Content-Type: application/json" \
  -d '{"query": "show me the ledger thing"}'
```

### 3. Use in Python
```python
from semantic_router import SemanticRouter

router = SemanticRouter()

@router.route("system_rollback", [
    "go back to where we started",
    "undo that change",
    "revert to previous snapshot"
])
def rollback_handler(query, context, metadata):
    return {"status": "reverted", "target": "state_snapshot_0"}

result = router.execute("can we go back to where we started please?")
print(result)
```

---

## License
Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.