#!/usr/bin/env python3
"""
HTML Structure Analysis - Investigate Page Breaks and Formatting Issues
Find the exact cause of the "Swedish officials" break
"""

import requests
from bs4 import BeautifulSoup
import html5lib
import re
from lxml import html, etree

def fetch_and_analyze_html_structure():
    """Fetch the Guardian page and analyze its HTML structure in detail"""
    
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print("🔍 FETCHING AND ANALYZING HTML STRUCTURE")
    print("=" * 60)
    
    response = requests.get(url, headers=headers)
    raw_html = response.text
    
    print(f"📄 Raw HTML size: {len(raw_html):,} characters")
    
    # Parse with different parsers to compare
    soup_html_parser = BeautifulSoup(raw_html, 'html.parser')
    soup_lxml = BeautifulSoup(raw_html, 'lxml')
    soup_html5lib = BeautifulSoup(raw_html, 'html5lib')
    
    print(f"\n🔍 SEARCHING FOR 'SWEDISH OFFICIALS' PHRASE:")
    
    # Find the exact HTML around "Swedish officials"
    search_text = "swedish officials"
    
    # Search in raw HTML
    raw_matches = []
    for match in re.finditer(search_text, raw_html, re.IGNORECASE):
        start = max(0, match.start() - 200)
        end = min(len(raw_html), match.end() + 200)
        context = raw_html[start:end]
        raw_matches.append((match.start(), context))
    
    print(f"Found {len(raw_matches)} matches in raw HTML:")
    for i, (pos, context) in enumerate(raw_matches):
        print(f"\nMATCH {i+1} at position {pos}:")
        print("-" * 40)
        # Show with special characters visible
        visible_context = repr(context)[1:-1]  # Remove outer quotes
        print(f"RAW HTML: {visible_context}")
        print("-" * 40)
    
    return soup_lxml, raw_html

def analyze_paragraph_structure(soup):
    """Analyze how paragraphs are structured in the Guardian article"""
    
    print(f"\n📋 ANALYZING PARAGRAPH STRUCTURE:")
    print("=" * 50)
    
    # Find all paragraphs with different selectors
    selectors_to_try = [
        ('Main content', 'div[data-gu-name="body"] p'),
        ('Article body', '.content__article-body p'),
        ('Generic article', 'article p'),
        ('All paragraphs', 'p')
    ]
    
    for name, selector in selectors_to_try:
        paragraphs = soup.select(selector)
        print(f"\n{name} ({selector}): {len(paragraphs)} paragraphs found")
        
        # Look for the problematic paragraph
        for i, p in enumerate(paragraphs[:10]):  # First 10 paragraphs
            text = p.get_text().strip()
            if "swedish officials" in text.lower():
                print(f"  📍 FOUND in paragraph {i+1}:")
                print(f"    Text: '{text[:100]}...'")
                print(f"    HTML: {str(p)[:200]}...")
                
                # Check for nested elements that might cause breaks
                nested_elements = p.find_all()
                if nested_elements:
                    print(f"    Nested elements: {[elem.name for elem in nested_elements]}")
                
                # Check parent structure
                parent = p.parent
                if parent:
                    print(f"    Parent: {parent.name} with class {parent.get('class', 'none')}")

