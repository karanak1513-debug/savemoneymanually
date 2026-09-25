with open('index.html', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        if 'auth-view' in line or 'dashboard-view' in line or 'authContainer' in line or 'dashboardContainer' in line:
            print(f"{idx}: {line.strip()[:100]}")
