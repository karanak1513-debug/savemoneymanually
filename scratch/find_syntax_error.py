with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i in range(4340, 4460):
    print(f"{i+1}: {repr(lines[i])}")
