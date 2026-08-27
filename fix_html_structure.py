"""Fix structural HTML issues in blog files and geo pages."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def fix_blog_files():
    """Fix stray </footer> and mismatched tags in blog files."""
    blog_files = list(ROOT.glob("blog-*.html"))
    fixed = 0
    for f in blog_files:
        content = f.read_text(encoding="utf-8")
        original = content
        
        # Pattern: </section>\n\n</footer>\n → </section>\n
        # (stray </footer> after CTA section)
        content = re.sub(r'</section>\s*\n\s*</footer>\s*\n', '</section>\n', content)
        
        # Pattern: </div>\n</footer>\n\n</footer> → </div>\n</footer>
        # (double </footer>)
        content = re.sub(r'</footer>\s*\n\s*</footer>', '</footer>', content)
        
        # Pattern: </div>\n    </div>\n</footer> where </footer> should be </section>
        # (CTA section closed with </footer> instead of </section>)
        content = re.sub(
            r'(<div class="cta-buttons">.*?</div>\s*</div>\s*</div>)\s*</footer>',
            r'\1</section>',
            content,
            flags=re.DOTALL
        )
        
        if content != original:
            f.write_text(content, encoding="utf-8")
            fixed += 1
            print(f"FIXED: {f.name}")
    
    return fixed

def fix_portfolio_filter():
    """Fix data-type → data-category mismatch in portfolio.html."""
    f = ROOT / "portfolio.html"
    if not f.exists():
        print("portfolio.html not found")
        return 0
    
    content = f.read_text(encoding="utf-8")
    original = content
    
    # Replace data-type with data-category on portfolio cards
    content = content.replace('data-type="', 'data-category="')
    
    if content != original:
        f.write_text(content, encoding="utf-8")
        print("FIXED: portfolio.html (data-type -> data-category)")
        return 1
    return 0

def fix_duplicate_nav_mobile():
    """Remove duplicate nav-mobile in portfolio.html."""
    f = ROOT / "portfolio.html"
    if not f.exists():
        return 0
    
    content = f.read_text(encoding="utf-8")
    original = content
    
    # Find and remove the second nav-mobile div
    # Pattern: two consecutive <div class="nav-mobile"> blocks
    pattern = r'(<div class="nav-mobile">.*?</div>)\s*(<div class="nav-mobile">)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        # Keep only the first one, remove the second
        content = re.sub(pattern, r'\1', content, flags=re.DOTALL)
    
    if content != original:
        f.write_text(content, encoding="utf-8")
        print("FIXED: portfolio.html (duplicate nav-mobile)")
        return 1
    return 0

if __name__ == "__main__":
    blog_fixed = fix_blog_files()
    portfolio_filter = fix_portfolio_filter()
    nav_mobile = fix_duplicate_nav_mobile()
    
    total = blog_fixed + portfolio_filter + nav_mobile
    print(f"\nTotal fixes: {total}")
    print(f"Blog files fixed: {blog_fixed}")
    print(f"Portfolio filter fixed: {portfolio_filter}")
    print(f"Duplicate nav-mobile fixed: {nav_mobile}")
