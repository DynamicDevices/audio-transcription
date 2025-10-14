#!/usr/bin/env python3
"""
Exact Text Analysis - Find the specific cause of "subjected to" pause
"""

import requests
from bs4 import BeautifulSoup
import re

def extract_exact_text_around_phrase():
    """Extract the exact text around 'subjected to' with all formatting visible"""
    
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    print("🔍 FINDING EXACT TEXT AROUND 'SUBJECTED TO'")
    print("=" * 60)
    
    # Find content div
    content_div = soup.select_one('div[data-gu-name="body"]')
    
    if not content_div:
        print("❌ Content div not found")
        return
    
    # Find all paragraphs containing "subjected to"
    target_paragraphs = []
    
    for i, p in enumerate(content_div.find_all('p')):
        text = p.get_text()
        if "subjected to" in text.lower():
            target_paragraphs.append((i, p, text))
    
    print(f"Found {len(target_paragraphs)} paragraphs containing 'subjected to':")
    
    for i, (para_num, p_element, full_text) in enumerate(target_paragraphs):
        print(f"\n📍 PARAGRAPH {i+1} (HTML paragraph #{para_num}):")
        
        # Show the raw HTML
        print("Raw HTML:")
        print(repr(str(p_element)[:500]))
        
        # Show the extracted text
        print("\nExtracted text:")
        print(repr(full_text[:300]))
        
        # Find the exact position of "subjected to"
        pos = full_text.lower().find("subjected to")
        if pos != -1:
            # Show context around it
            start = max(0, pos - 50)
            end = min(len(full_text), pos + 80)
            context = full_text[start:end]
            
            print(f"\nContext around 'subjected to':")
            print(f"Position {pos} in paragraph:")
            print(f"Text: '{context}'")
            print(f"Repr: {repr(context)}")
            
            # Check for specific problematic patterns
            issues = []
            
            # Check what comes right before "subjected to"
            before_pos = max(0, pos - 20)
            before_text = full_text[before_pos:pos]
            print(f"\n20 chars before: '{before_text}'")
            print(f"Repr: {repr(before_text)}")
            
            # Check what comes right after "subjected to"
            after_start = pos + len("subjected to")
            after_text = full_text[after_start:after_start + 20]
            print(f"\n20 chars after: '{after_text}'")
            print(f"Repr: {repr(after_text)}")
            
            # Look for specific pause-causing patterns
            if ", including" in context:
                issues.append("❌ Contains ', including' construction")
            if "harsh treatment" in context:
                issues.append("✅ Contains 'harsh treatment'")
            if re.search(r'["""]', context):
                issues.append("❌ Contains smart quotes")
            if re.search(r'[–—]', context):
                issues.append("❌ Contains em/en dashes")
            if "\n" in context:
                issues.append("❌ Contains newlines")
            if "  " in context:
                issues.append("❌ Contains multiple spaces")
                
            print(f"\n🔍 Issues found:")
            for issue in issues:
                print(f"   {issue}")
    
    return target_paragraphs

