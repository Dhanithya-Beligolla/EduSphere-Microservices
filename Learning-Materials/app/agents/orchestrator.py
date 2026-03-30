"""
Internal agent orchestrator — routes requests to the appropriate agent.
Acts as the central dispatch point for all agent-assisted operations.
"""

from typing import Any

from app.agents.base_agent import AgentResult
from app.agents.metadata_agent import MetadataAgent
from app.agents.classification_agent import ClassificationAgent
from app.agents.compliance_agent import ComplianceAgent
from app.core.logging import get_logger

logger = get_logger("agents.orchestrator")

# Instantiate agents once — they are stateless
_metadata_agent = MetadataAgent()
_classification_agent = ClassificationAgent()
_compliance_agent = ComplianceAgent()


class AgentOrchestrator:
    """
    Central routing module for agent-assisted operations.
    Routes task requests to specialized agent modules.
    """

    async def suggest_tags(self, material_data: dict[str, Any]) -> AgentResult:
        """Suggest tags for a material using the MetadataAgent."""
        logger.info("agent_suggest_tags", material_title=material_data.get("title"))
        context = {**material_data, "task": "suggest_tags"}
        return await _metadata_agent.execute(context)

    async def normalize_metadata(self, material_data: dict[str, Any]) -> AgentResult:
        """Normalize material metadata using the MetadataAgent."""
        logger.info("agent_normalize_metadata", material_title=material_data.get("title"))
        context = {**material_data, "task": "normalize_metadata"}
        return await _metadata_agent.execute(context)

    async def classify_resource(self, material_data: dict[str, Any]) -> AgentResult:
        """Classify resource type and audience using the ClassificationAgent."""
        logger.info("agent_classify_resource", material_title=material_data.get("title"))
        return await _classification_agent.execute(material_data)

    async def check_compliance(self, material_data: dict[str, Any]) -> AgentResult:
        """Check publish readiness using the ComplianceAgent."""
        logger.info("agent_check_compliance", material_title=material_data.get("title"))
        return await _compliance_agent.execute(material_data)


# Singleton orchestrator
orchestrator = AgentOrchestrator()
