# TRMM_Base Version Changelog

## v3.1 (2026-02-25)

### Centralized Company Customization

All brandable values are now consolidated into a single, well-documented "COMPANY CUSTOMIZATION" section at the top of the `<style>` block. Companies only need to edit that one section (plus the logo/company info in `<body>`) to fully brand all reports.

#### New CSS Custom Properties (27 added)

| Group | Variables | Purpose |
|-------|-----------|---------|
| Page | `--page-margin` | PDF margins |
| Typography | `--body-font`, `--body-color`, `--body-font-size` | Fonts and text |
| Header | `--header-padding`, `--header-border-radius`, `--header-h1-size`, `--header-h2-size`, `--logo-width`, `--logo-margin-right` | Header sizing |
| Table | `--table-font-size`, `--table-cell-padding`, `--table-row-border`, `--table-cell-bg`, `--table-thead-bg` | Table appearance |
| Filters | `--focus-ring`, `--combo-hover-bg`, `--badge-select-bg`, `--badge-select-color`, `--badge-select-border`, `--clear-btn-bg`, `--clear-btn-hover-bg` | Interactive controls |
| Badges | `--badge-padding`, `--badge-radius`, `--badge-font-size` | Status badges |
| Footer | `--footer-margin-top`, `--footer-padding-top`, `--footer-font-size`, `--footer-color` | Footer styling |

#### Hardcoded Values Replaced

~30 hardcoded color, font, and spacing values throughout CSS now reference CSS custom properties. Fixes include:
- Several `#ddd` borders now use `var(--border-color)` (were inconsistent)
- `#fff` backgrounds now use `var(--table-cell-bg)` for easy dark-mode potential
- Focus ring glow now uses `var(--focus-ring)` instead of hardcoded rgba

#### Company Info Fields (New)

Added ready-made fields for company branding that **auto-hide when empty** via CSS `:empty` pseudo-class:

- **`.header-company`** - Company name/phone line below report title in header
- **`.footer-company`** - Company info line in footer

When a company fills in their info, the fields appear automatically. When empty, they are invisible — no layout impact.

#### HTML Improvements

- Clear comment blocks marking every customizable area in `<body>`:
  - `COMPANY LOGO` — logo image URL and alt text
  - `COMPANY NAME / CONTACT INFO` — header company line
  - `DATE FORMAT` — strftime pattern with common format examples
  - `FOOTER COMPANY INFO` — footer company line
- Inline `style="width: 80px; height: auto;"` removed from logo `<img>` tag
- New `.header-logo img` CSS rule for proper logo scaling via `--logo-width` variable

#### Quick Start for Companies

1. Change `--header-bg` to your primary color
2. Change `--focus` to your accent color
3. Update the logo URL in the `<body>` section
4. Add your company name in `.header-company`
5. Add your company info in `.footer-company`
6. Adjust other variables as needed

#### Migration from v3.0

**Drop-in replacement.** No report template changes needed. All default values match v3.0 exactly, so visual output is identical. The only addition is the empty company info fields which are invisible by default.

#### Breaking Changes

None.

---

## v3.0 (2026-01-13)

### Major Release: Advanced Table Controls Framework

This is a **major architectural addition** that transforms TRMM_Base into a complete framework for building interactive, sortable, filterable data tables with professional UI controls.

#### What's New in v3.0

**Complete JavaScript Framework** (~600 lines):
- Global search across all columns
- Per-column filtering (text search, multi-select, range filters)
- Column sorting (text and numeric with locale-aware comparison)
- Combo box filter controls with search and multi-select
- Popover checkbox pickers
- Clear buttons on all filters (floating red X)
- Sticky table headers
- Row counter (filtered vs total)
- State management system
- Utility functions (debounce, stripHtml, popover positioning)

