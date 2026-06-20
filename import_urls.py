import csv
import json
import os
import sys

CONFIG_FILE = "config.json"

def import_from_csv(filepath):
    """
    Reads a CSV file with columns: name, url
    Example row: Bathroom Fitters Chelsea, https://buildaway.co.uk/location/...
    """
    targets = []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('name', '').strip()
            url = row.get('url', '').strip()
            if name and url:
                targets.append({"name": name, "url": url})
    return targets

def import_from_txt(filepath):
    """
    Reads a plain .txt file with one URL per line.
    Auto-generates a name from the URL slug.
    Example line: https://buildaway.co.uk/location/bathroom-fitters/chelsea-bathroom-fitters.html
    """
    targets = []
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            url = line.strip()
            if url.startswith('http'):
                # Auto-generate name from last part of URL
                slug = url.rstrip('/').split('/')[-1].replace('.html', '').replace('-', ' ').title()
                targets.append({"name": slug, "url": url})
    return targets

def save_config(targets):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"targets": targets}, f, indent=2)
    print(f"config.json updated with {len(targets)} URLs.")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python import_urls.py urls.csv   (CSV with 'name' and 'url' columns)")
        print("  python import_urls.py urls.txt   (plain text, one URL per line)")
        sys.exit(1)

    filepath = sys.argv[1]

    if not os.path.exists(filepath):
        print(f"Error: file '{filepath}' not found.")
        sys.exit(1)

    ext = os.path.splitext(filepath)[1].lower()

    if ext == '.csv':
        targets = import_from_csv(filepath)
    elif ext == '.txt':
        targets = import_from_txt(filepath)
    else:
        print("Unsupported file type. Use .csv or .txt")
        sys.exit(1)

    if not targets:
        print("No valid URLs found in the file.")
        sys.exit(1)

    save_config(targets)
    print("Done! Restart app.py to start monitoring the new URLs.")

if __name__ == "__main__":
    main()
