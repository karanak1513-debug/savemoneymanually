import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all ids containing goal, ledger, modal, stash, cal
all_ids = re.findall(r'\bid=["\']([a-zA-Z0-9_\-]+)["\']', html)
filtered = [i for i in all_ids if any(k in i.lower() for k in ['goal', 'ledger', 'modal', 'stash', 'cal', 'deposit', 'save'])]
for f_id in sorted(set(filtered)):
    print(f_id)