**Advanced CSS Styling** (~500 lines):
- Combo box controls (`.combo`, `.combo-input`, `.combo-right`, `.combo-btn`)
- Clear filter buttons (`.clear-filter-btn`) - different from print button
- Global search bar (`.search-wrap`, `.search-input`, `.search-icon`)
- Two-row header layout (`.headbar`, `.th-inner`, `.th-title`, `.sort-ind`)
- Popover styling (`.popover`, `.opt`)
- Range filter inputs (`.filter-wrap`, `.filter-input`)
- Selection badges (`.badge`)
- Table layout (`.table-wrap`, `table.vt`)
- Sticky header with z-index management
- Print mode refinements (filters auto-hidden with `.no-print`)

**Retained from v2.4:**
- Print button in header top-right corner
- Print-optimized styling (`@media print`)
- Color palette and theming (CSS custom properties)
- Typography and utilities
- Badge system
- Footer layout

### What's Included in the Base Template

The base template now provides:

1. **Full CSS** for all advanced table control components
2. **Complete JavaScript framework** with:
   - Utility functions (`$`, `$$`, `debounce`, `htmlNode`, `stripHtml`)
   - State management object
   - Data processing (`compare`, `valueFor`, `rowPassesFilters`, `getFilteredSortedData`)
   - Unique value extraction (`uniqueValues`, `uniqueValuesByKey`, `filteredRowsExcluding`)
   - Header builder (`buildHeader`)
   - Combo box builder (`buildCombo`)
   - Popover handlers (`togglePopover`, `togglePopoverDual`, `closePopover`, `placePopoverUnder`)
   - Body renderer (`renderBody`)
   - Counter updater (`updateCount`)
3. **Print button** - Retained from v2.4, auto-hidden when printing
4. **Documentation comments** explaining framework usage

### What Reports Must Provide

Reports using TRMM_Base v3.0 must provide:

1. **HTML structure** with specific IDs:
   ```html
   <div id="loading">Loading...</div>
   <div class="table-wrap" id="tableWrap" style="display:none">
       <table class="vt" id="dataTable">
           <thead id="tableHead"></thead>
           <tbody id="tableBody"></tbody>
       </table>
   </div>
   ```

2. **Data source** as JSON in script tag:
   ```html
   <script id="data-json" type="application/json">
   [
       { "field1": "value1", "field2": "value2", ... },
       ...
   ]
   </script>
   ```

3. **Column definitions** array:
   ```javascript
   var columns = [
       {
           id: 'field1',           // Data field name
           title: 'Column Title',   // Display name
           html: false,             // Does data contain HTML?
           filter: true,            // Enable filtering?
           selectable: true,        // Multi-select filter?
           sortable: true,          // Enable sorting?
           numeric: false,          // Numeric sorting?
           range: false,            // Range filter (min/max)?
           filterKey: 'field1Text', // Alternative field for filtering
           special: null            // Special handling (e.g., 'clientSite')
       },
       ...
   ];
   ```

4. **Initialization code**:
   ```javascript
   // Load and preprocess data
   var data = JSON.parse($('#data-json').textContent);

   // Build UI and render
   buildHeader();
   renderBody();
   updateCount();

   // Show table
   $('#loading').style.display = 'none';
   $('#tableWrap').style.display = 'block';
   ```

5. **Row counter elements** (optional):
   ```html
   <span id="visibleCount">0</span> of <span id="totalCount">0</span>
   ```

### Migration Guide

#### From v2.4 to v3.0

TRMM_Base v3.0 is **not a drop-in replacement** for v2.4. It requires restructuring your table HTML and adding column definitions.

**When to migrate:**
- Your report has a data table that would benefit from sorting/filtering
- You want professional, interactive table controls
- You're willing to restructure the table HTML

**How to migrate:**

1. **Update base template reference:**
   ```jinja2
   {% extends "TRMM_Base v3.0" %}
   ```

2. **Restructure table HTML:**
   - Remove existing `<table>` structure
   - Add loading indicator: `<div id="loading">Loading...</div>`
   - Add table wrapper with required IDs (see "What Reports Must Provide" above)

3. **Convert data to JSON:**
   - Embed your data as JSON in `<script id="data-json">` tag
   - Use Jinja2 to generate JSON from TRMM data sources

