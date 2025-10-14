#!/usr/bin/env python3
"""
Audio Analysis Tool - Debug Pause Issues
Analyze the exact text that's causing pauses and fix them
"""

import requests
from bs4 import BeautifulSoup
import re

def analyze_text_for_pauses():
    """Extract and analyze the exact text to find pause-causing patterns"""
    
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Get the raw content
    paragraphs = soup.find_all('p')
    content_paragraphs = [p.get_text().strip() for p in paragraphs 
                         if p.get_text().strip() and len(p.get_text().strip()) > 50]
    
    raw_content = '\n\n'.join(content_paragraphs)
    
    print("🔍 DEBUGGING PAUSE ISSUES")
    print("=" * 50)
    
    # Find the problematic phrase
    search_phrase = "she has been subjected to"
    
    # Look for the context around this phrase
    if search_phrase in raw_content.lower():
        # Find the position
        pos = raw_content.lower().find(search_phrase)
        
        # Extract 200 characters before and after
        start = max(0, pos - 200)
        end = min(len(raw_content), pos + 300)
        context = raw_content[start:end]
        
        print("📍 FOUND PROBLEMATIC AREA:")
        print("-" * 30)
        print(f"RAW TEXT: '{context}'")
        print("-" * 30)
        
        # Analyze what's causing the pause
        print("\n🔍 PAUSE ANALYSIS:")
        
        # Check for hidden characters
        context_repr = repr(context)
        print(f"WITH HIDDEN CHARS: {context_repr}")
        
        # Look for specific patterns that cause pauses
        issues = []
        
        if '\n' in context:
            issues.append("❌ Newline characters found")
        if '  ' in context:  # double spaces
            issues.append("❌ Multiple consecutive spaces")
        if '"' in context or '"' in context:
            issues.append("❌ Smart quotes that may cause pauses")
        if '–' in context or '—' in context:
            issues.append("❌ Em/en dashes")
        if ', including' in context.lower():
            issues.append("❌ Complex sentence structure with 'including'")
        
        for issue in issues:
            print(f"  {issue}")
        
        print(f"\n🎯 SPECIFIC PROBLEM AREA:")
        # Find the exact sentence with the issue
        sentences = context.split('.')
        for i, sentence in enumerate(sentences):
            if search_phrase in sentence.lower():
                print(f"SENTENCE {i}: '{sentence.strip()}'")
                
                # Check this specific sentence for issues
                if ', including' in sentence.lower():
                    print("  → FOUND: Complex clause with 'including' - this creates a pause!")
                if 'insufficient' in sentence.lower():
                    print("  → FOUND: Technical word 'insufficient' may cause hesitation")
                
        return context
    
    return None

def create_pause_optimized_text():
    """Create text specifically optimized to eliminate the identified pause"""
    
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract content
    paragraphs = soup.find_all('p')
    content_paragraphs = [p.get_text().strip() for p in paragraphs 
                         if p.get_text().strip() and len(p.get_text().strip()) > 50]
    
    content = ' '.join(content_paragraphs)  # Join with single spaces, not \n\n
    
    # AGGRESSIVE PAUSE ELIMINATION
    
    # 1. Remove all newlines first
    content = re.sub(r'\n+', ' ', content)
    
    # 2. Fix the specific problematic phrase
    # Replace complex "including insufficient" construction
    content = re.sub(
        r'harsh treatment, including insufficient amounts of both water and food',
        'harsh treatment with insufficient water and food',
        content
    )
    
    # 3. Simplify other complex constructions that cause pauses
    content = re.sub(r', including ([^,]+),', r' with \1,', content)
    
    # 4. Replace em/en dashes that cause weird pauses
    content = re.sub(r'\s*[–—]\s*', ' ', content)  # Replace with single space
    
    # 5. Fix smart quotes
    content = re.sub(r'[""]', '"', content)
    content = re.sub(r"['']", "'", content)
    
    # 6. Normalize all spacing
    content = re.sub(r'\s+', ' ', content)
    
    # 7. Fix sentence flow - ensure smooth transitions
    content = re.sub(r'\.([A-Z])', r'. \1', content)
    
    # 8. Remove "Exclusive:" prefix that sounds awkward
    content = re.sub(r'^Exclusive:\s*', '', content, flags=re.IGNORECASE)
    
    # 9. Truncate to reasonable length
    if len(content) > 4000:
        # Find a good breaking point
        truncated = content[:4000]
        last_period = truncated.rfind('. ')
        if last_period > 3500:
            content = truncated[:last_period + 1]
    
    # Create natural intro
    author = "Lorenzo Tondo"
    intro = f"Here's a Guardian news report about Greta Thunberg, reported by {author}. "
    
    full_text = intro + content.strip()
    
    return full_text

def main():
    # First, analyze what's causing the pause
    problematic_text = analyze_text_for_pauses()
    
    if problematic_text:
        print(f"\n🔧 CREATING OPTIMIZED VERSION...")
        
        # Create the fixed version
        optimized_text = create_pause_optimized_text()
        
        print(f"\n✅ OPTIMIZED TEXT PREVIEW:")
        print("-" * 40)
        
        # Show the specific area that was fixed
        search_phrase = "she has been subjected to"
        if search_phrase in optimized_text.lower():
            pos = optimized_text.lower().find(search_phrase)
            start = max(0, pos - 50)
            end = min(len(optimized_text), pos + 200)
            fixed_context = optimized_text[start:end]
            print(f"FIXED: '{fixed_context}'")
        
        print("-" * 40)
        
        # Save the analysis
        with open('pause_analysis.txt', 'w') as f:
            f.write("PAUSE ANALYSIS RESULTS\n")
            f.write("=" * 30 + "\n\n")
            f.write("PROBLEMATIC TEXT:\n")
            f.write(problematic_text + "\n\n")
            f.write("OPTIMIZED TEXT PREVIEW:\n")
            f.write(optimized_text[:500] + "...\n")
        
        print(f"\n📄 Analysis saved to: pause_analysis.txt")
        print(f"📝 Optimized text ready for audio generation")
        
        return optimized_text
    
    return None

if __name__ == "__main__":
    main()
