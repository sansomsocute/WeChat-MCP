from __future__ import annotations

from wechat_mcp.wechat_accessibility import (
    SearchEntry,
    _group_search_entries,
    _summarize_search_candidates,
)


def entries(*rows):
    return [SearchEntry(element=None, text=text, y=float(i)) for i, text in enumerate(rows)]


SNAPSHOT = entries(
    "Features", "File Transfer", "Chat Files",
    "Contacts", "Alice", "Bob", "View All(5)",
    "Group Chats", "Team", "Collapse",
    "Chat History", "Alice", "Alice",
    "More", "Search WeChat ID",
)


def test_groups_rows_by_every_section():
    assert _group_search_entries(SNAPSHOT) == {
        "Features": ["File Transfer", "Chat Files"],
        "Contacts": ["Alice", "Bob"],
        "Group Chats": ["Team"],
        "Chat History": ["Alice"],
        "More": ["Search WeChat ID"],
    }


def test_candidates_only_include_contacts_and_groups():
    assert _summarize_search_candidates(SNAPSHOT) == {
        "contacts": ["Alice", "Bob"],
        "group_chats": ["Team"],
    }


def test_candidates_capped_at_15():
    names = [f"Person {i}" for i in range(20)]
    assert len(_summarize_search_candidates(entries("Contacts", *names))["contacts"]) == 15
