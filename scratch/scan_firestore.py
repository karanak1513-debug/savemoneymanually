with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f'Total lines: {len(lines)}')

print('\n--- getDocs/getDoc calls ---')
for i, line in enumerate(lines):
    if 'getDocs(' in line or 'getDoc(' in line:
        print(f'  L{i+1}: {line.strip()[:90]}')

print('\n--- existing onSnapshot calls ---')
for i, line in enumerate(lines):
    if 'onSnapshot(' in line:
        print(f'  L{i+1}: {line.strip()[:90]}')

print('\n--- Key function / addDoc / deleteDoc ---')
for i, line in enumerate(lines):
    s = line.strip()
    if any(kw in s for kw in ['function initDataSync', 'function renderLedger', 'function renderGoal',
                               'enterDashboard', 'function recordTx', 'addDoc(', 'updateDoc(',
                               'deleteDoc(', 'function switchTab', 'ledgerUnsub', 'goalsUnsub']):
        print(f'  L{i+1}: {s[:90]}')
