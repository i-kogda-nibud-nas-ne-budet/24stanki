"""Debug: check how parse_inner_rules works on the original CSS."""
import re

CSS_PATH = r'D:\PROJECTS\24stanki\styles.css'
with open(CSS_PATH, 'r', encoding='utf-8') as f:
    css = f.read()

# Find first @media block
media_match = re.search(r'@media\s*\([^)]+\)\s*\{', css)
if media_match:
    start = media_match.start()
    # Find matching brace
    brace_start = css.index('{', start)
    depth = 0
    j = brace_start
    while j < len(css):
        if css[j] == '{': depth += 1
        elif css[j] == '}':
            depth -= 1
            if depth == 0:
                break
        j += 1
    
    media_block = css[start:j+1]
    print(f"First @media block length: {len(media_block)}")
    print(f"First 500 chars:")
    print(media_block[:500])
    print("\n---\n")
    
    # Extract inner (between outermost { })
    inner = media_block[brace_start+1:j]
    print(f"Inner length: {len(inner)}")
    print(f"First 500 chars of inner:")
    print(inner[:500])
    
    # Parse inner rules manually
    i = 0
    rules_found = []
    while i < len(inner):
        # skip whitespace
        while i < len(inner) and inner[i] in ' \t\n\r':
            i += 1
        if i >= len(inner):
            break
        
        # Find next {
        brace = inner.find('{', i)
        if brace == -1:
            break
        sel = inner[i:brace].strip()
        
        # Find matching }
        depth = 0
        j2 = brace
        while j2 < len(inner):
            if inner[j2] == '{': depth += 1
            elif inner[j2] == '}':
                depth -= 1
                if depth == 0:
                    body = inner[brace+1:j2].strip()
                    rules_found.append((sel, body[:80]))
                    i = j2 + 1
                    break
            j2 += 1
        else:
            break
    
    print(f"\nRules found in first @media: {len(rules_found)}")
    for sel, body in rules_found[:10]:
        print(f"  '{sel}' -> {body}...")
