#!/usr/bin/env python3
"""
Debug TTS Input - Show EXACTLY what text is being sent to TTS
"""

import requests
from bs4 import BeautifulSoup
import re

def debug_tts_input_step_by_step():
    """Debug every step of text processing to see where the problem occurs"""
    
    print("🔍 DEBUGGING TTS INPUT STEP BY STEP")
    print("=" * 50)
    
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    
    # Step 1: Get raw HTML
    print("STEP 1: Raw HTML fetch")
    response = requests.get(url, headers=headers)
    
    # Step 2: Parse with BeautifulSoup
    print("STEP 2: BeautifulSoup parsing")
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Step 3: Find the paragraph
    print("STEP 3: Find first paragraph")
    content_div = soup.select_one('div[data-gu-name="body"]')
    first_p = content_div.find('p')
    
    print(f"Raw paragraph HTML:")
    print(repr(str(first_p)[:200]))
    print(f"Full HTML: {str(first_p)}")
    
    # Step 4: Different text extraction methods
    print(f"\nSTEP 4: Text extraction methods")
    
    methods = {
        "get_text()": first_p.get_text(),
        "get_text(' ')": first_p.get_text(' '),
        "get_text(separator=' ', strip=True)": first_p.get_text(separator=' ', strip=True)
    }
    
    for method_name, extracted_text in methods.items():
        print(f"\n{method_name}:")
        print(f"  Length: {len(extracted_text)}")
        print(f"  Text: '{extracted_text}'")
        print(f"  Repr: {repr(extracted_text)}")
        
        # Check around "subjected to"
        pos = extracted_text.lower().find("subjected to")
        if pos != -1:
            context_start = max(0, pos - 30)
            context_end = min(len(extracted_text), pos + 50)
            context = extracted_text[context_start:context_end]
            print(f"  'subjected to' context: '{context}'")
            print(f"  Context repr: {repr(context)}")
    
    # Step 5: Apply our cleaning
    print(f"\nSTEP 5: Our text cleaning process")
    
    # This is exactly what we do in our scripts
    text = first_p.get_text(separator=' ', strip=True)
    print(f"After get_text: {repr(text)}")
    
    text = re.sub(r'\s+', ' ', text.strip())
    print(f"After regex cleanup: {repr(text)}")
    
    # Step 6: Check for invisible characters
    print(f"\nSTEP 6: Character-by-character analysis around 'subjected to'")
    
    pos = text.lower().find("subjected to")
    if pos != -1:
        # Show 20 characters before and after
        start = max(0, pos - 20)
        end = min(len(text), pos + len("subjected to") + 20)
        
        print(f"Characters around 'subjected to':")
        for i in range(start, end):
            char = text[i]
            ascii_code = ord(char)
            
            # Highlight the "subjected to" part
            if pos <= i < pos + len("subjected to"):
                marker = " <<<< TARGET"
            else:
                marker = ""
            
            print(f"  Position {i}: '{char}' (ASCII {ascii_code}){marker}")
    
    # Step 7: Test if the problem is in the link
    print(f"\nSTEP 7: Check if Greta Thunberg link causes issues")
    
    # Find the link in HTML
    link = first_p.find('a')
    if link:
        print(f"Found link: {link}")
        print(f"Link text: '{link.get_text()}'")
        print(f"Link repr: {repr(link.get_text())}")
        
        # Check if there are spaces around the link
        link_parent = str(first_p)
        link_pos = link_parent.find(str(link))
        if link_pos != -1:
            before_link = link_parent[max(0, link_pos-20):link_pos]
            after_link = link_parent[link_pos + len(str(link)):link_pos + len(str(link)) + 20]
            
            print(f"Before link: {repr(before_link)}")
            print(f"After link: {repr(after_link)}")
    
    # Step 8: Manual clean extraction
    print(f"\nSTEP 8: Manual clean extraction (no BeautifulSoup)")
    
    # Try to extract without BeautifulSoup processing
    manual_text = "The environmental campaigner Greta Thunberg has told Swedish officials she is being subjected to harsh treatment in Israeli custody after her detention and removal from a flotilla carrying aid to Gaza, according to correspondence seen by the Guardian."
    
    print(f"Manual text: '{manual_text}'")
    print(f"Manual repr: {repr(manual_text)}")
    
    # Compare with BeautifulSoup extraction
    if text == manual_text:
        print("✅ BeautifulSoup extraction matches manual text")
    else:
        print("❌ BeautifulSoup extraction differs from manual text")
        print(f"Difference at position: {next((i for i in range(min(len(text), len(manual_text))) if text[i] != manual_text[i]), 'No difference found')}")
    
    return text, manual_text

def test_tts_with_different_inputs():
    """Test TTS with different text inputs to isolate the problem"""
    
    print(f"\n🎵 TESTING TTS WITH DIFFERENT INPUTS")
    print("=" * 45)
    
    # Get the extracted text
    extracted_text, manual_text = debug_tts_input_step_by_step()
    
    # Test different inputs
    test_inputs = [
        ("extracted", extracted_text),
        ("manual", manual_text),
        ("minimal", "she is being subjected to harsh treatment"),
        ("no_being", "she is subjected to harsh treatment"),
        ("simple", "she faces harsh treatment")
    ]
    
    print(f"\nTesting {len(test_inputs)} different text inputs:")
    
    for name, text_input in test_inputs:
        print(f"\n{name.upper()}:")
        print(f"  Input: '{text_input}'")
        print(f"  Length: {len(text_input)} chars")
        print(f"  Words: {len(text_input.split())} words")
        
        # Show first 100 chars with repr
        preview = text_input[:100] + "..." if len(text_input) > 100 else text_input
        print(f"  Preview: '{preview}'")
        print(f"  Repr: {repr(text_input[:100])}")

def main():
    debug_tts_input_step_by_step()
    
    print(f"\n❓ QUESTION FOR YOU:")
    print(f"Looking at the step-by-step analysis above:")
    print(f"1. Do you see any unexpected characters in the repr() output?")
    print(f"2. Does the 'subjected to' context look wrong?") 
    print(f"3. Is there something in the HTML structure that I'm missing?")
    print(f"4. Should I be extracting the text differently?")

if __name__ == "__main__":
    main()
