import urllib.request

for port in [3000, 3001]:
    try:
        content = urllib.request.urlopen(f'http://localhost:{port}').read().decode('utf-8')
        print(f"Port {port}:")
        print("  Has 'app-opening-loader':", 'id="app-opening-loader"' in content)
        print("  Has 'loader-orbit-ring':", 'loader-orbit-ring' in content)
        print("  Has 'loader-progress-fill':", 'loader-progress-fill' in content)
        print("  Has 'Initializing Quota Math...':", 'Initializing Quota Math...' in content)
    except Exception as e:
        print(f"Port {port} error:", e)
