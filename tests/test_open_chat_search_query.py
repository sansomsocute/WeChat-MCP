from __future__ import annotations

import pytest

from wechat_mcp import wechat_accessibility as wa


@pytest.fixture
def fake_wechat(monkeypatch):
    calls: dict[str, object] = {}
    monkeypatch.setattr(wa, "get_wechat_ax_app", lambda: "app")
    monkeypatch.setattr(wa, "find_chat_element_by_name", lambda app, name: None)
    monkeypatch.setattr(wa.time, "sleep", lambda s: None)
    monkeypatch.setattr(wa, "focus_and_type_search", lambda app, text: calls.__setitem__("typed", text))

    def select(app, name):
        calls["matched"] = name
        return True, {"contacts": [], "group_chats": []}

    monkeypatch.setattr(wa, "_select_contact_from_search_results", select)
    return calls


def test_searches_the_chat_name_by_default(fake_wechat):
    assert wa.open_chat_for_contact("Alice") is None
    assert fake_wechat == {"typed": "Alice", "matched": "Alice"}


def test_search_query_is_typed_but_chat_name_must_match(fake_wechat):
    assert wa.open_chat_for_contact("魏璐佩", search_query="Lupei") is None
    assert fake_wechat == {"typed": "Lupei", "matched": "魏璐佩"}
