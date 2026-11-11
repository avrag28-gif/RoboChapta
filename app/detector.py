from enum import Enum
from dataclasses import dataclass

class CaptchaType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    CHECKBOX = "checkbox"
    INTERACTIVE = "interactive"
    UNKNOWN = "unknown"

@dataclass(frozen=True)
class Detection:
    captcha_type: CaptchaType
    confidence: float
    requires_human: bool

_ALLOWED = {item.value: item for item in CaptchaType if item is not CaptchaType.UNKNOWN}

def detect_captcha(metadata: dict) -> Detection:
    raw = str(metadata.get("type", "unknown")).strip().lower()
    kind = _ALLOWED.get(raw, CaptchaType.UNKNOWN)
    # Classification is metadata-based, not a claim that a challenge was solved.
    return Detection(
        captcha_type=kind,
        confidence=1.0 if kind is not CaptchaType.UNKNOWN else 0.0,
        requires_human=True,
    )
