#!/usr/bin/env python3
"""
Create Production Template with Embedded Base Template
=======================================================

This script takes a development template (with base template placeholder)
and creates a production-ready template with the full base template HTML embedded.

Usage:
    python create_production_template.py

Or import and use the function:
    from create_production_template import embed_base_template
    embed_base_template('dev_template/template.json', 'templates/template.json')
"""

import json
import os
from pathlib import Path


def embed_base_template(dev_template_path, output_path=None, base_template_path=None):
    """
    Embed the full base template HTML into a report template JSON.

    Args:
        dev_template_path: Path to development template JSON (with placeholder)
        output_path: Path to write production template (default: templates/ folder)
        base_template_path: Path to base template HTML (default: auto-detect from JSON)

    Returns:
        Path to the created production template
    """
    dev_template_path = Path(dev_template_path)

    # Read the development template
    print(f"Reading development template: {dev_template_path}")
    with open(dev_template_path, 'r', encoding='utf-8') as f:
        template_json = json.load(f)

    # Determine base template path
    if base_template_path is None:
        base_name = template_json['base_template']['name']
        # Try to find the base template file
        possible_paths = [
            Path('dev_base_template') / f'{base_name}.html',
            Path('../dev_base_template') / f'{base_name}.html',
            Path('.') / f'{base_name}.html'
        ]

        for path in possible_paths:
            if path.exists():
                base_template_path = path
                break

        if base_template_path is None:
            raise FileNotFoundError(
                f"Could not find base template: {base_name}.html\n"
                f"Tried: {[str(p) for p in possible_paths]}\n"
                f"Please specify base_template_path manually."
            )

    base_template_path = Path(base_template_path)

    # Read the base template HTML
    print(f"Reading base template: {base_template_path}")
    with open(base_template_path, 'r', encoding='utf-8') as f:
        base_html = f.read()

    # Replace the placeholder with actual HTML
    template_json['base_template']['html'] = base_html

    # Determine output path
    if output_path is None:
        # Default: templates/ folder with same filename
        output_path = Path('templates') / dev_template_path.name
        # If we're in dev_template/, go up one level
        if dev_template_path.parent.name == 'dev_template':
            output_path = dev_template_path.parent.parent / 'templates' / dev_template_path.name

    output_path = Path(output_path)

    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write production-ready JSON
    print(f"Writing production template: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(template_json, f, indent=2, ensure_ascii=False)

    print("✓ Production template created successfully!")
    print(f"\nTemplate size: {output_path.stat().st_size / 1024:.1f} KB")
    print(f"Base template: {template_json['base_template']['name']}")
    print(f"Report template: {template_json['template']['name']}")

    return output_path


def main():
    """
    Interactive script to create production templates.
    """
    print("=" * 70)
    print("Create Production Template with Embedded Base Template")
    print("=" * 70)
    print()

    # Find development templates
    dev_template_dir = Path('dev_template')
    if not dev_template_dir.exists():
        dev_template_dir = Path('.')

    json_files = list(dev_template_dir.glob('*.json'))

    if not json_files:
        print("No JSON files found in dev_template/")
        return

    print("Available development templates:")
    for i, path in enumerate(json_files, 1):
        print(f"  {i}. {path.name}")
    print()

    # Get user choice
    while True:
        try:
            choice = input(f"Select template (1-{len(json_files)}) or 'all': ").strip().lower()

            if choice == 'all':
                selected = json_files
                break
            else:
                idx = int(choice) - 1
                if 0 <= idx < len(json_files):
                    selected = [json_files[idx]]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(json_files)}")
        except (ValueError, KeyboardInterrupt):
            print("\nCancelled.")
            return

    print()

    # Process selected templates
    for template_path in selected:
        try:
            print(f"\nProcessing: {template_path.name}")
            print("-" * 70)
            output_path = embed_base_template(template_path)
            print()
        except Exception as e:
            print(f"✗ Error processing {template_path.name}: {e}")
            print()

    print("=" * 70)
    print("Done!")
    print()


if __name__ == '__main__':
    main()
