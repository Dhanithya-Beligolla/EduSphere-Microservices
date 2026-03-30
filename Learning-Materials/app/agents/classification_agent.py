"""
Classification Agent — deterministic rule-based resource classification.
Classifies materials by resource type and appropriate audience metadata.

No LLM dependency. Pure Python logic.
"""

import re
from typing import Any

from app.agents.base_agent import BaseAgent, AgentResult
from app.core.constants import ResourceType


# File extension to resource type inference
EXTENSION_MAP: dict[str, str] = {
    ".pdf": ResourceType.PDF.value,
    ".doc": ResourceType.DOC.value,
    ".docx": ResourceType.DOC.value,
    ".ppt": ResourceType.PPT.value,
    ".pptx": ResourceType.PPT.value,
    ".mp4": ResourceType.VIDEO.value,
    ".mov": ResourceType.VIDEO.value,
    ".avi": ResourceType.VIDEO.value,
    ".mkv": ResourceType.VIDEO.value,
    ".mp3": ResourceType.AUDIO.value,
    ".wav": ResourceType.AUDIO.value,
    ".ogg": ResourceType.AUDIO.value,
}

# URL pattern to resource type inference
URL_PATTERNS: list[tuple[str, str]] = [
    (r"youtube\.com|youtu\.be|vimeo\.com", ResourceType.VIDEO.value),
    (r"soundcloud\.com|spotify\.com", ResourceType.AUDIO.value),
    (r"drive\.google\.com.*\.pdf", ResourceType.PDF.value),
    (r"docs\.google\.com/presentation", ResourceType.PPT.value),
    (r"docs\.google\.com/document", ResourceType.DOC.value),
]

# Title keyword to audience suggestion
AUDIENCE_KEYWORDS: dict[str, dict[str, Any]] = {
    "past paper": {"isSuitableFor": ["exam-candidates"], "gradeHint": "10-11"},
    "pastpaper": {"isSuitableFor": ["exam-candidates"], "gradeHint": "10-11"},
    "o/l": {"isSuitableFor": ["o-level-students"], "gradeHint": "10-11"},
    "a/l": {"isSuitableFor": ["a-level-students"], "gradeHint": "12-13"},
    "revision": {"isSuitableFor": ["exam-candidates"], "gradeHint": None},
    "beginner": {"isSuitableFor": ["beginners"], "gradeHint": "6-8"},
    "advanced": {"isSuitableFor": ["advanced-learners"], "gradeHint": "10-13"},
    "practical": {"isSuitableFor": ["lab-students"], "gradeHint": None},
}


class ClassificationAgent(BaseAgent):
    """
    Deterministic classification agent for resource type detection
    and audience metadata suggestions.
    """

    @property
    def name(self) -> str:
        return "ClassificationAgent"

    async def execute(self, context: dict[str, Any]) -> AgentResult:
        """Classify a material's resource type and suggest audience metadata."""

        title = (context.get("title") or "").lower()
        description = (context.get("description") or "").lower()
        file_name = context.get("fileName", "")
        external_url = context.get("externalUrl", "")

        classified_type: str | None = None
        confidence: str = "low"
        audience_hints: list[dict] = []

        # 1. Try to classify by file extension
        if file_name:
            ext = "." + file_name.rsplit(".", 1)[-1].lower() if "." in file_name else ""
            if ext in EXTENSION_MAP:
                classified_type = EXTENSION_MAP[ext]
                confidence = "high"

        # 2. Try to classify by URL pattern
        if not classified_type and external_url:
            for pattern, resource_type in URL_PATTERNS:
                if re.search(pattern, external_url, re.IGNORECASE):
                    classified_type = resource_type
                    confidence = "medium"
                    break
            else:
                classified_type = ResourceType.LINK.value
                confidence = "low"

        # 3. Try to classify by title keywords
        if not classified_type:
            combined = f"{title} {description}"
            if "worksheet" in combined:
                classified_type = ResourceType.WORKSHEET.value
                confidence = "medium"
            elif "past paper" in combined or "pastpaper" in combined:
                classified_type = ResourceType.PAST_PAPER.value
                confidence = "medium"
            elif "revision" in combined:
                classified_type = ResourceType.REVISION_PACK.value
                confidence = "medium"
            elif "presentation" in combined or "slides" in combined:
                classified_type = ResourceType.PPT.value
                confidence = "low"
            elif "video" in combined:
                classified_type = ResourceType.VIDEO.value
                confidence = "low"

        # 4. Suggest audience metadata
        combined_text = f"{title} {description}"
        for keyword, hints in AUDIENCE_KEYWORDS.items():
            if keyword in combined_text:
                audience_hints.append({
                    "keyword": keyword,
                    **hints,
                })

        return AgentResult(
            success=True,
            data={
                "classifiedResourceType": classified_type,
                "confidence": confidence,
                "audienceHints": audience_hints,
            },
            messages=[
                f"Resource type classified as: {classified_type or 'unknown'} (confidence: {confidence})",
                f"Found {len(audience_hints)} audience hints",
            ],
        )
