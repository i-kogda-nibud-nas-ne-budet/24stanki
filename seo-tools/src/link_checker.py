#!/usr/bin/env python3
"""
Link checker for the 24stanki.ru website.
Checks for broken internal and external links, anchors, and resources.
"""

import os
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class LinkChecker:
    def __init__(self, base_dir, base_url="https://24stanki.ru"):
        self.base_dir = Path(base_dir)
        self.base_url = base_url
        self.checked_urls = {}
        self.broken_links = []
        self.visited_pages = set()
        
    def extract_links_from_html(self, html_content):
        """Extract all links from HTML."""
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []
        
        for tag in soup.find_all(['a', 'link', 'script', 'img', 'source']):
            if tag.name == 'a' and tag.get('href'):
                links.append(('a', tag.get('href')))
            elif tag.name == 'link' and tag.get('href'):
                links.append(('link', tag.get('href')))
            elif tag.name == 'script' and tag.get('src'):
                links.append(('script', tag.get('src')))
            elif tag.name == 'img' and tag.get('src'):
                links.append(('img', tag.get('src')))
            elif tag.name == 'source' and tag.get('src'):
                links.append(('source', tag.get('src')))
        
        return links
    
    def normalize_url(self, url, current_page):
        """Normalize URL to absolute path."""
        if url.startswith('http'):
            return url
        elif url.startswith('//'):
            return 'https:' + url
        elif url.startswith('/'):
            return self.base_url + url
        elif url.startswith('mailto:') or url.startswith('tel:'):
            return None  # Skip mailto and tel links
        elif url.startswith('#'):
            # Anchor link - check if it exists in current page
            return None  # We'll handle anchors separately
        else:
            # Relative URL
            if current_page:
                base_path = self.base_dir / current_page
                resolved = (base_path.parent / url).resolve()
                return str(resolved.relative_to(self.base_dir))
            return url
    
    def check_url_exists(self, url, is_local=False):
        """Check if URL exists (HTTP HEAD request)."""
        if url in self.checked_urls:
            return self.checked_urls[url]
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; 24stanki-link-checker/1.0)'
            }
            
            if is_local:
                # Check local file
                filepath = self.base_dir / url
                if filepath.exists():
                    self.checked_urls[url] = (True, "File exists")
                    return True, "File exists"
                else:
                    self.checked_urls[url] = (False, f"File not found: {filepath}")
                    return False, f"File not found: {filepath}"
            else:
                # Check external URL
                response = requests.head(
                    url, 
                    timeout=10,
                    headers=headers,
                    allow_redirects=True
                )
                
                if response.status_code < 400:
                    self.checked_urls[url] = (True, f"HTTP {response.status_code}")
                    return True, f"HTTP {response.status_code}"
                else:
                    self.checked_urls[url] = (False, f"HTTP {response.status_code}")
                    return False, f"HTTP {response.status_code}"
                    
        except requests.RequestException as e:
            self.checked_urls[url] = (False, str(e))
            return False, str(e)
    
    def check_anchors(self, html_content, page_url):
        """Check if anchor links exist in the page."""
        soup = BeautifulSoup(html_content, 'html.parser')
        anchors = []
        
        for tag in soup.find_all(['a', 'span', 'div', 'section'], id=True):
            anchors.append('#' + tag.get('id'))
        
        return anchors
    
    def check_page(self, html_file):
        """Check all links in a single HTML page."""
        html_path = self.base_dir / html_file
        
        if not html_path.exists():
            print(f"  ⚠ File not found: {html_file}")
            return
        
        print(f"Checking: {html_file}")
        
        try:
            content = html_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"  ✗ Error reading file: {e}")
            return
        
        links = self.extract_links_from_html(content)
        
        # Check anchors in this page
        local_anchors = self.check_anchors(content, html_file)
        
        for link_type, url in links:
            # Normalize URL
            normalized = self.normalize_url(url, html_file)
            
            if normalized is None:
                # Skip mailto, tel, or handle anchors differently
                if url.startswith('#'):
                    anchor = url
                    if anchor not in local_anchors:
                        self.broken_links.append({
                            'page': html_file,
                            'type': link_type,
                            'url': url,
                            'reason': f"Anchor {anchor} not found in page"
                        })
                continue
            
            # Determine if local or external
            is_local = not normalized.startswith(('http://', 'https://', '//'))
            
            # Check
            exists, reason = self.check_url_exists(normalized, is_local)
            
            if not exists:
                self.broken_links.append({
                    'page': html_file,
                    'type': link_type,
                    'url': url,
                    'normalized': normalized,
                    'reason': reason
                })
        
        self.visited_pages.add(html_file)
    
    def run(self, max_workers=5):
        """Run link checker on all HTML files."""
        print(f"Starting link check for {self.base_dir}")
        
        # Get all HTML files
        html_files = list(self.base_dir.glob('*.html'))
        print(f"Found {len(html_files)} HTML files to check")
        
        # Check each page
        for html_file in html_files:
            self.check_page(html_file.name)
            time.sleep(0.1)  # Be polite
        
        # Print summary
        print(f"\n{'='*60}")
        print(f"Link Check Summary")
        print(f"{'='*60}")
        print(f"Pages checked: {len(self.visited_pages)}")
        print(f"Broken links found: {len(self.broken_links)}")
        
        if self.broken_links:
            print(f"\nBroken links:")
            for broken in self.broken_links:
                print(f"  ✗ {broken['page']} -> {broken['url']}")
                print(f"    Reason: {broken['reason']}")
        else:
            print("\n✓ No broken links found!")
        
        return self.broken_links

def main():
    base_dir = Path(__file__).parent.parent.parent
    
    checker = LinkChecker(base_dir)
    broken_links = checker.run()
    
    # Save report
    report_path = base_dir / 'seo-tools' / 'output' / 'reports' / 'broken_links.csv'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    import csv
    with open(report_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['page', 'type', 'url', 'normalized', 'reason'])
        writer.writeheader()
        writer.writerows(broken_links)
    
    print(f"\nReport saved to: {report_path}")

if __name__ == '__main__':
    main()