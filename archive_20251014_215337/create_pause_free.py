#!/usr/bin/env python3
"""
Create Pause-Free Audio - Specific Fix for "subjected to" pause
"""

import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import re
import sys

def create_pause_free_audio():
    """Create audio with specific fixes for identified pause issues"""
    
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract content
    paragraphs = soup.find_all('p')
    content_paragraphs = [p.get_text().strip() for p in paragraphs 
                         if p.get_text().strip() and len(p.get_text().strip()) > 50]
    
    # Join with single spaces (no paragraph breaks)
    content = ' '.join(content_paragraphs)
    
    print("🔧 APPLYING SPECIFIC PAUSE FIXES...")
    
    # FIX 1: Remove "Exclusive:" prefix
    content = re.sub(r'^Exclusive:\s*', '', content, flags=re.IGNORECASE)
    
    # FIX 2: The specific problematic phrase - replace "including" structure
    original = "harsh treatment, including insufficient amounts of both water and food"
    replacement = "harsh treatment with insufficient water and food"
    content = content.replace(original, replacement)
    
    # FIX 3: More general "including" fixes that cause pauses
    content = re.sub(r', including insufficient amounts of ([^,]+)', r' with insufficient \1', content)
    content = re.sub(r', including ([^,]+),', r' with \1,', content)
    
    # FIX 4: Remove all newlines and normalize spacing
    content = re.sub(r'\n+', ' ', content)
    content = re.sub(r'\s+', ' ', content)
    
    # FIX 5: Replace dashes that cause pauses
    content = re.sub(r'\s*[–—]\s*', ' ', content)
    
    # FIX 6: Fix quotes
    content = re.sub(r'[""]', '"', content)
    content = re.sub(r"['']", "'", content)
    
    # FIX 7: Ensure smooth sentence transitions
    content = re.sub(r'\.([A-Z])', r'. \1', content)
    
    # FIX 8: Truncate smartly
    if len(content) > 4000:
        truncated = content[:4000]
        last_period = truncated.rfind('. ')
        if last_period > 3500:
            content = truncated[:last_period + 1]
    
    # Create smooth introduction
    author = "Lorenzo Tondo"
    intro = f"Here's a Guardian news report about Greta Thunberg, reported by {author}. "
    
    # Combine
    full_text = intro + content.strip()
    
    # Show the fixed problematic area
    search_phrase = "she has been subjected to"
    if search_phrase in full_text.lower():
        pos = full_text.lower().find(search_phrase)
        start = max(0, pos - 30)
        end = min(len(full_text), pos + 150)
        fixed_area = full_text[start:end]
        
        print("✅ FIXED PROBLEMATIC AREA:")
        print(f"'{fixed_area}'")
        print()
    
    return full_text

def main():
    print("🎧 Creating Pause-Free Audio - Targeted Fixes")
    print("=" * 50)
    
    # Create the optimized text
    audio_text = create_pause_free_audio()
    
    word_count = len(audio_text.split())
    duration = word_count / 175
    
    print(f"📊 Final text: {word_count} words, ~{duration:.1f} minutes")
    
    # Generate audio
    print("🎵 Generating pause-free audio...")
    
    try:
        tts = gTTS(
            text=audio_text,
            lang='en',
            tld='ie',  # Irish accent
            slow=False
        )
        
        filename = "guardian_article_pause_free.mp3"
        tts.save(filename)
        
        print("✅ SUCCESS! Pause-free audio created!")
        print(f"📱 File: {filename}")
        print(f"🎧 Duration: ~{duration:.1f} minutes")
        print()
        print("🔧 SPECIFIC FIXES APPLIED:")
        print("   ✅ Removed 'including insufficient amounts' pause")
        print("   ✅ Eliminated newline characters")
        print("   ✅ Replaced complex clauses with simple ones")
        print("   ✅ Fixed dash and quote pauses")
        print("   ✅ Smooth sentence flow")
        print()
        print("🎙️  The phrase 'she has been subjected to harsh treatment'")
        print("    should now flow naturally without pauses!")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
