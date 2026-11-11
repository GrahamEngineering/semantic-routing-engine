"""
Semantic Routing Engine (SRE) - Lightweight FastAPI / WSGI Gateway
Exposes OpenAI-compatible endpoints (/v1/chat/completions) and direct route endpoints (/v1/route)
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from semantic_router import SemanticRouter, Route

router = SemanticRouter(threshold=0.45)

# Example built-in default routes
@router.route("lineage_query", [
    "show me the ledger thing",
    "what is this tracking stuff",
    "view audit ledger",
    "show recent history and changes"
], metadata={"target": "sdk.lineage.get_history"})
def handle_lineage(query, context, metadata):
    return {"action": "open_ledger", "target": metadata.get("target"), "message": "Lineage Engine Triggered"}

@router.route("state_rollback", [
    "go back to where we started",
    "undo that last change",
    "revert to previous stable point",
    "emergency rollback"
], metadata={"target": "sdk.engine.rollback"})
def handle_rollback(query, context, metadata):
    return {"action": "rollback", "target": metadata.get("target"), "message": "Safe-State Rollback Executed"}

@router.route("system_status", [
    "what is the cluster doing",
    "check health status",
    "show running nodes and services",
    "how are the servers"
], metadata={"target": "sdk.cluster.get_status"})
def handle_status(query, context, metadata):
    return {"action": "cluster_status", "target": metadata.get("target"), "message": "Cluster Healthy (3 Nodes Ready)"}

class SREHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._send_json(200, {"status": "healthy", "engine": "Semantic Routing Engine v1.0", "routes": list(router.routes.keys())})
        else:
            self._send_json(404, {"error": "Not Found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length).decode("utf-8")
        data = json.loads(raw_body) if raw_body else {}

        if parsed.path in ["/v1/route", "/route"]:
            query = data.get("query", "")
            resp = router.execute(query, context=data.get("context", {}))
            self._send_json(200, resp)

        elif parsed.path in ["/v1/chat/completions", "/chat"]:
            messages = data.get("messages", [])
            query = messages[-1].get("content", "") if messages else ""
            resp = router.execute(query)
            
            # OpenAI-compatible response wrapper
            openai_resp = {
                "id": "sre-" + str(hash(query) & 0xffffffff),
                "object": "chat.completion",
                "model": "semantic-routing-engine-v1",
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": json.dumps(resp, indent=2)
                    },
                    "finish_reason": "stop"
                }],
                "usage": {"prompt_tokens": len(query.split()), "completion_tokens": 50, "total_tokens": len(query.split()) + 50}
            }
            self._send_json(200, openai_resp)
        else:
            self._send_json(404, {"error": "Endpoint not recognized"})

def run_server(port: int = 8089):
    server = HTTPServer(("0.0.0.0", port), SREHandler)
    print(f"Semantic Routing Gateway listening on http://0.0.0.0:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()