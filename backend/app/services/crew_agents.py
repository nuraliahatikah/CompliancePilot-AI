import json
import logging
import re
import time
from typing import Any

from app.config import get_settings
from app.models import RiskLevel
from app.services.rag_service import rag_service

logger = logging.getLogger(__name__)
settings = get_settings()

COMPLIANCE_KEYWORDS = {
    "employment": [
        "employee", "employer", "salary", "wage", "overtime", "termination",
        "notice period", "annual leave", "maternity", "rest day", "working hours",
        "contract of service", "probation", "severance",
    ],
    "data_protection": [
        "personal data", "data subject", "consent", "privacy", "confidential",
        "data processing", "data transfer", "cross-border", "retention",
        "access request", "sensitive data", "pdpa",
    ],
}

RISK_PATTERNS: list[dict[str, Any]] = [
    {
        "pattern": r"without\s+(?:prior\s+)?consent",
        "category": "Data Protection",
        "severity": "high",
        "title": "Processing without explicit consent",
        "regulation": "PDPA Section 6",
        "description": "Document may authorize processing of personal data without obtaining explicit consent from data subjects.",
    },
    {
        "pattern": r"transfer.{0,30}(?:outside|abroad|overseas|foreign)",
        "category": "Data Protection",
        "severity": "high",
        "title": "Cross-border data transfer",
        "regulation": "PDPA Section 130",
        "description": "Cross-border transfer of personal data detected without adequate safeguards or consent provisions.",
    },
    {
        "pattern": r"(?:indefinite|perpetual|unlimited).{0,20}(?:retention|storage|keep)",
        "category": "Data Protection",
        "severity": "medium",
        "title": "Indefinite data retention",
        "regulation": "PDPA Section 10",
        "description": "Personal data may be retained indefinitely, violating the retention principle.",
    },
    {
        "pattern": r"(?:no|without|waive).{0,20}(?:notice|prior\s+notice)",
        "category": "Employment",
        "severity": "high",
        "title": "Termination without notice",
        "regulation": "Employment Act Section 37",
        "description": "Contract may allow termination without proper notice period as required by the Employment Act.",
    },
    {
        "pattern": r"(?:more\s+than|exceed).{0,15}(?:8|eight)\s+hours",
        "category": "Employment",
        "severity": "medium",
        "title": "Excessive working hours",
        "regulation": "Employment Act Section 60A",
        "description": "Working hours may exceed statutory limits without adequate overtime compensation.",
    },
    {
        "pattern": r"(?:non-?compete|non-?competition).{0,30}(?:worldwide|global|indefinite|perpetual)",
        "category": "Employment",
        "severity": "medium",
        "title": "Overly broad non-compete clause",
        "regulation": "Employment Act Section 24",
        "description": "Non-compete restrictions may be unenforceable if they constitute restraint of trade beyond reasonable limits.",
    },
    {
        "pattern": r"(?:deduct|withhold).{0,20}wage",
        "category": "Employment",
        "severity": "medium",
        "title": "Unauthorized wage deductions",
        "regulation": "Employment Act Section 12",
        "description": "Contract may permit wage deductions not authorized under the Employment Act.",
    },
    {
        "pattern": r"(?:share|disclose|sell).{0,30}(?:third\s+part|affiliate|partner)",
        "category": "Data Protection",
        "severity": "medium",
        "title": "Third-party data sharing",
        "regulation": "PDPA Section 6 & 7",
        "description": "Broad third-party data sharing without clear notice and consent mechanisms.",
    },
]


