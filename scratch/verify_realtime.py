with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

checks = [
    # Auth
    ('onAuthStateChanged(auth',         'Auth observer present'),
    ('enterDashboard(user)',             'enterDashboard called from auth'),
    ('window.__sgInit',                  'Saving Guide init hook in auth'),

    # Firestore reads - must NOT have any getDoc
    ('getDocs(',                         'getDocs GONE'),
    ('await getDoc(',                    'await getDoc GONE'),

    # onSnapshot listeners
    ('unsubGoals = onSnapshot(',         'Goals onSnapshot'),
    ('unsubLedger = onSnapshot(',        'Ledger onSnapshot'),
    ('sgUnsubMsgs = onSnapshot(',        'Chat messages onSnapshot'),
    ('sgUnsubThread = onSnapshot(',      'Thread status onSnapshot'),
    ('sgUnsubAdmin = onSnapshot(',       'Admin threads onSnapshot'),

    # Sync badge
    ('fs-sync-badge',                    'Sync badge HTML/CSS'),
    ('__fsSyncStatus',                   'Sync badge JS function'),
    ('Firestore Realtime Active',        'Sync active label'),
    ('Firestore Connection Dropped',     'Sync error label'),

    # Console logging
    ('console.log("Realtime Sync Triggered [Goals]', 'Goals log'),
    ('console.log("Realtime Sync Triggered [Ledger]','Ledger log'),

    # Write functions (atomic)
    ('addDoc(ledgerCol,',                'addDoc for ledger'),
    ('addDoc(col,',                      'addDoc for goals'),
    ('serverTimestamp()',                 'serverTimestamp used'),

    # setDoc merge for thread
    ('merge: true',                      'setDoc merge on thread'),

    # Saving Guide
    ('BOT_TIMEOUT',                      'Bot 5s timeout'),
    ('BOT_AUTONOMOUS',                   'BOT_AUTONOMOUS state'),
    ('ADMIN_LIVE',                       'ADMIN_LIVE state'),
    ('sg-launcher',                      'Saving Guide launcher'),
]

# Check for presece/absence as appropriate
absent_checks = {'getDocs(', 'await getDoc('}

ok = fail = 0
for key, label in checks:
    found = key in text
    should_be_absent = key in absent_checks
    if should_be_absent:
        passed = not found
        icon = '✅' if passed else '❌ STILL PRESENT (BAD)'
    else:
        passed = found
        icon = '✅' if passed else '❌ MISSING'

    print(f'  {icon}  {label}')
    if passed: ok += 1
    else: fail += 1

print(f'\nResult: {ok}/{ok+fail} checks passed')