4. **Define columns:**
   - Create `columns` array describing your table structure
   - Specify which columns are filterable, sortable, etc.

5. **Add initialization code:**
   ```javascript
   buildHeader();
   renderBody();
   updateCount();
   $('#loading').style.display = 'none';
   $('#tableWrap').style.display = 'block';
   ```

6. **Test thoroughly:**
   - Verify all filters work
   - Check sorting on all columns
   - Test print output

#### From Device Inventory Report v1.9

If you have a report based on Device Inventory Report v1.9, you can **simplify** it:

1. **Remove custom JavaScript:**
   - Delete your copy of the filtering/sorting framework (~600 lines)
   - Keep only data preprocessing and initialization code

2. **Update to use base template functions:**
   - Replace custom `buildHeader()` with base template version
   - Replace custom `renderBody()` with base template version
   - Replace custom filter builders with base template version

3. **Benefits:**
   - Smaller report template
   - Automatic bug fixes and improvements from base template
   - Consistent behavior across all reports

### When to Use v3.0 vs v2.4

**Use TRMM_Base v3.0 for:**
- ✅ Data-heavy reports with tables (RECOMMENDED DEFAULT)
- ✅ Reports where users need to filter/sort data
- ✅ Professional, interactive table interfaces
- ✅ Reports with 10+ rows of data
- ✅ Any report where sorting or filtering adds value

**Use TRMM_Base v2.4 for:**
- ✅ Simple reports without data tables
- ✅ Static content (text, images, charts)
- ✅ Reports with custom JavaScript needs
- ✅ Very small tables (3-5 rows) where interactivity isn't needed

### Example Templates

**Simple Example:**
- File: `dev_template/Windows Updates Not Installed v2.0 - Advanced Table Controls.json`
- Shows: Basic usage with 4 columns, text and multi-select filters
- Best for: Learning the framework

**Production Example:**
- File: `templates/Device Inventory Report - Advanced DataTables v1.9 good column sort controls-export.json`
- Shows: Advanced usage with 9 columns, range filters, dual filters, HTML content
- Best for: Understanding complex implementations

### Breaking Changes

1. **Table structure:** Completely different HTML structure required
2. **JavaScript required:** Reports must provide column definitions and initialization
3. **IDs required:** Specific element IDs must be present (`#tableHead`, `#tableBody`, etc.)
4. **Data format:** Data must be provided as JSON array
5. **Template size:** Base template is significantly larger (~1400 lines vs 265 lines)

### Benefits

1. **Consistency:** All reports using v3.0 work the same way
2. **DRY principle:** Framework code written once, used everywhere
3. **Maintainability:** Bug fixes benefit all reports automatically
4. **Professional UX:** Polished, interactive controls
5. **Performance:** Client-side filtering is fast and responsive
6. **Mobile-friendly:** Responsive design works on all screen sizes
7. **Print-ready:** Filters automatically hidden, table prints cleanly

### Technical Details

**File Size:**
- v2.4: ~265 lines (11 KB)
- v3.0: ~1400 lines (56 KB)
- Increase justified by complete framework functionality

**Browser Compatibility:**
- ES5 JavaScript for broad compatibility
- Uses standard DOM APIs
- No external dependencies
- Tested in Chrome, Firefox, Safari, Edge

**Performance:**
- Debounced input (140ms for global search, 120ms for column search)
- Efficient array filtering and sorting
- Minimal DOM manipulation (full re-render only on filter/sort change)
- Handles 1000+ rows smoothly on modern browsers

**Accessibility:**
- ARIA labels on interactive controls
- Keyboard navigation support
- Screen reader compatible
- Proper semantic HTML

### Source Attribution

Advanced table controls extracted and generalized from:
- Device Inventory Report v1.9 by David Main
- Production-tested in TacticalRMM environments
- Refined based on real-world usage patterns

### Documentation

