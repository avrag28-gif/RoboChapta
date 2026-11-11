from app.detector import detect_captcha, CaptchaType

def test_supported_types_are_classified():
    for name, expected in [
        ("text", CaptchaType.TEXT),
        ("image", CaptchaType.IMAGE),
        ("audio", CaptchaType.AUDIO),
        ("checkbox", CaptchaType.CHECKBOX),
        ("interactive", CaptchaType.INTERACTIVE),
    ]:
        assert detect_captcha({"type": name}).captcha_type is expected

def test_unknown_type_is_safe():
    result = detect_captcha({"type": "not-a-captcha"})
    assert result.captcha_type is CaptchaType.UNKNOWN
    assert result.requires_human is True
