import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

ids = re.findall(r'id=["\']([^"\']+)["\']', content)
auth_dash_ids = [i for i in ids if any(k in i.lower() for k in ['auth', 'dash', 'view'])]
print("Matching IDs:", auth_dash_ids)
