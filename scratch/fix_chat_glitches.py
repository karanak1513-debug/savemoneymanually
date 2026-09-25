with open('index.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Replace corrupted chars
corrupted_count = content.count('\ufffd')
print(f"Total replacement characters found: {corrupted_count}")

# Replace \ud83d\ufffd in Namaste ji
content = content.replace('\ud83d\ufffd <strong>Namaste ji!</strong>', '👋 <strong>Namaste ji!</strong>')
content = content.replace('\ud83d\ufffd\ufe0f', '🛡️')
content = content.replace('Firebase 256-bit encrypted \ud83d\ufffd', 'Firebase 256-bit encrypted 🛡️')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Cleaned corrupted emojis.")
