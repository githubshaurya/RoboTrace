from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List

@dataclass(frozen=True)
class InstructionPerturbation:
    name: str
    text: str
    metadata: Dict[str, str]

_SIMPLE_SYNONYMS = {
    "pick": "grasp",
    "place": "put",
    "move": "shift",
    "push": "press",
    "pull": "draw",
    "open": "unclose",
    "close": "shut",
    "red": "crimson",
    "blue": "azure",
    "green": "emerald",
    "object": "item",
    "block": "cube",
}

def shorten_instruction(text: str, max_words: int = 6) -> str:
    words = text.split()
    return " ".join(words[:max_words]) if words else text

def mask_objects(text: str) -> str:
    return re.sub(r"\b(block|cube|cup|bowl|drawer|door|handle|object|item|tool|button)\b", "[OBJECT]", text, flags=re.IGNORECASE)

def synonym_replace(text: str) -> str:
    out = []
    for token in text.split():
        key = re.sub(r"[^A-Za-z]", "", token).lower()
        replacement = _SIMPLE_SYNONYMS.get(key)
        out.append(re.sub(key, replacement, token, flags=re.IGNORECASE) if replacement else token)
    return " ".join(out)

def add_distractor(text: str) -> str:
    return f"{text} Ignore any irrelevant background objects."

def make_ambiguous(text: str) -> str:
    return re.sub(r"\b(the|this|that|a|an)\s+([A-Za-z]+)", "the thing", text, count=1, flags=re.IGNORECASE)

def perturb_instruction(text: str) -> List[InstructionPerturbation]:
    text = text or ""
    return [
        InstructionPerturbation("original", text, {"kind": "identity"}),
        InstructionPerturbation("shortened", shorten_instruction(text), {"kind": "deletion"}),
        InstructionPerturbation("object_masking", mask_objects(text), {"kind": "masking"}),
        InstructionPerturbation("simple_synonyms", synonym_replace(text), {"kind": "lexical"}),
        InstructionPerturbation("distractor_phrase", add_distractor(text), {"kind": "distractor"}),
        InstructionPerturbation("ambiguous_wording", make_ambiguous(text), {"kind": "ambiguity"}),
    ]