def show_different_extraction_methods():
    """Show how different extraction methods handle the problematic text"""
    
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    print(f"\n🔬 COMPARING EXTRACTION METHODS")
    print("=" * 50)
    
    content_div = soup.select_one('div[data-gu-name="body"]')
    
    # Find the paragraph with "subjected to"
    target_p = None
    for p in content_div.find_all('p'):
        if "subjected to" in p.get_text().lower():
            target_p = p
            break
    
    if not target_p:
        print("❌ Target paragraph not found")
        return
    
    print("Target paragraph found. Testing different extraction methods:\n")
    
    # Method 1: get_text() default
    method1 = target_p.get_text()
    print("METHOD 1 - get_text() default:")
    print(f"Result: {repr(method1)}")
    
    # Method 2: get_text(separator=' ')
    method2 = target_p.get_text(separator=' ')
    print(f"\nMETHOD 2 - get_text(separator=' '):")
    print(f"Result: {repr(method2)}")
    
    # Method 3: get_text(separator=' ', strip=True)
    method3 = target_p.get_text(separator=' ', strip=True)
    print(f"\nMETHOD 3 - get_text(separator=' ', strip=True):")
    print(f"Result: {repr(method3)}")
    
    # Method 4: Manual text extraction
    method4 = ""
    for element in target_p.descendants:
        if element.string:
            method4 += element.string
    print(f"\nMETHOD 4 - Manual string extraction:")
    print(f"Result: {repr(method4)}")
    
    # Method 5: Our current zero-artifacts method
    method5 = target_p.get_text(separator=' ', strip=True)
    method5 = re.sub(r'\s+', ' ', method5)
    print(f"\nMETHOD 5 - Zero artifacts (current):")
    print(f"Result: {repr(method5)}")
    
    # Find "subjected to" in each and show exact context
    print(f"\n🎯 'SUBJECTED TO' CONTEXT IN EACH METHOD:")
    
    for i, (name, text) in enumerate([
        ("Method 1", method1),
        ("Method 2", method2), 
        ("Method 3", method3),
        ("Method 4", method4),
        ("Method 5", method5)
    ], 1):
        pos = text.lower().find("subjected to")
        if pos != -1:
            start = max(0, pos - 30)
            end = min(len(text), pos + 50)
            context = text[start:end]
            print(f"\n{name}: '{context}'")
            print(f"Repr: {repr(context)}")
        else:
            print(f"\n{name}: 'subjected to' not found")

def create_ultra_clean_test():
    """Create the cleanest possible version of just the problematic sentence"""
    
    print(f"\n🚀 CREATING ULTRA-CLEAN TEST")
    print("=" * 40)
    
    # Extract the exact problematic sentence
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    content_div = soup.select_one('div[data-gu-name="body"]')
    
    # Find the sentence with "subjected to"
    target_sentence = None
    for p in content_div.find_all('p'):
        text = p.get_text(separator=' ', strip=True)
        if "subjected to" in text.lower():
            # Split into sentences and find the right one
            sentences = text.split('. ')
            for sentence in sentences:
                if "subjected to" in sentence.lower():
                    target_sentence = sentence
                    break
            break
    
    if target_sentence:
        print(f"Original sentence:")
        print(f"'{target_sentence}'")
        print(f"Repr: {repr(target_sentence)}")
        
        # Apply ultra-cleaning
        clean_sentence = target_sentence
        
        # Remove all problematic patterns
        clean_sentence = re.sub(r'[""]', '', clean_sentence)  # Remove smart quotes
        clean_sentence = re.sub(r"['']", '', clean_sentence)  # Remove smart apostrophes
        clean_sentence = re.sub(r'[–—]', ' ', clean_sentence)  # Remove dashes
        clean_sentence = re.sub(r', including ([^,]+)', r' with \1', clean_sentence)  # Fix "including"
        clean_sentence = re.sub(r'\s+', ' ', clean_sentence)  # Normalize spaces
        clean_sentence = clean_sentence.strip()
        
        print(f"\nUltra-cleaned sentence:")
        print(f"'{clean_sentence}'")
        print(f"Repr: {repr(clean_sentence)}")
        
        # Show the specific "subjected to" area
        pos = clean_sentence.lower().find("subjected to")
        if pos != -1:
            start = max(0, pos - 20)
            end = min(len(clean_sentence), pos + 30)
            context = clean_sentence[start:end]
            print(f"\nCleaned 'subjected to' context:")
            print(f"'{context}'")
            print(f"Repr: {repr(context)}")
        
        return clean_sentence
    
    return None

def main():
    # Extract exact text around the phrase
    paragraphs = extract_exact_text_around_phrase()
    
    # Show different extraction methods
    show_different_extraction_methods()
    
    # Create ultra-clean test
    clean_sentence = create_ultra_clean_test()
    
    print(f"\n✅ ANALYSIS COMPLETE!")
    print(f"🎯 Check the output above to see exactly what's causing the pause")

if __name__ == "__main__":
    main()
