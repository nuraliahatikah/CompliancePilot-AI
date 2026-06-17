import logging
import re
from typing import Any

from app.config import get_settings
from app.data.regulations import MALAYSIAN_REGULATIONS

logger = logging.getLogger(__name__)
settings = get_settings()


class RAGService:
    """Vector retrieval over Malaysian Employment Act 1955 and PDPA regulations."""

    COLLECTION_NAME = "malaysian_compliance"

    def __init__(self) -> None:
        self._client = None
        self._collection = None
        self._initialized = False
        self._use_chroma = True
        self._fallback_docs = MALAYSIAN_REGULATIONS

    def initialize(self) -> None:
        if self._initialized:
            return

        settings.chroma_path.mkdir(parents=True, exist_ok=True)

        try:
            import chromadb
            from chromadb.config import Settings as ChromaSettings

            self._client = chromadb.PersistentClient(
                path=str(settings.chroma_path),
                settings=ChromaSettings(anonymized_telemetry=False),
            )
            self._collection = self._client.get_or_create_collection(
                name=self.COLLECTION_NAME,
                metadata={"description": "Malaysian Employment Act 1955 and PDPA"},
            )
            if self._collection.count() == 0:
                self._seed_collection()
            self._initialized = True
            logger.info("ChromaDB initialized with %d documents", self._collection.count())
        except Exception as exc:
            logger.warning("ChromaDB unavailable, using keyword fallback: %s", exc)
            self._use_chroma = False
            self._initialized = True

    def _seed_collection(self) -> None:
        ids = [f"reg_{i}" for i in range(len(MALAYSIAN_REGULATIONS))]
        documents = [r["content"] for r in MALAYSIAN_REGULATIONS]
        metadatas = [
            {
                "regulation": r["regulation"],
                "section": r["section"],
                "source": r["source"],
            }
            for r in MALAYSIAN_REGULATIONS
        ]
        self._collection.add(ids=ids, documents=documents, metadatas=metadatas)

    def query(self, query_text: str, top_k: int = 5) -> list[dict[str, Any]]:
        self.initialize()

        if self._use_chroma and self._collection is not None:
            try:
                results = self._collection.query(query_texts=[query_text], n_results=top_k)
                parsed: list[dict[str, Any]] = []
                if results and results.get("documents"):
                    for i, doc in enumerate(results["documents"][0]):
                        metadata = results["metadatas"][0][i] if results.get("metadatas") else {}
                        distance = results["distances"][0][i] if results.get("distances") else 0.5
                        relevance = max(0.0, min(1.0, 1.0 - distance))
                        parsed.append(
                            {
                                "content": doc,
                                "source": metadata.get("source", "Unknown"),
                                "regulation": metadata.get("regulation", "Unknown"),
                                "section": metadata.get("section", "Unknown"),
                                "relevance_score": round(relevance, 4),
                            }
                        )
                return parsed
            except Exception as exc:
                logger.warning("Chroma query failed, falling back: %s", exc)

        return self._keyword_search(query_text, top_k)

    def _keyword_search(self, query_text: str, top_k: int) -> list[dict[str, Any]]:
        query_terms = set(re.findall(r"\w+", query_text.lower()))
        scored: list[tuple[float, dict[str, str]]] = []

        for reg in self._fallback_docs:
            text = f"{reg['content']} {reg['section']} {reg['regulation']}".lower()
            text_terms = set(re.findall(r"\w+", text))
            overlap = len(query_terms & text_terms)
            if overlap > 0:
                score = overlap / max(len(query_terms), 1)
                scored.append((score, reg))

        scored.sort(key=lambda x: x[0], reverse=True)
        results: list[dict[str, Any]] = []
        for score, reg in scored[:top_k]:
            results.append(
                {
                    "content": reg["content"],
                    "source": reg["source"],
                    "regulation": reg["regulation"],
                    "section": reg["section"],
                    "relevance_score": round(min(score, 1.0), 4),
                }
            )
        return results

    def get_all_regulations(self) -> list[dict[str, str]]:
        return list(MALAYSIAN_REGULATIONS)

    def get_stats(self) -> dict[str, Any]:
        self.initialize()
        count = self._collection.count() if self._use_chroma and self._collection else len(self._fallback_docs)
        return {
            "total_documents": count,
            "collection_name": self.COLLECTION_NAME,
            "regulations": ["Employment Act 1955", "Personal Data Protection Act 2010"],
            "backend": "chromadb" if self._use_chroma else "keyword_fallback",
        }


rag_service = RAGService()
