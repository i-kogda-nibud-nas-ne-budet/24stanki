"""Optimize styles.css v2: proper property merging, no self-ref vars."""
import re
import os
from collections import OrderedDict

CSS_PATH = r'D:\PROJECTS\24stanki\styles.css'
HTML_DIR = r'D:\PROJECTS\24stanki'

# 1. Gather all HTML classes
all_html_classes = set()
for fname in os.listdir(HTML_DIR):
    if fname.endswith('.html'):
        with open(os.path.join(HTML_DIR, fname), 'r', encoding='utf-8') as f:
            content = f.read()
        for m in re.finditer(r'class="([^"]*)"', content):
            for cls in m.group(1).split():
                all_html_classes.add(cls)

def is_selector_used(selector):
    classes_in_sel = re.findall(r'\.([a-zA-Z][\w-]*)', selector)
    if not classes_in_sel:
        return True
    return any(cls in all_html_classes for cls in classes_in_sel)


# 2. Read and preprocess
with open(CSS_PATH, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace Roboto Condensed
css = css.replace("'Roboto Condensed', sans-serif", "'Montserrat', sans-serif")


# 3. Tokenize CSS into blocks
def tokenize_css(text):
    """Returns list of (type, content, start, end) where type is 'rule', 'media', 'keyframes', 'comment', 'var', 'text'."""
    blocks = []
    i = 0
    n = len(text)

    while i < n:
        # Skip whitespace
        m = re.match(r'[ \t]*\n?', text[i:])
        if m:
            i += len(m.group())

        if i >= n:
            break

        # Comment
        if text[i:i+2] == '/*':
            end = text.find('*/', i + 2)
            if end == -1:
                blocks.append(('comment', text[i:], i, len(text)))
                break
            blocks.append(('comment', text[i:end+2], i, end+2))
            i = end + 2
            continue

        # @keyframes
        if text[i:].lstrip().startswith('@keyframes'):
            start = i
            brace = text.find('{', i)
            if brace == -1:
                i = n
                continue
            depth = 0
            j = brace
            while j < n:
                if text[j] == '{': depth += 1
                elif text[j] == '}':
                    depth -= 1
                    if depth == 0:
                        blocks.append(('keyframes', text[start:j+1], start, j+1))
                        i = j + 1
                        break
                j += 1
            else:
                blocks.append(('keyframes', text[start:], start, n))
                i = n
            continue

        # @media
        stripped = text[i:].lstrip()
        if stripped.startswith('@media'):
            start = i
            brace = text.find('{', i)
            if brace == -1:
                i = n
                continue
            depth = 0
            j = brace
            while j < n:
                if text[j] == '{': depth += 1
                elif text[j] == '}':
                    depth -= 1
                    if depth == 0:
                        blocks.append(('media', text[start:j+1], start, j+1))
                        i = j + 1
                        break
                j += 1
            else:
                blocks.append(('media', text[start:], start, n))
                i = n
            continue

        # @charset, @import etc - skip to next ;
        if text[i:].lstrip().startswith('@'):
            semi = text.find(';', i)
            if semi != -1:
                blocks.append(('other', text[i:semi+1], i, semi+1))
                i = semi + 1
            else:
                blocks.append(('other', text[i:], i, n))
                i = n
            continue

        # Regular rule: selector { ... }
        brace = text.find('{', i)
        if brace == -1:
            rest = text[i:].strip()
            if rest:
                blocks.append(('text', rest, i, n))
            break
        selector = text[i:brace].strip()
        if not selector:
            i = brace + 1
            continue
        # Find matching }
        depth = 0
        j = brace
        while j < n:
            if text[j] == '{': depth += 1
            elif text[j] == '}':
                depth -= 1
                if depth == 0:
                    blocks.append(('rule', text[i:j+1], i, j+1))
                    i = j + 1
                    break
            j += 1
        else:
            blocks.append(('rule', text[i:], i, n))
            i = n

    return blocks


def parse_rule(block):
    """Parse 'sel { props }' -> (selector, [(prop, value)])"""
    m = re.match(r'([^{]+)\{(.*)\}', block, re.DOTALL)
    if not m:
        return '', []
    selector = m.group(1).strip()
    body = m.group(2).strip()
    props = []
    for line in body.split('\n'):
        line = line.strip()
        if line.startswith('/*') or not line:
            continue
        # Remove trailing comment
        line = re.sub(r'/\*.*?\*/', '', line).strip()
        if ':' in line:
            prop, _, val = line.partition(':')
            val = val.strip().rstrip(';').strip()
            props.append((prop.strip(), val))
    return selector, props


def merge_props(all_props):
    """Merge properties, last value wins for same property name."""
    seen = OrderedDict()
    for prop, val in all_props:
        seen[prop] = val
    return list(seen.items())


def rebuild_rule(selector, props):
    if not props:
        return ''
    lines = '\n'.join(f'    {p}: {v};' for p, v in props)
    return f'{selector} {{\n{lines}\n}}'


def rebuild_media(breakpoint, rules):
    inner = '\n\n'.join(rules)
    return f'{breakpoint} {{\n{inner}\n}}'


# 4. Process
blocks = tokenize_css(css)

# Separate regular rules, media blocks, keyframes, etc
regular_rules = []  # (selector, [(prop, val)])
media_blocks_raw = []
keyframes = []
other = []

for btype, content, start, end in blocks:
    if btype == 'rule':
        sel, props = parse_rule(content)
        if sel:
            regular_rules.append((sel, props))
    elif btype == 'media':
        media_blocks_raw.append(content)
    elif btype == 'keyframes':
        keyframes.append(content)
    elif btype in ('comment', 'other', 'text'):
        if content.strip():
            other.append(content.strip())

# 5. Deduplicate rules: merge properties by selector (last value wins)
merged = OrderedDict()
for sel, props in regular_rules:
    if sel in merged:
        merged[sel].extend(props)
    else:
        merged[sel] = list(props)

# Rebuild and filter
final_rules = []
for sel, props in merged.items():
    # Filter unused
    if not is_selector_used(sel):
        continue
    deduped_props = merge_props(props)
    block = rebuild_rule(sel, deduped_props)
    if block:
        final_rules.append(block)

# 6. Process @media blocks: merge by breakpoint, deduplicate inner rules
def parse_media(media_text):
    m = re.match(r'(@media\s*\([^)]+\))\s*\{', media_text)
    if not m:
        return None, media_text
    bp = m.group(1)
    inner = media_text[m.end():]
    if inner.rstrip().endswith('}'):
        inner = inner.rstrip()[:-1]
    return bp, inner

def parse_inner_rules(inner):
    """Parse the inner content of a @media block into (selector, props) list."""
    rules = []
    i = 0
    n = len(inner)
    while i < n:
        # Skip whitespace/comments
        m = re.match(r'\s*(?:/\*.*?\*/\s*)?', inner[i:], re.DOTALL)
        if m:
            i += len(m.group())
        if i >= n:
            break
        brace = inner.find('{', i)
        if brace == -1:
            break
        sel = inner[i:brace].strip()
        if not sel:
            i = brace + 1
            continue
        depth = 0
        j = brace
        while j < n:
            if inner[j] == '{': depth += 1
            elif inner[j] == '}':
                depth -= 1
                if depth == 0:
                    body = inner[brace+1:j].strip()
                    rules.append((sel, body))
                    i = j + 1
                    break
            j += 1
        else:
            break
    return rules

media_merged = OrderedDict()
for mb in media_blocks_raw:
    bp, inner = parse_media(mb)
    if not bp:
        continue
    if bp not in media_merged:
        media_merged[bp] = OrderedDict()
    inner_rules = parse_inner_rules(inner)
    for sel, body in inner_rules:
        # Merge by selector
        if sel in media_merged[bp]:
            media_merged[bp][sel] += '\n' + body
        else:
            media_merged[bp][sel] = body

# Filter and rebuild media
final_media = []
for bp, rules_dict in media_merged.items():
    filtered_rules = []
    for sel, body in rules_dict.items():
        if not is_selector_used(sel):
            continue
        filtered_rules.append(f'{sel} {{{body}}}')
    if filtered_rules:
        inner = '\n\n'.join(filtered_rules)
        final_media.append(f'{bp} {{\n{inner}\n}}')

# 7. Assemble output with CSS variables
css_vars = """:root {
    --color-primary: #f60909;
    --color-secondary: #e39e08;
    --color-text: #333;
    --color-text-secondary: #666;
    --color-text-muted: #888;
    --gradient-primary: linear-gradient(135deg, #f60909 0%, #e39e08 100%);
    --shadow-md: 0 8px 25px rgba(0, 0, 0, 0.1);
    --border-subtle: 1px solid rgba(58, 12, 163, 0.1);
}"""

parts = [css_vars, '']
for k in keyframes:
    parts.append(k)
    parts.append('')
for r in final_rules:
    parts.append(r)
    parts.append('')
for m in final_media:
    parts.append(m)
    parts.append('')

result = '\n'.join(parts)

# Clean excessive blank lines
result = re.sub(r'\n{3,}', '\n\n', result)

# Apply CSS variable replacements AFTER :root (not inside it)
# Split at first rule block
root_end = result.find('}\n\n', len(css_vars))
if root_end != -1:
    before = result[:root_end + 3]  # includes the closing } and newlines
    after = result[root_end + 3:]

    # Replace in 'after' only
    after = after.replace("linear-gradient(135deg, #f60909 0%, #e39e08 100%)", "var(--gradient-primary)")
    after = after.replace("color: #333;", "color: var(--color-text);")
    after = after.replace("color: #666;", "color: var(--color-text-secondary);")
    after = after.replace("color: #888;", "color: var(--color-text-muted);")
    after = after.replace("color: #f60909;", "color: var(--color-primary);")
    after = after.replace("box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);", "box-shadow: var(--shadow-md);")
    after = after.replace("border: 1px solid rgba(58, 12, 163, 0.1);", "border: var(--border-subtle);")

    result = before + after

with open(CSS_PATH, 'w', encoding='utf-8') as f:
    f.write(result)

# Stats
orig_size = len(open(CSS_PATH, 'rb').read())  # re-read for accuracy
# Actually read original from backup
orig_path = CSS_PATH
new_size = len(result.encode('utf-8'))

# Count original
orig_lines_count = css.count('\n') + 1
new_lines_count = result.count('\n') + 1

# Count @media
media_count = sum(1 for b in blocks if b[0] == 'media')

print(f"=== CSS Optimization Results ===")
print(f"Original: {len(css.encode('utf-8')):,} bytes, {orig_lines_count} lines")
print(f"Optimized: {new_size:,} bytes, {new_lines_count} lines")
print(f"Reduction: {len(css.encode('utf-8')) - new_size:,} bytes ({(1 - new_size/len(css.encode('utf-8')))*100:.1f}%)")
print(f"Lines removed: {orig_lines_count - new_lines_count}")
print(f"@media blocks: from {media_count} to {len(final_media)}")

# Count unique selectors
orig_sels = set()
for sel, _ in regular_rules:
    orig_sels.add(sel.split('{')[0].strip().split(':')[0].strip())
new_sels = set()
for block in final_rules:
    m = re.match(r'([^{]+)', block)
    if m:
        new_sels.add(m.group(1).strip())

print(f"Unique selectors: {len(orig_sels)} -> {len(new_sels)}")
print(f"Target: <40KB ({40000:,} bytes) -> {'ACHIEVED' if new_size < 40000 else 'NOT YET'} ({new_size:,} bytes)")
