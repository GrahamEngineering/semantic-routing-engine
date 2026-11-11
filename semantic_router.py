"""
Semantic Routing Engine (SRE) - Open Source API-to-SDK Interface
Licensed under Apache License, Version 2.0
Cleanroom Implementation - Zero Proprietary Telemetry
"""

import re
import math
import json
import logging
from typing import Callable, Dict, List, Optional, Any, Tuple

logger = logging.getLogger("SemanticRoutingEngine")

class Route:
    def __init__(self, name: str, utterances: List[str], handler: Optional[Callable] = None, metadata: Optional[Dict[str, Any]] = None):
        self.name = name
        self.utterances = utterances
        self.handler = handler
        self.metadata = metadata or {}
        self._tokens_set = [self._tokenize(u) for u in utterances]

    @staticmethod
    def _tokenize(text: str) -> frozenset:
        words = re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())
        return frozenset(words)

class SemanticRouter:
    """
    Bridges high-level natural language API requests (REST, Chat, OpenAI-compatible)
    to low-level SDK execution routines (tools, functions, deterministic state engines)
    using semantic intent matching instead of brittle regex or slash commands.
    """
    def __init__(self, threshold: float = 0.45, local_llm_url: Optional[str] = None):
        self.routes: Dict[str, Route] = {}
        self.threshold = threshold
        self.local_llm_url = local_llm_url

    def add_route(self, route: Route):
        self.routes[route.name] = route
        logger.info(f"Registered route: {route.name} ({len(route.utterances)} reference utterances)")

    def route(self, name: str, utterances: List[str], metadata: Optional[Dict[str, Any]] = None):
        def decorator(func: Callable):
            self.add_route(Route(name=name, utterances=utterances, handler=func, metadata=metadata))
            return func
        return decorator

    def _jaccard_similarity(self, a: frozenset, b: frozenset) -> float:
        if not a or not b:
            return 0.0
        intersection = len(a.intersection(b))
        union = len(a.union(b))
        return float(intersection) / float(union) if union > 0 else 0.0

    def match(self, query: str) -> Tuple[Optional[str], float, Optional[Dict[str, Any]]]:
        """
        Matches user query against registered routes.
        Returns: (route_name, confidence_score, metadata)
        """
        query_tokens = frozenset(re.findall(r'\b[a-zA-Z0-9_]+\b', query.lower()))
        best_route = None
        best_score = 0.0

        for r_name, r_obj in self.routes.items():
            for ref_tokens in r_obj._tokens_set:
                score = self._jaccard_similarity(query_tokens, ref_tokens)
                if any(w in query_tokens for w in ref_tokens):
                    overlap_ratio = len(query_tokens.intersection(ref_tokens)) / max(len(ref_tokens), 1)
                    score = max(score, overlap_ratio * 0.75)

                if score > best_score:
                    best_score = score
                    best_route = r_name

        if best_score >= self.threshold and best_route:
            return best_route, round(best_score, 4), self.routes[best_route].metadata
        return None, round(best_score, 4), None

    def execute(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Matches the query and deterministically invokes the underlying SDK handler.
        """
        matched_name, confidence, metadata = self.match(query)
        if not matched_name:
            return {
                "status": "fallback",
                "query": query,
                "matched_route": None,
                "confidence": confidence,
                "message": "No registered semantic route met the confidence threshold. Delegating to general LLM."
            }

        route_obj = self.routes[matched_name]
        result = None
        if route_obj.handler:
            try:
                result = route_obj.handler(query=query, context=context or {}, metadata=metadata)
            except Exception as e:
                logger.error(f"Error executing handler for {matched_name}: {e}")
                result = {"error": str(e)}

        return {
            "status": "routed",
            "query": query,
            "matched_route": matched_name,
            "confidence": confidence,
            "metadata": metadata,
            "result": result
        }