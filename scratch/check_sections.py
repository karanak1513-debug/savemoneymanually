with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx_dash = content.find('<div id="dashboard-view"')
idx_three = content.find('initThreeBackground')
idx_loader = content.find('initVaultCinematicLoader')
idx_module = content.find('<script type="module">')

print('Dashboard view index:', idx_dash)
print('initThreeBackground index:', idx_three)
print('initVaultCinematicLoader index:', idx_loader)
print('Module script index:', idx_module)
