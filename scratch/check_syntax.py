import subprocess

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

tag = '<script type="module">'
s = content.find(tag)
if s == -1:
    print("Could not find module script tag")
    exit(1)
e = content.find('</script>', s)

js = content[s + len(tag):e]
with open('scratch/module_code.js', 'w', encoding='utf-8') as f:
    f.write(js)

print(f"Extracted {len(js)} characters to scratch/module_code.js")
res = subprocess.run(["node", "--check", "scratch/module_code.js"], capture_output=True, text=True)
print("Exit code:", res.returncode)
if res.stdout: print("Stdout:", res.stdout)
if res.stderr: print("Stderr:", res.stderr)
if res.returncode == 0:
    print("ALL JAVASCRIPT SYNTAX VALID!")
