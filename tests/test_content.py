import re
from pathlib import Path

import pytest

from tasks import AVAILABLE_CATEGORIES

POSTS_DIR = Path(__file__).resolve().parent.parent / "content" / "posts"
POSTS = sorted(POSTS_DIR.glob("*.md"))


def _category(path: Path) -> str | None:
    # Metadata is the leading block of "Key: value" lines.
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            break
        key, _, value = line.partition(":")
        if key.strip().lower() == "category":
            return value.strip()
    return None


def test_posts_are_found():
    assert POSTS


@pytest.mark.parametrize("path", POSTS, ids=lambda p: p.name)
def test_category_is_available(path):
    assert _category(path) in AVAILABLE_CATEGORIES


@pytest.mark.parametrize("path", POSTS, ids=lambda p: p.name)
def test_no_bare_relative_image_reference(path):
    # Use ({static}/images/...) so images resolve on tag/category/author pages.
    assert not re.search(r"\]\(images/", path.read_text(encoding="utf-8"))
