import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Separate scripts from markup
script_matches = list(re.finditer(r'<script.*?>.*?</script>', html, re.DOTALL))
scripts_combined = "\n".join(m.group(0) for m in script_matches)

# Everything outside scripts is markup
markup_parts = []
last_end = 0
for m in script_matches:
    markup_parts.append(html[last_end:m.start()])
    last_end = m.end()
markup_parts.append(html[last_end:])
markup = "\n".join(markup_parts)

ids_in_markup = set(re.findall(r'\bid=["\']([a-zA-Z0-9_\-]+)["\']', markup))
ids_in_js = set(re.findall(r'getElementById\(["\']([a-zA-Z0-9_\-]+)["\']\)', scripts_combined))

print(f"Total IDs in markup: {len(ids_in_markup)}")
print(f"Total IDs in getElementById: {len(ids_in_js)}")

missing = ids_in_js - ids_in_markup
print(f"\nMissing IDs queried by getElementById ({len(missing)}):")
for mid in sorted(missing):
    # Check if they are dynamically created or used conditionally
    count = scripts_combined.count(f"'{mid}'") + scripts_combined.count(f'"{mid}"')
    print(f"  - {mid} (referenced {count} times)")

# Also check querySelector with #id
qs_ids = set(re.findall(r'querySelector\(["\']#([a-zA-Z0-9_\-]+)["\']\)', scripts_combined))
missing_qs = qs_ids - ids_in_markup
print(f"\nMissing IDs queried by querySelector('#...') ({len(missing_qs)}):")
for qid in sorted(missing_qs):
    print(f"  - {qid}")
