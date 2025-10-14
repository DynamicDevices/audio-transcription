#!/usr/bin/env python3
"""
Create Perfect Audio - Using Optimized HTML Extraction
Fix the Swedish officials break and all other formatting issues
"""

import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import re
import sys

def extract_perfect_text():
    """Extract text using the optimized method that eliminates breaks"""
    
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    print("🔧 EXTRACTING WITH OPTIMIZED METHOD...")
    
    # Find the main content area (this worked in our analysis)
    content_div = soup.select_one('div[data-gu-name="body"]')
    
    if not content_div:
        print("❌ Main content div not found")
        return None
    
    print("✅ Found main content div")
    
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
        skip_patterns = ['advertisement', 'subscribe', 'newsletter', 'follow us', 'sign up', 'download']
        if any(skip_word in text.lower() for skip_word in skip_patterns):
            continue
            
        clean_paragraphs.append(text)
    
    print(f"📊 Extracted {len(clean_paragraphs)} clean paragraphs")
    
    # Join with single spaces (NO paragraph breaks that cause pauses)
    optimized_text = ' '.join(clean_paragraphs)
    
    # AGGRESSIVE final cleanup for speech
    
    # Remove multiple spaces
    optimized_text = re.sub(r'\s+', ' ', optimized_text)
    
    # Remove problematic punctuation patterns
    optimized_text = re.sub(r'\s*[–—]\s*', ' ', optimized_text)  # Remove dashes
    
    # Fix quotes
    optimized_text = re.sub(r'[""]', '"', optimized_text)
    optimized_text = re.sub(r"['']", "'", optimized_text)
    
    # Ensure proper sentence spacing
    optimized_text = re.sub(r'\.([A-Z])', r'. \1', optimized_text)
    
    optimized_text = optimized_text.strip()
    
    print(f"✅ Final optimized text: {len(optimized_text)} characters")
    
    # Verify the Swedish officials area is clean
    if "swedish officials" in optimized_text.lower():
        pos = optimized_text.lower().find("swedish officials")
        start = max(0, pos - 30)
        end = min(len(optimized_text), pos + 80)
        context = optimized_text[start:end]
        print(f"🎯 Swedish officials context: '...{context}...'")
    
    return optimized_text

def create_perfect_audio():
    """Create audio with perfect text extraction"""
    
    print("🎧 CREATING PERFECT AUDIO FILE")
    print("=" * 50)
    
    # Extract optimized text
    optimized_text = extract_perfect_text()
    
    if not optimized_text:
        print("❌ Failed to extract text")
        return 1
    
    # Truncate to reasonable length for WhatsApp
    if len(optimized_text) > 4000:
        truncated = optimized_text[:4000]
        # Find last sentence
        last_period = truncated.rfind('. ')
        if last_period > 3500:
            optimized_text = truncated[:last_period + 1]
    
    # Create natural introduction
    intro = "Here's a Guardian news report about Greta Thunberg, reported by Lorenzo Tondo. "
    
    # Combine
    full_text = intro + optimized_text
    
    word_count = len(full_text.split())
    duration = word_count / 175
    
    print(f"📊 Final audio text:")
    print(f"   Words: {word_count}")
    print(f"   Duration: ~{duration:.1f} minutes")
    print(f"   Characters: {len(full_text)}")
    
    # Show first part to verify it's clean
    print(f"\n🎯 AUDIO PREVIEW (first 200 chars):")
    print(f"'{full_text[:200]}...'")
    
    # Generate audio
    print(f"\n🎵 Generating perfect audio...")
    
    try:
        tts = gTTS(
            text=full_text,
            lang='en',
            tld='ie',  # Irish accent
            slow=False
        )
        
        filename = "guardian_article_PERFECT.mp3"
        tts.save(filename)
        
        print("✅ SUCCESS! Perfect audio created!")
        print(f"📱 File: {filename}")
        print(f"🎧 Duration: ~{duration:.1f} minutes")
        print()
        print("🔧 FIXES APPLIED:")
        print("   ✅ Eliminated HTML formatting breaks")
        print("   ✅ Single-space paragraph joining (no \\n\\n)")
        print("   ✅ Aggressive whitespace cleanup")
        print("   ✅ Removed problematic dashes and quotes")
        print("   ✅ Perfect sentence flow")
        print()
        print("🎯 The 'Swedish officials' break should be COMPLETELY GONE!")
        print("   Listen specifically around 8-10 seconds for smooth flow.")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

def main():
    return create_perfect_audio()

if __name__ == "__main__":
    sys.exit(main())
