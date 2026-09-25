"""Remove legacy botMatch + old botRespond (L4237-L4294) precisely."""

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Before: {len(lines)} lines")

# Find botMatch and the second (legacy) botRespond
botmatch_lines = [i for i, l in enumerate(lines) if 'function botMatch(' in l]
old_respond_lines = [i for i, l in enumerate(lines) if 'async function botRespond(' in l]

print(f"botMatch at: {[x+1 for x in botmatch_lines]}")
print(f"botRespond at: {[x+1 for x in old_respond_lines]}")

# The legacy block starts at botMatch (4237 → index 4236)
# The legacy block ends with the closing } of the second botRespond
if len(botmatch_lines) >= 1 and len(old_respond_lines) >= 2:
    start_idx = botmatch_lines[0]  # start of botMatch
    legacy_respond_start = old_respond_lines[1]  # second botRespond

    # Find closing } of the second botRespond by scanning forward
    end_idx = None
    brace_depth = 0
    in_fn = False
    for i in range(legacy_respond_start, min(legacy_respond_start + 80, len(lines))):
        stripped = lines[i].strip()
        for ch in stripped:
            if ch == '{': brace_depth += 1; in_fn = True
            elif ch == '}': brace_depth -= 1
        if in_fn and brace_depth == 0:
            end_idx = i + 1  # exclusive
            break

    print(f"Block to remove: L{start_idx+1} to L{end_idx}")
    if end_idx and start_idx < end_idx:
        # Show preview
        for i in range(start_idx, min(start_idx+3, end_idx)):
            print(f"  L{i+1}: {lines[i].rstrip()[:70]}")
        print("  ...")
        for i in range(max(end_idx-3, start_idx), end_idx):
            print(f"  L{i+1}: {lines[i].rstrip()[:70]}")

        del lines[start_idx:end_idx]
        print(f"After: {len(lines)} lines")

        with open('index.html', 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print("✅ Legacy botMatch + botRespond removed")
    else:
        print("⚠️  Bad range, skip")
elif len(old_respond_lines) >= 2:
    # Only remove second botRespond (no botMatch to worry about)
    legacy_respond_start = old_respond_lines[1]
    end_idx = None
    brace_depth = 0
    in_fn = False
    for i in range(legacy_respond_start, min(legacy_respond_start + 80, len(lines))):
        stripped = lines[i].strip()
        for ch in stripped:
            if ch == '{': brace_depth += 1; in_fn = True
            elif ch == '}': brace_depth -= 1
        if in_fn and brace_depth == 0:
            end_idx = i + 1
            break
    print(f"Remove just botRespond duplicate: L{legacy_respond_start+1} to L{end_idx}")
    if end_idx:
        del lines[legacy_respond_start:end_idx]
        with open('index.html', 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"✅ Duplicate botRespond removed. Now: {len(lines)} lines")
else:
    print("✅ No duplicates found — nothing to remove")
