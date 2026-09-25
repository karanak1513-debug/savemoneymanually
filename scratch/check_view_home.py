with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="view-home"')
print('view-home idx:', idx)
if idx != -1:
    print(text[idx:idx+1500])
