"""
Compliance Agent — checks whether a material meets minimum
requirements for publishing.

Deterministic rule-based checks. No LLM dependency.
"""

from typing import Any

from app.agents.base_agent import BaseAgent, AgentResult
from app.core.constants import ResourceType


# Minimum required fields for publishing
REQUIRED_PUBLISH_FIELDS = ["title", "subjectId", "gradeId", "resourceType"]

# Resource types that require a file reference
FILE_REQUIRED_TYPES = {
    ResourceType.PDF.value,
    ResourceType.DOC.value,
    ResourceType.PPT.value,
    ResourceType.AUDIO.value,
    ResourceType.VIDEO.value,
    ResourceType.WORKSHEET.value,
    ResourceType.PAST_PAPER.value,
    ResourceType.REVISION_PACK.value,
}

# Resource types that require a URL
URL_REQUIRED_TYPES = {
    ResourceType.LINK.value,
}


class ComplianceAgent(BaseAgent):
    """
    Checks whether a material is ready for publishing.
    Validates metadata completeness, file references, and visibility configuration.
    """

    @property
    def name(self) -> str:
        return "ComplianceAgent"

    async def execute(self, context: dict[str, Any]) -> AgentResult:
        """
        Validate publish readiness of a material.

        Args:
            context: Material document data.

        Returns:
            AgentResult with compliance status and list of issues.
        """
        issues: list[str] = []
        warnings: list[str] = []

        # 1. Check required fields
        for field in REQUIRED_PUBLISH_FIELDS:
            value = context.get(field)
            if not value:
                issues.append(f"Missing required field: {field}")

        # 2. Check file/URL requirements based on resource type
        resource_type = context.get("resourceType", "")
        file_id = context.get("fileId")
        external_url = context.get("externalUrl")

        if resource_type in FILE_REQUIRED_TYPES:
            if not file_id:
                issues.append(
                    f"Resource type '{resource_type}' requires a fileId"
                )
        elif resource_type in URL_REQUIRED_TYPES:
            if not external_url:
                issues.append(
                    f"Resource type '{resource_type}' requires an externalUrl"
                )

        # 3. Check visibility configuration
        visibility = context.get("visibility", {})
        if not visibility:
            warnings.append("No visibility configuration set — defaults to school-wide")
        else:
            scope_type = visibility.get("scopeType", "")
            school_id = visibility.get("schoolId")
            if not school_id:
                issues.append("Visibility must include a schoolId")

        # 4. Check title quality
        title = context.get("title", "")
        if title and len(title) < 5:
            warnings.append("Title is very short — consider a more descriptive title")

        # 5. Check description
        description = context.get("description", "")
        if not description:
            warnings.append("No description provided — recommended for discoverability")

        # 6. Check tags
        tags = context.get("tags", [])
        if not tags:
            warnings.append("No tags set — tags improve searchability")

        is_compliant = len(issues) == 0

        return AgentResult(
            success=is_compliant,
            data={
                "isCompliant": is_compliant,
                "issues": issues,
                "warnings": warnings,
                "checkedFields": len(REQUIRED_PUBLISH_FIELDS) + 3,  # +3 for file, visibility, quality
            },
            messages=[
                f"Compliance check: {'PASSED' if is_compliant else 'FAILED'}",
                f"{len(issues)} issues, {len(warnings)} warnings",
            ],
            errors=issues if not is_compliant else [],
        )
