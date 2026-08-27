"""Fix blog files: add missing </footer> before CTA section."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

blog_files = list(ROOT.glob("blog-*.html"))
fixed = 0

for f in blog_files:
    content = f.read_text(encoding="utf-8")
    original = content
    
    # Pattern: </div>\n\n<!-- ===== CTA ===== -->\n<section
    # We need </footer> before <!-- ===== CTA ===== -->
    # But only if there's a <footer> tag earlier and no </footer> before CTA
    
    if '<footer class="footer">' in content and '<!-- ===== CTA ===== -->' in content:
        # Check if </footer> is missing before CTA
        cta_pos = content.find('<!-- ===== CTA ===== -->')
        footer_open_pos = content.rfind('<footer class="footer">', 0, cta_pos)
        
        if footer_open_pos > 0:
            # Find the </div> that closes the container before CTA
            # Look for the pattern: </div>\n\n<!-- ===== CTA ===== -->
            pattern = r'(</div>)\s*\n\s*(<!-- ===== CTA ===== -->)'
            if re.search(pattern, content):
                # Check if there's a </footer> between footer open and CTA
                between = content[footer_open_pos:cta_pos]
                if '</footer>' not in between:
                    # Add </footer> before CTA
                    content = re.sub(
                        pattern,
                        r'\1\n</footer>\n\n\2',
                        content
                    )
    
    if content != original:
        f.write_text(content, encoding="utf-8")
        fixed += 1
        print(f"FIXED: {f.name}")

print(f"\nTotal fixed: {fixed}")
