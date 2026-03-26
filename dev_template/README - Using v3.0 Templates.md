# Using TRMM_Base v3.0 Templates

## Issue: Blank White Page

If you're seeing a blank white page when using the Windows Updates Not Installed v2.0 template, it's because the base template HTML is not embedded in the JSON file.

## Solution: Import Base Template First

### Step 1: Import TRMM_Base v3.0 into TRMM

1. Open the file: `dev_base_template/TRMM_Base v3.0.html`
2. Copy the **entire contents** of the file
3. In TRMM, go to: **Settings → Reporting → Base Templates**
4. Click **"Create New Base Template"**
5. Name: `TRMM_Base v3.0`
6. Paste the HTML into the template field
7. Click **Save**

### Step 2: Import the Report Template

Now that the base template exists in TRMM, you can import the report template:

1. The report template JSON references: `"name": "TRMM_Base v3.0"`
2. TRMM will find and use the base template you just created
3. Import the Windows Updates Not Installed v2.0 JSON normally

## Alternative: Embed Base Template in JSON

For production templates (in `templates/` folder), we embed the complete base template HTML in the JSON file's `base_template.html` field.

### To create a production-ready JSON:

```python
import json

# Read the base template HTML
with open('dev_base_template/TRMM_Base v3.0.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

# Read the report template JSON
with open('dev_template/Windows Updates Not Installed v2.0 - Advanced Table Controls.json', 'r', encoding='utf-8') as f:
    template_json = json.load(f)

# Replace the placeholder with actual HTML
template_json['base_template']['html'] = base_html

# Write production-ready JSON
with open('templates/Windows Updates Not Installed v2.0 - Advanced Table Controls.json', 'w', encoding='utf-8') as f:
    json.dump(template_json, f, indent=2, ensure_ascii=False)

print("Production template created!")
```

## Development Workflow

### For Development (`dev_template/` folder):
- Base template HTML is a placeholder comment
- **You must import the base template separately into TRMM**
- Easier to edit and version control (separate files)

### For Production (`templates/` folder):
- Base template HTML is fully embedded
- Complete, self-contained JSON file
- Users can import directly into TRMM without separate base template import

## Troubleshooting

**Q: Still seeing blank page after importing base template?**

A: Check that:
1. Base template name matches exactly: `TRMM_Base v3.0`
2. Report template references the correct name in `base_template.name`
3. No JavaScript errors in browser console (F12)
4. Data source query returns results (check `template_variables`)

**Q: JavaScript errors about undefined functions (buildHeader, renderBody)?**

A: The base template wasn't loaded. Import TRMM_Base v3.0 into TRMM first.

**Q: Table shows "Loading..." forever?**

A: Check:
1. Data source query is correct and returns data
2. JSON data is valid (check browser console)
3. Column definitions match your data fields
4. IDs are correct: `#tableHead`, `#tableBody`, `#loading`, `#tableWrap`

## Example: Device Inventory Report

For a working production example with embedded base template, see:
`templates/Device Inventory Report - Advanced DataTables v1.9 good column sort controls-export.json`

This file has the complete base template HTML embedded, so it works immediately when imported into TRMM.
