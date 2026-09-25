import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all event listeners
listeners = re.findall(r'([a-zA-Z0-9_\-\$\.]+)\s*(\??\.)\s*addEventListener\(', html)

print(f"Total addEventListener calls: {len(listeners)}")
unsafe_listeners = []
for el, op in listeners:
    if op != '?.':
        unsafe_listeners.append(el)

print(f"Listeners without optional chaining (?.): {len(unsafe_listeners)}")
for u in unsafe_listeners:
    print(f"  - {u}")
