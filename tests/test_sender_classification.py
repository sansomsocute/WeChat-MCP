from __future__ import annotations

from PIL import Image, ImageDraw

from wechat_mcp.fetch_messages_by_chat_utils import classify_sender_for_message

WIDTH, ROW_HEIGHT = 700, 60


def chat_row(background, bubble, side):
    """One message row: a bubble plus avatar on the given side of a plain background."""
    image = Image.new("RGB", (WIDTH, ROW_HEIGHT), background)
    draw = ImageDraw.Draw(image)
    if side == "right":
        draw.rectangle((560, 10, 630, 50), fill=bubble)
        draw.rectangle((650, 10, 685, 45), fill=(120, 90, 60))
    else:
        draw.rectangle((15, 10, 50, 45), fill=(120, 90, 60))
        draw.rectangle((70, 10, 140, 50), fill=bubble)
    return image


def classify(image):
    return classify_sender_for_message(image, (0, 0), (0, 0), (WIDTH, ROW_HEIGHT))


def test_light_mode():
    light, green, white = (250, 250, 250), (149, 236, 105), (255, 255, 255)
    assert classify(chat_row(light, green, "right")) == "ME"
    assert classify(chat_row(light, white, "left")) == "OTHER"


def test_dark_mode():
    dark, green, grey = (17, 17, 17), (38, 179, 89), (44, 44, 44)
    assert classify(chat_row(dark, green, "right")) == "ME"
    assert classify(chat_row(dark, grey, "left")) == "OTHER"


def test_empty_row_is_unknown():
    assert classify(Image.new("RGB", (WIDTH, ROW_HEIGHT), (250, 250, 250))) == "UNKNOWN"
