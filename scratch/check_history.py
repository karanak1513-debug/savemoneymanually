with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('tab-history-desktop:', 'tab-history-desktop' in text)
print('tab-history (mobile):', 'id="tab-history"' in text)
print('view-history:', 'id="view-history"' in text)
print('TABS array has history:', "'history'" in text)
print('renderHistory in text:', 'function renderHistory()' in text)