Complete documentation available in:
- `CLAUDE.md` - Framework usage guide, column definitions, customization
- `dev_base_template/TRMM_Base v3.0.html` - Inline code comments
- `dev_template/Windows Updates Not Installed v2.0 - Advanced Table Controls.json` - Working example

---

## v2.4 (2025-12-31)

### Print Button Float Fix

Fixed the print button to truly float over content without displacing other header elements.

#### Layout Changes

**Removed Content Displacement:**
- Removed `margin-right: 130px` from `.header-date` class
- Header date and other elements now maintain their natural positioning
- Content no longer shifts left to make room for the button

**Improved Z-Index:**
- Added `z-index: 10` to `.print-controls`
- Ensures button always floats on top of other content
- Button can overlap header date if needed (semi-transparent design makes this acceptable)

#### Visual Benefits

1. **Natural Layout:** Header elements flow naturally without forced margins
2. **True Floating:** Print button genuinely floats over content with proper z-index
3. **No Displacement:** Date and titles maintain consistent positioning
4. **Cleaner Code:** Removed workaround margin that was compensating for absolute positioning

### Migration from v2.3

To upgrade from v2.3 to v2.4, simply replace the base_template section. The only changes are:
- Removed one CSS property (`margin-right` from `.header-date`)
- Added one CSS property (`z-index: 10` to `.print-controls`)

### Breaking Changes

None. Fully backwards compatible. This is a visual improvement that fixes layout displacement.

---

## v2.3 (2025-12-31)

### Print Button Float Fix

Fixed the print button to truly float over content without displacing other header elements.

#### Layout Changes

**Removed Content Displacement:**
- Removed `margin-right: 130px` from `.header-date` class
- Header date and other elements now maintain their natural positioning
- Content no longer shifts left to make room for the button

**Improved Z-Index:**
- Added `z-index: 10` to `.print-controls`
- Ensures button always floats on top of other content
- Button can overlap header date if needed (semi-transparent design makes this acceptable)

#### Visual Benefits

1. **Natural Layout:** Header elements flow naturally without forced margins
2. **True Floating:** Print button genuinely floats over content with proper z-index
3. **No Displacement:** Date and titles maintain consistent positioning
4. **Cleaner Code:** Removed workaround margin that was compensating for absolute positioning

### Migration from v2.2

To upgrade from v2.2 to v2.3, simply replace the base_template section. The only changes are:
- Removed one CSS property (`margin-right` from `.header-date`)
- Added one CSS property (`z-index: 10` to `.print-controls`)

### Breaking Changes

None. Fully backwards compatible. This is a visual improvement that fixes layout displacement.

---

## v2.2 (2025-12-31)

### Print Button Position Update

Improved the print button placement for better visual integration with the header.

#### Layout Changes

**Print Button in Header:**
- Moved print button from below header into top-right corner of header
- Uses absolute positioning within the header container
- Header now uses `position: relative` to contain the button
- Button positioned at `top: 20px; right: 20px` within header

**Styling Updates:**
- Print button now has semi-transparent background: `rgba(255, 255, 255, 0.2)`
- Border added with transparency: `1px solid rgba(255, 255, 255, 0.3)`
- Hover state increases opacity for better visual feedback
- Smaller, more compact button size: `padding: 8px 16px`
- Shortened button text from "🖨️ Print Report" to "🖨️ Print"

**Header Date Adjustment:**
- Added `margin-right: 130px` to `.header-date` to prevent overlap with button
- Ensures adequate spacing between date and print button

#### Visual Benefits

1. **Cleaner Layout:** Button integrated into header instead of separate row
2. **Better Use of Space:** Eliminates extra margin below header
3. **Professional Appearance:** Semi-transparent button blends with header
4. **Improved UX:** Button in expected location (top-right corner)

### Migration from v2.1

To upgrade from v2.1 to v2.2, simply replace the base_template section. The changes are:
- Print button moved into header HTML structure
- Updated CSS for `.report-header`, `.print-controls`, and `.header-date`
- Updated button styling with transparency effects

### Breaking Changes

None. Fully backwards compatible with report content.

---

## v2.1 (2025-12-31)

