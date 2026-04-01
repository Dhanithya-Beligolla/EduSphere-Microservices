"""
Metadata Agent — deterministic rule-based helpers for:
- Tag suggestion based on title, description, and resource type
- Title cleaning and normalization
- Metadata normalization (trimming, casing, deduplication)

No LLM dependency. Pure Python logic.
"""

import re
from typing import Any

from app.agents.base_agent import BaseAgent, AgentResult
from app.core.constants import ResourceType, Medium


# ── Tag suggestion keyword map ──
# Maps keywords to suggested tags. Designed for Sri Lankan school context.
KEYWORD_TAG_MAP: dict[str, list[str]] = {
    # Subjects
    "math": ["mathematics", "numeracy"],
    "mathematics": ["mathematics", "numeracy"],
    "science": ["science", "stem"],
    "biology": ["biology", "life-sciences", "science"],
    "chemistry": ["chemistry", "science"],
    "physics": ["physics", "science"],
    "english": ["english", "language"],
    "sinhala": ["sinhala", "language"],
    "tamil": ["tamil", "language"],
    "ict": ["ict", "technology", "computer-science"],
    "history": ["history", "social-studies"],
    "geography": ["geography", "social-studies"],
    "commerce": ["commerce", "business-studies"],
    "accounting": ["accounting", "business-studies"],
    "art": ["art", "creative-arts"],
    "music": ["music", "creative-arts"],
    # Resource types
    "revision": ["revision", "exam-prep"],
    "past paper": ["past-paper", "exam-prep"],
    "pastpaper": ["past-paper", "exam-prep"],
    "worksheet": ["worksheet", "practice"],
    "notes": ["notes", "study-material"],
    "presentation": ["presentation", "visual-learning"],
    "video": ["video", "multimedia"],
    "lab": ["laboratory", "practical"],
    "experiment": ["laboratory", "practical"],
    # Grade levels
    "grade 6": ["grade-6", "junior-secondary"],
    "grade 7": ["grade-7", "junior-secondary"],
    "grade 8": ["grade-8", "junior-secondary"],
    "grade 9": ["grade-9", "senior-secondary"],
    "grade 10": ["grade-10", "senior-secondary"],
    "grade 11": ["grade-11", "senior-secondary"],
    "o/l": ["ordinary-level", "o-level", "exam-prep"],
    "a/l": ["advanced-level", "a-level", "exam-prep"],
    "ol": ["ordinary-level", "o-level", "exam-prep"],
    "al": ["advanced-level", "a-level", "exam-prep"],
    # Terms
    "term 1": ["term-1", "first-term"],
    "term 2": ["term-2", "second-term"],
    "term 3": ["term-3", "third-term"],
}

# Resource type to tag mappings
RESOURCE_TAG_MAP: dict[str, list[str]] = {
    ResourceType.PDF.value: ["document", "pdf"],
    ResourceType.VIDEO.value: ["video", "multimedia"],
    ResourceType.AUDIO.value: ["audio", "multimedia"],
    ResourceType.PPT.value: ["presentation", "slides"],
    ResourceType.WORKSHEET.value: ["worksheet", "practice"],
    ResourceType.PAST_PAPER.value: ["past-paper", "exam-prep"],
    ResourceType.REVISION_PACK.value: ["revision", "study-pack"],
    ResourceType.DOC.value: ["document"],
    ResourceType.LINK.value: ["external-resource", "link"],
}


class MetadataAgent(BaseAgent):
    """
    Deterministic metadata normalization and tag suggestion agent.
    """

    @property
    def name(self) -> str:
        return "MetadataAgent"

    async def execute(self, context: dict[str, Any]) -> AgentResult:
        """Route to the correct sub-task."""
        task = context.get("task", "suggest_tags")

        if task == "suggest_tags":
            return await self.suggest_tags(context)
        elif task == "normalize_metadata":
            return await self.normalize_metadata(context)
        else:
            return AgentResult(success=False, errors=[f"Unknown task: {task}"])

    async def suggest_tags(self, context: dict[str, Any]) -> AgentResult:
        """
        Suggest tags based on title, description, resource type, and existing tags.
        Uses keyword matching against the predefined tag map.
        """
        title = (context.get("title") or "").lower()
        description = (context.get("description") or "").lower()
        resource_type = context.get("resourceType", "")
        existing_tags = set(context.get("tags") or [])
        medium = context.get("medium", "")

        combined_text = f"{title} {description}"
        suggested = set()

        # Match keywords in text
        for keyword, tags in KEYWORD_TAG_MAP.items():
            if keyword in combined_text:
                suggested.update(tags)

        # Add resource-type based tags
        if resource_type in RESOURCE_TAG_MAP:
            suggested.update(RESOURCE_TAG_MAP[resource_type])

        # Add medium
        if medium:
            suggested.add(f"{medium.lower()}-medium")

        # Remove tags that already exist
        new_suggestions = sorted(suggested - existing_tags)

        return AgentResult(
            success=True,
            data={
                "suggestedTags": new_suggestions,
                "existingTags": sorted(existing_tags),
                "allTags": sorted(existing_tags | suggested),
            },
            messages=[f"Found {len(new_suggestions)} new tag suggestions"],
        )

    async def normalize_metadata(self, context: dict[str, Any]) -> AgentResult:
        """
        Normalize material metadata:
        - Trim whitespace from title and description
        - Title case the title
        - Deduplicate tags
        - Lowercase all tags
        - Remove empty strings from arrays
        """
        normalized: dict[str, Any] = {}
        changes: list[str] = []

        # Title normalization
        title = context.get("title", "")
        if title:
            clean_title = re.sub(r'\s+', ' ', title.strip())
            # Title case, but keep common abbreviations uppercase
            words = []
            for word in clean_title.split():
                if word.upper() in {"PDF", "PPT", "DOC", "ICT", "O/L", "A/L", "IT"}:
                    words.append(word.upper())
                else:
                    words.append(word.capitalize())
            normalized_title = " ".join(words)
            if normalized_title != title:
                changes.append(f"Title normalized: '{title}' -> '{normalized_title}'")
            normalized["title"] = normalized_title

        # Description normalization
        description = context.get("description", "")
        if description:
            clean_desc = re.sub(r'\s+', ' ', description.strip())
            if clean_desc != description:
                changes.append("Description whitespace normalized")
            normalized["description"] = clean_desc

        # Tag normalization
        tags = context.get("tags", [])
        if tags:
            clean_tags = sorted(set(
                tag.lower().strip()
                for tag in tags
                if tag and tag.strip()
            ))
            if clean_tags != tags:
                changes.append(f"Tags normalized: {len(tags)} -> {len(clean_tags)} unique tags")
            normalized["tags"] = clean_tags

        return AgentResult(
            success=True,
            data={"normalized": normalized, "changes": changes},
            messages=[f"Applied {len(changes)} normalizations"],
        )
