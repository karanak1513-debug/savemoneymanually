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

# Find buttons and forms in markup that might not be in JS
buttons_with_ids = re.findall(r'<button[^>]+id=["\']([a-zA-Z0-9_\-]+)["\']', markup)
unhandled_buttons = []
for b_id in buttons_with_ids:
    if b_id not in scripts_combined:
        unhandled_buttons.append(b_id)

print(f"Total buttons with IDs: {len(buttons_with_ids)}")
print(f"Buttons NOT referenced in scripts: {len(unhandled_buttons)}")
for b in sorted(unhandled_buttons):
    print(f"  - {b}")
