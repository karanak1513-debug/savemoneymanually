with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="tab-home"')
print('tab-home idx:', idx)
if idx != -1:
    idx_nav = text.rfind('<nav', 0, idx)
    end_nav = text.find('</nav>', idx)
    print('=== MOBILE NAV ===')
    print(text[idx_nav:end_nav+6])
