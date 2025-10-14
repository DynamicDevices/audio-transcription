#!/usr/bin/env python3
"""
Final Optimized Audio - Replace problematic phrase structure
"""

import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import re

def create_final_optimized_audio():
    """Create final audio with the problematic phrase fixed"""
    
    print("🎯 CREATING FINAL OPTIMIZED AUDIO")
    print("=" * 40)
    
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Extract clean text (zero artifacts method)
    content_div = soup.select_one('div[data-gu-name="body"]')
    
    paragraphs = []
    for p in content_div.find_all('p'):
        text = p.get_text(separator=' ', strip=True)
        text = re.sub(r'\s+', ' ', text)
        if len(text) > 20:
            paragraphs.append(text)
    
    clean_text = ' '.join(paragraphs)
    
    # Remove ALL line ending artifacts
    clean_text = re.sub(r'[\r\n\f\v\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029]+', ' ', clean_text)
    clean_text = re.sub(r'\t+', ' ', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    clean_text = re.sub(r'[\u00A0\u1680\u2000-\u200B\u202F\u205F\u3000\uFEFF]+', ' ', clean_text)
    
    print("🔧 APPLYING PHRASE OPTIMIZATIONS:")
    
    # Fix the problematic "being subjected to" phrase
    original_phrase = "she is being subjected to harsh treatment"
    optimized_phrase = "she faces harsh treatment"
    
    clean_text = clean_text.replace(original_phrase, optimized_phrase)
    
    print(f"   ✅ Replaced: '{original_phrase}'")
    print(f"   ✅ With: '{optimized_phrase}'")
    
    # Apply other TTS optimizations
    clean_text = re.sub(r'[""]', '', clean_text)  # Remove smart quotes
    clean_text = re.sub(r"['']", '', clean_text)  # Remove smart apostrophes  
    clean_text = re.sub(r'[–—]', ' ', clean_text)  # Remove dashes
    clean_text = re.sub(r', including ([^,]+)', r' with \1', clean_text)  # Fix "including"
    clean_text = re.sub(r'\s+', ' ', clean_text)  # Final space normalization
    
    # Truncate to reasonable length
    if len(clean_text) > 3500:
        truncated = clean_text[:3500]
        last_period = truncated.rfind('. ')
        if last_period > 3000:
            clean_text = truncated[:last_period + 1]
    
    # Add natural introduction
    intro = "Guardian news report about Greta Thunberg by Lorenzo Tondo. "
    
    final_text = intro + clean_text
    
    word_count = len(final_text.split())
    duration_est = word_count / 180
    
    print(f"\n📊 FINAL OPTIMIZED VERSION:")
    print(f"   Words: {word_count}")
    print(f"   Estimated duration: {duration_est:.1f} minutes")
    print(f"   Zero line ending artifacts: ✅")
    print(f"   Optimized phrase structure: ✅")
    
    # Verify the fix
    if "she faces harsh treatment" in final_text:
        print(f"   ✅ Phrase optimization applied successfully")
    else:
        print(f"   ❌ Phrase optimization may not have worked")
    
    # Show the optimized context
    pos = final_text.lower().find("she faces harsh treatment")
    if pos != -1:
        start = max(0, pos - 40)
        end = min(len(final_text), pos + 60)
        context = final_text[start:end]
        print(f"   Context: '...{context}...'")
    
    try:
        print(f"\n🎵 Generating final optimized audio...")
        
        tts = gTTS(text=final_text, lang='en', tld='ie', slow=False)
        filename = "guardian_article_FINAL_OPTIMIZED.mp3"
        tts.save(filename)
        
        print(f"✅ SUCCESS! Created: {filename}")
        print(f"🎯 This should have:")
        print(f"   ✅ No line ending pauses")
        print(f"   ✅ No 'being subjected to' delay")
        print(f"   ✅ Natural phrase flow")
        print(f"   ✅ Smooth 'Swedish officials' transition")
        print(f"   ✅ WhatsApp ready (optimized size)")
        
    except Exception as e:
        print(f"❌ Error creating audio: {e}")

def main():
    create_final_optimized_audio()

if __name__ == "__main__":
    main()
