#!/usr/bin/env python3
"""
Extreme TTS Optimization - Eliminate ALL Unnatural Pauses
Create the most natural-flowing audio possible
"""

import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import re

def create_extreme_optimized_text():
    """Create text with EXTREME optimization for natural TTS flow"""
    
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    content_div = soup.select_one('div[data-gu-name="body"]')
    if not content_div:
        return None
    
    paragraphs = []
    for p in content_div.find_all('p'):
        text = p.get_text(separator=' ', strip=True)
        text = re.sub(r'\s+', ' ', text)
        if len(text) > 20:
            paragraphs.append(text)
    
    raw_text = ' '.join(paragraphs)
    
    print("🚀 EXTREME TTS OPTIMIZATION:")
    
    # EXTREME MEASURES to eliminate ALL pause-causing patterns
    
    optimized = raw_text
    
    # 1. ELIMINATE ALL PUNCTUATION that causes pauses
    
    # Remove ALL quotation marks (major pause causers)
    optimized = re.sub(r'[""]', '', optimized)
    optimized = re.sub(r"['']", '', optimized)
    
    # Remove ALL dashes and hyphens
    optimized = re.sub(r'[–—\-]', ' ', optimized)
    
    # Remove ALL parentheses and their content
    optimized = re.sub(r'\([^)]*\)', '', optimized)
    
    # Remove ALL brackets and their content  
    optimized = re.sub(r'\[[^\]]*\]', '', optimized)
    
    # 2. MINIMIZE SENTENCE BREAKS
    
    # Replace periods with commas where possible (shorter pauses)
    # Keep periods only for major sentence breaks
    sentences = optimized.split('. ')
    
    processed_sentences = []
    for i, sentence in enumerate(sentences):
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # For short sentences, connect with comma instead of period
        if len(sentence.split()) < 15 and i < len(sentences) - 1:
            processed_sentences.append(sentence + ',')
        else:
            processed_sentences.append(sentence + '.')
    
    optimized = ' '.join(processed_sentences)
    
    # 3. ELIMINATE COMPLEX CONSTRUCTIONS
    
    # Replace "according to X" (causes pauses)
    optimized = re.sub(r', according to ([^,]+),', r'. \1 reports', optimized)
    optimized = re.sub(r'according to ([^,]+)', r'\1 reports', optimized)
    
    # Replace "including X" (major pause causer)
    optimized = re.sub(r', including ([^,]+)', r' with \1', optimized)
    optimized = re.sub(r'including ([^,]+)', r'with \1', optimized)
    
    # Replace complex relative clauses
    optimized = re.sub(r', which ([^,]+),', r' and \1', optimized)
    optimized = re.sub(r', who ([^,]+),', r' and \1', optimized)
    
    # 4. SIMPLIFY NUMBERS AND TECHNICAL TERMS
    
    # Spell out numbers that might cause hesitation
    optimized = re.sub(r'\b437\b', 'four hundred and thirty seven', optimized)
    optimized = re.sub(r'\b16-year\b', 'sixteen year', optimized)
    
    # 5. AGGRESSIVE WHITESPACE AND PUNCTUATION CLEANUP
    
    # Remove multiple consecutive punctuation
    optimized = re.sub(r'[.,]{2,}', '.', optimized)
    optimized = re.sub(r'[,]{2,}', ',', optimized)
    
    # Fix spacing around punctuation
    optimized = re.sub(r'\s*([.,:;!?])\s*', r'\1 ', optimized)
    
    # Remove excessive commas that cause micro-pauses
    optimized = re.sub(r',\s*,', ',', optimized)
    
    # Normalize all whitespace
    optimized = re.sub(r'\s+', ' ', optimized)
    
    # 6. FINAL FLOW OPTIMIZATION
    
    # Ensure smooth sentence transitions
    optimized = re.sub(r'\.([A-Z])', r'. \1', optimized)
    
    # Remove trailing punctuation issues
    optimized = re.sub(r'\s+\.', '.', optimized)
    optimized = re.sub(r'\s+,', ',', optimized)
    
    optimized = optimized.strip()
    
    # Truncate to optimal length (shorter = fewer pauses)
    if len(optimized) > 3000:
        truncated = optimized[:3000]
        last_period = truncated.rfind('. ')
        if last_period > 2500:
            optimized = truncated[:last_period + 1]
    
    print(f"   Original: {len(raw_text)} chars")
    print(f"   Extreme optimized: {len(optimized)} chars")
    print(f"   Reduction: {len(raw_text) - len(optimized)} chars")
    
    return optimized

def main():
    print("⚡ EXTREME AUDIO OPTIMIZATION")
    print("=" * 50)
    
    # Create extremely optimized text
    extreme_text = create_extreme_optimized_text()
    
    if not extreme_text:
        print("❌ Failed to create optimized text")
        return
    
    # Minimal, natural introduction
    intro = "Guardian news report about Greta Thunberg by Lorenzo Tondo. "
    
    full_text = intro + extreme_text
    
    word_count = len(full_text.split())
    estimated_duration = word_count / 180  # Faster speech rate estimate
    
    print(f"\n📊 EXTREME VERSION STATS:")
    print(f"   Words: {word_count}")
    print(f"   Estimated duration: {estimated_duration:.1f} minutes")
    print(f"   Characters: {len(full_text)}")
    
    print(f"\n🎯 PREVIEW (first 300 chars):")
    print(f"'{full_text[:300]}...'")
    
    # Generate audio
    print(f"\n⚡ Creating EXTREME audio...")
    
    try:
        tts = gTTS(
            text=full_text,
            lang='en',
            tld='ie',  # Irish accent
            slow=False
        )
        
        filename = "guardian_article_EXTREME.mp3"
        tts.save(filename)
        
        print(f"✅ SUCCESS! Created: {filename}")
        print(f"🎧 This should have MINIMAL pauses and maximum flow!")
        print(f"🎯 Listen specifically for smooth 'Swedish officials' transition")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