### New Features: Print Formatting

Added comprehensive print formatting capabilities that work automatically when users print or save as PDF from their browser.

#### Print-Specific Styles (`@media print`)

**Page Break Control:**
- Tables automatically handle page breaks properly
- Table rows avoid breaking across pages (`page-break-inside: avoid`)
- Table headers repeat on each printed page (`display: table-header-group`)
- Prevents widows and orphans in text content

**Color Preservation:**
- Colors are preserved when printing using `print-color-adjust: exact`
- Applies to header backgrounds, badges, and status row colors
- Ensures branded colors appear in printed output

**Print Optimization:**
- Interactive elements hidden automatically (`.no-print` class)
- Optimized spacing for print media
- Rounded corners removed for cleaner print output
- Links don't show URLs by default (cleaner appearance)

**Screen-Only Content:**
- New `.print-only` class for content that only appears in print
- New `.no-print` class for content hidden when printing

#### New UI Elements

**Print Button:**
- Added print button in header section
- Automatically hidden when printing (`.no-print` class)
- Styled to match header color scheme
- Uses browser's native print dialog

#### CSS Improvements

**New Utility Classes:**
```css
.no-print      /* Hide element when printing */
.print-only    /* Show element only when printing */
.print-button  /* Styled print button */
.print-controls /* Container for print UI elements */
```

### Migration from v2.0

To upgrade existing reports to v2.1:

1. Replace the `base_template` section in your JSON file with the new v2.1 base_template
2. Update the extends statement in your template_md to reference v2.1:
   ```jinja2
   {% extends "TRMM_Base v2.1" %}
   ```
3. No other changes required - all new features are backwards compatible

### Breaking Changes

None. This is a fully backwards-compatible update.

### Technical Details

**Print Color Adjustment:**
The new version uses multiple vendor prefixes to ensure color preservation across browsers:
- `-webkit-print-color-adjust: exact` (Chrome/Safari)
- `print-color-adjust: exact` (Firefox/Standard)
- `color-adjust: exact` (Fallback)

**Page Break Properties:**
- `page-break-inside: avoid` on table rows
- `page-break-after: auto` for flow control
- `orphans: 3` and `widows: 3` for text content

### Benefits

1. **No Extra Configuration:** Print formatting works automatically
2. **Professional Output:** Printed reports look polished and branded
3. **User-Friendly:** Print button makes printing obvious to end users
4. **Universal:** Works with browser print and PDF generation
5. **Customizable:** Individual reports can override print styles if needed

### Usage Examples

**Add print-only content:**
```html
<div class="print-only">
    <p>This message only appears when printing</p>
</div>
```

**Hide interactive elements:**
```html
<button class="no-print">Click Me</button>
```

**Override print styles in individual reports:**
```css
@media print {
    @page {
        size: letter landscape; /* Force landscape */
    }

    .report-table {
        font-size: 10px; /* Smaller for dense data */
    }
}
```

---

## v2.0

Initial standardized base template with:
- CSS custom properties for theming
- Standard table structure and styling
- Badge system for status indicators
- Header/footer layout
- Stub classes for report-specific overrides
- PDF page settings

### Structure

- Color palette using CSS variables
- Typography and utility classes
- Header layout with logo and date
- Table styling with sortable headers
- Badge components
- Footer layout

---

## Version History Summary

| Version | Date | Key Changes |
|---------|------|-------------|
| v3.1 | 2026-02-25 | Centralized company customization, 27 new CSS variables, company info fields |
| v3.0 | 2026-01-13 | Advanced Table Controls framework (JS filtering, sorting, combo boxes) |
| v2.4 | 2025-12-31 | Fixed print button to float without displacing content, added z-index |
| v2.3 | 2025-12-31 | Duplicate of v2.4 (print button float fix) |
| v2.2 | 2025-12-31 | Print button moved to header top-right corner, improved styling |
| v2.1 | 2025-12-31 | Print formatting, print button, page break control |
| v2.0 | Previous | Initial standardized base template |