class ComplianceAnalysisPipeline:
    """Multi-agent compliance analysis using CrewAI with intelligent fallback."""

    def analyze(self, document_text: str, document_type: str = "contract") -> dict[str, Any]:
        start = time.time()
        rag_query = self._build_rag_query(document_text, document_type)
        rag_sources = rag_service.query(rag_query, top_k=8)

        if settings.openai_api_key:
            try:
                result = self._run_crewai_pipeline(document_text, document_type, rag_sources)
                result["processing_time_seconds"] = round(time.time() - start, 2)
                result["rag_sources"] = rag_sources
                return result
            except Exception as exc:
                logger.warning("CrewAI pipeline failed, using rule-based analysis: %s", exc)

        result = self._run_rule_based_analysis(document_text, document_type, rag_sources)
        result["processing_time_seconds"] = round(time.time() - start, 2)
        result["rag_sources"] = rag_sources
        return result

    def _build_rag_query(self, text: str, document_type: str) -> str:
        sample = text[:2000].lower()
        topics: list[str] = [document_type]
        for category, keywords in COMPLIANCE_KEYWORDS.items():
            if any(kw in sample for kw in keywords):
                topics.append(category.replace("_", " "))
        return " ".join(topics) + " " + sample[:500]

    def _run_crewai_pipeline(
        self, document_text: str, document_type: str, rag_sources: list[dict[str, Any]]
    ) -> dict[str, Any]:
        from crewai import Agent, Crew, Process, Task
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key, temperature=0.1)
        rag_context = "\n\n".join(
            f"[{s['regulation']} - {s['section']}]: {s['content']}" for s in rag_sources[:6]
        )
        truncated_doc = document_text[:12000]

        legal_analyst = Agent(
            role="Legal Compliance Analyst",
            goal="Identify legal and regulatory compliance issues in business documents under Malaysian law",
            backstory=(
                "Expert Malaysian employment and data protection lawyer with deep knowledge of "
                "Employment Act 1955 and PDPA 2010."
            ),
            llm=llm,
            verbose=False,
        )

        risk_assessor = Agent(
            role="Risk Assessment Specialist",
            goal="Quantify compliance risk and prioritize findings by severity",
            backstory="Senior compliance officer specializing in enterprise risk scoring and audit preparation.",
            llm=llm,
            verbose=False,
        )

        policy_advisor = Agent(
            role="Policy Recommendation Advisor",
            goal="Provide actionable remediation recommendations for identified compliance gaps",
            backstory="Compliance consultant who helps organizations remediate regulatory gaps efficiently.",
            llm=llm,
            verbose=False,
        )

        analysis_task = Task(
            description=(
                f"Analyze this {document_type} document for compliance with Malaysian Employment Act 1955 "
                f"and PDPA 2010. Use the regulatory context provided.\n\n"
                f"REGULATORY CONTEXT:\n{rag_context}\n\n"
                f"DOCUMENT:\n{truncated_doc}\n\n"
                "Return a JSON object with keys: findings (list of objects with category, severity, "
                "title, description, regulation_reference, clause_excerpt), compliance_gaps (list of strings), "
                "and summary (string)."
            ),
            expected_output="JSON with findings, compliance_gaps, and summary",
            agent=legal_analyst,
        )

        risk_task = Task(
            description=(
                "Based on the legal analysis findings, calculate a risk_score (0-100) and risk_level "
                "(low/medium/high/critical). Return JSON with risk_score, risk_level, and risk_rationale."
            ),
            expected_output="JSON with risk_score, risk_level, risk_rationale",
            agent=risk_assessor,
            context=[analysis_task],
        )

        recommendation_task = Task(
            description=(
                "Based on all findings, provide prioritized recommendations. "
                "Return JSON with recommendations (list of actionable strings)."
            ),
            expected_output="JSON with recommendations list",
            agent=policy_advisor,
            context=[analysis_task, risk_task],
        )

        crew = Crew(
            agents=[legal_analyst, risk_assessor, policy_advisor],
            tasks=[analysis_task, risk_task, recommendation_task],
            process=Process.sequential,
            verbose=False,
        )

        crew.kickoff()

        analysis_output = self._parse_agent_json(str(analysis_task.output))
        risk_output = self._parse_agent_json(str(risk_task.output))
        rec_output = self._parse_agent_json(str(recommendation_task.output))

        findings = analysis_output.get("findings", [])
        risk_score = float(risk_output.get("risk_score", 50))
        risk_level = self._score_to_level(risk_score)

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "summary": analysis_output.get("summary", "AI-powered compliance analysis completed."),
            "findings": findings,
            "recommendations": rec_output.get("recommendations", []),
            "compliance_gaps": analysis_output.get("compliance_gaps", []),
            "agent_outputs": {
                "legal_analyst": analysis_output,
                "risk_assessor": risk_output,
                "policy_advisor": rec_output,
                "pipeline": "crewai",
            },
        }

    def _run_rule_based_analysis(
        self, document_text: str, document_type: str, rag_sources: list[dict[str, Any]]
    ) -> dict[str, Any]:
        text_lower = document_text.lower()
        findings: list[dict[str, Any]] = []
        seen_titles: set[str] = set()

        for pattern_def in RISK_PATTERNS:
            matches = list(re.finditer(pattern_def["pattern"], text_lower, re.IGNORECASE))
            if matches and pattern_def["title"] not in seen_titles:
                match = matches[0]
                start = max(0, match.start() - 80)
                end = min(len(document_text), match.end() + 80)
                excerpt = document_text[start:end].strip()
                findings.append(
                    {
                        "category": pattern_def["category"],
                        "severity": pattern_def["severity"],
                        "title": pattern_def["title"],
                        "description": pattern_def["description"],
                        "regulation_reference": pattern_def["regulation"],
                        "clause_excerpt": excerpt,
                    }
                )
                seen_titles.add(pattern_def["title"])

        for rag_item in rag_sources[:4]:
            reg_keywords = rag_item["section"].lower().split()
            content_keywords = [w for w in reg_keywords if len(w) > 4]
            if any(kw in text_lower for kw in content_keywords):
                title = f"Potential gap: {rag_item['section']}"
                if title not in seen_titles:
                    findings.append(
                        {
                            "category": rag_item["regulation"],
                            "severity": "medium",
                            "title": title,
                            "description": (
                                f"Document content may not fully comply with {rag_item['section']}. "
                                f"Review against: {rag_item['content'][:200]}"
                            ),
                            "regulation_reference": rag_item["section"],
                            "clause_excerpt": None,
                        }
                    )
                    seen_titles.add(title)

        severity_weights = {"critical": 25, "high": 18, "medium": 10, "low": 5}
        base_score = sum(severity_weights.get(f["severity"], 5) for f in findings)
        risk_score = min(100.0, max(5.0, base_score))
        risk_level = self._score_to_level(risk_score)

        compliance_gaps = [f["title"] for f in findings if f["severity"] in ("high", "critical")]
        recommendations = self._generate_recommendations(findings, document_type)

        summary = (
            f"Rule-based compliance analysis of {document_type} identified {len(findings)} finding(s) "
            f"with an overall risk score of {risk_score:.0f}/100 ({risk_level.value} risk). "
            f"Analysis cross-referenced {len(rag_sources)} Malaysian regulatory sources "
            f"(Employment Act 1955 & PDPA 2010)."
        )

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "summary": summary,
            "findings": findings,
            "recommendations": recommendations,
            "compliance_gaps": compliance_gaps,
            "agent_outputs": {
                "legal_analyst": {"findings": findings, "summary": summary},
                "risk_assessor": {"risk_score": risk_score, "risk_level": risk_level.value},
                "policy_advisor": {"recommendations": recommendations},
                "pipeline": "rule_based_rag",
            },
        }

    def _generate_recommendations(self, findings: list[dict[str, Any]], document_type: str) -> list[str]:
        recs: list[str] = []
        categories = {f["category"] for f in findings}

        if "Data Protection" in categories or any("PDPA" in f.get("regulation_reference", "") for f in findings):
            recs.append(
                "Implement a PDPA-compliant privacy notice and obtain explicit consent before processing personal data."
            )
            recs.append(
                "Review data retention schedules and ensure personal data is deleted when no longer required."
            )
            recs.append(
                "Assess cross-border data transfers and ensure destination countries have adequate data protection laws."
            )

        if "Employment" in categories or any("Employment Act" in f.get("regulation_reference", "") for f in findings):
            recs.append(
                "Align termination clauses with Employment Act 1955 notice period requirements based on length of service."
            )
            recs.append(
                "Ensure working hours and overtime provisions comply with Section 60A limits and compensation rates."
            )
            recs.append(
                "Review annual leave, maternity leave, and rest day entitlements against statutory minimums."
            )

        if not recs:
            recs.append(f"Schedule periodic review of this {document_type} against current Malaysian regulations.")
            recs.append("Maintain an audit trail of all compliance reviews and remediation actions.")
            recs.append("Consult legal counsel for formal compliance certification.")

        high_findings = [f for f in findings if f["severity"] in ("high", "critical")]
        if high_findings:
            recs.insert(0, f"URGENT: Address {len(high_findings)} high-severity finding(s) before contract execution.")

        return recs[:8]

    def _parse_agent_json(self, output: str) -> dict[str, Any]:
        try:
            json_match = re.search(r"\{[\s\S]*\}", output)
            if json_match:
                return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
        return {"raw_output": output}

    def _score_to_level(self, score: float) -> RiskLevel:
        if score >= 75:
            return RiskLevel.CRITICAL
        if score >= 50:
            return RiskLevel.HIGH
        if score >= 25:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW


compliance_pipeline = ComplianceAnalysisPipeline()