def extract_clean_text_analysis(soup, raw_html):
    """Extract text and identify exactly where breaks are coming from"""
    
    print(f"\n🔧 TEXT EXTRACTION ANALYSIS:")
    print("=" * 50)
    
    # Method 1: BeautifulSoup get_text()
    paragraphs = soup.find_all('p')
    method1_paragraphs = []
    for p in paragraphs:
        text = p.get_text().strip()
        if text and len(text) > 20:
            method1_paragraphs.append(text)
    
    method1_text = '\n\n'.join(method1_paragraphs)
    
    # Method 2: BeautifulSoup get_text() with separator
    method2_text = soup.get_text(separator=' ', strip=True)
    
    # Method 3: Manual text extraction preserving structure
    content_div = soup.find('div', {'data-gu-name': 'body'})
    if content_div:
        method3_paragraphs = []
        for p in content_div.find_all('p'):
            text = p.get_text(separator=' ', strip=True)
            if text and len(text) > 20:
                method3_paragraphs.append(text)
        method3_text = ' '.join(method3_paragraphs)
    else:
        method3_text = "Content div not found"
    
    # Find "Swedish officials" in each method
    methods = [
        ("Method 1 (paragraph join)", method1_text),
        ("Method 2 (get_text)", method2_text),
        ("Method 3 (manual)", method3_text)
    ]
    
    for method_name, text in methods:
        print(f"\n{method_name}:")
        if "swedish officials" in text.lower():
            pos = text.lower().find("swedish officials")
            start = max(0, pos - 100)
            end = min(len(text), pos + 100)
            context = text[start:end]
            print(f"  FOUND: '...{context}...'")
            
            # Check for problematic characters around it
            char_analysis = repr(context)
            if '\\n' in char_analysis:
                print(f"  ⚠️  NEWLINES DETECTED: {char_analysis}")
            if '\\t' in char_analysis:
                print(f"  ⚠️  TABS DETECTED: {char_analysis}")
        else:
            print(f"  NOT FOUND")

def create_optimized_extraction():
    """Create the most optimized text extraction method"""
    
    print(f"\n🚀 CREATING OPTIMIZED EXTRACTION:")
    print("=" * 50)
    
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Find the main content area
    content_selectors = [
        'div[data-gu-name="body"]',
        '.content__article-body',
        'article'
    ]
    
    content_div = None
    for selector in content_selectors:
        content_div = soup.select_one(selector)
        if content_div:
            print(f"✅ Found content using: {selector}")
            break
    
    if not content_div:
        print("❌ No content div found, using body")
        content_div = soup.body
    
    # Extract paragraphs with aggressive cleaning
    clean_paragraphs = []
    
    for p in content_div.find_all('p'):
        # Get text and aggressively clean it
        text = p.get_text(separator=' ', strip=True)
        
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Skip short paragraphs (likely navigation/ads)
        if len(text) < 20:
            continue
            
        # Skip paragraphs with certain patterns (ads, navigation)
        if any(skip_word in text.lower() for skip_word in ['advertisement', 'subscribe', 'newsletter', 'follow us']):
            continue
            
        clean_paragraphs.append(text)
    
    # Join with single spaces (no paragraph breaks)
    optimized_text = ' '.join(clean_paragraphs)
    
    # Final cleanup
    optimized_text = re.sub(r'\s+', ' ', optimized_text).strip()
    
    print(f"📊 Optimized text length: {len(optimized_text)} characters")
    
    # Check the Swedish officials area
    if "swedish officials" in optimized_text.lower():
        pos = optimized_text.lower().find("swedish officials")
        start = max(0, pos - 50)
        end = min(len(optimized_text), pos + 100)
        context = optimized_text[start:end]
        print(f"✅ Swedish officials context: '...{context}...'")
    
    return optimized_text

def main():
    # Analyze HTML structure
    soup, raw_html = fetch_and_analyze_html_structure()
    
    # Analyze paragraph structure
    analyze_paragraph_structure(soup)
    
    # Compare text extraction methods
    extract_clean_text_analysis(soup, raw_html)
    
    # Create optimized version
    optimized_text = create_optimized_extraction()
    
    # Save analysis results
    with open('html_analysis_results.txt', 'w') as f:
        f.write("HTML ANALYSIS RESULTS\n")
        f.write("=" * 30 + "\n\n")
        f.write("OPTIMIZED TEXT:\n")
        f.write(optimized_text + "\n")
    
    print(f"\n✅ Analysis complete! Check html_analysis_results.txt")
    print(f"🎯 Next: Use optimized text extraction to create better audio")

if __name__ == "__main__":
    main()
