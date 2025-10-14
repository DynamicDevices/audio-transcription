#!/usr/bin/env python3
"""
Deep Line Ending Analysis - Check for ANY line ending artifacts
"""

import requests
from bs4 import BeautifulSoup
import re

def deep_line_ending_analysis():
    """Exhaustive check for line ending issues"""
    
    print("🔍 DEEP LINE ENDING ANALYSIS")
    print("=" * 40)
    
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Get first paragraph
    content_div = soup.select_one('div[data-gu-name="body"]')
    first_p = content_div.find('p')
    
    print("1. RAW HTML ANALYSIS:")
    html_str = str(first_p)
    print(f"Raw HTML: {repr(html_str[:200])}...")
    
    # Check for line endings in HTML
    line_endings_in_html = []
    for i, char in enumerate(html_str):
        if ord(char) in [10, 13, 9]:  # \n, \r, \t
            line_endings_in_html.append((i, char, ord(char)))
    
    print(f"Line endings in HTML: {len(line_endings_in_html)}")
    for pos, char, code in line_endings_in_html[:10]:  # Show first 10
        print(f"  Position {pos}: {repr(char)} (ASCII {code})")
    
    print(f"\n2. DIFFERENT EXTRACTION METHODS:")
    
    # Method 1: Default get_text()
    text1 = first_p.get_text()
    print(f"Method 1 (default get_text): {repr(text1[:100])}...")
    
    # Method 2: get_text with space separator
    text2 = first_p.get_text(separator=' ')
    print(f"Method 2 (space separator): {repr(text2[:100])}...")
    
    # Method 3: get_text with empty separator
    text3 = first_p.get_text(separator='')
    print(f"Method 3 (no separator): {repr(text3[:100])}...")
    
    # Method 4: Manual string extraction
    text4 = ""
    for element in first_p.descendants:
        if element.string:
            text4 += element.string
    print(f"Method 4 (manual): {repr(text4[:100])}...")
    
    # Method 5: Strip each element
    text5 = ""
    for element in first_p.descendants:
        if element.string:
            text5 += element.string.strip() + " "
    text5 = text5.strip()
    print(f"Method 5 (strip each): {repr(text5[:100])}...")
    
    print(f"\n3. LINE ENDING DETECTION IN EACH METHOD:")
    
    methods = [
        ("Method 1", text1),
        ("Method 2", text2),
        ("Method 3", text3),
        ("Method 4", text4),
        ("Method 5", text5)
    ]
    
    for method_name, text in methods:
        line_endings = []
        for i, char in enumerate(text):
            if ord(char) in [10, 13, 9, 160]:  # \n, \r, \t, non-breaking space
                line_endings.append((i, char, ord(char)))
        
        print(f"{method_name}: {len(line_endings)} line endings")
        for pos, char, code in line_endings[:5]:  # Show first 5
            print(f"  Position {pos}: {repr(char)} (ASCII {code})")
    
    print(f"\n4. FOCUS ON 'SUBJECTED TO' AREA:")
    
    # Find "subjected to" in each method and check surrounding characters
    for method_name, text in methods:
        pos = text.lower().find("subjected to")
        if pos != -1:
            # Check 10 characters before and after
            start = max(0, pos - 10)
            end = min(len(text), pos + len("subjected to") + 10)
            
            print(f"\n{method_name} - 'subjected to' context:")
            for i in range(start, end):
                char = text[i]
                ascii_val = ord(char)
                is_problem = ascii_val in [9, 10, 13, 160]
                marker = " ⚠️" if is_problem else ""
                
                print(f"  {i:3}: '{char}' (ASCII {ascii_val:3}){marker}")

def create_ultra_clean_extraction():
    """Create the cleanest possible extraction"""
    
    print(f"\n5. ULTRA-CLEAN EXTRACTION:")
    
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    content_div = soup.select_one('div[data-gu-name="body"]')
    first_p = content_div.find('p')
    
    # Ultra-clean extraction
    clean_text = ""
    for element in first_p.descendants:
        if element.string and element.string.strip():
            # Clean each string fragment
            fragment = element.string.strip()
            
            # Remove ALL possible line ending characters
            fragment = re.sub(r'[\r\n\f\v\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029\u00A0\u1680\u2000-\u200B\u202F\u205F\u3000\uFEFF]+', ' ', fragment)
            
            # Replace tabs with spaces
            fragment = re.sub(r'\t+', ' ', fragment)
            
            # Normalize all whitespace
            fragment = re.sub(r'\s+', ' ', fragment)
            
            if fragment:
                clean_text += fragment + " "
    
    # Final cleanup
    clean_text = clean_text.strip()
    clean_text = re.sub(r'\s+', ' ', clean_text)
    
    print(f"Ultra-clean text: {repr(clean_text)}")
    
    # Check for ANY problematic characters
    problems = []
    for i, char in enumerate(clean_text):
        ascii_val = ord(char)
        if ascii_val < 32 or ascii_val == 127 or ascii_val > 126:
            if ascii_val != 32:  # Allow regular spaces
                problems.append((i, char, ascii_val))
    
    print(f"Problematic characters: {len(problems)}")
    for pos, char, code in problems:
        print(f"  Position {pos}: {repr(char)} (ASCII {code})")
    
    return clean_text

def main():
    # Deep analysis
    deep_line_ending_analysis()
    
    # Create ultra-clean version
    ultra_clean = create_ultra_clean_extraction()
    
    # Save for testing
    with open('ultra_clean_first_paragraph.txt', 'w', encoding='utf-8') as f:
        f.write("ULTRA-CLEAN FIRST PARAGRAPH\n")
        f.write("=" * 30 + "\n\n")
        f.write("TEXT:\n")
        f.write(ultra_clean)
        f.write("\n\nREPR:\n")
        f.write(repr(ultra_clean))
    
    print(f"\n✅ DEEP ANALYSIS COMPLETE!")
    print(f"📄 Saved ultra-clean version: ultra_clean_first_paragraph.txt")
    print(f"🎯 This should reveal any hidden line ending artifacts")

if __name__ == "__main__":
    main()
