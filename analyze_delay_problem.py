#!/usr/bin/env python3
"""
Analyze the exact "subjected to" -> "harsh" delay problem
"""

import requests
from bs4 import BeautifulSoup
import re

def analyze_subjected_to_harsh_delay():
    """Analyze what's causing the delay between 'subjected to' and 'harsh'"""
    
    print("🔍 ANALYZING 'SUBJECTED TO' -> 'HARSH' DELAY")
    print("=" * 50)
    
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Get the first paragraph HTML
    content_div = soup.select_one('div[data-gu-name="body"]')
    first_p = content_div.find('p')
    
    print("📝 RAW HTML OF FIRST PARAGRAPH:")
    print(first_p.prettify())
    
    print("\n🔍 SEARCHING FOR 'SUBJECTED TO' IN RAW HTML:")
    html_str = str(first_p)
    
    # Find the position of "subjected to" in the HTML
    pos = html_str.lower().find("subjected to")
    if pos != -1:
        # Show 100 characters around it
        start = max(0, pos - 50)
        end = min(len(html_str), pos + 100)
        context = html_str[start:end]
        
        print(f"HTML Context around 'subjected to':")
        print(f"'{context}'")
        print(f"\nWith hidden characters:")
        print(repr(context))
    
    # Test different text extraction methods
    print(f"\n🧪 DIFFERENT EXTRACTION METHODS:")
    
    # Method 1: Default get_text()
    text1 = first_p.get_text()
    print(f"Method 1 (default): {repr(text1)}")
    
    # Method 2: get_text(separator=' ')
    text2 = first_p.get_text(separator=' ')
    print(f"Method 2 (space sep): {repr(text2)}")
    
    # Method 3: get_text(separator='')
    text3 = first_p.get_text(separator='')
    print(f"Method 3 (no sep): {repr(text3)}")
    
    # Method 4: Manual extraction
    text4 = ""
    for element in first_p.descendants:
        if element.string:
            text4 += element.string.strip() + " "
    text4 = text4.strip()
    print(f"Method 4 (manual): {repr(text4)}")
    
    # Find "subjected to" in each method and show what comes after
    methods = [
        ("Method 1", text1),
        ("Method 2", text2), 
        ("Method 3", text3),
        ("Method 4", text4)
    ]
    
    print(f"\n🎯 'SUBJECTED TO' ANALYSIS IN EACH METHOD:")
    
    for method_name, text in methods:
        pos = text.lower().find("subjected to")
        if pos != -1:
            # Show 20 chars before and after
            start = max(0, pos - 20)
            end = min(len(text), pos + len("subjected to") + 20)
            context = text[start:end]
            
            print(f"\n{method_name}:")
            print(f"  Context: '{context}'")
            print(f"  Repr: {repr(context)}")
            
            # Check what's immediately after "subjected to"
            after_pos = pos + len("subjected to")
            next_10_chars = text[after_pos:after_pos + 10]
            print(f"  Next 10 chars: {repr(next_10_chars)}")

def create_fix_options():
    """Create different fix options for the delay"""
    
    print(f"\n🔧 FIX OPTIONS:")
    
    # Get the problematic text
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    content_div = soup.select_one('div[data-gu-name="body"]')
    first_p = content_div.find('p')
    
    original_text = first_p.get_text(separator=' ', strip=True)
    original_text = re.sub(r'\s+', ' ', original_text)
    
    print(f"Original: '{original_text}'")
    
    # Option 1: Replace "being subjected to harsh treatment"
    option1 = original_text.replace("being subjected to harsh treatment", "facing harsh treatment")
    print(f"\nOption 1 - Replace entire phrase:")
    print(f"  '{option1}'")
    
    # Option 2: Replace just "subjected to"
    option2 = original_text.replace("subjected to", "facing")
    print(f"\nOption 2 - Replace 'subjected to':")
    print(f"  '{option2}'")
    
    # Option 3: Replace "being subjected to"
    option3 = original_text.replace("being subjected to", "experiencing")
    print(f"\nOption 3 - Replace 'being subjected to':")
    print(f"  '{option3}'")
    
    # Option 4: Completely rephrase
    option4 = original_text.replace("she is being subjected to harsh treatment", "she faces harsh treatment")
    print(f"\nOption 4 - Complete rephrase:")
    print(f"  '{option4}'")
    
    # Option 5: Active voice
    option5 = original_text.replace("she is being subjected to harsh treatment in Israeli custody", "Israeli forces are treating her harshly in custody")
    print(f"\nOption 5 - Active voice:")
    print(f"  '{option5}'")
    
    return [
        ("Option 1", option1),
        ("Option 2", option2),
        ("Option 3", option3),
        ("Option 4", option4),
        ("Option 5", option5)
    ]

def main():
    # Analyze the problem
    analyze_subjected_to_harsh_delay()
    
    # Show fix options
    fix_options = create_fix_options()
    
    print(f"\n✅ ANALYSIS COMPLETE!")
    print(f"🎯 The delay is likely caused by HTML formatting around 'subjected to'")
    print(f"💡 Choose which fix option sounds most natural for your father")

if __name__ == "__main__":
    main()
