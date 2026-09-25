import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check for modal and interactive buttons in index.html
test_elements = [
    'modal-add-goal',
    'btn-create-goal-modal',
    'form-add-goal',
    'modal-stash',
    'btn-stash-action',
    'form-stash',
    'sidebar',
    'sidebarToggleBtn',
    'dashboard-view',
    'auth-view',
    'tab-home',
    'tab-goals',
    'tab-calendar',
    'tab-ledger',
    'totalStashedDisplay',
    'toast-container',
    'goals-container',
    'ledger-rows',
    'cal-grid'
]

for el_id in test_elements:
    in_markup = f'id="{el_id}"' in html or f"id='{el_id}'" in html
    in_script = f"'{el_id}'" in html or f'"{el_id}"' in html
    print(f"ID '{el_id}': in_markup={in_markup}, in_script={in_script}")
