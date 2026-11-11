"""
Semantic Routing Engine (SRE) - Python Client SDK
Use this inside agent pipelines, CLI utilities, or Python test suites.
"""

from semantic_router import SemanticRouter, Route

class SREClient:
    def __init__(self, threshold: float = 0.45):
        self.router = SemanticRouter(threshold=threshold)

    def register(self, name: str, utterances: list, metadata: dict = None):
        return self.router.route(name=name, utterances=utterances, metadata=metadata)

    def query(self, text: str, context: dict = None):
        return self.router.execute(text, context=context)

# Example usage:
if __name__ == "__main__":
    client = SREClient()

    @client.register("deploy_production", [
        "ship it to prod",
        "deploy the current release",
        "promote staging to production",
        "release the build"
    ])
    def deploy_handler(query, context, metadata):
        return {"action": "deploy_prod", "message": f"Deployment approved for query: '{query}'"}

    test_queries = [
        "hey man ship it to prod please",
        "can you promote staging to production?",
        "what's the weather like today?"
    ]

    for q in test_queries:
        res = client.query(q)
        print(f"Query: '{q}' -> Status: {res['status']} | Route: {res.get('matched_route')} (Conf: {res['confidence']})")