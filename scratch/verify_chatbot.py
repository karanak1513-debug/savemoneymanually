with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

checks = [
    'chatbot-launcher', 'chatbot-window', 'admin-console-overlay',
    'TWO-WAY LIVE SUPPORT', 'initChatSystem', 'BOT_RULES',
    'admin-threads-list', 'admin-reply-send', 'ensureChatThread',
    'support_threads', 'AGENT_CONNECTED', 'AGENT_REQUESTED'
]
for c in checks:
    status = 'FOUND' if c in text else 'MISSING'
    print(f'{c}: {status}')
