import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pytest
import validators

# Adjust these paths as needed
ROOT = Path(__file__).parent
TEMPLATE_DIR = ROOT / "templates"
INDEX_FILE = ROOT / "index.json"

# Gather all .json files in the templates directory
TEMPLATE_FILES = list(TEMPLATE_DIR.glob("*.json"))


class ReportNamingConvention:
    """Represents the naming patterns found in reporting templates."""
    
    # Common patterns observed in the templates
    PATTERNS = [
        # Pattern 1: Subject_By Scope [descriptors] (format) version
        r"^(.+?)_By\s+([^(]+?)(?:\s+\((.+?)\))?(?:\s+(v[\d.]+))?$",
        # Pattern 2: Subject Report_by Scope [descriptors] (format) version  
        r"^(.+?)\s+Report_by\s+([^(]+?)(?:\s+\((.+?)\))?(?:\s+(v[\d.]+))?$",
        # Pattern 3: All Fields - Subject [descriptors] (format) version
        r"^All\s+Fields\s+-\s+([^(]+?)(?:\s+\((.+?)\))?(?:\s+(v[\d.]+))?$",
        # Pattern 4: Simple Subject [descriptors] (format) version
        r"^([^(]+?)(?:\s+\((.+?)\))?(?:\s+(v[\d.]+))?$"
    ]
    
    # Update VALID_SCOPES to include base scopes, validation will extract base scope
    VALID_SCOPES = {"Client", "Site", "Agent", "Device", "Software Name", "ClientThenSite"}
    VALID_FORMATS = {"csv", "pdf", "html"}
    VERSION_PATTERN = r"^v\d+(?:\.\d+)*$"

    @classmethod
    def _extract_base_scope(cls, scope_text: str) -> str:
        """Extract the base organizational scope from scope text that may include descriptors."""
        scope_text = scope_text.strip()
        
        # Check for each valid scope at the beginning
        for valid_scope in cls.VALID_SCOPES:
            if scope_text.startswith(valid_scope):
                return valid_scope
        
        return scope_text
    
    @classmethod
    def parse_name(cls, name: str) -> Optional[Dict[str, str]]:
        """Parse a report name and extract components."""
        for pattern in cls.PATTERNS:
            match = re.match(pattern, name, re.IGNORECASE)
            if match:
                groups = match.groups()
                
                if "All Fields" in name:
                    return {
                        "type": "all_fields",
                        "subject": groups[0] if groups[0] else "",
                        "format": groups[1] if len(groups) > 1 and groups[1] else None,
                        "version": groups[2] if len(groups) > 2 and groups[2] else None
                    }
                elif "_By " in name or "Report_by " in name:
                    return {
                        "type": "scoped",
                        "subject": groups[0] if groups[0] else "",
                        "scope": groups[1] if len(groups) > 1 and groups[1] else None,
                        "format": groups[2] if len(groups) > 2 and groups[2] else None,
                        "version": groups[3] if len(groups) > 3 and groups[3] else None
                    }
                else:
                    return {
                        "type": "simple",
                        "subject": groups[0] if groups[0] else "",
                        "format": groups[1] if len(groups) > 1 and groups[1] else None,
                        "version": groups[2] if len(groups) > 2 and groups[2] else None
                    }
        return None
    
    @classmethod
    def validate_name(cls, name: str) -> Tuple[bool, List[str]]:
        """Validate a report name against conventions."""
        errors = []
        parsed = cls.parse_name(name)
        
        if not parsed:
            errors.append(f"Name '{name}' doesn't match any known pattern")
            return False, errors
        
        # Validate scope if present
        if parsed.get("scope"):
            base_scope = cls._extract_base_scope(parsed["scope"])
            if base_scope not in cls.VALID_SCOPES:
                errors.append(f"Invalid base scope '{base_scope}' from '{parsed['scope']}'. Valid: {cls.VALID_SCOPES}")
        
        # Validate format if present
        if parsed.get("format") and parsed["format"] not in cls.VALID_FORMATS:
            errors.append(f"Invalid format '{parsed['format']}'. Valid: {cls.VALID_FORMATS}")
        
        # Validate version if present
        if parsed.get("version") and not re.match(cls.VERSION_PATTERN, parsed["version"]):
            errors.append(f"Invalid version format '{parsed['version']}'. Expected: v1.0, v1.2.3, etc.")
        
        return len(errors) == 0, errors


@pytest.mark.parametrize(
    "template_file",
    TEMPLATE_FILES,
    ids=[f.stem for f in TEMPLATE_FILES]
)
def test_template_name_matches_filename(template_file: Path):
    """
    Verify that the 'template.name' inside each JSON equals the filename (without .json).
    """
    content = json.loads(template_file.read_text(encoding="utf-8"))
    actual_name = content["template"]["name"]
    expected_name = template_file.stem
    
    assert actual_name == expected_name


@pytest.mark.parametrize(
    "template_file",
    TEMPLATE_FILES,
    ids=[f.stem for f in TEMPLATE_FILES]
)
def test_template_naming_convention(template_file: Path):
    """
    Verify that template names follow established naming conventions.
    """
    content = json.loads(template_file.read_text(encoding="utf-8"))
    template_name = content["template"]["name"]
    
    is_valid, errors = ReportNamingConvention.validate_name(template_name)
    
    if not is_valid:
        pytest.fail(f"Template '{template_name}' violates naming convention:\n" + 
                   "\n".join(f"  - {error}" for error in errors))

def test_index_integrity():
    """
    Validate index.json entries:
      - download_url is a valid URL
      - download_url starts with the expected base path
      - no duplicate names
      - every entry corresponds to an existing template file
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

    # Check that all indexed files exist
    indexed_names = set(seen_names)
    template_filenames = {p.stem for p in TEMPLATE_FILES}
    missing_files = indexed_names - template_filenames
    
    assert not missing_files, \
        f"The following entries in index.json do not have a corresponding template file: {sorted(list(missing_files))}"
