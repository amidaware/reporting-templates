import json
from pathlib import Path

import pytest
import validators

# Adjust these paths as needed
ROOT = Path(__file__).parent
TEMPLATE_DIR = ROOT / "templates"
INDEX_FILE = ROOT / "index.json"

# Gather all .json files in the templates directory
TEMPLATE_FILES = list(TEMPLATE_DIR.glob("*.json"))


@pytest.mark.parametrize(
    "template_file",
    TEMPLATE_FILES,
    ids=[f.stem for f in TEMPLATE_FILES]
)
def test_template_name_matches_filename(template_file: Path):
    """
    Verify that the 'template.name' inside each JSON equals the filename (without .json).
    When this fails, pytest will show a string diff between expected vs actual.
    """
    content = json.loads(template_file.read_text(encoding="utf-8"))
    actual_name = content["template"]["name"]
    expected_name = template_file.stem

    # Plain assert gives VSCode a diff view on mismatch
    assert actual_name == expected_name


def test_index_integrity():
    """
    Validate index.json entries:
      - download_url is a valid URL
      - download_url starts with the expected base path
      - no duplicate names
    """
    index = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    seen_names = []

    for entry in index:
        url = entry.get("download_url", "")
        # URL format check
        assert validators.url(url), f"Invalid URL: {url}"
        # Base path check
        assert url.startswith(
            "https://raw.githubusercontent.com/amidaware/reporting-templates/master"
        ), f"URL does not start with expected base: {url}"
        # Collect names for duplicate detection
        seen_names.append(entry.get("name", ""))

    # Duplicate check
    assert len(seen_names) == len(set(seen_names)), "Duplicate names found in index.json"
