with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="tab-home"')
print('pos of mobile tab-home:', pos)
if pos != -1:
    print(text[pos-100:pos+800])
