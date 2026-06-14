from unittest.mock import MagicMock

import pytest

import tasks
from tasks import POST_TEMPLATE, _build_slug, _validate_datetime


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("2026-06-14 12:00:00", True),
        ("2026-06-14", False),
        ("not-a-date", False),
    ],
)
def test_validate_datetime(value, expected):
    assert _validate_datetime(value) is expected


def test_build_slug_uses_post_date_not_today():
    # slug date must come from the given Date, not datetime.now()
    assert _build_slug("CFP Closed", "2026-06-02 09:00:00") == "2026-06-02-cfp-closed"


def test_build_slug_dash_joins_title_words():
    assert _build_slug("Hello World Post", "2024-01-09 00:00:00") == (
        "2024-01-09-hello-world-post"
    )


def test_post_template_no_leading_whitespace():
    rendered = POST_TEMPLATE.format(
        title="T",
        date="2026-06-15 00:00:00",
        modified="2026-06-15 00:00:00",
        category="announcement",
        tags="tag1",
        slug="2026-06-15-t",
        authors="Author",
        summary="Summary",
    )
    for line in rendered.splitlines():
        assert not line.startswith(" "), f"Line has leading space: {line!r}"


def _setup_create_post_mocks(monkeypatch):
    """Set up mocks shared by both create_post test cases."""
    monkeypatch.setattr(
        "tasks.questionary.form",
        lambda **kw: MagicMock(
            ask=lambda: {
                "title": "Test Post",
                "date": "2026-06-15 09:00:00",
                "category": "announcement",
            }
        ),
    )
    monkeypatch.setattr(
        "tasks._ask_multiple_inputs_question",
        lambda *a, **kw: "tag1",
    )
    monkeypatch.setattr(
        "tasks.questionary.text",
        lambda *a, **kw: MagicMock(ask=lambda: "Some summary"),
    )
    mock_print = MagicMock()
    monkeypatch.setattr("tasks.questionary.print", mock_print)
    return mock_print


def test_create_post_writes_new_file(monkeypatch, tmp_path):
    (tmp_path / "content" / "posts").mkdir(parents=True)
    monkeypatch.chdir(tmp_path)
    _setup_create_post_mocks(monkeypatch)

    tasks.create_post.__wrapped__(MagicMock())

    expected_file = tmp_path / "content" / "posts" / "2026-06-15-test-post.md"
    assert expected_file.exists()
    content = expected_file.read_text()
    assert "Test Post" in content
    assert "2026-06-15-test-post" in content


def test_create_post_does_not_overwrite_existing_file(monkeypatch, tmp_path):
    (tmp_path / "content" / "posts").mkdir(parents=True)
    monkeypatch.chdir(tmp_path)
    mock_print = _setup_create_post_mocks(monkeypatch)

    existing_file = tmp_path / "content" / "posts" / "2026-06-15-test-post.md"
    existing_file.write_text("ORIGINAL CONTENT")

    with pytest.raises(SystemExit) as exc:
        tasks.create_post.__wrapped__(MagicMock())

    assert exc.value.code == 1
    assert existing_file.read_text() == "ORIGINAL CONTENT"
    error_calls = [
        call
        for call in mock_print.call_args_list
        if call.kwargs.get("style") == "bold fg:red"
    ]
    assert len(error_calls) == 1, "Expected exactly one red error print call"
