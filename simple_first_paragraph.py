#!/usr/bin/env python3
"""
Simple First Paragraph Audio - No complications, just the basic first paragraph
"""

import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import re

def create_simple_first_paragraph_audio():
    """Create simple audio of just the first paragraph"""
    
    print("🎵 CREATING SIMPLE FIRST PARAGRAPH AUDIO")
    print("=" * 45)
    
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Get just the first paragraph
    content_div = soup.select_one('div[data-gu-name="body"]')
    first_p = content_div.find('p')
    
    # Clean text - minimal processing
    text = first_p.get_text(separator=' ', strip=True)
    text = re.sub(r'\s+', ' ', text.strip())
    
    print(f"📝 FIRST PARAGRAPH TEXT:")
    print(f"'{text}'")
    print(f"\nLength: {len(text)} characters")
    print(f"Words: {len(text.split())} words")
    
    try:
        print(f"\n🎵 Creating audio...")
        
        tts = gTTS(text=text, lang='en', tld='ie', slow=False)
        filename = "first_paragraph_only.mp3"
        tts.save(filename)
        
        print(f"✅ Created: {filename}")
        print(f"🎧 Listen to this file and tell me where you hear delays")
        
        # Save the text too
        with open('first_paragraph_text.txt', 'w') as f:
            f.write("FIRST PARAGRAPH TEXT\n")
            f.write("=" * 20 + "\n\n")
            f.write(text)
        
        print(f"📄 Text saved: first_paragraph_text.txt")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    create_simple_first_paragraph_audio()

if __name__ == "__main__":
    main()
